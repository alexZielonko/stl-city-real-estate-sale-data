import logging
import requests
from urllib.parse import urlencode

log = logging.getLogger()


class Property_Info_Requestor:
    BASE_URL = 'https://www.stlouis-mo.gov/data/address-Search/index.cfm'

    def __get_url_params(self, row):
        """Returns encoded url parameters to query property data STL City address search endpoint"""

        params = {
            'addr': row['SITEADDR'],
            'stname': row['StName'],
            'stnum': row['LowAddrNum'],
            'parcelid': row["ParcelId"]
        }

        return urlencode(params)

    def __get_require_req_payload(self):
        """Returns required fields to include property pricing and tax history data in response"""

        return {
            'RealEstatePropertyInfor': 'RealEstatePropertyInfor',
            'Submit': 'Change Selections'
        }

    def fetch_page_for_row(self, row):
        """Returns a response containing HTML that can be subsequently parsed and persisted in the database"""

        url = self.BASE_URL + '?' + self.__get_url_params(row)
        data = self.__get_require_req_payload()

        try:
            response = requests.post(url, data=data)

            log.info('Fetched url: ' + url)

            return response.text
        except:
            log.error('Failed to fetch url: ' + url)
            return ''
