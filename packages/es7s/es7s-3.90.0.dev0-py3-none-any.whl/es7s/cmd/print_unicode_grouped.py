# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2024 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
import re
import unicodedata
from collections import deque
from dataclasses import dataclass

import pytermor as pt
from es7s_commons.column import _dcu
from holms.core import CategoryStyles, Attribute, Options, Char
from holms.core.writer import Row, Column, get_view, CHAR_PLACEHOLDER
from holms.db import resolve_category

from ._base import _BaseAction
from ..shared import get_stdout, get_logger


@dataclass
class CharGroup:
    categ: str
    values: list[str]

    def append(self, val):
        self.values.append(val)


class action(_BaseAction):
    def __init__(self, *args, **kwargs):
        self._catstyles = CategoryStyles()
        self._render_name = lambda c: get_view(Attribute.NAME).render(
            Options(),
            Row(c, 0, 0),
            Column(Attribute.NUMBER, 0, 0),
        )
        self._run(*args, **kwargs)

    def _run(self, start: int, end: int):
        if end < start:
            end = start + 0xFF
        prev_categ = None
        chars = [*map(chr, range(start, end + 1))]
        queue = deque()

        while chars:
            categ = None
            if c := chars.pop(0):
                categ = unicodedata.category(c)
            if prev_categ and categ and (prev_categ != categ or (prev_categ[0] != categ[0] and categ[0] == 'L')):
                queue.append(CharGroup(prev_categ, []))
            prev_categ = categ
            if c:
                if not queue:
                    queue.append(CharGroup(categ, []))
                queue[-1].append(c)

        for grp in queue:
            self._print_categ(grp.values, grp.categ)

    def _ucs(self, c) -> str:
        return f"U+{ord(c):X}"

    def _print_categ(self, g, categ):
        if not g or not categ:
            return

        def _p(c):
            return (
                pt.pad(2)
                + "\t".join([self._print_char(c), self._ucs(c), self._render_name(Char(c))])
                + pt.pad(2)
            )

        def _c(c):
            try:
                cat_abbr = unicodedata.category(c)
                cat = resolve_category(cat_abbr)
            except ValueError as e:
                get_logger().warning(f"Failed to determine category of {c!r}: {e}")
                return "?"
            st = self._catstyles.get(cat_abbr)
            return get_stdout().render(cat.name, st)

        start = _p(g[0])
        end = None if len(g) < 2 else _p(g[-1])
        bounds = [*map(str.expandtabs, pt.filtern((start, end)))]
        max_len = max(len(_dcu(b)) for b in bounds)
        chars = [Char(c) for c in g]
        assigned = [c for c in chars if not c.is_invalid and not c.is_unassigned]
        counts = len(chars),
        cat = _c(g[0])
        cc = " {}  {}".format(_dcu(cat), *counts)
        bounds = [cc + pt.pad(max(0, max_len - len(_dcu(cc))))] + bounds

        label = pt.LINE_SINGLE.make(4 + max(len(_dcu(b)) for b in bounds), bounds)
        label = [*label]
        label[1] = re.sub(rf'{_dcu(cat)}(\s+\d+)(\s+)(?=\s)', rf'{cat}\2\1', label[1])
        stdout = get_stdout()
        [stdout.echo(line) for line in label]
        stdout.echo("".join(self._print_char(c) for c in chars))
        stdout.echo("")

    def _print_char(self, c: Char | str) -> str:
        if not isinstance(c, Char):
            c = Char(c)
        if c.should_print_placeholder:
            return CHAR_PLACEHOLDER
        return c.value
