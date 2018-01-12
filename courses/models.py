from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator, MinValueValidator
from django.db import models
from learning_styles.models import LearningStyles
from resources.models import Resources

__version__ = '1.0'
__author__ = 'Callum Dempsey Leach'


class Courses(models.Model):
    """
    Courses. Defines courses (this implementation is coupled with the Resources table to add a Logo).
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(max_length=100, validators=[MaxLengthValidator(100)])
    description = models.CharField(max_length=100, validators=[MaxLengthValidator(100)], default="")
    logo = models.OneToOneField(Resources, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Courses"

    def __str__(self):
        return self.title


class Lessons(models.Model):
    """
    Lessons. Defines lessons.
    """
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    # The sequence number determines any ordering of lessons as well as serving as a candidate primary key.
    sequence_number = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    title = models.CharField(max_length=100, validators=[MaxLengthValidator(100)])
    description = models.CharField(max_length=100, validators=[MaxLengthValidator(100)], default="")
    resources = models.ManyToManyField(LearningStyles, through='LessonsLearningStylesResources', max_length=500,
                                       related_name='resources')
    user_progress = models.ManyToManyField(User, through='UserLessonsCompleted')

    class Meta:
        verbose_name_plural = "Lessons"
        unique_together = ("course", "sequence_number")

    def __str__(self):
        course = str(self.course)
        sequence_number = str(self.sequence_number)
        title = str(self.title)
        string = "Lesson course, " + course + ". Lesson sequence number, " + sequence_number + ". Title " + title
        return string



class UserLessonsCompleted(models.Model):
    """
    UserLessonsCompleted. Defines lessons the user has completed.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lessons, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Course Progress"

    def __str__(self):
        user = str(self.user)
        lesson = str(self.lesson)
        string = "Lesson Save Data for " + user + ": " + lesson
        return string


class LessonsLearningStylesResources(models.Model):
    """
    Lesson Learning Style Resources Many to Many. Defines all the resources accessible for each lesson based on LearningStyle
    """
    lesson = models.ForeignKey(Lessons, on_delete=models.CASCADE)
    learning_style = models.ForeignKey(LearningStyles, on_delete=models.CASCADE)
    resource = models.OneToOneField(Resources, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, validators=[MaxLengthValidator(100)])
    description = models.CharField(max_length=100, validators=[MaxLengthValidator(100)], default="")

    class Meta:
        verbose_name_plural = "Lessons Learning Style Resources"

    def __str__(self):
        lesson = str(self.lesson_id)
        learning_style = str(self.learning_style)
        string = lesson + ": " + learning_style
        return string
