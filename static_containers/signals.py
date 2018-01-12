"""
Django signals are dispatched whenever conditions are met across the whole application
https://docs.djangoproject.com/en/1.11/ref/signals

Signals for static containers ensure atomic handling of creating and removing docker container entities in the database.
"""

import os
from django.db import transaction
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from courses.models import LessonsLearningStylesResources
from static_containers.docker_api.container_utils import force_remove_container
from static_containers.manage.dockercontainers import get_docker_container_from_resource
from static_containers.models import DockerContainers, min_host_port_value


@receiver(post_save, sender=LessonsLearningStylesResources)
def create_docker_container_from_learning_resource_handler(sender, instance, created, **kwargs):
    """
    Django signal implementation ensuring atomic creation of docker containers for each learning resource.
    https://docs.djangoproject.com/en/1.11/ref/signals/
    """
    if not created:
        # If it was not created then this is a new instance, we need to update the flag.
        docker_container = get_docker_container_from_resource(instance)
        docker_container.build = True
        docker_container.save()
        return
    else:
        # We need to ensure this operation will not result in duplicate ports (Django won't do this for us as it
        # isn't a key). We can do this by defining a critical section to enforce atomicity in the application.
        # BEGIN CRITICAL SECTION #
        #
        resource_name_with_ext = os.path.basename(str(instance.resource.file))
        resource_name_without_ext = os.path.splitext(resource_name_with_ext)[0]
        with transaction.atomic():
            if DockerContainers.objects.count() != 0:
                # Order by host port descending then get the first.
                current_largest_host_port = DockerContainers.objects.order_by('-host_port').first()
                port = current_largest_host_port.host_port
                port = port + 1
                docker_container = DockerContainers.objects.create(resource=instance, host_port=port, build=True,
                                                                   unique_name=resource_name_without_ext)
                # Call the method defined in saving the resources dock instance to the database
            else:
                docker_container = DockerContainers.objects.create(resource=instance, host_port=min_host_port_value,
                                                                   build=True,
                                                                   unique_name=resource_name_without_ext)
        docker_container.save()
        # END CRITICAL SECTION #


@receiver(pre_delete, sender=LessonsLearningStylesResources)
def remove_docker_container_handler(sender, instance, *args, **kwargs):
    """
    Django signal implementation of removal of docker container and docker container in the Docker engine.
    """
    # We need to remove associated containers with old resources or it is possible for old ports on old containers (
    # that are active) to conflict with new assignments. This will crash Django - not good.
    # Fortunately the solution to this is simple courtesy cleanup.
    docker_container = get_docker_container_from_resource(instance)
    print(docker_container.unique_name)
    container_name = docker_container.unique_name
    force_remove_container(container_name)
