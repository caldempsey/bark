import re
import traceback

import docker
from docker.errors import APIError

# Use the directory of all containers to identify if a container exists.
from static_containers.models import max_host_port_value, min_host_port_value


def has_container(container_name: str):
    """
    Checks if a container at a name exists using the Docker Engine.
    :param container_name: String of name
    """
    client = docker.APIClient(base_url='unix://var/run/docker.sock')
    # Something the Docker engine does is prepend a `/` to names for some reason, we will need to account for that.
    container_name = str("/" + container_name)
    containers = (client.containers(all=True))
    for container in containers:
        # Returns a set of containers as dictionaries. Search for keys of value "Names" (which is the key value in
        # test data, see below)...
        #
        # [{'Names': ['/website2'], 'State': 'running',
        # 'Id': '58068a86f5e5086be6192c9ef242177861c8820195385e4633e9fb992a6eaf3f', 'Created': 1502995186,
        # 'HostConfig': {'NetworkMode': 'default'}, 'ImageID':
        # 'sha256:57ff420a68ee6977441035471e991800d42adeb78f8797a540bb2cf74060d62e', 'NetworkSettings': {'Networks':
        # {'bridge': {'EndpointID': '787b2d5d10c30fe336a0d467bd70ba3b2e985c827971eb67086a5d067ef915ba',
        # 'GlobalIPv6PrefixLen': 0, 'GlobalIPv6Address': '', 'NetworkID':
        # '1e1b2bbca525b51d5a85fe8a90ad1545f0f01225db6a72bfdb83b65b1b09574e', 'IPPrefixLen': 16, 'DriverOpts': None,
        # 'Links': None, 'IPv6Gateway': '', 'Aliases': None, 'IPAddress': '172.17.0.2', 'Gateway': '172.17.0.1',
        # 'IPAMConfig': None, 'MacAddress': '02:42:ac:11:00:02'}}}, 'Mounts': [], 'Status': 'Up 4 minutes',
        # 'Command': "nginx -g 'daemon off;'", 'Image': 'website-container100:latest', 'Labels': {}, 'Ports': [{
        # 'PrivatePort': 80, 'IP': '0.0.0.0', 'PublicPort': 8002, 'Type': 'tcp'}]}]
        for name in container.get("Names"):
            if name == container_name:
                return True
    return False


def instantiate_bound_container(container_image: str, container_name: str, container_port: int, host_port: int):
    assert validate_container_name(container_image)
    assert validate_container_name(container_name)
    assert 0 < container_port
    assert not host_port < min_host_port_value or max_host_port_value < host_port
    port_bind = {str(container_port) + '/tcp': host_port}
    client = docker.from_env()
    client.containers.run(container_image,
                          detach=True, name=container_name, ports=port_bind)




def force_remove_container(container_name: str):
    """
    Force remove a container.
    :param container_name: The container to force remove.
    """

    # Permanently removes a container. A nuance to this operation is if the container does not exist and we try to remove
    # it this will cause an error state, but we don't want to shut down system if we remove a container which doesn't
    # exist [job done] or ignore the error in case it's a significant error. Therefore we check to see if the container
    # exists before executing (it should be removed). This limitation means that only one process can remove a container
    # at any given time [anything more than that and we might cause a race condition where multiple processes are trying
    # to remove the same container and pass the "has_container" check].

    try:
        # Remove the container_name only if the container_name exists.
        if has_container(container_name):
            client = docker.APIClient(base_url='unix://var/run/docker.sock')
            client.remove_container(container=container_name, force=True)
            return True
        else:
            return True
    except APIError:
        traceback.print_tb(APIError.__traceback__)
        exit(-1)


def start_container(container: str):
    """
    Starts an exited container.

    :param container: The container name.
    :return: Returns true if the container is started (which also occurs if already running).
    """
    try:
        assert validate_container_name(container)
        client = docker.APIClient(base_url='unix://var/run/docker.sock')
        client.start(container=container)
        return True
    # If the container is valid and a reference to it exists then if it won't start it's a problem
    # with the individual container (and not the whole daemon). We raise an interface error in this circumstance without
    # shutting down the system, as it could be the container is temporarily not available (has just been removed).
    except (APIError):
        print(
            "Docker daemon returned the following error when starting container " + container
            + " the container has been flagged to be re-built \n \n")
        # Provide interface error stacktrace
        traceback.print_tb(APIError.__traceback__)


def validate_container_name(container_name: str):
    if re.match("^[a-z0-9]*$", container_name):
        return True
    else:
        return False
