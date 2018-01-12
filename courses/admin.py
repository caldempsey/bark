"""
Registers models so they can be used by the built-in Django administrator.
"""

from django.contrib import admin
from courses.models import Lessons, Courses, UserLessonsCompleted
from courses.models import LessonsLearningStylesResources

# Register models to the adminsitrator site.

admin.site.register(Courses)
admin.site.register(Lessons)
admin.site.register(LessonsLearningStylesResources)
admin.site.register(UserLessonsCompleted)
