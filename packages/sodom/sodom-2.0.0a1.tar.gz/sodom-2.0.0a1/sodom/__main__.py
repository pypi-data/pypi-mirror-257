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

from sodom import *
from sodom.renderers import render_now

def __main__():
    with html(lang='en') as doc:
        with head():
            meta(charset='utf-8')
            meta(name='viewport', content='width=device-width, initial-scale=1, shrink-to-fit=no')
            title('Hello sodom!')
            link(rel='stylesheet', href='https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css')
        with body():
            with section(class_='section'):
                with div(class_='container'):
                    with h1(class_='title'):
                        text('Hello World')
                    with p(class_='subtitle'):
                        text('My first website with ')
                        with a(href='https://pypi.org/project/sodom/'):
                            strong('sodom')
                        text('!')
    render_now(doc)


if __name__ == '__main__':
    __main__()
