from django.template import Context, Template
from django.test import SimpleTestCase


class IntspaceFilterTests(SimpleTestCase):
    def render_template(self, string, context=None):
        context = context or {}
        context = Context(context)
        template = Template('{% load pola_extras %}' + string)
        return template.render(context)

    def test_intspace_filter(self):
        rendered = self.render_template('{{ 1234|intspace }}')
        self.assertEqual(rendered, '1 234')

    def test_intspace_with_large_number(self):
        rendered = self.render_template('{{ 1234567890|intspace }}')
        self.assertEqual(rendered, '1 234 567 890')

    def test_intspace_with_negative_number(self):
        rendered = self.render_template('{{ -1234|intspace }}')
        self.assertEqual(rendered, '-1 234')

    def test_intspace_with_zero(self):
        rendered = self.render_template('{{ 0|intspace }}')
        self.assertEqual(rendered, '0')
