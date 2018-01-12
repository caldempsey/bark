from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models

from courses.models import LessonsLearningStylesResources

# Define the minimum and maximum port values for containers (they creep up).
max_host_port_value = 22000
min_host_port_value = 10000


class DockerContainers(models.Model):
    """
    Defines the DockerContainers model.
    """
    resource = models.OneToOneField(LessonsLearningStylesResources, on_delete=models.CASCADE)
    unique_name = models.CharField(null=False, unique=True, max_length=500)
    host_port = models.PositiveIntegerField(unique=True,
                                            validators=[MinLengthValidator(min_host_port_value),
                                                        MaxLengthValidator(max_host_port_value)],
                                            null=False)
    build = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Docker Containers"
