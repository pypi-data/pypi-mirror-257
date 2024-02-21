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

import asyncio
import builtins
from concurrent.futures import ThreadPoolExecutor
import pickle
import tempfile
from threading import Barrier as ThreadBarrier
from asyncio import Barrier as AsyncBarrier
from time import time as time_
from uuid import uuid4
import webbrowser
import pytest

from sodom.attrs import Attrs, render_attrs, freeze
from sodom.context import ctx
from sodom.elements import CURRENT_ELEMENT
from sodom.renderers import render, render_html, render_now
from sodom import *
import sodom


def _rand_attr():
    return {
        str(uuid4()): str(uuid4())
    }


class TestHTMLElement:
    def test_lt(self):
        doc = div() < Attrs(foo='bar')
        assert doc.attrs == {'foo': 'bar'}
        assert doc.attrs != {'foo': ''}

        doc = div() < (Attrs(foo='bar'), Attrs(foo='baz'))
        assert doc.attrs == {'foo': 'bar baz'}
        assert doc.attrs != {'foo': 'bar'}
        assert doc.attrs != {'foo': 'baz'}
        assert doc.attrs != {'foo': ''}

    def test_mod(self):
        doc = div()
        assert doc.ctx is None
        current_ctx = ctx()
        doc = doc % current_ctx
        assert doc.ctx is current_ctx

        doc = div() < Attrs(foo='bar')
        assert doc.ctx is None
        assert doc.attrs['foo'] == 'bar'
        current_ctx = ctx()
        doc = doc % current_ctx < Attrs(foo='baz')
        assert doc.ctx is current_ctx
        assert doc.attrs['foo'] == 'bar baz'

    def test_call(self):
        attr = _rand_attr()

        doc = div(**attr)
        assert doc.tag == div.tag
        assert doc.attrs == attr and div.attrs == {}
        assert doc.parent is None
        assert doc is not div
        assert type(doc) is type(div)

    def test_call_with_context(self):
        attr = _rand_attr()

        with div() as doc:
            elem = div(**attr)
        assert elem.tag == div.tag
        assert elem.attrs == attr and div.attrs == {}
        assert elem.parent == doc
        assert div.parent is None

        current_ctx = ctx(
            '<CUSTOM_NEWLINE>',
            '<CUSTOM_TABULATION>',
            1,
            '<CUSTOM_QUOTES>',
            '<CUSTOM_UNDERSCORE_REPLACER>',
            '<CUSTOM_SEPARATOR>',
            ('<CUSTOM_SPECIAL_ATTRS>'),
        )

        with div(**{'<CUSTOM_SPECIAL_ATTRS>_foo': 'bar'}) % current_ctx as doc:
            elem = div(**attr)
        assert elem.tag == div.tag
        assert elem.attrs == attr and div.attrs == {}
        assert elem.parent == doc
        assert div.parent is None

        assert (
            '<CUSTOM_TABULATION><div <CUSTOM<CUSTOM_UNDERSCORE_REPLACER>SPECIAL<CUSTOM_UNDERSCORE_REPLACER>ATTRS><CUSTOM_UNDERSCORE_REPLACER>foo=<CUSTOM_QUOTES>bar<CUSTOM_QUOTES>><CUSTOM_NEWLINE>'
            f'<CUSTOM_TABULATION><CUSTOM_TABULATION><div {tuple(attr.keys())[0]}=<CUSTOM_QUOTES>{tuple(attr.values())[0]}<CUSTOM_QUOTES>></div><CUSTOM_NEWLINE>'
            '<CUSTOM_TABULATION></div>'
        ) == render(doc)

        current_ctx = ctx(
            '<CUSTOM_NEWLINE>',
            '<CUSTOM_TABULATION>',
            1,
            '<CUSTOM_QUOTES>',
            '_',
            '<CUSTOM_SEPARATOR>',
            ('<CUSTOM-SPECIAL-ATTRS>'),
        )

        with div(**{'<CUSTOM-SPECIAL-ATTRS>_foo': 'bar'}) % current_ctx as doc:
            elem = div(**attr)

        assert (
            '<CUSTOM_TABULATION><div <CUSTOM-SPECIAL-ATTRS>-foo=<CUSTOM_QUOTES>bar<CUSTOM_QUOTES>><CUSTOM_NEWLINE>'
            f'<CUSTOM_TABULATION><CUSTOM_TABULATION><div {tuple(attr.keys())[0]}=<CUSTOM_QUOTES>{tuple(attr.values())[0]}<CUSTOM_QUOTES>></div><CUSTOM_NEWLINE>'
            '<CUSTOM_TABULATION></div>'
        ) == render(doc % current_ctx)


class TestVoidElement:
    def test_render_with_tag(self):
        doc = hr()
        assert '<hr>' == render(doc)

    def test_render_with_attrs(self):
        doc = hr(test1='test1', test2='test2', test3='test3')
        assert '<hr test1="test1" test2="test2" test3="test3">' == render(doc)

    def test_repr_and_str(self):
        h = hr()
        assert '<hr @{}>'.format(id(h)) == repr(h)


class TestNormalElement:
    def test_render_with_tag(self):
        doc = div()
        assert '<div></div>' == render(doc)

    def test_render_with_attrs(self):
        elem = div(test1='test1', test2='test2', test3='test3')
        assert '<div test1="test1" test2="test2" test3="test3"></div>' == render(elem)

    def test_context_var(self):
        with div() as doc:
            assert CURRENT_ELEMENT.get() == doc
        with pytest.raises(LookupError):
            CURRENT_ELEMENT.get()

    def test_render_with_children(self):
        with div('0') as doc:
            text('1')
            div()
            text('2')
            div()
            text('3')
            with div('40'):
                text('41')
                div()
                text('42')
                div()
                text('43')
                div()
                text('44')
            text('5')

        assert (
            f'<div>\n'
            '  0\n'
            '  1\n'
            f'  <div></div>\n'
            '  2\n'
            f'  <div></div>\n'
            '  3\n'
            f'  <div>\n'
            '    40\n'
            '    41\n'
            f'    <div></div>\n'
            '    42\n'
            f'    <div></div>\n'
            '    43\n'
            f'    <div></div>\n'
            '    44\n'
            '  </div>\n'
            '  5\n'
            '</div>'
        ) == render(doc)

    def test_repr_and_str(self):
        d = div()
        assert '<div @{}>:0</div>'.format(id(d)) == repr(d)
        assert '<div @{}>:0</div>'.format(id(d)) == str(d)

        with div(attr='attr') as d:
            div()
        assert '<div attr="attr" @{}>:1</div>'.format(id(d)) == repr(d)
        assert '<div attr="attr" @{}>:1</div>'.format(id(d)) == str(d)

    def test_add_children(self):
        with div() as doc:
            h = hr()
        assert h in doc.children
        assert h.parent == doc

    def test_empty_attr_adding(self):
        with div() as doc:
            Attrs(disabled='')()
        assert (
            '<div disabled></div>'
        ) == render(doc)

    def test_empty_attr_removing(self):
        doc = div() < {'disabled': ''}
        doc.attrs.pop('disabled')
        assert (
            '<div></div>'
        ) == render(doc)

    def test_pickle(self):
        with div(foo='bar') as doc:
            br()
        p = pickle.dumps(doc)
        unpickled_doc = pickle.loads(p)
        assert render(doc) == render(unpickled_doc)


class TestAttrs:
    def test_torow(self):
        attrs = Attrs(
            foo='bar',
            class_='bar',
            _class='bar',
            _class_='bar',
            class__='bar',
            _class__='bar',
            __class='bar',
            __class_='bar',
            __class__='bar',
        )

        assert render_attrs(freeze(attrs)) == (
            'foo="bar" '
            'class="bar" '
            'class="bar" '
            'class="bar" '
            'class="bar" '
            'class="bar" '
            'class="bar" '
            'class="bar" '
            'class="bar"'
        )

        assert render_attrs(freeze(attrs), separator=', ') == (
            'foo="bar", '
            'class="bar", '
            'class="bar", '
            'class="bar", '
            'class="bar", '
            'class="bar", '
            'class="bar", '
            'class="bar", '
            'class="bar"'
        )

        assert render_attrs(freeze(attrs), quotes='\'') == (
            'foo=\'bar\' '
            'class=\'bar\' '
            'class=\'bar\' '
            'class=\'bar\' '
            'class=\'bar\' '
            'class=\'bar\' '
            'class=\'bar\' '
            'class=\'bar\' '
            'class=\'bar\''
        )

    def test_torow_underscore_replacer(self):
        attrs = Attrs(
            foo_bar='baz',
        )

        assert render_attrs(freeze(attrs), underscore_replacer='-') == (
            'foo-bar="baz"'
        )

        assert render_attrs(freeze(attrs), underscore_replacer='_') == (
            'foo_bar="baz"'
        )

    def test_call_attr_with_context(self):
        attr0 = Attrs(foo='bar')
        attr1 = Attrs(foo='baz')

        with div() as doc:
            attr0()
            attr1()

        assert doc.attrs['foo'] == f'{attr0['foo']} {attr1['foo']}'

class TestRenderers:
    def test_text(self):
        text_data = str(uuid4())
        with div() as d:
            text(text_data)
        assert text_data in d.children

    def test_render(self):
        result = render('')
        assert result == ''

        with div(foo='bar') as doc:
            br()
            text('0')

        result = render(doc, '1')
        assert (
            '<div foo="bar">\n'
            '  <br>\n'
            '  0\n'
            '</div>\n'
            '1'
        ) == result

    def test_render_html(self):
        d = div()
        assert (
            '<!DOCTYPE html>\n'
            + render(d)
        ) == render_html(d)

    def test_render_now(self, monkeypatch: pytest.MonkeyPatch):
        with monkeypatch.context() as m:
            checklist = {
                'is_tempfile_created': False,
                'if_file_wrote': False,
                'is_webbrowser_opened': False,
            }

            m.setattr(
                builtins,
                'open',
                type(
                    'open', (),
                    {
                        '__call__': lambda self, *args: self,
                        'write': lambda self, *args: checklist.update(if_file_wrote=True),
                        '__enter__': lambda self: self,
                        '__exit__': lambda self, *args: None,
                    }
                )()
            )

            m.setattr(
                tempfile,
                'mktemp',
                lambda *args: checklist.update(is_tempfile_created=True),
            )

            m.setattr(
                webbrowser,
                'open_new_tab',
                lambda *args: checklist.update(is_webbrowser_opened=True),
            )

            render_now('')
            assert all(checklist.values())


class TestContext:
    @pytest.mark.asyncio
    async def test_building_html_in_two_tasks(self):
        async def task1(b: AsyncBarrier):
            await b.wait()
            with div() as d:
                await b.wait()
                text('task1')
                await b.wait()
                text('task1')
                await b.wait()
            await b.wait()
            return d

        async def task2(b: AsyncBarrier):
            await b.wait()
            with div() as d:
                await b.wait()
                text('task2')
                await b.wait()
                text('task2')
                await b.wait()
            await b.wait()
            return d

        CORO_NUMBER = 2
        b = AsyncBarrier(CORO_NUMBER)

        div1, div2 = await asyncio.gather(
            task1(b),
            task2(b),
        )

        assert div1.children[0] == 'task1'
        assert div1.children[1] == 'task1'
        assert div2.children[0] == 'task2'
        assert div2.children[1] == 'task2'

    def test_building_html_in_two_threads(self):
        def task1(b: ThreadBarrier):
            b.wait()
            with div() as d:
                b.wait()
                text('task1')
                b.wait()
                text('task1')
                b.wait()
            b.wait()
            return d

        def task2(b: ThreadBarrier):
            b.wait()
            with div() as d:
                b.wait()
                text('task2')
                b.wait()
                text('task2')
                b.wait()
            b.wait()
            return d

        THREAD_NUMBER = 2
        with ThreadPoolExecutor(THREAD_NUMBER) as pool:
            b = ThreadBarrier(THREAD_NUMBER)
            t1 = pool.submit(task1, b)
            t2 = pool.submit(task2, b)
            div1 = t1.result()
            div2 = t2.result()

        assert div1.children[0] == 'task1'
        assert div1.children[1] == 'task1'
        assert div2.children[0] == 'task2'
        assert div2.children[1] == 'task2'


def _sodom_case():
    with sodom.body() as root:
        with sodom.div(class_='d-flex flex-column flex-md-row align-items-center p-3 px-md-4 mb-3 bg-white border-bottom box-shadow'):
            with sodom.h5(class_='my-0 mr-md-auto font-weight-normal'):
                sodom.text('Company name')
            with sodom.nav(class_='my-2 my-md-0 mr-md-3'):
                with sodom.a(class_='p-2 text-dark', href='#'):
                    text('Features')
                with sodom.a(class_='p-2 text-dark', href='#'):
                    text('Enterprise')
                with sodom.a(class_='p-2 text-dark', href='#'):
                    text('Support')
                with sodom.a(class_='p-2 text-dark', href='#'):
                    text('Pricing')
    result = str(root)
    pass


def _dominate_case():
    with dominate_tags.body() as root:
        with dominate_tags.div(cls='d-flex flex-column flex-md-row align-items-center p-3 px-md-4 mb-3 bg-white border-bottom box-shadow'):
            with dominate_tags.h5(cls='my-0 mr-md-auto font-weight-normal'):
                dominate_text('Company name')
            with dominate_tags.nav(cls='my-2 my-md-0 mr-md-3'):
                with dominate_tags.a(cls='p-2 text-dark', href='#'):
                    dominate_text('Features')
                with dominate_tags.a(cls='p-2 text-dark', href='#'):
                    dominate_text('Enterprise')
                with dominate_tags.a(cls='p-2 text-dark', href='#'):
                    dominate_text('Support')
                with dominate_tags.a(cls='p-2 text-dark', href='#'):
                    dominate_text('Pricing')
    result = root.render()
    pass


try:
    from dominate import tags as dominate_tags
    from dominate.util import text as dominate_text
except ImportError:
    pass
else:
    def test_performance_dominate():
        # d = _dominate_case()
        # s = _sodom_case()

        RUNS = 10_000

        sodom_case_total_time = 0
        for _ in range(RUNS):
            start = time_()
            _sodom_case()
            sodom_case_total_time += time_() - start

        dominate_case_total_time = 0
        for _ in range(RUNS):
            start = time_()
            _dominate_case()
            dominate_case_total_time += time_() - start

        print()
        print('sodom_case_total_time: ', sodom_case_total_time, '; ', sodom_case_total_time / RUNS, sep='')
        print('dominate_case_total_time: ', dominate_case_total_time, '; ', dominate_case_total_time / RUNS, sep='')
        ratio = dominate_case_total_time / sodom_case_total_time
        print('ratio:', ratio)
        assert ratio >= 1
