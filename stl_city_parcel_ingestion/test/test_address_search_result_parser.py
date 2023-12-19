import unittest
from pathlib import Path

from parcel_processor.address_search_result_parser import AddressSearchResultParser


class Testing(unittest.TestCase):

    def setUp(self):
        data_path = Path(__file__).parent / \
            './mocks/stl_city_search_output.html'
        self.mock_data = open(data_path, 'r')
        self.parser = AddressSearchResultParser(self.mock_data)

    def tearDown(self):
        self.mock_data.close()

    def test_get_property_meta(self):
        actual = self.parser.get_property_meta()

        expected = {
            'primary_address': '1528 MENARD ST ST LOUIS MO 63104',
            'owner_name': 'SANDERS, JAMES M',
            'parcel_id': '0391-9-160.000',
            'collector_of_revenue_account': '0391-00-01600',
            'precinct': 'Ward 8, Precinct 16',
            'property_class': 'RESIDENTIAL'
        }

        self.assertEqual(actual, expected)

    def test_get_sales_history(self):
        actual = self.parser.get_sales_history()

        expected = [{'date': '09/24/2002', 'price': 'n/a', 'transaction_type': 'Rltd. Pty.'},
                    {'date': '09/01/1969', 'price': '$83,148.00', 'transaction_type': 'Valid'}]

        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
