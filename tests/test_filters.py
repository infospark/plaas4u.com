import unittest
from plaas4u_app import playing


class Tests(unittest.TestCase):
    def test_extract_float_should_work_with_commas(self):  # test method
        input_string = "423,543.34"
        expected_result = 423543.34
        actual_result = playing.extract_float_from_string(input_string)
        self.assertEqual(actual_result, expected_result)

    def test_extract_float_should_work_with_round_numbers(self):  # test method
        input_string = "423543"
        expected_result = 423543
        actual_result = playing.extract_float_from_string(input_string)
        self.assertEqual(actual_result, expected_result)

    def test_extract_float_should_work_with_currency_symbols(self):  # test method
        input_string = "R 423,543.00"
        expected_result = 423543
        actual_result = playing.extract_float_from_string(input_string)
        self.assertEqual(actual_result, expected_result)