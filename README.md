# Simple Log

Simple Log is built to complement Python's built-in
[`logging`](https://docs.python.org/3/library/logging.html) library. It allows you to temporarily
redirect logging output to a list.


## Usage

```python
import logging
from simplelog import log_to_list

logger = logging.getLogger(
```


## Example

Take a scenario where you have live production code running on multiple threads and logging
information to various locations. You want to speculatively run the same code and capture any
records that would otherwise be logged, without impacting any other logging.

The core code looks something like this:

```python
def core_code(logger: Logger = None):
    logger = logger or logging.getLogger(__name__)

    # whoops, we found something to warn about...
    logger.warning("Some warning")
```

Typically, calls to this function would result in the warning being logged. However, we can
redirect the logging to a list instead as follows:

```python
from simplelog import redirect_logger_to_log

with redirect_logger_to_log("core_code") as log:
    # run the core code speculatively...
    core_code()

assert len(log.warnings) == 1
```


## To Do
- [ ] `ListHandler` currently changes the logging for all threads/processes, but we probably only want
  to change it for a _specifc_ thread/process. Whereas other logging functions are inherently
  multithreaded/multiprocessed (eg, they can all write to the same file), speculatively running
  code and logging the output to a list is thread-specific. We're setting certain parameters (eg,
  pretending we're far in the future) in a specific thread, and we need the results of _that_
  _thread_. Look into best practices for thread- and process-specific logging.
- [ ] Flesh out documentation.
- [ ] Add unit tests and CI.
- [ ] Put on pypi.
