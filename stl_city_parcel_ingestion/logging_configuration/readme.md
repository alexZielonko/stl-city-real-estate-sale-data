# logging_configuration

The `logging_configuration` package is used to encapsulate, as the name implies, the logging configuration for the `stl_city_parcel_ingestion` package.

This configuration allows us to specify where logs of various severities are output. The initial logging configuration outputs `debug` logs to the terminal while `info` logs are output into specific files.

Logs output to the console are ephemeral and easily lost. Outputting important logs directly to files simplifies debugging and maintenance, whether locally or within distributed systems.
