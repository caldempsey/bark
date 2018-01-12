from collections import Iterable

from django.contrib.auth.models import User

from learning_styles.models import UserLearningStyles, LearningStyles

__version__ = '1.0'
__author__ = 'Callum Dempsey Leach'


def add_to_user_userlearningstyles_collection(user: User, learning_styles: Iterable):
    """
    Add a collection of learning styles to a user.

    :param user: The User object
    :param learning_styles: The LearningStyles objects as an iterable.
    """
    for learning_style in learning_styles:
        add_to_user_userlearningstyles(user, learning_style)


def add_to_user_userlearningstyles(user: User, learning_style: LearningStyles):
    """
    Add a learning style to a user.

    :param user: The User object
    :param learning_style: The LearningStyles object
    """
    UserLearningStyles.objects.create(user=user, learning_style=learning_style)


def purge_user_userlearningstyles(user: User):
    """
    Remove all learning styles from a User.

    :param user: The User object.
    """
    UserLearningStyles.objects.filter(user=user).delete()


def get_user_learning_styles_from_user(user: User) -> list:
    """
    Return all of a User's learning styles.
    :param user: The User object
    :return: Returns a list of their learning styles.
    """
    user_learning_styles = UserLearningStyles.objects.filter(user=user)
    learning_styles = []
    for user_learning_style in user_learning_styles:
        # For each learning style of the user learning styles object.
        learning_styles.append(user_learning_style.learning_style)
    return learning_styles
