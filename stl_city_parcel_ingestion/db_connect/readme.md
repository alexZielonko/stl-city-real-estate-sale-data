# db_connect

This package is used by both the parent `stl_city_parcel_ingestion` package and the sibling `db_migrations` package for database connections. This package can be configured to connect to local or remote database instances.

## Setup

Configuration for the `db_connect` package should be specified within a `database.ini` file.

Create a new `database.ini` file in this directory to use the package. See the `database.example.ini` file for an example configuration structure.
