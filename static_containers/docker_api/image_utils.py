import os

import docker
from django.db.models.fields.files import FieldFile

from bark.settings import MEDIA_ROOT


# Prepares a dockerfile for a html resource by writing a dockerfile for that resource.
# The dockerfile will be written for nginx container deployment
def prepare_nginx_dockerfile_for_resource(resource_file: FieldFile):
    """
    Prepares a dockerfile for a html resource by writing a dockerfile for that resource.
    The dockerfile will be written for nginx container deployment
    :param resource_file:
    """
    # Specify dockerfile template.
    template = "library/dockerfiles/nginx_alpine.txt"
    # String conversion to the file at media_root so we can handle the field file with the OS module.
    resource_file = str(MEDIA_ROOT + "/" + str(resource_file))
    resource_abspath = os.path.abspath(resource_file)
    # Ensure the resource is a file.
    try:
        if not os.path.isfile(resource_abspath):
            raise AssertionError
    except AssertionError:
        print("No file found at " + resource_abspath + ", do you have permissions?")
        exit(-1)
    # Ensure we have the absolute path of the resource.
    resource_abspath = os.path.abspath(resource_file)
    dockerfile_path = os.path.dirname(resource_abspath)
    # Define local variables we will be using#
    filename = os.path.basename(resource_abspath)
    replacements = {'[RESOURCE_FILENAME]': filename}
    # Read the lines of the in-file to a string
    infile = open(os.path.join(os.path.dirname(__file__), template)).read()
    # Create the dockerfile to write to #
    outfile = open(dockerfile_path + '/Dockerfile', '+w')
    # Write to dockerfile making replacements using the dictionary defined #
    for i in replacements.keys():
        infile = infile.replace(i, replacements[i])
    outfile.write(infile)
    print("Wrote " + str(dockerfile_path))
    outfile.close()


def get_dockerfile(resource_file: FieldFile):
    """
    Given a file will return its Dockerfile (if one exists). Otherwise this will throw an assertion error.
    :param resource_file: The file to acquire a Dockerfile for.
    :return: Returns the directory of the Dockerfile.
    """
    # String conversion to the file at media_root so we can handle the field file with the OS module.
    resource_file = str(MEDIA_ROOT + "/" + str(resource_file))
    # Ensure we have absolute path to the file.
    resource_abspath = os.path.abspath(resource_file)
    # Ensure the resource is a file.
    try:
        if not os.path.isfile(resource_abspath):
            raise AssertionError
    except AssertionError:
        # Present some more useful assertion information than what's given by "just assert".
        print("No file found at " + resource_abspath + ", do you have permissions?")
        exit(-1)
    dockerfile = os.path.dirname(resource_abspath)
    return dockerfile


def has_resource_file_dockerfile(resource_file: FieldFile):
    """
    Will check that a file at a location has a Dockerfile. In most cases this should always be called before retrieving one or generating one.
    :param resource_file: Location of the file.
    :return: Returns true if a dockerfile exists.
    """
    # String conversion to the file at media_root so we can handle the field file with the OS module.
    resource_file = str(MEDIA_ROOT + "/" + str(resource_file))
    # Ensure we have absolute path to the file.
    resource_abspath = os.path.abspath(resource_file)
    # Ensure the resource is a file.
    try:
        if not os.path.isfile(resource_abspath):
            raise AssertionError
    except AssertionError:
        # Present some more useful assertion information than what's given by "just assert".
        print("No file found at" + resource_abspath + ", do you have permissions?")
        exit(-1)
    dockerfile = os.path.dirname(resource_abspath) + '/Dockerfile'
    return os.path.isfile(dockerfile)


def create_image(dockerfile_path: str, image_name: str):
    """
    Creates an image from a dockerfile at a path.
    :param dockerfile_path: Dockerfile path.
    :param image_name: Name of the image.
    """
    # Ensure we have a dockerfile.
    try:
        if not os.path.isfile(dockerfile_path + "/Dockerfile"):
            raise AssertionError
    except AssertionError:
        # Present some more useful assertion information than what's given by "just assert".
        print("No file found at" + dockerfile_path + ", do you have permissions?")
        exit(-1)
    client = docker.from_env()
    client.images.build(path=dockerfile_path, tag=image_name)
    # Return true if the new image was successfully created.
    return True
