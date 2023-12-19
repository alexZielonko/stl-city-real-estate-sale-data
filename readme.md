# St. Louis City Parcel Sale Data

It is difficult to find a comprehensive set of sale record data for the properties within the St. Louis City limits.

This proof-of-concept project leverages a publicly available list of basic parcel metadata to programmatically find and persist detailed sale records and other property characteristics from the [City of St. Louis' Address Search](https://www.stlouis-mo.gov/data/address-Search/). This is otherwise not possible using the city's open data resources.

The project's input file can be found within St. Louis City's [Parcel Joining Data Dataset](https://www.stlouis-mo.gov/data/datasets/distribution.cfm?id=195).

Within this repo, the input file can found [here](https://github.com/alexZielonko/stl-city-real-estate-sale-data/tree/main/stl_city_parcel_ingestion/parcel_processor/csv_reader/data/stl-city-parcel-data.csv). As the original dataset includes over 130,000 parcel records, this version has been truncated for the purpose of this proof-of-concept.

## Project Architecture

This diagram illustrates the dataflow and processing of the core `stl_city_parcel_ingestion` package that is contained within this repository.

All of the packages are authored in Python, and the process' output data is ultimately persisted in an AWS RDS Database PostgreSQL instance.

![Architecture Diagram](https://raw.githubusercontent.com/alexZielonko/stl-city-real-estate-sale-data/main/stl_city_parcel_ingestion/documentation/stl-city-parcel-ingestion-diagram.svg)

## Quickstart

1. Install the project's dependencies
2. Create a `database.ini` file with the appropriate database credentials
3. Run the `stl_city_parcel_ingestion` package

## Setup

### Installing Dependencies

To install the project dependencies, run:

```
pip3 install -r requirements.txt
```

This project specifies dependencies in the `requirements.txt`. This file specifies the external Python packages used by this project along with a specific version.

Explicitly specifying external package versions helps ensure `stl_city_parcel_ingestion` is able to run consistently across environments. This practice is helpful when running projects across local development and cloud environments.

#### Generating the `requirements.txt` File

The `requirements.txt` file should be updated as new external dependencies are introduced.

The `requirements.txt` file for this project was generated using the [pipreqs](https://pypi.org/project/pipreqs/), which dynamically creates the requirements file based on this project's imports.

To generate a new `requirements.txt` file, run the following command:

```
python3 -m  pipreqs.pipreqs .
```

### Database Configuration

This project's database configuration should be specified as a new file, `db_connect/database.ini`.

The `database.ini` file is excluded from the Git repo via the `.gitignore` file for security purposes. As such, new project developers will need to create a new `database.ini` file.

You'll find an example of the database configuration in [db_connect/database.example.ini](https://github.com/alexZielonko/stl-city-real-estate-sale-data/tree/main/stl_city_parcel_ingestion/db_connect/database.example.ini). It should look something like,

```
[postgresql]
host=DATABASE_HOST
database=DATABASE_NAME
user=DATABASE_USER_NAME
password=DATABASE_PASSWORD
```

Add the `database.ini` file to the [`db_connect` directory](https://github.com/alexZielonko/stl-city-real-estate-sale-data/tree/main/stl_city_parcel_ingestion/db_connect). Then reach out to me or another developer on the project for information on how to obtain development database credentials.

## Running the Project

After installing project dependencies and creating the `database.ini` file, run the project using the following command:

```
python3 stl_city_parcel_ingestion
```

## Logging

A bespoke `logging_configuration` package is used to encapsulate, as the name implies, the logging configuration for the this package.

This configuration allows us to specify where logs of various severities are output. The initial logging configuration outputs `debug` logs to the terminal while `info` logs are output into specific files.

Logs output to the console are ephemeral and easily lost. Outputting important logs directly to files simplifies debugging and maintenance, whether locally or within distributed systems.

## Database

The initial database schema for the proof of concept contains two tables. The first table maintains the parcel metadata while the other table contains all of the sale records. There is a one-to-many relationship between the parcel records and the sale records.

Here's an illustration of the proof-of-concept schema:

![Database schema diagram](https://raw.githubusercontent.com/alexZielonko/stl-city-real-estate-sale-data/main/stl_city_parcel_ingestion/documentation/one-to-many-schema-diagram.svg)

The database was initially developed using an [AWS RDS PostgreSQL instance](https://aws.amazon.com/rds/postgresql/). However, the program can be run to connect and persist data on any PostgreSQL database provided the configuration information is specified in the `database.ini`.

### Running Migrations

The `main_parcel_data` and `parcel_sale_records` table creation SQL queries are stored in the [db_migrations package](https://github.com/alexZielonko/stl-city-real-estate-sale-data/tree/main/stl_city_parcel_ingestion/db_migrations).

This package supports database migrations for the parent `stl_city_parcel_ingestion` package. These migrations allow for the creation of the package's expected database structure across different environments.

The package can be extended to support additional database needs as new functionality is added to `stl_city_parcel_ingestion`.

To run the migrations, run the following in the terminal:

```
python3 stl_city_parcel_ingestion/db_migrations
```

## Testing

Tests for this project are specified in the [stl_city_parcel_ingestion/test](https://github.com/alexZielonko/stl-city-real-estate-sale-data/tree/main/stl_city_parcel_ingestion/test) directory.

The command to execute the test suite is located in the `stl_city_parcel_ingestion` package's [makefile](https://github.com/alexZielonko/stl-city-real-estate-sale-data/tree/main/stl_city_parcel_ingestion/Makefile).

To run the tests, navigate to the `stl_city_parcel_ingestion` directory in the terminal and run:

```
make unit
```

If all of the tests are passing, the output should look something like:

```
$ make unit

python3 -m unittest discover .
...
----------------------------------------------------------------------
Ran 3 tests in 0.021s

OK
```
