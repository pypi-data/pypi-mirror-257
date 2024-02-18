import unittest
import json
from collections import OrderedDict

from . import *

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TestJsonUtil(unittest.TestCase):
    def test_diff(self):
        diff_simple_eq = diff(1, 1)
        self.assertEqual(diff_simple_eq['op'], None)
        self.assertTrue('val' in diff_simple_eq)

        diff_simple_neq = diff(1, 2)
        self.assertTrue(diff_simple_neq['val'], 2)
        self.assertEqual(diff_simple_neq['op'], 'mod')

        diff_dict0 = diff({'x': 0}, {'x': 0})
        self.assertEqual(diff_dict0['op'], None)

        diff_dict1 = diff({'x': 0}, {'x': 1})
        self.assertTrue(diff_dict1['diff'])
        self.assertTrue(diff_dict1['op'], 'dict')

        diff_dict2 = diff(
            {
                'x': {'s': 0}, 
                'y': {'s': 0}
            },
            {
                'x': {'s': 0},
                'y': {'s': 1}
            }
        )
        logger.debug(json.dumps(diff_dict2, indent=2))

        self.assertEqual(diff_dict2['diff']['y']['diff']['s']['val_from'], 0)
        self.assertEqual(diff_dict2['diff']['y']['diff']['s']['val'], 1)
        self.assertEqual(diff_dict2['op'], 'dict')
        self.assertEqual(diff_dict2['diff']['y']['diff']['s']['op'], 'mod')

        # TODO: test explicit_group_list

    def test_dict_to_sorted(self):
        dict_a = OrderedDict({
            'a': 1,
            'b': 2,
            'c': 3,
            'd': {
                'a': 1,
                'b': 2
            }
        })
        dict_b = OrderedDict({
            'c': 3,
            'b': 2,
            'd': {
                'b': 2,
                'a': 1
            },
            'a': 1,
        })
        self.assertNotEqual(dict_a, dict_b)

        sorted_a = dict_to_sorted(dict_a)
        sorted_b = dict_to_sorted(dict_b)
        self.assertEqual(sorted_a, sorted_b)
