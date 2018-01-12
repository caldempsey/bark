from django.core.exceptions import ObjectDoesNotExist
from docker.errors import APIError
from communicate.exceptions.resource_exceptions import ResourceNotFoundException
from communicate.exceptions.static_containers import RenderResourceFailedException
from courses.models import LessonsLearningStylesResources
from static_containers.docker_api.container_utils import has_container, force_remove_container, \
    instantiate_bound_container, start_container
from static_containers.docker_api.image_utils import prepare_nginx_dockerfile_for_resource, \
    has_resource_file_dockerfile, \
    get_dockerfile, create_image
from static_containers.manage.dockercontainers import get_docker_container_from_resource, \
    flag_docker_container_for_rebuild


def lessonslearningstyleresource_to_nginx_alpine_static_container(
        learning_resource: LessonsLearningStylesResources) -> int:
    """
    Given a lessonlearningstyleresource will spawn an nginx alpine container.
    :param learning_resource: The LessonsLearningStylesResource.
    :return: Returns the port that the resource is currently live on.
    :raises: In the case of an API error which can be permitted and does not crash
    the server (some Docker API errors are difficult "NotFound"
    when seeing if something exists), will raise a RenderResourceFailedException.
    """
    # Get the DockerContainer object containing Docker image and container related information.
    docker_container = get_docker_container_from_resource(learning_resource)
    # Get the unique port of the resource object. If an exception occurs here we need to look at the database.
    resource_port = docker_container.host_port
    # Get the resource file object #
    try:
        resource_file = learning_resource.resource.file
    except ObjectDoesNotExist:
        raise ResourceNotFoundException
    # Check the resource has a dockerfile, if not build one
    if not has_resource_file_dockerfile(resource_file):
        prepare_nginx_dockerfile_for_resource(resource_file)
    # Get the dockerfile path
    dockerfile = get_dockerfile(resource_file)
    # Set container name and image name to be the unique name.
    container_name = docker_container.unique_name.lower()
    image_name = docker_container.unique_name.lower()
    if docker_container.build:
        create_image(dockerfile, image_name)
        # If a container for the resource object already exists it needs to be rebuilt.
        # Some people might lose access temporarily during this time.
        if has_container(container_name):
            # Remove the container for the container object
            force_remove_container(container_name)
        # Instantiate a new container using the database details and NGINX default port (80).
        instantiate_bound_container(container_name, image_name, 80, resource_port)
        flag_docker_container_for_rebuild(docker_container, False)
        docker_container.save()
    # If the resource doesn't require rebuilding from a new image then *just* check a container exists (it
    # should if we just instantiated one).
    if not has_container(container_name):
        instantiate_bound_container(container_name, image_name, 80, resource_port)
    # Make sure the container is spun up or refreshed. If an interface error occurs then return a Http500 response
    # (as it may or may not require further investigation).
    try:
        start_container(container_name)
    except APIError:
        raise RenderResourceFailedException
    # Render the resource port with the attached port.
    return resource_port
