import logging
from bs4 import BeautifulSoup

log = logging.getLogger()


class AddressSearchResultParser:
    def __init__(self, html_doc):
        self.soup = BeautifulSoup(html_doc, 'html.parser')

    def parse_page(self):
        """
        This method serves as the primary interface for the class.

        Returns dict containing unprocessed `property_meta` & `sales_history` data for later output into database
        """

        property_meta = self.get_property_meta()
        sales_history = self.get_sales_history()

        return {
            'property_meta': property_meta,
            'sales_history': sales_history
        }

    def process_table_data_elements(self, table_data_elements):
        """Return a list of strings, where each string is the "text" within an html <td> element"""

        table_data_list = []

        # Get the text content of the html element and add to new list
        for datum in table_data_elements:
            table_data_list.append(datum.contents[0])

        return table_data_list

    def get_property_meta(self):
        """Returns meta data about property, such as the owner, property class, and precinct"""

        try:
            # Find all table data elements within html document
            meta_table_data_elements = self.soup.table.find_all('td')

            # Get the text content of the html element and add to new list
            meta_data_contents = self.process_table_data_elements(
                meta_table_data_elements
            )

            # Unpack meta data content list into named variables
            primary_address, owner_name, parcel_id, collector_of_revenue_account, neighborhood, ward, precinct, property_class, * \
                rest = meta_data_contents

            return {
                "primary_address": primary_address,
                "owner_name": owner_name,
                "parcel_id": parcel_id,
                "collector_of_revenue_account": collector_of_revenue_account,
                "precinct": precinct.strip(),
                "property_class": property_class.strip(),
            }

        except Exception as err:
            log.error(
                f'AddressSearchResultParser.get_property_meta - something went wrong: {err}')
            return {}

    def process_sale_history_row(self, row):
        """Extracts a row's sale data information, returning it as a dict"""

        raw_row_data = row.find_all('td')
        row_data = self.process_table_data_elements(raw_row_data)

        date, price, sale_type = row_data

        return {
            'date': date.strip(),
            'price': price.strip(),
            'transaction_type': sale_type.strip()
        }

    def get_sales_history(self):
        """Returns a list of each sale records for the property"""

        try:
            # Find a table element on the page with the sale record attribute
            sales_tables = self.soup.find_all(
                'table', summary='List of sale records')

            table_rows = sales_tables[0].find_all('tr')
            table_rows_without_header_columns = table_rows[1:]

            sale_history = map(self.process_sale_history_row,
                               table_rows_without_header_columns)

            return list(sale_history)

        except IndexError as err:
            log.error(
                f'Failed to find sales history table for property: {err}')
            return []
        except Exception as err:
            log.error(
                f'AddressSearchResultParser.get_sales_history - something went wrong: {err}')
            return []
