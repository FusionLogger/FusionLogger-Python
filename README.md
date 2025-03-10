# FusionLogger-Python

FusionLogger-Python is a centralized logging framework that provides configurable log levels and dynamic scopes for fine-grained control over application logging. It features structured log records, flexible template-based formatting via tokens, and a fluent builder for easy logger configuration.

## Features

- **Configurable Log Levels:** Supports `DEBUG`, `INFO`, `WARNING`, and `CRITICAL` levels.
- **Dynamic Scopes:** Easily set and clear logging scopes for contextual logging.
- **Flexible Formatting:** Customizable output format via token-based formatting; define log formats and datetime formats through string parameters in the formatter constructor.
- **Dual Logging Outputs:** Supports both console and file logging (file mode: append).
- **High Performance:** Capable of processing approximately 3000 log messages per second.

## Requirements

- **Python Versions:**  
  - Developed under Python 3.12  
  - Linted with PyLint under Python 3.8, 3.9, and 3.10
- **External Dependencies:** None

## Installation

Install FusionLogger-Python via pip:

```bash
pip install fusion_logger_lasse27
```

## Usage

A simple usage example can be found in the provided `TestBenchmark.py` file. Here is a brief example of how to initialize and use the logger:

```python
from fusion_logger import FusionLoggerBuilder, FusionLogLevel

# Build and configure the logger
logger = FusionLoggerBuilder() \
    .set_name("MyAppLogger") \
    .set_min_level(FusionLogLevel.DEBUG) \
    .write_to_file("app.log") \
    .build()

# Log messages at different levels
logger.debug("This is a debug message.")
logger.info("This is an info message.")
logger.warning("This is a warning message.")
logger.critical("This is a critical error message.")
```

## Configuration

- **Logging Levels:**  
  Set the minimum output level (e.g., DEBUG, INFO, WARNING, CRITICAL) using the fluent builder.
  
- **Output Formats:**  
  Specify custom log output formats by passing a format string to the `FusionLogFormatter` constructor.  
  Additionally, provide a custom datetime format string (using `datetime.strftime()` formatting) if desired.

- **File Logging:**  
  The logger writes log entries to files in append mode. Simply add file paths via the builder methods.

## Provided Components

- **FusionLogger:** Core logging class handling log message creation and processing.
- **FusionLoggerBuilder:** Fluent builder for easy and chainable logger configuration.
- **FusionLogProcessor:** Singleton-based processor for handling log records (work in progress for thread safety).
- **FusionLogFormatter:** Component to format log records based on templates.
- **FusionLogRecord:** Structured container for all log entry metadata.
- **FusionLogLevel:** Enum defining available log severity levels.

## Performance & Best Practices

For best performance, initialize the logger during application startup. The token-based formatting approach is optimized for high throughput, achieving roughly 3000 messages per second. Note that while the processor's singleton implementation is designed for thread-safe operations, full thread safety is still a work in progress.

## Known Issues

- There are currently no known bugs.

## License

This project is licensed under the [MIT License](LICENSE).

## Additional Information

For further details, please refer to the `pyproject.toml` file which contains project metadata and hosting information (e.g., GitHub repository details).