import unittest
from plaas4u_app import Farms


class TestFiltersAndSorts(unittest.TestCase):
    farm_1 = {
        "Listing Number": "1"
        , "Size (ha)": "200"
        , "Price (Rand)": "100000"
        , "Bedrooms": 3
    }
    # And another hypothetical farm
    farm_2 = {
        "Listing Number": "2"
        , "Size (ha)": "300"
        , "Price (Rand)": "150000"
        , "Bedrooms": 2
    }
    farm_3 = {
        "Listing Number": "3"
        , "Size (ha)": "2500"
        , "Price (Rand)": "125000"
        , "Bedrooms": None
    }

    all_farms = [farm_1, farm_2, farm_3]

    def test_filter_by_min_and_max(self):
        big_farms = Farms.filter_by_min_max(self.all_farms, "Size (ha)", 2000, 9999)
        self.assertEqual(len(big_farms), 1)


    def test_filter_by_min_and_max_on_none_values(self):
        filtered_farms = Farms.filter_by_min_max(self.all_farms, "Bedrooms", 3, 99)
        self.assertEqual(len(filtered_farms), 1)


    def test_filter_by_min_and_max_on_missing_key(self):
        filtered_farms = Farms.filter_by_min_max(self.all_farms, "Wine Yield", 3, 99)
        self.assertEqual(len(filtered_farms), 1)


    def test_extract_float_should_work_with_commas(self):  # test method
        input_string = "423,543.34"
        expected_result = 423543.34
        actual_result = Farms.extract_float_from_string(input_string)
        self.assertEqual(actual_result, expected_result)

    def test_extract_float_should_work_with_round_numbers(self):  # test method
        input_string = "423543"
        expected_result = 423543
        actual_result = Farms.extract_float_from_string(input_string)
        self.assertEqual(actual_result, expected_result)

    def test_extract_float_should_work_with_currency_symbols(self):  # test method
        input_string = "R 423,543.00"
        expected_result = 423543
        actual_result = Farms.extract_float_from_string(input_string)
        self.assertEqual(actual_result, expected_result)

    def test_filter_by_price_filters_out_expensive_farms(self): # test method
        maximum_price = 120000
        # we expect the filter function to just return a list that only contains farm_1
        # as it was the only one under the specified price
        expected_result = [self.farm_1]
        actual_result = Farms.filter_by_min_max(self.all_farms, "Price (Rand)", 0,  maximum_price)
        self.assertEqual(actual_result, expected_result)

    def test_filter_by_size_filters_out_small_farms(self):
        minimum_size = 1000
        expected_result = [self.farm_3]
        actual_result = Farms.filter_by_min_max(self.all_farms, 'Size (ha)', minimum_size, 999999999)
        self.assertEqual(actual_result, expected_result)

    def test_sort_by_hectares(self):
        sorted_farms = Farms.sort_by_key(self.all_farms, 'Size (ha)')
        self.assertTrue(sorted_farms[0]['Size (ha)'] == '200')
        self.assertTrue(sorted_farms[-1]['Size (ha)'] == '2500')

    def test_sort_by_price(self):
        sorted_farms = Farms.sort_by_key(self.all_farms, 'Price (Rand)')
        self.assertTrue(sorted_farms[0]['Price (Rand)'] == '100000')
        self.assertTrue(sorted_farms[-1]['Price (Rand)'] == '150000')

    def test_sort_by_price_desc(self):
        sorted_farms = Farms.sort_by_key(self.all_farms, 'Price (Rand)', reverse_sort=True)
        self.assertTrue(sorted_farms[0]['Price (Rand)'] == '150000')
        self.assertTrue(sorted_farms[-1]['Price (Rand)'] == '100000')

