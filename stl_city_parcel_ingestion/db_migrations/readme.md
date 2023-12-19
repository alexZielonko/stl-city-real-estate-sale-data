# db_migrations

This package supports database migrations for the parent `stl_city_parcel_ingestion` package. These migrations allow for the creation of the `stl_city_parcel_ingestion` package's expected database structure across different environments.

The package can be extended to support additional database needs as new functionality is added to `stl_city_parcel_ingestion`.

## How to run this package

### Setup - Specify a database

The `stl_city_parcel_ingestion/db_connect` package expects a child `database.ini`.

Create and/or edit the `database.ini` file to specify which database this package's migrations are ran against.

### Run the Package

Execute the following command from the directory containing the `stl_city_parcel_ingestion` package,

```bash
python3 stl_city_parcel_ingestion/db_migrations
```
