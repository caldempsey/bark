from django.shortcuts import redirect

## Login Required Middleware Exception List ##

urls_exception_list = ['/login',
                       '/logout',
                       '/register',
                       '/',
                       '/support',
                       '/authenticate', ]


class LoginRequiredMiddleware:
    """
    The LoginRedirectMiddleware provides the functionality to prevent access to the website to unauthorized users.
    The LoginRedirectMiddleware defines an exception list of urls "urls_exception_list" of allowed urls.
    """
    def __init__(self, get_response):
        # Required notation for *all* middleware execution (see Django documentation). Initialize the class with an
        # instance of itself and an external "get_response" method (from the Django middleware). This assigns the
        # "get_response" property to the field variable "get_response" in the class (no explicit type declaration
        # required). https://docs.djangoproject.com/en/1.11/topics/http/middleware/#writing-your-own-middleware
        self.get_response = get_response

    # Code to be executed for each request before any subsequent view is called.
    def __call__(self, request):
        # Returns the HttpResponse object from the Django view function.
        response = self.get_response(request)
        return response

    # The process_view method runs before Django calls any view function
    # https://docs.djangoproject.com/en/1.11/topics/http/middleware/#view-middleware. "request" is the HttpRequest
    # object [wrapped by Django], view_func is the view function (remember Python allows for function variables),
    # view args are all positional arguments passed to the view, view_kwargs reflect the dictionary of keyword
    # arguments that 'will be' passed to the view. Since we are handling the dictionary object of arguments that will
    #  be passed to the view from the view function [a consequence of how Django handles view functions] we are able
    # to utilize those arguments a-proiri to serving the client.

    def process_view(self, request, view_func, view_args, view_kwargs):
        path = request.path_info
        # We can write our Python code now! Assert the request has the attribute user (all HTTP requests should have
        # the attribute user from the AuthenticationMiddleware (which wraps the HTTP request) if this is not there is
        #  something seriously wrong, see
        # https://docs.djangoproject.com/en/1.11/ref/request-response/#attributes).
        assert hasattr(request, 'user')
        # Iterates through accepted list of URLS (check syntax) and identifies if the URL is in the list of exceptions.
        if path in urls_exception_list or request.user.is_authenticated():
            return None
        else:
            return redirect('public_interfaces:login')
