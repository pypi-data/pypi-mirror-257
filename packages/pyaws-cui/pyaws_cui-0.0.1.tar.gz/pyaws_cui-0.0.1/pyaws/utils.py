"""File containing utility functions for pyaws.

This file is meant to contain utility classes and functions for pyaws.  
These functions are meant to be used by other pyaws modules.

    - DateTimeEncoder: Custom JSON encoder class for datetime objects.
    - HandleAwsError: Class to handle AWS error responses.
"""

import json
import datetime
import pyaws.logger as LOGGER

class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder class for datetime objects.
    """
    def default(self, obj):
        """Default encoder method.
        """
        LOGGER.write('Utils - DateTimeEncoder - default - obj: {}'.format(obj))
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super(DateTimeEncoder, self).default(obj)

class HandleAwsError:
    """Class to handle AWS error responses.

    This class is meant to be used as a decorator to handle AWS error responses.

    Example usage to decorate all methods in a class:
    @UTILS.HandleAwsError.decorate_all_methods(UTILS.HandleAwsError.handle_aws_error)

    Example usage to decorate a single method:
    @UTILS.HandleAwsError.handle_aws_error
    """

    def decorate_all_methods(decorator):
        def class_decorator(cls):
            for attr_name, attr_value in cls.__dict__.items():
                if callable(attr_value):
                    setattr(cls, attr_name, decorator(attr_value))
            return cls
        return class_decorator


    def handle_aws_error(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                LOGGER.write(f"Utils - HandleAwsError - Error in {func.__name__}: {str(e)}")
                # Return or raise a custom error message or object as needed
                return f"Error occurred:\n {str(e)}"
        return wrapper
