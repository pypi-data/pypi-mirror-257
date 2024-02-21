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

import html

from sodom.context import DEFAULT_RENDER_CONTEXT, RenderContext
from sodom.elements import ANY_ELEMENT


def text(
    text: str,
    escape: bool = True,
) -> str:
    from sodom.elements import CURRENT_ELEMENT

    try:
        elem = CURRENT_ELEMENT.get()
    except LookupError as e:
        raise RuntimeError(f'{text} required sodom context') from e
    else:
        if escape:
            text = html.escape(text)
        elem.children.append(text)
    return text


def render(
    *elems: ANY_ELEMENT,
    ctx: RenderContext = DEFAULT_RENDER_CONTEXT,
) -> str:
    rendered_elems = list[str]()
    for elem in elems:
        if isinstance(elem, str):
            rendered_elem = f'{ctx.tabulation * ctx.level}{elem}'
        else:
            rendered_elem = elem.__html__(elem.ctx or ctx)
        rendered_elems.append(rendered_elem)
    return ctx.newline.join(rendered_elems)


def render_html(
    *elems: ANY_ELEMENT,
    ctx: RenderContext = DEFAULT_RENDER_CONTEXT,
) -> str:
    return render(
        '<!DOCTYPE html>',
        *elems,
        ctx=ctx,
    )


def render_now(root: ANY_ELEMENT):
    import tempfile
    import webbrowser

    tmp_file_path = tempfile.mktemp('.html', 'sodom.')
    with open(tmp_file_path, 'w+') as f:
        html = render_html(root)
        f.write(html)
    webbrowser.open_new_tab(tmp_file_path)
