import locale
from datetime import datetime

locale.setlocale(locale.LC_ALL, '')


class DataNormalizer:
    def __init__(self, raw_parcel_input_entry={}, address_search_results={}):
        self.raw_parcel_data = raw_parcel_input_entry
        self.address_search_results = address_search_results

    def run(self):
        """Returns a dict containing:
        * `main_parcel_data` that is ready for persistance in the `main_parcel_data` table
        * `sale_records`, a list of sale records that are ready for persistance in the `parcel_sale_records` table
        """

        return {
            'main_parcel_data': self.__format_main_parcel_data(),
            'sale_records': self.__format_sale_records()
        }

    def __format_main_parcel_data(self):
        """Formats the parcel data into a dict for persistance into the `main_parcel_data` table"""

        property_meta = self.address_search_results['property_meta']

        return {
            'parcel_id': self.raw_parcel_data['ParcelId'],
            'primary_address': property_meta['primary_address'],
            'precinct': property_meta['precinct'],
            'property_class': property_meta['property_class'],
            'zip_code': self.raw_parcel_data['ZIP'],
        }

    def __convert_price_to_number(self, price_value):
        """
        Converts a string currency value formatted like `'$123.45'` to a float, `123.45`

        Returns `-1` if unable to convert the `price_value` to a float, or if the price value is missing
        """

        try:
            return locale.atof(price_value.strip("$"))

        # Handles cases where the price is "n/a" or otherwise missing
        except ValueError:
            return -1
        except:
            return -1

    def __format_sale_record_date(self, date_str):
        """Converts the sale record date from the STl City Address Search result format, `MM-DD-YYYY`, 
        to the format supported by PostgreSQL, `YYYY-MM-DD`
        """

        try:
            date_obj = datetime.strptime(date_str, '%m/%d/%Y')
            return date_obj.strftime('%Y-%m-%d')
        except:
            # Fallback to Missouri statehood date if sale record is missing the date
            return '1821-08-10'

    def __format_sale_record(self, sale_record):
        """Returns a formatted sale record dict"""

        return {
            'date': self.__format_sale_record_date(sale_record['date']),
            'price': self.__convert_price_to_number(sale_record['price']),
            'transaction_type': sale_record['transaction_type']
        }

    def __format_sale_records(self):
        """Returns a list of sale records formatted for persistance in the `parcel_sale_records` table"""

        formatted_search_results = map(
            self.__format_sale_record,
            self.address_search_results['sales_history']
        )

        return list(formatted_search_results)
