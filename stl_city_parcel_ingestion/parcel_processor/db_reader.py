import logging

from stl_city_parcel_ingestion.db_connect import DbConnect

log = logging.getLogger()


class DbReader:
    def __init__(self):
        self.connection = DbConnect().connection

    def get_parcel_data_records(self, parcel_id):
        """Returns a list of parcel records from the `main_parcel_data` table"""

        cursor = self.connection.cursor()

        sql = f"SELECT * FROM main_parcel_data WHERE parcel_id like '{parcel_id}'"

        cursor.execute(sql)
        records = cursor.fetchall()
        cursor.close()

        return records
