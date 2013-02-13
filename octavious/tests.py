import unittest

from octavious.pipeline import Plugin, Pipeline
from octavious.utils import load_symbol, call_symbol


class Plugin1(Plugin):

    def pre_process(self, input):
        return {'pre_processed_1': True}

    def post_process(self, input, output):
        output['post_processed_1'] = True
        return output


class Plugin2(Plugin):

    def pre_process(self, input):
        return {'pre_processed_2': True}

    def post_process(self, input, output):
        new_output = output.copy()
        new_output['post_processed_2'] = True
        return new_output


class Plugin3(Plugin):

    def pre_process(self, input):
        return {'pre_processed_3': True}

    def post_process(self, input, output):
        output['post_processed_3'] = True
        return output


class Plugin4(object):
    pass


class TestUtils(unittest.TestCase):

    def test_load_symbol(self):
        plugin_class = load_symbol('octavious.tests', 'Plugin1')
        self.assertEqual(plugin_class.__name__, 'Plugin1')
        with self.assertRaises(ImportError):
            load_symbol('octavious.tests', 'NotAvailableSymbol')

    def test_call_symbol(self):
        plugin = call_symbol('octavious.tests', 'Plugin1')
        self.assertEqual(plugin.__class__.__name__, 'Plugin1')
        self.assertTrue(isinstance(plugin, Plugin1))
        with self.assertRaises(ImportError):
            call_symbol('octavious.tests', 'NotAvailableSymbol')


class TestPipeline(unittest.TestCase):

    def test_pipeline(self):
        plugins = [
            call_symbol('octavious.tests', 'Plugin1'),
            call_symbol('octavious.tests', 'Plugin2'),
            call_symbol('octavious.tests', 'Plugin3'),
        ]
        pipeline = Pipeline(plugins)
        output = pipeline.pre_process({})
        output = pipeline.post_process({}, output)
        self.assertTrue(output['pre_processed_1'])
        self.assertTrue(output['post_processed_1'])
        self.assertTrue(output['post_processed_2'])
        self.assertTrue(output['post_processed_3'])
        with self.assertRaises(KeyError):
            self.assertTrue(output['pre_processed_2'])
        with self.assertRaises(KeyError):
            self.assertTrue(output['pre_processed_3'])

if __name__ == '__main__':
    unittest.main()
