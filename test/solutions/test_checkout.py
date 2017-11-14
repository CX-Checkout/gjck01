from lib.solutions.checkout import (
    checkout,
    get_sku_counts,
    grouper,
    get_group_discounts,
    get_string_of_skus_in_offer,
    sorted_by_most_expensive_first
)


from parameterizedtestcase import ParameterizedTestCase

class MyTests (ParameterizedTestCase):
    def test_no_items_return_0(self):
        self.assertEqual(checkout(''), 0)

    @ParameterizedTestCase.parameterize(
        ("basket", "expected_output"),
        [
            ("A", 50),
            ("B", 30),
            ("C", 20),
            ("D", 15),
            ("E", 40),
            ("F", 10),
            ("G", 20),
            ("H", 10),
        ]
    )
    def test_single_items(self, basket, expected_output):
        self.assertEqual(checkout(basket), expected_output)

    @ParameterizedTestCase.parameterize(
        ("basket", "expected_output"),
        [
            ("AB", 80),
        ]
    )
    def test_no_special_offer_group(self, basket, expected_output):
        self.assertEqual(checkout(basket), expected_output)

    @ParameterizedTestCase.parameterize(
        ("basket", "expected_output"),
        [
            ("AAA", 130),
            ("A"*6, 250),
            ("A"*4, 180),
            ("A"*5, 200),
        ]
    )
    def test_special_offer_for_As(self, basket, expected_output):
        self.assertEqual(checkout(basket), expected_output)

    @ParameterizedTestCase.parameterize(
        ("basket", "expected_output"),
        [
            ("BB", 45),
            ("BBBB", 90),
            ("BBB", 75),
        ]
    )
    def test_special_offer_for_Bs(self, basket, expected_output):
        self.assertEqual(checkout(basket), expected_output)

    @ParameterizedTestCase.parameterize(
        ("basket", "expected_output"),
        [
            ("EEB", 80),
            ("EEBB", 110),
            ("EEBBB", 125),
            ("EE", 80),
        ]
    )
    def test_special_offer_for_Es(self, basket, expected_output):
        self.assertEqual(checkout(basket), expected_output)

    @ParameterizedTestCase.parameterize(
        ("basket", "expected_output"),
        [
            ("FF", 20),
            ("FFF", 20),
            ("FFFF", 30),
        ]
    )
    def test_special_offer_for_Fs(self, basket, expected_output):
        self.assertEqual(checkout(basket), expected_output)

    @ParameterizedTestCase.parameterize(
        ("basket", "expected_output"),
        [
            ("H"*5, 45),
            ("H" * 10, 80),
        ]
    )
    def test_special_offer_for_Hs(self, basket, expected_output):
        self.assertEqual(checkout(basket), expected_output)

    @ParameterizedTestCase.parameterize(
        ("basket", "expected_output"),
        [
            ("U" * 3, 120),
        ]
    )
    def test_special_offer_for_Hs(self, basket, expected_output):
        self.assertEqual(checkout(basket), expected_output)

    @ParameterizedTestCase.parameterize(
        ("basket"),
        [
            (50,),
        ]
    )
    def test_invalid_inputs(self, basket):
        self.assertEqual(checkout(basket), -1)

    @ParameterizedTestCase.parameterize(
        ("basket", "expected_price"),
        [
            ('SST', 45),
            ('SSX', 45),
            ('SSSSSS', 90),
            ('SSSXXX', 90),
            ('SSSSSSZ', 110),
        ]
    )
    def test_any_3_of_STXYZ_for_45_offer(self, basket, expected_price):
        self.assertEqual(checkout(basket), expected_price)



class TestGetSkuCounts(ParameterizedTestCase):
    @ParameterizedTestCase.parameterize(
        ("basket", "expected_output"),
        [
            ("A", {'A': 1}),
            ("AA", {'A': 2}),
            ("BAA", {'A': 2, 'B': 1}),
        ]
    )
    def test_counts(self, basket, expected_output):
        sku_counts = get_sku_counts(basket)
        non_zero_sku_counts = {k: v for k, v in sku_counts.items() if v > 0}
        self.assertDictEqual(non_zero_sku_counts, expected_output)


class TestGrouper(ParameterizedTestCase):
    @ParameterizedTestCase.parameterize(
        ("basket", "expected_groups"),
        [
            ("AAA", [('A', 'A', 'A')]),
            ("AAAA", [('A', 'A', 'A')]),
            ("AAAAA", [('A', 'A', 'A')]),
            ("AAAAAA", [('A', 'A', 'A'), ('A', 'A', 'A')]),
            ("ABCDEF", [('A', 'B', 'C'), ('D', 'E', 'F')]),
            ('ZSSSSSS', [('Z', 'S', 'S'), ('S', 'S', 'S')]),
        ]
    )
    def test(self, basket, expected_groups):
        self.assertEqual(grouper(basket, 3), expected_groups)


class TestGetGroupDiscounts(ParameterizedTestCase):
    @ParameterizedTestCase.parameterize(
        ("sku_counts", "expected_discount"),
        [
            ({'S': 2, 'T': 1}, 15),
            ({'S': 6, 'Z': 1}, 31),
        ]
    )
    def test(self, sku_counts, expected_discount):
        self.assertEqual(get_group_discounts(sku_counts), expected_discount)


class TestGetStringOfSkusInOffer(ParameterizedTestCase):
    @ParameterizedTestCase.parameterize(
        ("sku_counts", "expected_discount"),
        [
            ({'S': 2, 'T': 1}, 'SST'),
            ({'S': 2, 'T': 1, 'A': 4}, 'SST'),
        ]
    )
    def test(self, sku_counts, expected_string):
        self.assertEqual(
            get_string_of_skus_in_offer(
                sku_counts,
                ['S', 'T', 'X', 'Y', 'Z']
            ),
            expected_string
        )



class TestSortedByMostExpensiveFirst(ParameterizedTestCase):
    @ParameterizedTestCase.parameterize(
        ("sku_string", "expected_output"),
        [
            ('XYZ', 'ZYX'),
            ('SSSSSSZ', 'ZSSSSSS'),
        ]
    )
    def test(self, skus_string, expected_output):
        self.assertEqual(
            sorted_by_most_expensive_first(skus_string),
            expected_output
        )