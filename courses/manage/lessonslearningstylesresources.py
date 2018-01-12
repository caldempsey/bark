"""LessonsLearningStylesResources provides an interface of subroutines for the management of
LessonsLearningStylesResources models (and thus the entities in the database). Operations in this module refer to
operations which are performable on LessonsLearningStylesResources entities or are within reason to do with the
domain of LessonsLearningStylesResources management. """

from collections import Iterable
from django.db.models import QuerySet
from courses.models import Lessons
from courses.models import LessonsLearningStylesResources

__version__ = '1.0'
__author__ = 'Callum Dempsey Leach'

def get_lessonslearningstyleresource_from_id(id: int) -> LessonsLearningStylesResources:
    """
    Gets the lessonslearningstyleresource with a corresponding an id.

    :param id: The id of the LessonsLearningStylesResources object to obtain.
    :return: Returns the resource at the id.
    :raises: Raises an ObjectDoesNotExist exception if the object does not exist.
    """
    return LessonsLearningStylesResources.objects.get(id=id)


def remove_lessonlearningstyleresources_ids_from_lesson(lesson: Lessons, ids: Iterable) -> None:
    """
    Given an iterable list of primary keys safely removes the corresponding LessonsLearningStylesResources from a
    Lessons object (will have a null effect if the id is not for that lesson).
    :param lesson: The Lessons object.
    :param ids: Iterable of ids
    """
    assert all([str(i).isdigit() and int(i) > 0 for i in ids])
    LessonsLearningStylesResources.objects.filter(lesson=lesson, pk__in=ids).delete()


def get_all_learning_styles_lesson_resources(learning_styles: Iterable, lesson: Lessons) -> QuerySet:
    """
    Given an iterable of LearningStyles objects returns associated lesson resources.

    :param learning_styles: The list of LearningStyles objects.
    :param lesson: The Lessons object.
    :return: returns all associable LessonsResources objects.
    """
    resources = LessonsLearningStylesResources.objects.filter(learning_style__in=learning_styles, lesson=lesson)
    return resources


def has_lesson_resource(lesson: Lessons, resource: LessonsLearningStylesResources) -> bool:
    """
    Identifies if a Lessons object has a Resources object.

    :param lesson: The Lessons object.
    :param resource: The Resources object.
    :return: Returns true if true otherwise returns false.
    """
    has_resource = LessonsLearningStylesResources.objects.filter(lesson=lesson, id=resource.id).exists()
    return has_resource


def get_excluded_learning_styles_lesson_resources(learning_styles: Iterable, lesson: Lessons) -> QuerySet:
    """
    Passed a collection of LearningStyles objects and a Lessons object, get all the resources for that lesson that are *not* for that learning style.

    :param learning_styles: The LearningStyles objects.
    :param lesson: The Lessons Object
    :return: Returns a Queryset of requested resources.
    """
    resources = LessonsLearningStylesResources.objects.filter(lesson=lesson).exclude(learning_style__in=learning_styles)
    return resources
