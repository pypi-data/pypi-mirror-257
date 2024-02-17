#!/bin/env python3
# -----------------------------------------------------------------------------
#  pytermor [ANSI formatted terminal output toolset]
#  (c) 2022-2023. A. Shavykin <0.delameter@gmail.com>
#  Licensed under GNU Lesser General Public License v3.0
# -----------------------------------------------------------------------------

from __future__ import annotations

import os
import sys

import pytermor as pt
import pytermor.common


class Main:
    STYLES_1 = {
        "A": pt.Style(fg=pt.ColorRGB(0x943CE0), bg=pt.ColorRGB(0x553592), bold=True),
        "B": pt.Style(fg=pt.ColorRGB(0x8D408C), bg=pt.ColorRGB(0x6E3DC7), bold=True),
        "C": pt.Style(fg=pt.ColorRGB(0x6F3E98), bg=pt.ColorRGB(0x9838A3), bold=True),
    }
    STYLES_2 = {
        "A": pt.Style(fg=pt.ColorRGB(0x006F00), bg=pt.ColorRGB(0x005000), bold=True),
        "B": pt.Style(fg=pt.ColorRGB(0x003500), bg=pt.ColorRGB(0x005000), bold=True),
        "C": pt.Style(fg=pt.ColorRGB(0x6F0000), bg=pt.ColorRGB(0x500000), bold=True),
        "D": pt.Style(fg=pt.ColorRGB(0x350000), bg=pt.ColorRGB(0x500000), bold=True),
    }
    WIDTH = 52

    def __init__(self):
        self.run()

    def run(self):
        if "--help" in sys.argv or "help" in sys.argv:
            self._print_help(0)

        pt.echo(
            ["", "Look at the rectangle below. In normal conditions you:"],
            wrap=True,
            indent_first=2,
        )
        pt.echo(
            [
                "",
                "1) should see that it's a magenta rectangle with some purple letters inside;",
                "2) should be able to read the full word (although it can be challenging);",
                "3) can distinguish 3 sections of the rectangle with different brightness.",
            ],
            wrap=True,
            indent_first=2,
            indent_subseq=5,
        )

        pt.echo()
        pt.echo(pytermor.pad(10) + '┌──────────────────────────┐')
        pt.echo(pytermor.pad(10) + '│ ', nl=False)
        wparts = ["★ins", "pira", "tion"]
        for style in reversed(self.STYLES_1.values()):
            wpart = (lambda s: s.ljust(8))(" ".join(wparts.pop(0).upper()))
            pt.echo(wpart, style, pt.SgrRenderer(), nl=False)
            if len(wparts) == 0:
                break

        pt.echo(' │')
        pt.echo(pytermor.pad(10) + '└──────────────────────────┘')
        pt.echo(
            [
                "",
                "If ALL these conditions are met, your terminal is working in either "
                "256 color mode or True Color mode. If ANY of these is false -- the "
                "terminal doesn't support neither 256-colors nor True Color mode and "
                "is operating in legacy 16-colors or even monochrome mode. It means "
                "that your terminal does not support advanced SGR formatting (or, which "
                "is more likely, these capabilities are disabled). Your environment "
                "variables are set as follows: ",
                "",
                f"  TERM={os.environ.get('TERM', '')}",
                f"  COLORTERM={os.environ.get('COLORTERM', '')}",
                "",
                "-"*min(80, pt.get_terminal_width()-4),
                "",
                "Previous test cannot tell with enough confidence, which mode exactly "
                "you are running -- the difference between advanced modes would be "
                "insignificant. However, the next test was specially designed to "
                "distinguish between True Color mode and 256 colors mode:",
            ],
            wrap=True,
            indent_first=2,
        )

        pt.echo()
        pt.echo(pytermor.pad(8) + '┌──────────────────────────────┐')
        pt.echo(pytermor.pad(8) + '│ ', nl=False)
        wparts = ["man", "ifes", "tat", "ion·"]
        for style in self.STYLES_2.values():
            wpart = (lambda s: s.center(7))(" ".join(wparts.pop(0).upper()))
            style.inversed = not style.inversed
            pt.echo(wpart, style, pt.SgrRenderer(), nl=False)
            if len(wparts) == 0:
                break

        pt.echo(' │')
        pt.echo(pytermor.pad(8) + '└──────────────────────────────┘')
        pt.echo(
            ["", "Same as before, there are three conditions. You:"],
            wrap=True,
            indent_first=2,
        )
        pt.echo(
            [
                "",
                "1) should see that the left part is a green rectangle with some "
                "green letters inside, and the right part is similar, except the "
                "color is red;",
                "2) should be able to read the full word;",
                "3) can recognize 4 sections of the target with different brightness -- "
                "the green sections (4 total).",
            ],
            wrap=True,
            indent_first=2,
            indent_subseq=5,
        )
        pt.echo(
            [
                "",
                "If ALL these are met -- your terminal is in True Color mode and "
                "can display full variety of RGB color space (16M colors). Otherwise "
                "the mode is indexed xterm-256.",
                "",
                "-"*min(80, pt.get_terminal_width()-4),
                "",
                "IMPORTANT",
                "",
                "When the output is redirected to a file or a pipe, the library detects "
                "that the receiving end is not a terminal emulator and automatically "
                "disables all the formatting. This is intended. To keep the formatting "
                "even in redirected output, set the environment var PYTERMOR_FORCE_OUTPUT_MODE "
                "to either of: 'xterm-16', 'xterm-256' or 'true_color'.",
                "",
                "Your output device " + f"IS{[' NOT', ''][sys.stdout.isatty()]} a terminal emulator.",
                "\x1b[m"
            ],
            wrap=True,
            indent_first=2,
        )

    def _print_help(self, exit_code: int = None):
        print(
            """
USAGE: 
    terminal_color_mode
    
Script made for manual testing of terminal color mode capabilities. No arguments
of options. Run and follow the instructions.
"""
        )
        if exit_code is not None:
            exit(exit_code)


if __name__ == "__main__":
    try:
        Main()
    except Exception as e:
        pt.echo(f"[ERROR] {type(e).__qualname__}: {e}\n", fmt=pt.Styles.ERROR)
        # raise e
