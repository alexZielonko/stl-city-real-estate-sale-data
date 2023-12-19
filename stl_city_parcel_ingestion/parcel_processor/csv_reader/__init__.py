from pathlib import Path


class Csv_Reader:
    """Creates an abstracted interface to open input data file"""

    def __init__(self):
        input_data_file_path = "data/stl-city-parcel-data.csv"
        self.file = Path(__file__).parent / input_data_file_path

    def open_data_file(self):
        """Open and expose input data file"""

        return self.file.open()
