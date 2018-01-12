"""
Courses Forms

Django forms are a tool which allow us to write Python code and export HTML forms in the contexts of our view. Feel
free to use these to help update the database.

https://docs.djangoproject.com/en/1.11/ref/forms/
"""

import zipfile
from django import forms
from django.forms import ModelForm
from courses.manage.courses import has_course_sequence_number
from courses.manage.lessons import sequence_lessons
from courses.models import Courses, Lessons
from courses.models import LessonsLearningStylesResources
from learning_styles.models import LearningStyles
from resources.manage.resources import create_resource


class CoursesCreateForm(ModelForm):
    logo = forms.ImageField(required=False,
                            label='Select an image for your course'
                            )

    class Meta:
        model = Courses
        fields = ['title', 'description', 'logo']

    def clean_logo(self):
        cleaned_data = super(CoursesCreateForm, self).clean()
        logo = cleaned_data.get('logo')
        if logo:
            logo = create_resource(logo)
            # At this stage we can create a resource and link the resource object to the form (rather than the
            # uploaded logo).
            return logo


class CoursesEditForm(CoursesCreateForm):
    class Meta:
        model = Courses
        fields = ['title', 'description', 'logo']


class LessonsCreateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        maximum_sequence_number = kwargs.pop('maximum_sequence_number')
        # If the course attribute exists as a kwarg then get it
        self.course = kwargs.pop('course')
        super(LessonsCreateForm, self).__init__(*args, **kwargs)
        self.fields['sequence_number'] = forms.IntegerField(required=True, initial=maximum_sequence_number,
                                                            max_value=maximum_sequence_number, min_value=1)

    def clean_sequence_number(self):
        cleaned_data = super(LessonsCreateForm, self).clean()
        sequence_number = cleaned_data.get('sequence_number')
        if has_course_sequence_number(self.course, sequence_number):
            raise forms.ValidationError("Sequence number already exists. Please choose a unique sequence number.")
        else:
            return sequence_number

    def save(self, commit=True):
        # Create a Lessons instance but don't commit it to the DB
        Lessons = super(LessonsCreateForm, self).save(commit=False)
        if commit:
            Lessons.course = self.course
            Lessons.save()
        return Lessons

    class Meta:
        model = Lessons
        fields = ['sequence_number', 'title', 'description']


class LessonsEditForm(LessonsCreateForm):
    def __init__(self, *args, **kwargs):
        self.lesson = kwargs.pop('lesson')
        super(LessonsEditForm, self).__init__(*args, **kwargs)

    def clean_sequence_number(self):
        cleaned_data = super(LessonsCreateForm, self).clean()
        sequence_number = cleaned_data.get('sequence_number')

        if sequence_number == self.lesson.sequence_number:
            return self.lesson.sequence_number
        if has_course_sequence_number(self.course, sequence_number):
            raise forms.ValidationError("Sequence number already exists. Please choose a unique sequence number.")
        return sequence_number

    def save(self, commit=True):
        # Create a Lessons instance but don't commit it to the DB
        lesson = super(LessonsEditForm, self).save(commit=False)
        if commit:
            lesson.course = self.course
            lesson.id = self.lesson.id
            lesson.save()
            # If a user changes a value from 3-4 in a sequence 1,2,3 then the sequence will be 1,2,4.
            # The lessons should be sequenced here to 1,2,3,4.
            sequence_lessons(lesson.course)
        return lesson

    class Meta:
        model = Lessons
        fields = ['sequence_number', 'title', 'description']


class LessonsLearningStylesResourcesCreateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        # If the course attribute exists as a kwarg then get it
        self.course = kwargs.pop('course')
        self.lesson = kwargs.pop('lesson')
        super(LessonsLearningStylesResourcesCreateForm, self).__init__(*args, **kwargs)

    learning_style = forms.ModelChoiceField(
        queryset=LearningStyles.objects.all(),
        widget=forms.Select,
        required=True,
        initial=0,
    )
    resources = forms.FileField(
        label='Please specify a zip file containing index.html',
        required=True,
    )

    def clean_resources(self):
        cleaned_data = super(LessonsLearningStylesResourcesCreateForm, self).clean()
        resource = cleaned_data.get('resources')
        if resource:
            # Check if the file is a zip file
            if zipfile.is_zipfile(resource):
                zip_file = zipfile.ZipFile(resource)
                found_index = False
                for file in zip_file.namelist():
                    if file == "index.html":
                        found_index = True
                if not found_index:
                    raise forms.ValidationError("Zip file does not contain 'index.html'.")
                # At this stage we can create a resource and link the resource object to the form (rather than the
                # uploaded resource).
                self.resources = create_resource(resource)
            else:
                raise forms.ValidationError("Please upload a zip file containing 'index.html'.")
            return resource

    def save(self, commit=True):
        # Create a LessonsLearningStyleResources instance but don't commit to the DB.
        lessonslearningstyleresource = super(LessonsLearningStylesResourcesCreateForm, self).save(commit=False)
        if commit:
            # Append form values from "self"
            lessonslearningstyleresource.lesson = self.lesson
            lessonslearningstyleresource.resource = self.resources
            lessonslearningstyleresource.save()
        return lessonslearningstyleresource

    class Meta:
        model = LessonsLearningStylesResources
        fields = ['title', 'description', 'learning_style', 'resources']


class LessonsLearningStylesResourcesEditForm(LessonsLearningStylesResourcesCreateForm):
    def __init__(self, *args, **kwargs):
        self.lessonlearningstyleresource = kwargs.pop('lessonlearningstyleresource')
        super(LessonsLearningStylesResourcesEditForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        # Create a LessonsLearningStyleResources instance but don't commit to the DB.
        lessonslearningstyleresource = super(LessonsLearningStylesResourcesEditForm, self).save(commit=False)
        # Append form values from "self".
        if commit:
            lessonslearningstyleresource.id = self.lessonlearningstyleresource.id
            lessonslearningstyleresource.lesson = self.lesson
            lessonslearningstyleresource.resource = self.resources
            lessonslearningstyleresource.save()
        return lessonslearningstyleresource

    class Meta:
        model = LessonsLearningStylesResources
        fields = ['title', 'description', 'learning_style', 'resources']
