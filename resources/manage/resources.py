from resources.models import Resources


def create_resource(resource):
    """
    Creates a resource file from the file passed

    :param resource: The resource passed.
    """
    return Resources.objects.create(file=resource)
