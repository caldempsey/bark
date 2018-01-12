"""
Registers models so they can be used by the built-in Django administrator.
"""

from django.contrib import admin

from learning_styles.models import LearningStyles, UserLearningStyles

admin.site.register(LearningStyles)
admin.site.register(UserLearningStyles)
