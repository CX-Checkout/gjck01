from unittest import TestCase
from lib.solutions.checkout import checkout

from parameterizedtestcase import ParameterizedTestCase

class MyTests (ParameterizedTestCase):
    def test_no_items_return_0(self):
        self.assertEqual(checkout(''), 0)

    @ParameterizedTestCase.parameterize(
        ("input", "expected_output"),
        [
            ("A", 50),
            ("B", 30),
            ("C", 20),
            ("D", 15),
        ]
    )
    def test_single_items(self, input, expected_output):
        self.assertEqual(checkout(input), expected_output)

    @ParameterizedTestCase.parameterize(
        ("input", "expected_output"),
        [
            ("AB", 80),
        ]
    )
    def test_no_special_offer_group(self, input, expected_output):
        self.assertEqual(checkout(input), expected_output)

    @ParameterizedTestCase.parameterize(
        ("input", "expected_output"),
        [
            ("AAA", 130),
            ("AAAAAA", 260),
            ("AAAA", 180),
        ]
    )
    def test_special_offer_for_As(self, input, expected_output):
        self.assertEqual(checkout(input), expected_output)

    @ParameterizedTestCase.parameterize(
        ("input", "expected_output"),
        [
            ("BB", 45),
            ("BBBB", 90),
            ("BBB", 75),
        ]
    )
    def test_special_offer_for_Bs(self, input, expected_output):
        self.assertEqual(checkout(input), expected_output)

    @ParameterizedTestCase.parameterize(
        ("input"),
        [
            (50,),
            ('X',)
        ]
    )
    def test_invalid_inputs(self, input):
        self.assertEqual(checkout(input), -1)