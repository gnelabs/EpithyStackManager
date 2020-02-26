
__author__ = "Nathan Ward"

import functools
from typing import Callable

#Declare routes available.
REGISTER = {}

def register_view(name: str) -> Callable:
    """
    Decorator to register views. Similar to flask.
    """
    @functools.wraps(name)
    def wrapper(f):
        REGISTER[name] = f
        return f
    return wrapper

#Relative import of all web (human) lambdas and api lambdas
from web import *
from api import *

#Client-side routes. Single-page apps that use react browser router
#mimick server-side routes, but don't actually go beyond /. This
#list allows API gateway to succeed the request and kick it back to
#the client react app as part of stackManEnvInfo.currentView. This
#makes it so bookmarks work with API gateway.
available_react_views = (
    '/'
)
for react_view in available_react_views:
    REGISTER[react_view] = react_app.lambda_handler