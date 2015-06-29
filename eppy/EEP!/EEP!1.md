# EEP!: 1
* Title: Standard for the use of logging in Eppy 
* Version: 0.0.6
* Last-Modified: 29 Jun 2015
* Author: Jamie Bull <jamie.bull@oco-carbon.com>
* Status: Draft
* Type: Standards Track
* Created: 17-Jun-2015
* Eppy-Version: >=0.4.6.4a

## Abstract
This inaugural Eppy Enhancement Proposal (EEP!) puts forward use cases
for logging, from both a developer and a user perspective.

The proposal is not that logging is made a requirement, just that logging
should be implemented easily and consistently where a developer sees a need.

## Rationale
Logging has two main use cases, each of which has unique characteristics
that mean it should be treated differently.

In the case of developers, when errors arise, the stack trace often does not
contain enough information to understand what has caused the problem. In
these situations, logging can reveal not only the call stack, but also
information about the data and parameters. Unexpected values could suggest
the need for additional tests and/or input validation.

This could be followed in real time by viewing the tail of a log file or by
viewing the output to stdout.

For users, a track of what is happening in their program can be useful when
learning how Eppy software does what it does. They may also appreciate being
able to submit a log along with a bug report, and this should allow
contributors to understand the source of errors more quickly.

A user may also want to refer to more detailed logs to at a later time,
particularly useful when using Eppy to generate large numbers of IDFs from
variable and perhaps invalid inputs.

## Proposed standards

### Logging module
All logging in Eppy should make use of the **eppylog** module. This will 
help to ensure a consistent logging format is followed across modules.

To implement ad-hoc logging within a module, all that needs to be added
is the following code:
```python
from eppy import eppylog

# create a module-level logger 
logger = eppylog.getlogger(__name__)

# used as follows
logger.debug("This is a DEBUG level message")
logger.info("This is an INFO level message")
```
### Verbosity & log levels
The level for a logging call should generally follow those recommended by
the logging module documentation, ["Logging HOWTO"] [1] in the Python
documentation. For the most part, developers will be interested in the
`DEBUG` level messages which contain details of data and parameters,
while users will likely be more concerned with `INFO` level messages which
track the 10000 ft view of activity.

Given that there are at least two use cases, and that logs can grow
very large, there should be a verbosity flag that can be set to hide
messages below a given level. Messages could be hidden either in a log
file for a specific logging level, or by not logging them at all (e.g.
not logging at the debug level for general users). This should be set in
the config file and should be configurable during runtime.

The default is no logging, other than for `CRITICAL` messages, if any.
More verbose logging can then be activated when needed.

The verbosity of a logger can be set in two ways. Firsty, by changing
the value for the `level` parameter of a logger in the **eppylog.ini**
file.
```
[logger_console]
level = DEBUG
handlers = consoleHandler
qualname = console
```
Secondly, you can set log levels programmatically as follows:
```python
from eppy import eppylog

# log all debug-level or higher messages to the JSON log
eppylog.setloggerlevel('json', 'DEBUG')
# log all info-level or higher messages to the console
eppylog.setloggerlevel('console', 'INFO')
```

### Log formats
**"console"** logs to _std.err._

This logs directly to the console:

```
29/06/2015 11:19:07 INFO     function: eppy.tests.test_eppylog.decorated_info_function, args: (2, 4), kwargs: {'c': 6}, returns: [14]
29/06/2015 11:20:32 DEBUG    function: eppy.tests.test_eppylog.decorated_debug_function, args: (2, 4), kwargs: {'c': 6}, returns: [14]
```
**"file"** logs to _eppylog.log_

This will log to a rotating text file saved with a .log extension. Format is as
follows:

```
29/06/2015 11:19:07 INFO     function: eppy.tests.test_eppylog.decorated_info_function, args: (2, 4), kwargs: {'c': 6}, returns: [14]
29/06/2015 11:20:32 DEBUG    function: eppy.tests.test_eppylog.decorated_debug_function, args: (2, 4), kwargs: {'c': 6}, returns: [14]
```
**"json"** logs to _eppylog.json_

This logs to a rotating json file. The schema is:

```
{"asctime": "YYYY-MM-DD HH:MM:SS,mmm",
"function": module.function, 
"returns": [list of return values], 
"args": [list of positional args], 
"log_level": log level, e.g. DEBUG, 
"kwargs": {dict of keyword args}}
``` 
## Decorator
It is also possible to use a decorator to implement logging. Using a decorator 
has three benefits. Firstly, it's much easier to write. Secondly, it reduces clutter
within functions since the logging happens outside the function itself. And thirdly,
it encourages breaking functions down into smaller units which can be logged (and also
tested) individually.

There is an example of using a decorator to log function calls available from the [Python
Wiki] [2]. This has been modified to include the parameters and return value,
as well as to take a log level parameter.

When used in a module it looks like:
```python
from eppy import eppylog

@eppylog.loglevel('debug')
def my_function(a, b, c=0):
    return a * b + c

my_function(2, 4, 6)
```
In json format this appends a JSON-formatted record like the following to an
eppy.json rotating log file:

```
{"asctime": "2015-06-29 11:27:13,296", "function": "eppy.my_module.my_function", "returns": [14], "args": [2, 4], "log_level": 10, "kwargs": {"c": 6}}
```	

## References
[1]: <https://docs.python.org/2/howto/logging.html> "Logging HOWTO, Vinay Sajip"

[2]: <https://wiki.python.org/moin/PythonDecoratorLibrary#Logging_decorator_with_specified_logger_.28or_default.29> "Logging decorator with specified logger"
[1] ["Logging HOWTO", Vinay Sajip](https://docs.python.org/2/howto/logging.html)

[2] ["Logging decorator with specified logger", Python Decorator Library](https://wiki.python.org/moin/PythonDecoratorLibrary#Logging_decorator_with_specified_logger_.28or_default.29)


## Copyright
This document has been placed in the public domain.
