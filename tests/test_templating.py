from unittest import TestCase

from induction import Induction
from jinja2.exceptions import TemplateNotFound

app = Induction(__name__, template_folder='tests/templates')


class TemplatingTests(TestCase):
    def test_render_template(self):
        rendered = app.render_template('index.html', test=True)
        self.assertEqual(rendered, 'Test!')

        rendered = app.render_template('index.html', test=False)
        self.assertEqual(rendered, 'Nope!')

    def test_template_does_not_exist(self):
        with self.assertRaises(TemplateNotFound):
            app.render_template('inexisting.html')

    def test_select_template(self):
        rendered = app.render_template(['foo.html', 'index.html'], test=False)
        self.assertEqual(rendered, 'Nope!')
