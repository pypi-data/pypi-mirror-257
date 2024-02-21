# -----------------------------------------------------------------------------
#  pytermor [ANSI formatted terminal output toolset]
#  (c) 2022-2023. A. Shavykin <0.delameter@gmail.com>
#  Licensed under GNU Lesser General Public License v3.0
# -----------------------------------------------------------------------------
"""
Formatters for prettier output and utility classes to avoid writing boilerplate
code when dealing with escape sequences. Also includes several Python Standard
Library methods rewritten for correct work with strings containing control sequences.

:fas:`sitemap;sd-text-primary` `guide.filter_class_diagram`

"""
from __future__ import annotations

import codecs
import math
import os
import re
import typing as t
from abc import ABCMeta, abstractmethod
from collections import deque
from dataclasses import dataclass, field
from functools import lru_cache, reduce
from hashlib import md5, shake_128
from math import ceil, floor
from typing import Union
from .style import FT
from .ansi import ESCAPE_SEQ_REGEX
from .common import chunk, pad, cut
from .exception import ArgTypeError, LogicError
from .term import get_terminal_width

codecs.register_error("replace_with_qmark", lambda e: ("?", e.start + 1))  # pragma: no cover


SGR_SEQ_REGEX = re.compile(R"(?P<esc>\x1b)(?P<csi>\[)(?P<param>[0-9;:]*)(?P<final>m)")
"""
Regular expression that matches :term:`SGR` sequences. Group 3 can be used for 
sequence params extraction.

:meta hide-value:
"""

CSI_SEQ_REGEX = re.compile(R"(?P<esc>\x1b)(?P<csi>\[)(?P<param>([0-9;:<=>?])*)(?P<final>[@A-Za-z])")
"""
Regular expression that matches CSI sequences (a superset which includes 
:term:`SGRs <SGR>`). 

:meta hide-value:
"""

CONTROL_CHARS = [*range(0x00, 0x08 + 1), *range(0x0E, 0x1F + 1), 0x7F]
"""
Set of ASCII control characters: :hex:`0x00-0x08`, :hex:`0x0E-0x1F` and
:hex:`0x7F`.

:meta hide-value:
"""
WHITESPACE_CHARS = [*range(0x09, 0x0D + 1), 0x20]
""" 
Set of ASCII whitespace characters: :hex:`0x09-0x0D` and :hex:`0x20`.

:meta hide-value:
"""
PRINTABLE_CHARS = [*range(0x21, 0x7E + 1)]
"""
Set of ASCII "normal" characters, i.e. non-control and non-space ones:
letters, digits and punctuation (:hex:`0x21-0x7E`).

:meta hide-value:
"""
NON_ASCII_CHARS = [*range(0x80, 0xFF + 1)]
""" 
Set of bytes that are invalid in ASCII-7 context: :hex:`0x80-0xFF`.

:meta hide-value: 
"""

UCS_CHAR_CPS = {
    re.compile(r"[\U000fffff-\U0010ffff]"): 6,
    re.compile(r"[\U00010000-\U000fffff]"): 5,
    re.compile(r"[\u1000-\uffff]"): 4,
    re.compile(r"[\u0100-\u0fff]"): 3,
    re.compile(r"[\u0010-\u00ff]"): 2,
    re.compile(r"[\u0000-\u000f]"): 1,
}

UTF8_BYTES_CHARS = {
    re.compile(r"[\U00010000-\U0010ffff]"): 4,
    re.compile(r"[\u0800-\uffff]"): 3,
    re.compile(r"[\u0080-\u07ff]"): 2,
    re.compile(r"[\x00-\x7f]"): 1,
}


_F = t.TypeVar("_F", bound=t.Callable[..., t.Any])

IT = t.TypeVar("IT", str, bytes)
""" input-type """
OT = t.TypeVar("OT", str, bytes)
"""output-type"""
PTT = Union[IT, t.Pattern[IT]]
""" pattern type """
RPT = Union[OT, t.Callable[[t.Match[OT]], OT]]
""" replacer type """
MPT = t.Dict[int, IT]
""" # map """


class IFilter(t.Generic[IT, OT], metaclass=ABCMeta):
    """
    Main idea is to provide a common interface for string filtering, that can make
    possible working with filters like with objects rather than with functions/lambdas.
    """

    _CLASS_NAME_LAST_SUBST = {
        "Noop": "Nop",
        "Whitespace": "Ws",
        "NonPrints": "Np",
    }
    _WORD_SPLIT_REGEX = re.compile(r"([A-Z][a-z]*)(?=[A-Z])")
    _VOWELS_FILTER_REGEX = re.compile(r"[aeui](?!$)")

    _stack: t.ClassVar[t.Deque[str]] = deque()
    _default_inst: t.ClassVar[IFilter]
    _name_max_len: t.ClassVar[int] = 0

    def __new__(cls: t.Type[IFilter], *args, **kwargs) -> IFilter:
        IFilter._name_max_len = max(IFilter._name_max_len, len(str(cls)))
        if not len(args) and not len(kwargs):
            if not hasattr(cls, "_default_inst"):
                cls._default_inst = super().__new__(cls)
            return cls._default_inst
        return super().__new__(cls)

    def __init__(self) -> None:
        super().__init__()

    def __call__(self, s: IT) -> OT:
        """Can be used instead of `apply()`"""
        return self.apply(s)

    def __repr__(self) -> str:
        prefix = ""
        if self is getattr(self.__class__, "_default_inst", ""):
            prefix = "*"
        return prefix + self.__class__.__name__

    def apply(self, inp: IT, extra: t.Any = None) -> OT:
        """
        Apply the filter to input *str* or *bytes*.

        :param inp:   input string
        :param extra: additional options
        :return: transformed string; the type can match the input type,
                 as well as be different -- that depends on filter type.
        """
        IFilter._stack.append(self.get_abbrev_name())
        result = self._apply(inp, extra)
        IFilter._stack.pop()
        return result

    @classmethod
    def get_abbrev_name(cls) -> str:
        def _process_word(*w) -> str:
            widx, word = w
            if widx == len(words) - 1:
                return word[:3]  # + (word.replace('e', ''))[-2:]
            word = cls._VOWELS_FILTER_REGEX.sub("", word)
            if widx == 0:
                return word[:4]
            return word[:3]  # 1..(n-1)

        name = reduce(
            lambda s, c: s.replace(*c),
            cls._CLASS_NAME_LAST_SUBST.items(),
            cls.__name__,
        )
        words = cls._WORD_SPLIT_REGEX.split(name)
        return "".join(_process_word(*w) for w in enumerate(words))

    @classmethod
    def get_name_max_len(cls) -> int:
        return min(cls._name_max_len, 20)

    @abstractmethod
    def _apply(self, inp: IT, extra: t.Any = None) -> OT:
        raise NotImplementedError


class IRefilter(IFilter[IT, str], metaclass=ABCMeta):
    """
    *Refilters* are rendering filters (output is *str* with SGRs).
    """

    @abstractmethod
    def _render(self, v: IT, st: FT) -> str:
        ...


class NoopFilter(IFilter[IT, OT]):
    """ """

    def _apply(self, inp: IT, extra: t.Any = None) -> OT:
        return inp


class OmniDecoder(IFilter[IT, str]):
    """ """

    def _apply(self, inp: IT, extra: t.Any = None) -> str:
        return inp.decode() if isinstance(inp, bytes) else inp


class OmniEncoder(IFilter[IT, bytes]):
    """ """

    def _apply(self, inp: IT, extra: t.Any = None) -> bytes:
        return inp.encode() if isinstance(inp, str) else inp


class OmniPadder(IFilter[IT, IT]):
    def __init__(self, width: int = 1):
        self._padding: t.Dict[t.Type[IT], IT] = {
            str: pad(width),
            bytes: pad(width).encode(),
        }
        super().__init__()

    def _apply(self, inp: IT, extra: t.Any = None) -> IT:
        padding = self._padding.get(str)
        if issubclass(type(inp), bytes):
            padding = self._padding.get(bytes)
        return padding + inp + padding


# -----------------------------------------------------------------------------
# Filters[Replacers]


class StringReplacer(IFilter[str, str]):
    """
    .
    """

    def __init__(self, pattern: PTT[str], repl: RPT[str]):
        super().__init__()

        if isinstance(pattern, str):
            self._pattern: t.Pattern[str] = re.compile(pattern)
        else:
            self._pattern: t.Pattern[str] = pattern
        self._repl = repl

    def _apply(self, inp: str, extra: t.Any = None) -> str:
        return self._pattern.sub(self._repl, inp)


class StringReplacerChain(StringReplacer):
    """
    .
    """

    def __init__(self, pattern: PTT[str], *repls: IFilter[str, str]):
        super().__init__(pattern, lambda m: m.group(0))
        self._repls: t.Deque[IFilter[str, str]] = deque(repls)

    def _apply(self, inp: str, extra: t.Any = None) -> str:
        return self._pattern.sub(self._replace_wrapper, inp)

    def _replace_wrapper(self, m: t.Match) -> str:
        return reduce(lambda s, c: c.apply(s), self._repls, self._repl(m))


class EscSeqStringReplacer(StringReplacer):
    ""","""

    def __init__(self, repl: RPT[str] = ""):
        super().__init__(ESCAPE_SEQ_REGEX, repl)


class SgrStringReplacer(StringReplacer):
    """
    Find all `SGR <SequenceSGR>` seqs (e.g., ``ESC [1;4m``) and replace with
    given string. More specific version of :class:`~CsiReplacer`.

    :param repl:
        Replacement, can contain regexp groups (see :meth:`apply_filters()`).
    """

    def __init__(self, repl: RPT[str] = ""):
        super().__init__(SGR_SEQ_REGEX, repl)


class CsiStringReplacer(StringReplacer):
    """
    Find all `CSI <SequenceCSI>` seqs (i.e., starting with :ansi:`ESC`\\ ``[``) and replace
    with given string. Less specific version of :class:`SgrReplacer`, as CSI
    consists of SGR and many other sequence subtypes.

    :param repl:
        Replacement, can contain regexp groups (see :meth:`apply_filters()`).
    """

    def __init__(self, repl: RPT[str] = ""):
        super().__init__(CSI_SEQ_REGEX, repl)


class StringLinearizer(StringReplacer):
    """
    Filter transforms all whitespace sequences in the input string
    into a single space character, or into a specified string. Most obvious
    application is pre-formatting strings for log output in order to keep
    the messages one-lined.

    :param repl: Replacement character(s).
    """

    def __init__(self, repl: RPT[str] = " "):
        super().__init__(re.compile(r"\s+"), repl)


class WhitespaceRemover(StringReplacer):
    """
    Special case of `StringLinearizer`. Removes all the whitespaces from the
    input string.
    """

    def __init__(self):
        super().__init__(re.compile(r"\s+"), "")


class AbstractNamedGroupsRefilter(IRefilter[str], StringReplacer, metaclass=ABCMeta):
    """
    Substitute the input by applying following rules:

      - Named groups which name is found in ``group_st_map`` keys are replaced with
        themselves styled as specified in a corresponding map values.
      - Regular/unnamed groups are kept as is, unless there is an "" (empty string) key
        in ``group_st_map``, in which case a style corresponding to such key is applied
        to all these groups.
      - Groups with names not present in the map, as well as lookaheads and lookbehinds,
        are kept as is (unstyled).
      - Non-capturing groups' contents and matched characters not belonging to any group
        are thrown away.
      - Not matched parts of the input are kept as is.

    .. code-block :: python

        >>> import pytermor as pt
        >>> class SgrNamedGroupsRefilter(AbstractNamedGroupsRefilter):
        ...     def _render(self, v: IT, st: FT) -> str:
        ...         return pt.render(v, st, pt.SgrRenderer(pt.OutputMode.XTERM_16))
        >>> SgrNamedGroupsRefilter(
        ...     re.compile(r'<?(<)(?P<val>.+?)(>)>?'),
        ...     {"val": pt.cv.GREEN},
        ... ).apply("text <<link>> text")
        'text <\x1b[32mlink\x1b[39m> text'

    """

    def __init__(self, pattern: PTT[str], group_st_map: dict[str, FT]):
        """
        :param group_st_map:
        """
        self._group_st_map = group_st_map
        self._groups_name_index: dict[int, str] = {v: k for k, v in pattern.groupindex.items()}
        super(AbstractNamedGroupsRefilter, self).__init__(pattern, self._replace_by_key)
        super(StringReplacer, self).__init__()

    def _replace_by_key(self, m: re.Match) -> str:
        return "".join(self._process_group(idx + 1, v) for idx, v in enumerate(m.groups()))

    def _process_group(self, idx: int, v: str) -> str:
        if not v:
            return ""
        k = self._groups_name_index.get(idx, "")
        if k not in self._group_st_map.keys():
            return v
        return self._render(v, self._group_st_map.get(k))


# -----------------------------------------------------------------------------
# Filters[Mappers]


class OmniMapper(IFilter[IT, IT]):
    """
    Input type: *str*, *bytes*. Abstract mapper. Replaces every character found in
    map keys to corresponding map value. Map should be a dictionary of this type:
    ``dict[int, str|bytes]``; moreover, length of *str*/*bytes* must be strictly 1
    character (ASCII codepage). If there is a necessity to map Unicode characters,
    `StringMapper` should be used instead.

    >>> OmniMapper({0x20: '.'}).apply(b'abc def ghi')
    b'abc.def.ghi'

    For mass mapping it is better to subclass `OmniMapper` and override two methods --
    `_get_default_keys` and `_get_default_replacer`. In this case you don't have to
    manually compose a replacement map with every character you want to replace.

    :param override: a dictionary with mappings: keys must be *ints*, values must be
                     either a single-char *strs* or *bytes*.
    :see: `NonPrintsOmniVisualizer`
    """

    def __init__(self, override: MPT = None):
        super().__init__()
        self._make_maps(override)

    def _get_default_keys(self) -> t.List[int]:
        """
        Helper method for avoiding character map manual composing in the mapper subclass.

        :return: List of int codes that should be replaced by default (i.e., without
                 taking ``override`` argument into account, or when it is not present).
        """
        return []

    def _get_default_replacer(self) -> IT:
        """
        Helper method for avoiding character map manual composing in the mapper subclass.

        :return: Default replacement character for int codes that are not present in
                 ``override`` keys list, or when there is no overriding at all.
        """
        raise NotImplementedError

    def _make_maps(self, override: MPT | None):
        self._maps = {
            str: str.maketrans(self._make_premap(str, override)),
            bytes: bytes.maketrans(*self._make_bytemaps(override)),
        }

    def _make_premap(self, inp_type: t.Type[IT], override: MPT | None, single=False) -> t.Dict[int, IT]:
        default_map = dict()
        default_replacer = None
        for i in self._get_default_keys():
            if default_replacer is None:
                default_replacer = self._transcode(self._get_default_replacer(), inp_type)
            default_map.setdefault(i, default_replacer)

        if override is None:
            return default_map
        if not isinstance(override, dict):
            raise ArgTypeError(override, "override", MPT, None)

        if single and not all(isinstance(k, int) and 0 <= k <= 255 for k in override.keys()):
            raise TypeError("Mapper keys should be ints such as: 0 <= key <= 255")
        if not all(isinstance(v, (str, bytes)) for v in override.values()):
            raise TypeError("Map values should be either 'str' or 'bytes' single chars")
        for i, v in override.items():
            default_map.update({i: self._transcode(v, inp_type)})
        return default_map

    def _make_bytemaps(self, override: MPT | None) -> t.Tuple[bytes, bytes]:
        premap = self._make_premap(bytes, override, single=True)
        srcmap = b"".join(int.to_bytes(k, 1, "big") for k in premap.keys())
        for v in premap.values():
            if len(v) != 1:
                raise ValueError(
                    "All OmniMapper replacement values should be one byte long (i.e. be "
                    "an ASCII char). To utilize non-ASCII characters use StringMapper."
                )
        destmap = b"".join(premap.values())
        return srcmap, destmap

    def _apply(self, inp: IT, extra: t.Any = None) -> IT:
        return inp.translate(self._maps[type(inp)])

    def _transcode(self, inp: IT, target: t.Type[RPT]) -> RPT:
        if isinstance(inp, target):
            return inp
        return inp.encode() if isinstance(inp, str) else inp.decode()


class StringMapper(OmniMapper[str]):
    """
    a
    """

    def _make_maps(self, override: MPT | None):
        self._maps = {str: str.maketrans(self._make_premap(str, override))}

    def _apply(self, inp: str, extra: t.Any = None) -> str:
        if isinstance(inp, bytes):
            raise TypeError("String mappers allow 'str' as input only")
        return super()._apply(inp, extra)


class NonPrintsOmniVisualizer(OmniMapper):
    """
    Input type: *str*, *bytes*. Replace every whitespace character with ``.``.
    """

    def _get_default_keys(self) -> t.List[int]:
        return WHITESPACE_CHARS + CONTROL_CHARS

    def _get_default_replacer(self) -> IT:
        return b"."


class NonPrintsStringVisualizer(StringMapper):
    """
    Input type: *str*. Replace every whitespace character with "·", except
    newlines. Newlines are kept and get prepneded with same char by default,
    but this behaviour can be disabled with ``keep_newlines`` = *False*.

        >>> NonPrintsStringVisualizer(keep_newlines=False).apply("S"+os.linesep+"K")
        'S↵K'

    :param keep_newlines: When *True*, transform newline characters into "↵\\\\n", or
                          into just "↵" otherwise.
    """

    def __init__(self, keep_newlines: bool = True):
        override = {
            0x09: "⇥",
            0x0A: "↵" + ("\n" if keep_newlines else ""),
            0x0B: "⤓",
            0x0C: "↡",
            0x0D: "⇤",
            0x20: "␣",
        }
        super().__init__(override)

    def _get_default_keys(self) -> t.List[int]:
        return WHITESPACE_CHARS + CONTROL_CHARS

    def _get_default_replacer(self) -> str:
        return "·"


class OmniSanitizer(OmniMapper):
    """
    Input type: *str*, *bytes*. Replace every control character and every non-ASCII
    character (0x80-0xFF) with ".", or with specified char. Note that the replacement
    should be a single ASCII character, because ``Omni-`` filters are designed to work
    with *str* inputs and *bytes* inputs on equal terms.

    :param repl: Value to replace control/non-ascii characters with. Should be strictly 1
                 character long.
    """

    def __init__(self, repl: IT = b"."):
        self._override_replacer = repl
        super().__init__()

    def _get_default_keys(self) -> t.List[int]:
        return CONTROL_CHARS + NON_ASCII_CHARS

    def _get_default_replacer(self) -> IT:
        return self._override_replacer


# -----------------------------------------------------------------------------
# Filters[Tracers]


class AbstractTracer(IFilter[IT, str], metaclass=ABCMeta):
    def __init__(self, max_output_width: int = None):
        super().__init__()
        self._max_output_width: int = max_output_width or get_terminal_width()
        self._state: _TracerState = _TracerState()

    def _apply(self, inp: IT, extra: TracerExtra = None) -> str:
        if not inp:
            inp = inp[:]  # empty string/bytes
        if not extra:
            extra = TracerExtra()

        addr_shift = extra.addr_shift
        self._state.reset(inp, self.get_max_chars_per_line(inp, addr_shift), addr_shift)
        if self._state.char_per_line < 1:
            raise ValueError(
                f"Maximum output width ({self._max_output_width}) "
                f"is too low, cant fit even one char/group per line"
            )
        self._state.inp_size_len = self._get_input_size_len(addr_shift)
        self._state.address_len = len(self._format_address(self._state.inp_size))

        while len(inp) > 0 or len(self._state.rows) == 0:
            inp, part = (
                inp[self._state.char_per_line :],
                inp[: self._state.char_per_line],
            )
            if extra.hash:
                self._add_line_hash(part)
            self._process(part)
            self._state.lineno += 1
            self._state.address += self._state.char_per_line

        flabel_left = ""
        flabel_right = f"({self._format_address(self._state.inp_size)})"
        if extra.hash:
            flabel_left = f"[{self._compute_total_hash()}]"
        footer = self._format_line_separator("-", flabel_left, flabel_right)

        hlabel_left = cut(extra.label, len(footer))
        header = self._format_line_separator("_", hlabel_left)

        return "\n".join([header, *self._render_rows(), footer, ""])

    def _add_line_hash(self, part: t.AnyStr):
        if isinstance(part, str):
            part = part.encode()
        self._state.part_hashes += md5(part).hexdigest()

    def _compute_total_hash(self) -> str:
        return shake_128(self._state.part_hashes.encode()).hexdigest(10)

    def _format_address(self, override: int = None) -> str:
        address = override if override is not None else self._state.address
        result = str(address).rjust(self._state.inp_size_len or 0)
        return result

    def _format_line_separator(self, fill: str, label_left="", label_right="") -> str:
        return (
            label_left
            + fill * (self._get_output_line_len() - len(label_left) - len(label_right))
            + label_right
        )

    def _get_vert_sep_char(self):
        return "|"

    def _get_input_size_len(self, addr_shift: int) -> int:
        return len(str(self._state.inp_size + addr_shift))

    def _process(self, part: IT):
        row = self._make_row(part)
        if self._state.cols_max_len is None:
            self._state.cols_max_len = [0] * len(row)
        for col_idx, col_val in enumerate(row):
            self._state.cols_max_len[col_idx] = max(
                0, self._state.cols_max_len[col_idx], len(col_val)
            )
        self._state.rows.append(row)

    def _get_output_line_len(self) -> int:
        # useless before processing
        if self._state.cols_max_len is None:  # pragma: no cover
            raise LogicError
        return sum(ml for ml in self._state.cols_max_len)

    def _render_rows(self) -> t.Iterable[str]:
        if self._state.cols_max_len is None:  # pragma: no cover
            return
        for row in self._state.rows:
            row_str = ""
            for col_idx, col_val in enumerate(row):
                row_str += col_val.rjust(self._state.cols_max_len[col_idx])
            yield row_str

    @abstractmethod
    def _make_row(self, part: IT) -> t.List[str]:
        raise NotImplementedError

    @abstractmethod
    def get_max_chars_per_line(self, inp: IT, addr_shift: int) -> int:
        raise NotImplementedError


class BytesTracer(AbstractTracer[bytes]):
    """
    str/bytes as byte hex codes, grouped by 4

    .. code-block:: PtTracerDump
       :caption: Example output

         0x00 | 35 30 20 35  34 20 35 35  20 C2 B0 43  20 20 33 39  20 2B 30 20
         0x14 | 20 20 33 39  6D 73 20 31  20 52 55 20  20 E2 88 86  20 35 68 20
         0x28 | 31 38 6D 20  20 20 EE 8C  8D 20 E2 80  8E 20 2B 32  30 C2 B0 43
         0x3C | 20 20 54 68  20 30 31 20  4A 75 6E 20  20 31 36 20  32 38 20 20
         0x50 | E2 96 95 E2  9C 94 E2 96  8F 46 55 4C  4C 20
    """

    GROUP_SIZE = 4

    def _make_row(self, part: IT) -> t.List[str]:
        if not isinstance(part, bytes):  # pragma: no cover
            raise ArgTypeError(part, "inp", bytes)
        return [
            " ",
            self._format_address(),
            " ",
            self._get_vert_sep_char(),
            " ",
            *self._format_main(part),
        ]

    def _format_address(self, override: int = None) -> str:
        address = override if override is not None else self._state.address
        return f"0x{address:0{self._state.inp_size_len or 0}X}"

    def _format_main(self, part: bytes) -> t.Iterable[str]:
        for c in chunk(part, self.GROUP_SIZE):
            yield (" ".join([f"{b:02X}" for b in (*c,)])).ljust(3 * self.GROUP_SIZE + 1)

    def _get_input_size_len(self, addr_shift: int) -> int:
        return 2 * ceil(len(f"{(self._state.inp_size+addr_shift):X}") / 2)

    def get_max_chars_per_line(self, inp: bytes, addr_shift: int) -> int:
        """
        For the details see `Tracers math <appendix.tracers-math.bytes-tracer>`.

        :param inp:
        :param addr_shift:
        """
        l_ihex = len(f"{len(inp) + addr_shift:x}")
        l_t = self._max_output_width
        c_lmax = self.GROUP_SIZE * floor((l_t - ceil(l_ihex / 2) - 6) / 13)
        return self._round_chars_per_line(c_lmax)

    @classmethod
    def _round_chars_per_line(cls, cpl: int) -> int:
        return cls.GROUP_SIZE * floor(cpl / cls.GROUP_SIZE)


class AbstractStringTracer(AbstractTracer[str], metaclass=ABCMeta):
    def __init__(self, max_output_width: int = None):
        self._output_filters = [NonPrintsStringVisualizer(keep_newlines=False)]
        super().__init__(max_output_width)

    @abstractmethod
    def _format_main(self, part: str) -> t.Iterable[str]:
        raise NotImplementedError

    def _format_output_text(self, text: str) -> str:
        return apply_filters(text, *self._output_filters).ljust(self._state.char_per_line)


# noinspection NonAsciiCharacters
class StringTracer(AbstractStringTracer):
    """
    str as byte hex codes (UTF-8), grouped by characters

    .. code-block:: PtTracerDump
       :caption: Example output

          0 |     35     30     20 35 34 20 35     35     20   c2b0 43 20 |50␣54␣55␣°C␣
         12 |     20     33     39 20 2b 30 20     20     20     33 39 6d |␣39␣+0␣␣␣39m
         24 |     73     20     31 20 52 55 20     20 e28886     20 35 68 |s␣1␣RU␣␣∆␣5h
         36 |     20     31     38 6d 20 20 20 ee8c8d     20 e2808e 20 2b |␣18m␣␣␣␣‎␣+
         48 |     32     30   c2b0 43 20 20 54     68     20     30 31 20 |20°C␣␣Th␣01␣
         60 |     4a     75     6e 20 20 31 36     20     32     38 20 20 |Jun␣␣16␣28␣␣
         72 | e29695 e29c94 e2968f 46 55 4c 4c     20                     |▕✔▏FULL␣
    """

    def _make_row(self, part: str) -> t.List[str]:
        return [
            " ",
            self._format_address(),
            " ",
            self._get_vert_sep_char(),
            " ",
            *self._format_main(part),
            self._get_vert_sep_char(),
            self._format_output_text(part),
        ]

    def _format_main(self, part: str) -> t.Iterable[str]:
        for s in part:
            yield "".join(f"{b:02x}" for b in s.encode())
            yield " "
        yield from [""] * 2 * (self._state.char_per_line - len(part))

    # noinspection NonAsciiCharacters
    def get_max_chars_per_line(self, inp: str, addr_shift: int) -> int:
        """
        For the details see `Tracers math <appendix.tracers-math.string-tracer>`.

        :param inp:
        :param addr_shift:
        """
        l_off = len(str(len(inp) + addr_shift))
        l_t = self._max_output_width
        c_umax = get_max_utf8_bytes_char_length(inp)
        result = floor((l_t - l_off - 5) / (2 * c_umax + 2))
        return result


# noinspection NonAsciiCharacters
class StringUcpTracer(AbstractStringTracer):
    """
    str as Unicode codepoints

    .. code-block:: PtTracerDump
       :caption: Example output

          0 |U+   20   34   36 20 34 36 20 34   36   20 B0 43 20 20 33   39 20 2B |␣46␣46␣46␣°C␣␣39␣+
         18 |U+   30   20   20 20 35 20 6D 73   20   31 20 52 55 20 20 2206 20 37 |0␣␣␣5␣ms␣1␣RU␣␣∆␣7
         36 |U+   68   20   32 33 6D 20 20 20 FA93 200E 20 2B 31 33 B0   43 20 20 |h␣23m␣␣␣望‎␣+13°C␣␣
         54 |U+   46   72   20 30 32 20 4A 75   6E   20 20 30 32 3A 34   38 20 20 |Fr␣02␣Jun␣␣02:48␣␣
         72 |U+ 2595 2714 258F 46 55 4C 4C 20                                     |▕✔▏FULL␣
    """

    def _make_row(self, part: str) -> t.List[str]:
        return [
            " ",
            self._format_address(),
            " ",
            self._get_vert_sep_char(),
            "U+ ",
            *self._format_main(part),
            self._get_vert_sep_char(),
            self._format_output_text(part),
        ]

    def _format_main(self, part: str) -> t.Iterable[str]:
        for s in part:
            yield from [f"{ord(s):>02X}", " "]
        yield from [""] * 2 * (self._state.char_per_line - len(part))

    def get_max_chars_per_line(self, inp: str, addr_shift: int) -> int:
        """
        For the details see `Tracers math <appendix.tracers-math.string-ucp-tracer>`.

        :param inp:
        :type inp:
        """
        l_off = len(str(len(inp) + addr_shift))
        l_t = self._max_output_width
        c_ucmax = get_max_ucs_chars_cp_length(inp)
        result = floor((l_t - l_off - 7) / (c_ucmax + 2))
        return result


@dataclass(frozen=True)
class TracerExtra:
    label: str = ""
    addr_shift: int = 0
    hash: bool = False


@dataclass
class _TracerState:
    inp_size: int = field(init=False, default=None)
    lineno: int = field(init=False, default=None)
    address: int = field(init=False, default=None)

    char_per_line: int = field(init=False, default=None)
    inp_size_len: int = field(init=False, default=None)
    address_len: int = field(init=False, default=None)

    rows: t.List[t.List[str]] = field(init=False, default=None)
    cols_max_len: t.List[int] | None = field(init=False, default=None)
    part_hashes: str = field(init=False, default=None)

    def reset(self, inp: IT, char_per_line: int, addr_shift: int):
        self.inp_size = len(inp)
        self.lineno = 0
        self.address = addr_shift

        self.char_per_line = char_per_line
        self.inp_size_len = 0
        self.address_len = 0

        self.rows = []
        self.cols_max_len = None
        self.part_hashes = ""


@lru_cache
def _get_tracer(tracer_cls: t.Type[AbstractTracer], max_width: int) -> AbstractTracer:
    return tracer_cls(max_width)


# @TODO  - special handling of one-line input
#        - squash repeating lines
def dump(
        data: t.Any,
        tracer_cls: t.Type[AbstractTracer] = None,
        extra: TracerExtra = None,
        force_width: int = None,
) -> str:
    """
    .
    """
    if not isinstance(data, (str, bytes)):
        data = str(data)
    if not tracer_cls:
        if isinstance(data, str):
            tracer_cls = StringUcpTracer
        else:
            tracer_cls = BytesTracer

    terminal_width = get_terminal_width()
    width = force_width or terminal_width
    tracer = _get_tracer(tracer_cls, width)
    return tracer.apply(data, extra)


def get_max_ucs_chars_cp_length(string: str) -> int:
    """."""
    for regex, length in UCS_CHAR_CPS.items():
        if regex.search(string):
            return length
    return 0


def get_max_utf8_bytes_char_length(string: str) -> int:
    """cc"""
    for regex, length in UTF8_BYTES_CHARS.items():
        if regex.search(string):
            return length
    return 0


# -----------------------------------------------------------------------------


def ljust_sgr(string: str, width: int, fillchar: str = " ") -> str:
    """
    SGR-formatting-aware implementation of ``str.ljust``.

    Return a left-justified string of length ``width``. Padding is done
    using the specified fill character (default is a space).
    """
    actual_len = len(apply_filters(string, SgrStringReplacer))
    return string + fillchar * max(0, width - actual_len)


def center_sgr(string: str, width: int, fillchar: str = " ") -> str:
    """
    SGR-formatting-aware implementation of ``str.center``.

    Return a centered string of length ``width``. Padding is done using the
    specified fill character (default is a space).
    """
    actual_len = len(apply_filters(string, SgrStringReplacer))

    fill_len = max(0, width - actual_len)
    if fill_len == 0:
        return string

    if actual_len % 2 == 1:
        right_fill_len = math.ceil(fill_len / 2)
    else:
        right_fill_len = math.floor(fill_len / 2)
    left_fill_len = fill_len - right_fill_len
    return (fillchar * left_fill_len) + string + (fillchar * right_fill_len)


def rjust_sgr(string: str, width: int, fillchar: str = " ") -> str:
    """
    SGR-formatting-aware implementation of ``str.rjust``.

    Return a right-justified string of length ``width``. Padding is done
    using the specified fill character (default is a space).
    """
    actual_len = len(apply_filters(string, SgrStringReplacer))
    return fillchar * max(0, width - actual_len) + string


def apply_filters(inp: IT, *args: Union[IFilter, t.Type[IFilter]]) -> OT:
    """
    Method for applying dynamic filter list to a target string/bytes.

    Example (will replace all :ansi:`ESC` control characters to ``E`` and
    thus make SGR params visible)::

        >>> from pytermor import SeqIndex
        >>> test_str = f'{SeqIndex.RED}test{SeqIndex.COLOR_OFF}'
        >>> apply_filters(test_str, SgrStringReplacer('E\\2\\3\\4'))
        'E[31mtestE[39m'

        >>> apply_filters('\x1b[31mtest\x1b[39m', OmniSanitizer)
        '.[31mtest.[39m'

    Note that type of ``inp`` argument must be same as filter parameterized
    input type (`IT`), i.e. `StringReplacer` is ``IFilter[str, str]`` type,
    so you can apply it only to *str*-type inputs.

    :param inp:    String/bytes to filter.
    :param args:   Instance(s) implementing `IFilter` or their type(s).
    """

    def instantiate(f):
        return f() if isinstance(f, type) else f

    return reduce(lambda s, f: instantiate(f)(s), args, inp)
