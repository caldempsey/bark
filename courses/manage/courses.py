"""Courses provides an interface of subroutines for the management of Courses models (and thus the entities in the
database). Operations in this module refer to operations which are performable on Courses entities or are within
reason to do with the domain of Courses management.

Courses in the standard implementation have logos which are saved to the "Resources" entries in a database.

To use the courses model a respective "Resources" model should thus be defined. If this feature is not desired then
removing the "logo" field from the Courses model should be a task performed by integrating developers. This will
de-couple courses from the rest of the implementing application.
"""

from collections import Iterable

from django.contrib.auth.models import User
from django.db.models import QuerySet

from courses.models import Courses, Lessons

__version__ = '1.0'
__author__ = 'Callum Dempsey Leach'


def get_all() -> QuerySet:
    """
    Return all course entries in the database as a QuerySet object of Course objects.
    :return: Returns all Courses in a QuerySet.
    """
    return Courses.objects.all()


def get_courses_from_user(user: User) -> QuerySet:
    """
    Provided a User object (as a foreign entity) will return all courses for that user as a QuerySet object.
    :param user: The User object specified.
    :return: Returns a QuerySet object of all courses with a specific user as a foreign key.
    """
    courses = Courses.objects.filter(author=user)
    return courses


def remove_courses_ids_from_user(user: User, ids: Iterable) -> None:
    """
    Provided a User object and iterable list of "id" variables will safely remove all ids for that user.
    :param user: The User object specified.
    :param ids: An iterable list of ids to remove from the specified User object.
    """
    # We need to be careful with these kinds of assertions because Django will accept str values "1" and int value 1.
    # To overcome this we use Python list comprehension in conjunction with wrapping variables.
    assert all([str(i).isdigit() and int(i) > 0 for i in ids])
    # Primary keys can be of any type so
    # Only delete course objects for the user for the ids passed. For all non-corresponding ids, do nothing.
    Courses.objects.filter(author=user, pk__in=ids).delete()


def has_user_course(user: User, course: Courses):
    """
    Validates whether a course has a User object as its foreign key.
    :param user:  The Users object to be validated.
    :param course: The Courses object to be validated.
    :return: Returns true if the user object has the course, returns false otherwise.
    """
    has_course = Courses.objects.filter(id=course.id, author=user).exists()
    return has_course


def has_course_lesson(course: Courses, lesson: Lessons):
    """
    Validates whether a Lesson has a Course object as its foreign key.
    :param course: The Courses object to be validated.
    :param lesson: The Lessons object to be validated.
    :return: Returns true if the Lesson object exists with the Course as a foreign key, returns false otherwise.
    """
    has_lesson = Lessons.objects.filter(id=lesson.id, course=course).exists()
    return has_lesson


def get_course_from_id(id: int):
    """
    Provided an id variable returns the course object.
    :param id: The id of the course to acquire.
    :return: Returns the Courses object at the specified id.
    :raises
    ObjectDoesNotExist: if the object is not found.
    """
    assert int(id) > 0
    # Return the courses object with the specified id from the database as a Courses object.
    return Courses.objects.get(id=id)


def generate_next_lesson_sequence_number(course: Courses) -> int:
    """
    Provided a Courses object will generate the next lesson's sequence number. If the course happens to have no
    Lessons will return "1" as representative of the first lesson in the sequence.
    :param course: The Course object to generate the next lesson sequence number for.
    :return: Returns the sequence number as an integer.
    """
    # For all Lessons objects count the number of Lessons objects with the course passed as a foreign key.
    if Lessons.objects.filter(course=course).count() == 0:
        # If the value is 0 then determine the next sequence number for lessons as 1.
        next_sequence_number = 1
    else:
        # Otherwise attain the greatest sequence number Lessons for a course (ordering by sequence number ascending
        # i.e. "9,8,7" and getting the first value.
        last_sequence_number = Lessons.objects.filter(course=course).order_by(
            '-sequence_number').first().sequence_number
        # The next sequence number is that value +1.
        next_sequence_number = last_sequence_number + 1
    # Assert the return value is not negative or 0.
    assert next_sequence_number > 0
    return next_sequence_number


def has_course_sequence_number(course: Courses, sequence_number: int) -> bool:
    """
     Provided a Courses object will identify if a lesson at the specified sequence number exists.
     :param course: The Course object to generate the next lesson sequence number for.
     :return: Returns true if the sequence number exists otherwise returns false.
     """
    assert int(sequence_number) > 0
    has_lesson = course.lessons_set.filter(course=course, sequence_number=sequence_number).exists()
    return has_lesson


def get_course_lesson_from_sequence_number(course: Courses, sequence_number: int):
    """
    Provided a Courses object and a sequence number will return the Lessons object of the course at the specified
    sequence number.
    :param course: The Courses object.
    :param sequence_number: The sequence number of the Lessons
    object to return.
    :return: Returns the Lessons object from the course and sequence number provided.
    :raises:
    ObjectDoesNotExist: If the object does not exist.
    """
    assert int(sequence_number) > 0
    return Lessons.objects.get(course=course, sequence_number=sequence_number)
