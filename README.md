# Simple Log

## Usage

```python
>>> logger = logging.getLogger(__name__)
>>> log = create_simple_log(logger)
>>> logger.error("Something bad happened")
>>> log
[<LogRecord: __main__, 40, <input>, 1, "blah">]
>>> log.errors
[<LogRecord: __main__, 40, <input>, 1, "blah">]
>>> log.warnings
[]
```
