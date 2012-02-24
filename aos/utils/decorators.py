from common_utils import TextPlainResponse
from django.http import HttpResponseServerError
import os
import traceback

def execute_only_in_dev_server(f):
    """
        This decorator checks that the decorated function is executed just if we are in local environment (not allowed in the cloud)
    """
    def wrapper(request, **kwargs):
        if not os.environ.get('SERVER_SOFTWARE', '').startswith('Development'):
            return TextPlainResponse('This test can only be executed against LOCAL server')
        else:
            return f(request=request, **kwargs)
    return wrapper

def catch_exceptions(f):
    """
        This decorator catches every exception during the request returning  an error and printing the stack trace
    """
    def wrapper(request, **kwargs):
        try:
            return f(request=request, **kwargs)
        except Exception, e:
            traceback.print_exc()
            return HttpResponseServerError(e)
    return wrapper