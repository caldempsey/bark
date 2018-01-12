from static_containers.models import DockerContainers


def get_docker_container_from_resource(resource):
    """
    Given a resource  will return a docker container for the resource if one exists.
    :param resource: The resource (duck typed).
    :return: The container for the resource.
    """
    assert DockerContainers.objects.filter(resource=resource).exists()
    return DockerContainers.objects.get(resource=resource)


def get_docker_container_port_from_resource(resource):
    """
    Given a resource which has a valid container, will return the port of the resource.
    :param resource: The resource (duck typed).
    :return:
    """
    docker_image = get_docker_container_from_resource(resource)
    host_port = docker_image.host_port
    return host_port


def has_docker_container_unique_name(unique_name: str) -> bool:
    """
    Identifies if a docker container exists with the name passed.
    :param unique_name: The name to check as a string.
    :return: Returns boolean true or false.
    """
    return DockerContainers.objects.filter(unique_name=unique_name).exists()


# Returns true when the operation completes.
def flag_docker_container_for_rebuild(docker_container: DockerContainers, requires_rebuild: bool):
    """
    Given a DockerContainers object updates the flag signalling whether the container that it needs re-instancing.
    :param docker_container: The DockerContainer object.
    :param requires_rebuild: The value to update with.
    """
    docker_container.build = requires_rebuild
    docker_container.save()
