"""
LearningStyles Forms

Django forms are a tool which allow us to write Python code and export HTML forms in the contexts of our view. Feel
free to use these to help update the database.

https://docs.djangoproject.com/en/1.11/ref/forms/
"""

from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from learning_styles.models import LearningStyles


class LearningStylesConfigurationForm(ModelForm):
    # Configuration for each of the Felder-Silverman learning styles.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Construct the form with empty labels. Labels are determined by the database and not the fields.
        self.fields['active_reflective'].label = ""
        self.fields['visual_verbal'].label = ""
        self.fields['sensing_intuitive'].label = ""
        self.fields['sequential_global'].label = ""

    active_reflective = forms.ModelChoiceField(
        queryset=LearningStyles.objects.filter(spectrum_id__exact=0),
        widget=forms.RadioSelect,
        required=True, initial=0)
    sequential_global = forms.ModelChoiceField(
        queryset=LearningStyles.objects.filter(spectrum_id__exact=1),
        widget=forms.RadioSelect,
        required=True, initial=0)
    visual_verbal = forms.ModelChoiceField(
        queryset=LearningStyles.objects.filter(spectrum_id__exact=2),
        widget=forms.RadioSelect,
        required=True, initial=0)
    sensing_intuitive = forms.ModelChoiceField(
        queryset=LearningStyles.objects.filter(spectrum_id__exact=3),
        widget=forms.RadioSelect,
        required=True, initial=0)

    class Meta:
        model = User
        # Registration of each of the Felder-Silverman Learning Styles on the form
        fields = ('active_reflective', 'visual_verbal', 'sensing_intuitive', 'sequential_global')
