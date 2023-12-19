import logging

from .data_normalizer import DataNormalizer
from stl_city_parcel_ingestion.db_connect import DbConnect


log = logging.getLogger()


class DbWriter:
    def __init__(self):
        self.connection = DbConnect().connection

    def persist_main_parcel_record(self, record):
        """Saves primary parcel record entry to the database as a single unique record"""

        sql = "INSERT INTO main_parcel_data (parcel_id, zip_code, primary_address, precinct, property_class) VALUES (%s, %s, %s, %s, %s)"
        values = (
            record['parcel_id'],
            record['zip_code'],
            record['primary_address'],
            record['precinct'],
            record['property_class']
        )

        log.info('INSERT: ' + sql)
        cursor = self.connection.cursor()

        cursor.execute(sql, values)
        self.connection.commit()

        cursor.close()

    def persist_sale_records(self, parcel_data, sale_records):
        """Saves all of a parcel's sale records to the database records"""

        cursor = self.connection.cursor()

        log.info('Persisting sale records')
        log.info(sale_records)

        for record in sale_records:
            sql = "INSERT INTO parcel_sale_records (parcel_id, date, price, transaction_type) VALUES (%s, %s, %s, %s)"
            values = (
                parcel_data['parcel_id'],
                record['date'],
                record['price'],
                record['transaction_type'],
            )
            log.info('INSERT: ' + sql)
            cursor.execute(sql, values)

        self.connection.commit()
        cursor.close()

    def persist_parcel_data(self, raw_parcel_input_entry={}, address_search_results={}):
        """Handles saving of parcel data and sale records in database"""

        data_normalizer = DataNormalizer(
            raw_parcel_input_entry=raw_parcel_input_entry,
            address_search_results=address_search_results
        )

        normalized_data = data_normalizer.run()

        self.persist_main_parcel_record(normalized_data['main_parcel_data'])
        self.persist_sale_records(
            normalized_data['main_parcel_data'],
            normalized_data['sale_records']
        )
