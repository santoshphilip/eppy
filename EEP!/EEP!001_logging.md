# EEP!: 1
* Title: Standard for the use of logging in Eppy 
* Version: 0.0.2
* Last-Modified: 26 Jun 2015
* Author: Jamie Bull jamie.bull@oco-carbon.com
* Status: Draft
* Type: Standards Track
* Created: 17-Jun-2015
* Eppy-Version: >=0.4.6.4a

## Abstract
This inaugural Eppy Enhancement Proposal (EEP!) puts forward use cases
for logging, from both a developer and a user perspective.

The proposal is not that logging is made a requirement, just that logging
can be implemented easily and consistently where a developer sees a need.

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
All logging should use a logging configuration file. This could either be
directly in a python file (quicker to code), or alternatively an .ini
file (easier for users to edit). This will help to ensure a consistent
logging format is followed across modules. To implement logging within a
module, all that needs to be added is the following code:

	import eppy.log_config  # module location tbd
	
	# create a module-level logger 
	logger = log_config.get_logger(__name__)
	
	# used as follows
	logger.debug("This is a DEBUG level message")
	logger.info("This is an INFO level message")

### Log levels
The level for a logging call should generally follow those recommended by
the logging module documentation, "Logging HOWTO" [1] in the Python
documentation. For the most part, developers will be interested in the
DEBUG level messages which contain details of data and parameters,
while users will likely be more concerned with INFO level messages which
track the 10000 ft view of activity.

### Verbosity
Given that there are at least two use cases, and that logs can grow
very large, there should be a verbosity flag that can be set to hide
messages below a given level. Messages could be hidden either in a log
file for a specific logging level, or by not logging them at all (e.g.
not logging at the debug level for general users). This should be set in
the config file and should be configurable during runtime.

The default should be no logging, to be turned on when needed.

### Log format
* standard log format
This would log to a (rotating?) text file saved with a .log extension.
* json format
This would save to a .json file. Suggested schema would be:

'timestamp': unix timestamp,
'log_level': one of the Python log levels, e.g. INFO, DEBUG
'call': module and function name
'args': list of positional args
'kwargs': dict of keyword args
'return_values': list of return values
    
## Implementation
It should be possible to use a decorator to implement logging. There is an
example of using a decorator to log function calls available from the Python
Wiki [2]. For our purposes, it will need modifying to include the parameters
and return value, as well as to take a log level parameter.

When used in a module it would look like:
    
    @logged(debug)
    def my_function(a, b, c=0):
        return a * b + c
        
    print my_function(2, 4, 6)

In json format this would append something like:

    [{'timestamp': 1435317572,
      'log_level': 'DEBUG',
	  'call': my_function,
	  'args': [2, 4],
	  'kwargs': {'c': 6},
	  'return_values': [14]}]
	
Using a decorator to implement this gives three benefits. Firstly, it's much
easier to write. Secondly, it reduces clutter within functions since the
logging happens outside the function itself. And thirdly, it encourages
breaking functions down into smaller units which can be logged (and also
tested) individually.

## References
[1] Logging HOWTO, Vinay Sajip
https://docs.python.org/2/howto/logging.html
[2] Logging decorator with specified logger
https://wiki.python.org/moin/PythonDecoratorLibrary#Logging_decorator_with_specified_logger_.28or_default.29

## Copyright
This document has been placed in the public domain.