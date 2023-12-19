import unittest
from unittest.mock import patch

from parcel_processor.property_info_requestor import Property_Info_Requestor


class Testing(unittest.TestCase):

    def test_calls_post_with_expected_url(self):
        mock_row_data = {
            'SITEADDR': '1234 MOCK_STREET_NAME ST',
            'StName': 'MOCK_STREET_NAME',
            'LowAddrNum': '1234',
            'ParcelId': '100'
        }

        property_info_requestor = Property_Info_Requestor()

        with patch('requests.post') as spy:
            property_info_requestor.fetch_page_for_row(mock_row_data)

            expected_url = 'https://www.stlouis-mo.gov/data/address-Search/index.cfm?addr=1234+MOCK_STREET_NAME+ST&stname=MOCK_STREET_NAME&stnum=1234&parcelid=100'
            expected_data = {
                'RealEstatePropertyInfor': 'RealEstatePropertyInfor', 'Submit': 'Change Selections'
            }

            spy.assert_called_once_with(expected_url, data=expected_data)


if __name__ == '__main__':
    unittest.main()
