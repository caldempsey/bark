from django.contrib import auth
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.views.generic import View
from public_interfaces.forms import UserForm


class IndexView(View):
    """
    LoginView is responsible for facilitating the task of providing a home-page interface.
    """

    def get(self, request):
        index_template = 'public/index.html'
        return render(request, index_template)


class LoginView(View):
    """
    LoginView is responsible for facilitating the task of providing a login interface.
    """

    def get(self, request):
        """
        Serves the login template to users.
        """
        if request.user.is_authenticated():
            auth.logout(request)
            return redirect("public_interfaces:index")

        return render(request, 'public/login.html')

    def post(self, request):
        """
        Handles login template details from users.
        """
        user = request.user
        # If the user already is authenticated, then return to the index.
        if request.user.is_authenticated():
            return redirect("public_interfaces:index")
    #    If the user is not already authenticated, then authenticate the user from POST data.
        # Validate number is in post_data
        try:
            if 'username' not in request.POST or 'password' not in request.POST:
                raise AttributeError
        except AttributeError:
            # Graceful return of no user in the event that invalid POST is passed.
            return None
        # In-case a user is already logged into the account [i.e. somewhere else], then we need to log them out using
        #  the Django framework.
        auth.logout(request)
        # Access POST data https://code.djangoproject.com/wiki/HttpRequest
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        # If the user does not exist (None)
        if user is not None:
            login(request, user)
            # Redirect to profile page
            return redirect('/')
        else:
            # If not we need to pass a csrf token with the context and error message to the template (no need to
            # raise a system error).
            context = {}
            context.update(csrf(request))
            context.update({"error_message": "Your username and password did not match. Please try again."})
            return render(request, 'public/login.html',
                          context)


class LogoutView(View):
    """
    LogoutView is responsible for facilitating a task of logging out users.
    """

    def get(self, request):
        # Django shortcut to cleanly logout a user from a request.
        auth.logout(request)
        return redirect('/')


class RegistrationView(View):
    """
    RegistrationView is responsible for facilitating an interface to register.
    """

    template_name = 'public/registration_form.html'

    def get(self, request):
        """
        Get interface for the user registration.
        """
        user_form = UserForm(request.GET)

        return render(request, self.template_name, {'user_form': user_form,
                                                    })

    def post(self, request):
        """
        Post interface for user registration. Checks if the registration form sent by POST data is valid.
        """
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            # Save the user form. The Django framework will identify if the user already exists.
            user = user_form.save()
            # User is saved to the database
            # Return user object if credentials are correct.
            if user is not None:
                login(request, user)
                return redirect('public_interfaces:index')
        return render(request, self.template_name, {'user_form': user_form,
                                                    })
