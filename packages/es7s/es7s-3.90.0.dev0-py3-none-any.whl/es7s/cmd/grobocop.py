# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import unicodedata
from collections.abc import Iterable

import pytermor as pt
from es7s_commons import columns
from holms.db import resolve_ascii_cc

from es7s.shared import (
    get_app_config_yaml,
    get_stdout,
    with_terminal_state,
    ProxiedTerminalState,
    get_logger,
)
from es7s.shared.styles import Styles as _BaseStyles
from ._base import _BaseAction

LTR_CHAR = "\u200e"
CHRCOL_NUM = 16


class Styles(_BaseStyles):
    def __init__(self):
        self.CC = pt.Style(fg=pt.cv.HI_RED)
        self.WS = pt.Style(fg=pt.cv.CYAN)
        self.INVALID = self.TEXT_LABEL
        self.MULTIBYTE = pt.Style(fg=pt.cv.DEEP_SKY_BLUE_1)
        self.BG = pt.Style(bg=pt.cv.NAVY_BLUE)
        self.SUB_BG = pt.Style(bg=pt.cv.DARK_BLUE, bold=True).autopick_fg()
        self.SUBTITLE = pt.Style(self.BG, bold=True, fg="gray-89")
        self.UNDEFINED = pt.Style(self.BG, fg=pt.cv.DARK_BLUE)
        self.BG_TOP = pt.Style(self.UNDEFINED, overlined=True)
        self.AXIS = pt.Style(self.BG, fg=pt.cvr.AIR_SUPERIORITY_BLUE)


class action(_BaseAction):
    def __init__(self, input_cps: tuple[str] | list[str], all: bool, list: bool, wide: bool):
        self.COL_WIDTH = (3, 4)[wide]
        self.MARGIN_LEFT =  self.COL_WIDTH
        self.MARGIN_RIGHT = self.COL_WIDTH

        self._cp_config = get_app_config_yaml("codepages")
        self._cp_names, self._cp_defs = self._make_map(self._cp_config)
        self._styles: Styles = Styles()
        self._wide = wide

        if all:
            input_cps = [*self._cp_names]
        if not input_cps:
            input_cps = ["ascii"]

        if list:
            get_stdout().echo("\n".join(self._cp_names))
            return

        input_cps = [*map(str.lower, input_cps)]
        for input_cp in input_cps:
            if input_cp not in self._cp_defs.keys():
                raise RuntimeError(
                    f"Unknown codepage: {input_cp!r}. See supported codepages with '--list'"
                )

        run_fn = with_terminal_state(tabs_interval=self.COL_WIDTH)(self._run)
        run_fn(input_cps=input_cps)

    def _make_map(self, cp_cofnig: list[dict]) -> tuple[list[str], dict[str, dict[str]]]:
        cp_names = list()
        cp_defs = dict()
        for cp in cp_cofnig:
            code = cp.get("code").lower()
            cp_names.append(code)
            for tfn in [
                lambda s: s,
                lambda s: s.replace('_', '-'),
                lambda s: s.replace('_', ''),
            ]:
                tcode = tfn(code)
                cp_defs[tcode] = cp
                for a in cp.get("aliases", []):
                    ta = tfn(a).lower()
                    cp_defs[ta] = cp_defs[tcode]
        return cp_names, cp_defs

    def _run(self, termstate: ProxiedTerminalState, input_cps: list[str]):
        lines = []
        sectsize = None
        for cp in input_cps:
            sect = self._print_cp(cp)
            if not sectsize:
                sectsize = len(sect)
            elif sectsize != len(sect):
                raise RuntimeError(f"Inconsistent sections sizes: {sectsize}, {len(sect)}")
            lines.extend(sect)

        c, ts = columns(
            lines,
            sectsize=sectsize,
            gap=["", "\t"][self._wide],
            sectgap=[0, 1][self._wide],
            tabsize=self.COL_WIDTH,
        )
        get_stdout().echoi_rendered(c)
        get_logger().debug(ts)

    def _print_cp(self, cp: str) -> list[str]:
        result = [
            self._format_top(cp),
            *self._format_main(cp),
            *self._format_bottom(),
        ]
        return result

    def _format_top(self, codepage: str) -> pt.Text:
        cpdef = self._cp_defs[codepage]

        max_len = self.COL_WIDTH * CHRCOL_NUM
        # if self._wide:
        max_len += self.MARGIN_LEFT + self.MARGIN_RIGHT
        space_left = max_len
        result = pt.Text()

        cp_el = (codepage, len(codepage) + self.MARGIN_LEFT + self.MARGIN_RIGHT, "^", self._styles.SUB_BG)

        alias_el = None
        if self._wide:
            alias_vis = cpdef.get("alias_vis", pt.pad(self.MARGIN_LEFT))
            if not alias_vis.isspace():
                alias_vis = f"({alias_vis})"
            alias_w = len(alias_vis)
            alias_el = (alias_vis, alias_w+2, "^", self._styles.BG)

        if self._wide:
            lang_el = (', '.join(cpdef.get("languages", ["*"])) + pt.pad(self.MARGIN_RIGHT), None, ">", self._styles.AXIS)
        else:
            lang_el = ('', None, None, self._styles.BG)

        for el in [cp_el, alias_el, lang_el]:
            if not el:
                continue
            string, w, align, st = el
            if w is None:
                w = space_left
                space_left = 0
            result += pt.Fragment(pt.fit(string, w, align=align), st)
            space_left = max(0, space_left-w)
            if space_left == 0:
                break

        return result

    def _format_bottom(self) -> Iterable[pt.Text]:
        # if not self._wide:
        #     return
        result = pt.Fragment(pt.fit("", self.MARGIN_LEFT), self._styles.BG)
        for lo in range(0, CHRCOL_NUM):
            result += pt.Fragment(f"{lo:^{self.COL_WIDTH}x}", self._styles.AXIS)
        result += pt.Fragment(pt.fit("", self.MARGIN_RIGHT), self._styles.BG)
        yield result
        return

    def _format_main(self, codepage: str) -> Iterable[pt.RT]:
        for hi in range(0, CHRCOL_NUM):
            line = ""
            # if  self._wide:
            line += pt.Fragment(f"{hi:x}x".ljust(self.MARGIN_LEFT), self._styles.AXIS)
            for lo in range(0, CHRCOL_NUM):
                i = lo + (hi << 4)
                c = bytes([i]).decode(codepage, errors="replace")
                st = self._styles.TEXT_SUBTITLE
                if c == "�" and (smb := self._sample_multibyte(codepage, i)):
                    c = smb
                    st = self._styles.MULTIBYTE
                c, st = self._format_char(c, st, hi, lo, i)
                if not c.endswith(LTR_CHAR):
                    c = f"{c:^{self.COL_WIDTH}.{self.COL_WIDTH}s}"
                cellw = len(c) if not c.endswith(LTR_CHAR) else len(c[:-1])
                if cellw < self.COL_WIDTH:  # and lo < CHRCOL_NUM-1:
                    c += '\t'
                line += pt.Fragment(c, st)
            # if  self._wide:
            line += pt.Fragment(pt.fit("▏", self.MARGIN_RIGHT), self._styles.UNDEFINED)
            yield line

    def _format_char(self, char: str, st: pt.FT, hi: int, lo: int, i: int) -> tuple[str, pt.FT]:
        s, cw = char, 1
        try:
            ucc = unicodedata.category(char)
            cw = pt.guess_char_width(char)
        except TypeError:
            ucc = ""
            s, st = f"?", self._styles.WARNING_ACCENT

        if ucc.startswith("C"):
            if ucc.startswith("Co"):
                s, st = f"?", self._styles.WARNING_LABEL
            else:
                st = self._styles.CC

                if char == "\u00AD":
                    s = "SHY"
                elif char == "\u200C":
                    s = "ZWNJ"
                elif char == "\u200D":
                    s = "ZWJ"
                elif char == "\u200E":
                    s = "LRM"
                elif char == "\u200F":
                    s = "RLM"
                else:
                    try:
                        s = resolve_ascii_cc(ord(char)).abbr
                    except LookupError:
                        s = f"?"

        elif ucc.startswith("Z"):
            st = self._styles.WS
            if char == "\x20":
                s = "SP"
            elif char == "\xa0":
                s = "NBSP"

        elif char == "�":
            s = f"▏{i:02x}".center(self.COL_WIDTH)
            st = pt.Style(self._styles.UNDEFINED, overlined=True, underlined=(hi == CHRCOL_NUM - 1))

        else:
            s = " " * (2 - max(cw, len(char))) + char + LTR_CHAR

        if ucc.startswith(("C", "Z")):
            if (hi - lo) % 2 == 1:
                st = st.clone()
                st.dim = True
        return s, st

    def _sample_multibyte(self, cp: str, i: int) -> str | None:
        size = self._cp_defs[cp].get("size")
        start = 0xB0 if size > 16 else 0xB0
        if size >= 16:
            for j in range(start, 0xFF):
                b = bytes([i, j])
                try:
                    c = b.decode(cp)
                except:
                    pass
                else:
                    return c
        return None
