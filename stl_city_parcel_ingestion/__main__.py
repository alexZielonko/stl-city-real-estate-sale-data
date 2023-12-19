from parcel_processor import StlCityParcelProcessor
from logging_configuration import initialize_logging


def main():
    initialize_logging()
    processor = StlCityParcelProcessor()
    processor.run()


if __name__ == '__main__':
    main()
