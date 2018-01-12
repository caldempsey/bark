from django.contrib.auth.models import User
from roles.models import UserRoles


def has_user_leader_role(user: User):
    """
    Simple function of whether a user has a leader role.

    :param user: The Users object.
    :return: Returns whether the user has a leader role.
    """
    is_true = UserRoles.objects.filter(user=user, role='leader').exists()
    return is_true
