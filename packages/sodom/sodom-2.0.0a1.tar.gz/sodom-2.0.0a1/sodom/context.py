from dataclasses import dataclass
from typing import Sequence

DEFAULT_NEWLINE = '\n'
DEFAULT_TABULATION = '  '
DEFAULT_LEVEL = 0
DEFAULT_QUOTES = '"'
DEFAULT_UNDERSCORE_REPLACER = '-'
DEFAULT_SEPARATOR = ' '
DEFAULT_SPECIAL_ATTRS = (
    'data',
    'aria',
    'x',
    'v',
    'hx',
)

DEFAULT_ELEM_CONTEXT = (
    DEFAULT_NEWLINE,
    DEFAULT_TABULATION,
    DEFAULT_LEVEL,
)

DEFAULT_ATTR_CONTEXT = (
    DEFAULT_QUOTES,
    DEFAULT_UNDERSCORE_REPLACER,
    DEFAULT_SEPARATOR,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class RenderContext:
    ##### ELEMS #####
    newline: str = DEFAULT_NEWLINE
    tabulation: str = DEFAULT_TABULATION
    level: int = DEFAULT_LEVEL

    ##### ATTRS #####
    quotes: str = DEFAULT_QUOTES
    underscore_replacer: str = DEFAULT_UNDERSCORE_REPLACER
    separator: str = DEFAULT_SEPARATOR
    special_attrs: Sequence[str] = DEFAULT_SPECIAL_ATTRS

    def with_next_level(self) -> 'RenderContext':
        copied_self = ctx(
            newline=self.newline,
            tabulation=self.tabulation,
            level=self.level + 1,
            quotes=self.quotes,
            underscore_replacer=self.underscore_replacer,
            separator=self.separator,
            special_attrs=self.special_attrs,
        )
        return copied_self


DEFAULT_RENDER_CONTEXT = RenderContext()


def ctx(
    ##### ELEMS #####
    newline: str = DEFAULT_NEWLINE,
    tabulation: str = DEFAULT_TABULATION,
    level: int = DEFAULT_LEVEL,

    ##### ATTRS #####
    quotes: str = DEFAULT_QUOTES,
    underscore_replacer: str = DEFAULT_UNDERSCORE_REPLACER,
    separator: str = DEFAULT_SEPARATOR,
    special_attrs: Sequence[str] = DEFAULT_SPECIAL_ATTRS,
) -> RenderContext:
    result = RenderContext(
        newline=newline,
        tabulation=tabulation,
        level=level,
        quotes=quotes,
        underscore_replacer=underscore_replacer,
        separator=separator,
        special_attrs=special_attrs,
    )
    return result
