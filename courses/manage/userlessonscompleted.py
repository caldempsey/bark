"""UserLessonsCompleted provides an interface of subroutines for the management of
LessonsLearningStylesResources models (and thus the entities in the database). Operations in this module refer to
operations which are performable on UserLessonsCompleted entities or are within reason to do with the
domain of UserLessonsCompleted management. """

import math
from collections import Iterable

from django.contrib.auth.models import User
from django.db.models import QuerySet

from courses.models import UserLessonsCompleted, Lessons, Courses

__version__ = '1.0'
__author__ = 'Callum Dempsey Leach'


def add_user_completed_lesson(user: User, lesson: Lessons) -> None:
    """
    Adds a completed lesson to a user.

    :param user: The User object.
    :param lesson: The Lessons object.
    """
    UserLessonsCompleted.objects.create(user=user, lesson=lesson)


# Returns a QuerySet of all the completed lessons of a user profile for a course.
def has_user_completed_course_lesson(user: User, course: Courses) -> bool:
    """
    Returns whether a user has completed a course lesson.

    :param user: The User object.
    :param lesson: The Lessons object.
    :return: Returns true if the user has completed the course otherwise returns false.
    """
    has_completed = UserLessonsCompleted.objects.filter(user=user).filter(lesson__course_id=course).exists()
    return has_completed


def get_user_course_completion_percentages(user: User, courses: Iterable) -> dict:
    """
    Returns a percentage of completed lessons for each course passed to the dictionary.

    :param user: The User object.
    :param courses: The Courses object.
    :return:
    """
    # For each course get the percentage of lessons completed by the user.
    course_completion_percentages = {}
    for course in courses:
        number_of_lessons = len(course.lessons_set.all())
        if number_of_lessons == 0:
            course_completion_percentages.update({course.id: 0})
        else:
            # Count the completed lessons belonging to the course, turn that into a percentage against the number of
            # lessons.
            completed_lessons = UserLessonsCompleted.objects.filter(lesson__course=course,
                                                                    user=user).count()
            completion_percentage = math.floor((float(completed_lessons) / float(number_of_lessons) * 100))
            course_completion_percentages.update({course.id: completion_percentage})
    return course_completion_percentages


def has_user_completed_lesson(user: User, lesson: Lessons) -> bool:
    """
    Returns whether or not a user has completed a lesson.

    :param user: The User object.
    :param lesson: The Lessons object.
    :return: Returns true if the user has completed the lesson otherwise returns false.
    """
    has_completed = UserLessonsCompleted.objects.filter(user=user, lesson=lesson).exists()
    return has_completed


# Returns a sorted set of all the completed lessons of a user profile for a course.
def has_user_completed_course_lessons(user: User, course: Courses) -> QuerySet:
    """
    Returns whether a user has completed any lessons of a course.

    :param user: The User object.
    :param course: The Courses object.
    :return: Returns true if any lessons of a course are complete otherwise returns false.
    """
    lessons = UserLessonsCompleted.objects.filter(user=user).filter(lesson__course_id=course).exists()
    return lessons


def get_user_completed_lessons_sorted(user: User, course: Courses):
    """
    Returns a sorted set of all the completed lessons of a user profile for a course.
    :param user: The User object.
    :param course: The Courses object.
    :return: Returns a sorted set of all the completed lessons of a user for a course.
    """
    lessons = UserLessonsCompleted.objects.filter(user=user).filter(lesson__course_id=course).order_by(
        'lesson__sequence_number')
    return lessons


def purge_user_course_progress(user: User, course: Courses) -> None:
    """
    Purges (deletes) all user progress for a given course.
    :param user: The User object.
    :param course: The Courses object.
    """
    UserLessonsCompleted.objects.filter(lesson__course_id=course.id, user=user).delete()


def purge_user_progress(user: User) -> None:
    """
    Purges (deletes) all user progress for a given user.
    :param user: User object to purge.
    """
    UserLessonsCompleted.objects.filter(user=user).delete()
