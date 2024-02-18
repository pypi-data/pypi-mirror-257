import unittest
import json
from collections import OrderedDict

from . import *

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TestHashUtil(unittest.TestCase):
    def test_dict_hash(self):
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
        dict_c = OrderedDict({
            'a': 1,
            'b': 2,
            'c': 3,
            'd': {
                'a': 1,
                'b': 2
            }
        })
        dict_d = OrderedDict({
            'a': 1
        })
        self.assertNotEqual(dict_a, dict_b)
        self.assertEqual(dict_a, dict_c)
        self.assertNotEqual(get_dict_hash(dict_a), get_dict_hash(dict_d))
        self.assertEqual(get_dict_hash(dict_a), get_dict_hash(dict_b))
        self.assertEqual(get_dict_hash(dict_a), get_dict_hash(dict_c))
