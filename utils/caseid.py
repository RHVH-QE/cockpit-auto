import os
from functools import wraps


def add_case_id(*case_id):
    """
    Decorator to add case id to a test.
    """
    def decorator(function):
        @wraps(function)
        def wrapper(self, *args, **kwargs):
            self.case_id = case_id
            function(self, *args, **kwargs)
            self.case_state = True
        return wrapper
    return decorator


def check_case_id(function):
    """
    Decorator to check case id at the end of a test.
    """
    @wraps(function)
    def wrapper(self, *args, **kwargs):
        function(self, *args, **kwargs)
        if self.case_id:
            if self.case_state:
                result = 'passed'
            else:
                result = 'failed'
            with open(os.environ['POLARION_RESULT_FILE'], 'a') as f:
                for case in self.case_id:
                    f.write("{}: {}\n".format(case, result))
    return wrapper
