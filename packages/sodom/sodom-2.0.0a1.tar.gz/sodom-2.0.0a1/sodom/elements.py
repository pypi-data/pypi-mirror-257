__license__ = '''
sodom
Copyright (C) 2023  Dmitry Protasov (inbox@protaz.ru)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General
Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

from contextvars import ContextVar, Token
from operator import truth
from typing import Any, Iterable, MutableSequence, Optional, Self, Sequence

from sodom.attrs import Attrs, render_attrs, freeze
from sodom.context import DEFAULT_RENDER_CONTEXT, RenderContext
from sodom.literals import ANY_TAGS, NORMAL_TAGS, VOID_TAGS


CURRENT_ELEMENT = ContextVar['NORMAL_ELEMENT']('CURRENT_ELEMENT')


def _opening_tag_content(
    tag: ANY_TAGS,
    frozenattrs: Iterable[tuple[str, str]],
    quotes: str,
    underscore_replacer: str,
    separator: str,
    special_attrs: Sequence[str],
) -> str:
    result = ' '.join(filter(
        truth,
        (
            tag,
            render_attrs(
                frozenattrs,
                quotes,
                underscore_replacer,
                separator,
                special_attrs,
            ),
        ),
    ))

    return result


_opening_tag_format = '{}<{}>'.format
_closing_tag_format = '{}</{}>'.format
_void_repr_format = '<{} @{}>'.format
_normal_repr_format = '<{} @{}>:{}</{}>'.format
_fast_elem_copy = lambda elem: type(elem)(elem.tag, **elem.attrs)
_fast_elem_parent_update = lambda elem: elem._set_parent(CURRENT_ELEMENT.get(None))


class HTMLElement[TAG: ANY_TAGS]:
    __slots__ = (
        'parent',
        'tag',
        'attrs',
        'ctx',
    )

    parent: 'NORMAL_ELEMENT | None'
    tag: TAG
    attrs: Attrs
    ctx: Optional[RenderContext]

    def __init__(self, tag: TAG, **attrs: str) -> None:
        self.parent = None
        self.tag = tag
        self.attrs = Attrs(attrs)
        self.ctx = None

    def __lt__(self, other_attrs: dict[str, str] | Sequence[dict[str, str]]) -> Self:
        if isinstance(other_attrs, dict):
            other_attrs = (other_attrs,)

        for other_attr in other_attrs:
            self.attrs |= other_attr

        return self

    def __mod__(self: Self, ctx: RenderContext) -> Self:
        self.ctx = ctx
        return self

    def __call__(
        self: Self,
        **attrs: str,
    ) -> Self:
        copied_self = _fast_elem_copy(self)
        copied_self.attrs |= attrs
        _fast_elem_parent_update(copied_self)
        return copied_self

    def _set_parent(
        self: Self,
        new_parent: 'NormalElement[Any] | None',
    ) -> None:
        if self.parent is not None:
            self.parent.children.remove(self)
        if new_parent is not None:
            new_parent.children.append(self)
        self.parent = new_parent

    def __html__(
        self: Self,
        ctx: RenderContext,
    ) -> str:
        raise NotImplementedError()


class VoidElement[TAG: VOID_TAGS](HTMLElement[TAG]):
    __slots__ = ()

    def __init__(self, tag: TAG, **attrs: str) -> None:
        super().__init__(tag, **attrs)

    ##### RENDERING #####
    def __html__(
        self: Self,
        ctx: RenderContext,
    ) -> str:
        tag_content = _opening_tag_content(
            self.tag,
            freeze(self.attrs),
            ctx.quotes,
            ctx.underscore_replacer,
            ctx.separator,
            ctx.special_attrs,
        )
        result = _opening_tag_format(ctx.tabulation * ctx.level, tag_content)
        return result

    def __repr__(self) -> str:
        ctx = self.ctx or DEFAULT_RENDER_CONTEXT

        tag_content = _opening_tag_content(
            self.tag,
            freeze(self.attrs),
            ctx.quotes,
            ctx.underscore_replacer,
            ctx.separator,
            ctx.special_attrs,
        )
        result = _void_repr_format(tag_content, id(self))
        return result


class NormalElement[TAG: NORMAL_TAGS](HTMLElement[TAG]):
    __slots__ = (
        'children',
        '_context_token',
    )

    children: MutableSequence['ANY_ELEMENT']
    _context_token: Token['NORMAL_ELEMENT']

    def __init__(self, tag: TAG, **attrs: str) -> None:
        super().__init__(tag, **attrs)
        self.children = list['ANY_ELEMENT']()

    def __call__(
        self: Self,
        text: Optional[str] = None,
        **attrs: str,
    ) -> Self:
        copied_self = super().__call__(**attrs)
        if text is not None:
            copied_self.children.append(text)
        return copied_self

    ##### PICKLE STATE #####
    def __getstate__(self: Self, *args, **kwargs):
        *results, state = super().__getstate__(*args, **kwargs) # type: ignore
        state.pop('_context_token', None)
        return *results, state

    ##### CONTEXT MANAGEMENT #####
    def __enter__(self) -> Self:
        self._context_token = CURRENT_ELEMENT.set(self)
        return self

    def __exit__(self, *_) -> None:
        CURRENT_ELEMENT.reset(self._context_token)
        del self._context_token

    ##### RENDERING #####
    def __html__(
        self: Self,
        ctx: RenderContext,
    ) -> str:
        from sodom.renderers import render

        HAS_NEWLINE = truth(ctx.newline)
        HAS_TAG_BODY_CONTENT = truth(self.children)

        opening_tag_content = _opening_tag_content(
            self.tag,
            freeze(self.attrs),
            ctx.quotes,
            ctx.underscore_replacer,
            ctx.separator,
            ctx.special_attrs,
        )
        opening_tag_tabulation = ctx.tabulation * ctx.level * HAS_NEWLINE
        closing_tag_tabulation = opening_tag_tabulation * HAS_TAG_BODY_CONTENT
        inner_tag_separator = f'{ctx.newline * HAS_TAG_BODY_CONTENT}'

        opening_tag = _opening_tag_format(opening_tag_tabulation, opening_tag_content)
        tag_content = render(*self.children, ctx=ctx.with_next_level())
        closing_tag = _closing_tag_format(closing_tag_tabulation, self.tag)

        result = inner_tag_separator.join((
            opening_tag,
            tag_content,
            closing_tag,
        ))
        return result

    def __repr__(self) -> str:
        ctx = self.ctx or DEFAULT_RENDER_CONTEXT

        tag_content = _opening_tag_content(
            self.tag,
            freeze(self.attrs),
            ctx.quotes,
            ctx.underscore_replacer,
            ctx.separator,
            ctx.special_attrs,
        )

        result = _normal_repr_format(
            tag_content,
            id(self),
            len(self.children),
            self.tag,
        )

        return result


VOID_ELEMENT = VoidElement[VOID_TAGS]
NORMAL_ELEMENT = NormalElement[NORMAL_TAGS]
ANY_ELEMENT = HTMLElement[Any] | str
