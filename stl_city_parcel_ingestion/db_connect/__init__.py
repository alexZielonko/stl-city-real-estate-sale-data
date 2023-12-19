import logging
import psycopg2

from pathlib import Path
from configparser import ConfigParser

from stl_city_parcel_ingestion.logging_configuration import initialize_logging


log = logging.getLogger()
filePath = Path(__file__).parent / 'database.ini'


def get_config(section='postgresql'):
    """Load database.ini configuration file and return entries as a dict for runtime usage"""

    parser = ConfigParser()
    parser.read(filePath)

    database_params = {}

    if parser.has_section(section):
        params = parser.items(section)

        for param in params:
            key, value = param
            database_params[key] = value

    else:
        raise Exception(
            f'Section {section} not found in the {filePath}')

    return database_params


class DbConnect:
    """Authenticates and connects to the AWS RDS Postgresql database"""

    def __init__(self):
        initialize_logging()

        database_params = get_config()

        log.info('Connecting to the database')

        self.connection = psycopg2.connect(**database_params)

        log.info('Database connection established 🔗')
