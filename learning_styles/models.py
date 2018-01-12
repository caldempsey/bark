from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator
from django.db import models


class LearningStyles(models.Model):
    """
    The Learning Styles model provides LearningStyles.
    """
    name = models.CharField(max_length=100, validators=[MaxLengthValidator(100)])
    # Identifies if the learning style is on the same spectrum
    spectrum_id = models.PositiveIntegerField(default=0)
    user = models.ManyToManyField(User, through='UserLearningStyles')

    class Meta:
        verbose_name_plural = "Learning Styles"

    def __str__(self):
        return self.name

class UserLearningStyles(models.Model):
    """
    UserLearningStyles attributes learning styles to the Django user model.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    learning_style = models.ForeignKey(LearningStyles, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Users Learning Style"

    def __str__(self):
        user = str(self.user)
        learning_style = str(self.learning_style)
        string = (user + " : " + learning_style)
        return string
