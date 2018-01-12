import re

from django.http import Http404

from roles.manage.roles import has_user_leader_role

# Configuration
leader_urls = re.compile("^(/leaders|/leaders/.+)$")


# Redirect to leaders view for all regex matches class LeadersRedirectMiddleware:

class LeadersRedirectMiddleware:
    """
    The LeadersRedirectMiddleware will use the configuration stated in leader_urls to redirect users who do not have
    the Leaders role to the home page.
    """
    def __init__(self, get_response):
        # Required notation for *all* middleware execution (see Django documentation). Initialize the class with an
        # instance of itself and an external "get_response" method (from the Django middleware). This assigns the
        # "get_response" property to the field variable "get_response" in the class (no explicit type declaration
        # required). https://docs.djangoproject.com/en/1.11/topics/http/middleware/#writing-your-own-middleware
        self.get_response = get_response

    def __call__(self, request):
        # Returns the HttpResponse object from the Django view function.
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user')
        path = request.path_info
        user = request.user
        if leader_urls.match(path):
            if not has_user_leader_role(user):
                raise Http404

        return None
