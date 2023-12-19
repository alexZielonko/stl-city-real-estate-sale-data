import csv
import json
import time
import logging

from .address_search_result_parser import AddressSearchResultParser
from .property_info_requestor import Property_Info_Requestor
from .csv_reader import Csv_Reader
from .db_writer import DbWriter
from .db_reader import DbReader

log = logging.getLogger()


class StlCityParcelProcessor:
    # Sleep between iterations to avoid overwhelming STL City Address Search
    SEARCH_DEBOUNCE_TIME = 4
    # Limit number of parcel records to search & update in the database for the proof-of-concept
    POC_RECORD_SEARCH_LIMIT = 1050
    # Parcel id column identifier in source csv data file
    PARCEL_ID_KEY = 'ParcelId'

    def run(self):
        """
        This is the main entry point for StlCityParcelProcessor package.

        Loads input data csv file and fetches additional property information from the STL City 
        Gov Address Search website. After fetching additional property information, normalize 
        and persist data into remote database for further data processing and analysis.
        """
        try:
            self.__set_up()

            with Csv_Reader().open_data_file() as stl_city_parcel_data_file:
                csv_reader = csv.DictReader(stl_city_parcel_data_file)
                self.__parse_csv(csv_reader)

        finally:
            self.__tear_down()

    def __set_up(self):
        """Instantiate database read/write interfaces"""

        self.db_reader = DbReader()
        self.db_writer = DbWriter()

    def __tear_down(self):
        """Close database connections"""

        self.db_reader.connection.close()
        self.db_writer.connection.close()

    def __write_debug_search_page(self, html):
        """Writes the HTML response from the last searched parcel on failure, useful for debugging"""

        with open('DEBUG--last_fetched_property_page.html', 'w') as writer:
            writer.write(html)

    def __get_did_fetch_parcel(self, parcel_id):
        """Checks the database to determine if we already have an entry for a particular parcel id"""

        records = self.db_reader.get_parcel_data_records(parcel_id)
        did_previously_fetch_parcel = len(records) > 0
        return did_previously_fetch_parcel

    def __debounce_next_search(self):
        """Sleep between iterations to avoid overwhelming STL City Address Search"""

        time.sleep(self.SEARCH_DEBOUNCE_TIME)

    def __search_address(self, row):
        """
        Searches the STL City Address portal for a particular parcel id

        Returns property meta data and sale history
        """

        try:
            log.info('Searching row: ' + json.dumps(row))

            # Get HTML page from STL City Address Search
            property_search = Property_Info_Requestor()
            page_html = property_search.fetch_page_for_row(row)

            # Parse HTML address search HTML
            search_result = AddressSearchResultParser(page_html).parse_page()

            log.info('Address search results: ' + json.dumps(search_result))

            return search_result

        except Exception as err:
            log.error(f'__search_address error: {err}')
            self.__write_debug_search_page(page_html)

    def __save_address_search_results(self, row, addr_search_results):
        """Save address search results to database"""

        try:
            self.db_writer.persist_parcel_data(
                raw_parcel_input_entry=row,
                address_search_results=addr_search_results
            )

            log.info(f'Saved parcel id to database: {row[self.PARCEL_ID_KEY]}')
        except Exception as err:
            log.error(f'__save_address_search_results error: {err}')

    def __parse_csv(self, csv_reader):
        """Request, parse, and persist property information for each row in the input csv file"""

        for index, row in enumerate(csv_reader):
            parcel_id = row[self.PARCEL_ID_KEY]

            # Exit the loop if the index exceeds the limit for the proof-of-concept
            if index >= self.POC_RECORD_SEARCH_LIMIT:
                break

            # Skip iteration if we already fetched data for this parcel id
            if self.__get_did_fetch_parcel(parcel_id):
                log.info('Previously fetched parcel id: ' + parcel_id)
                continue

            addr_search_results = self.__search_address(row)
            self.__save_address_search_results(row, addr_search_results)
            self.__debounce_next_search()

        log.info(f'Finished parsing {self.POC_RECORD_SEARCH_LIMIT} records.')
