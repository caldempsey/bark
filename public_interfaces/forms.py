"""
Public Interface Forms

Django forms are a tool which allow us to write Python code and export HTML forms in the contexts of our view.


https://docs.djangoproject.com/en/1.11/ref/forms/
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Inherit from UserCreationForms
class UserForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ('username',
                  'first_name',
                  'last_name',
                  'email',
                  'password1',
                  'password2'
                  )
        # Override the save method for default UserCreationForms

    # Commit=True is Django's de-facto method to allow a method to save to the database.
    def save(self, commit=True):
        # Get an instance of the user object without committing to saving the instance. We haven't finished editing
        # the data to be stored in to the model so we don't want to database commit just yet.
        user = super(UserForm, self).save(commit=False)
        # Cleaned data is Django's de-facto method for parsing data before storing it into the database.
        # Set user.first_name of the newly created user object to cleaned first_name (from the field).
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        # Create the user in the database when user.save is run [commit is true from the paramater].
        if commit:
            user.save()
        return user
