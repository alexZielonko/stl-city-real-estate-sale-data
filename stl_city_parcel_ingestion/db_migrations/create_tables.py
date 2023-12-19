import logging

from stl_city_parcel_ingestion.db_connect import DbConnect

log = logging.getLogger('migration')


class CreateTables:
    def __init__(self):
        database = DbConnect()
        self.connection = database.connection

    def run(self):
        log.info('Creating tables...')
        self.__migrate()
        self.__tear_down()

    def __tear_down(self):
        self.connection.commit()
        self.connection.close()

    def __migrate(self):
        cursor = self.connection.cursor()

        # Create base tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS main_parcel_data (
                parcel_id VARCHAR(45) NOT NULL,
                zip_code INT,
                primary_address VARCHAR(255),
                precinct VARCHAR(255),
                property_class VARCHAR(55),
                created_at timestamp default current_timestamp,
                PRIMARY KEY (parcel_id)
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS parcel_sale_records (
                id SERIAL,
                parcel_id VARCHAR(45) NOT NULL,
                date DATE NOT NULL,
                price INT,
                transaction_type VARCHAR(255),
                created_at timestamp default current_timestamp,
                PRIMARY KEY (id)
            );
        """)

        log.info('Migration complete ✅')

        cursor.close()
