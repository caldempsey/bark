"""
Lessons provides an interface of subroutines for the management of Lessons models (and thus the entities in the
database). Operations in this module refer to operations which are performable on Lessons entities (not as
encapsulated by Courses) or are within reason to do with the domain of Lessons management.

Lessons in the standard implementation have Courses as foreign key entities.
"""
from collections import Iterable
from courses.models import Lessons, Courses

__version__ = '1.0'
__author__ = 'Callum Dempsey Leach'


def get_lesson_from_id(id: int) -> Lessons:
    """
    Provided an id corresponding to a primary key of a Lessons object, will return a Lesson
    :param lesson_id: The id of the Lessons object requested as an integer.
    :return: Returns the Lessons object requested.
    """
    assert str(id).isdigit()
    assert int(id) > 0
    lesson = Lessons.objects.get(id=id)
    return lesson


def has_next_lesson(lesson: Lessons) -> bool:
    """
    Given a Lessons object identifies if a next lesson exists in that lessons course's sequence.
    :param lesson: The Lessons object to identify if a next lesson exists.
    :return: Returns true if the Lessons object exists otherwise returns false.
    """
    lesson_course = lesson.course
    lesson_sequence_number = lesson.sequence_number
    next_lesson_sequence_number = lesson_sequence_number + 1
    has_next = Lessons.objects.filter(course=lesson_course, sequence_number=next_lesson_sequence_number).exists()
    return has_next


# Given a lesson object returns the next lesson in the lesson sequence.
def get_next_lesson(lesson: Lessons) -> Lessons:
    """
    Given a lesson object returns the next lesson in the lesson sequence.
    :param lesson: The Lessons object to get the next lesson from.
    :return: Returns true if the Lessons object exists otherwise returns false.
    :raises: ObjectDoesNotExist if the object does not exist.
    """
    assert has_next_lesson(lesson)
    lesson_course = lesson.course
    lesson_sequence_number = lesson.sequence_number
    next_lesson_sequence_number = lesson_sequence_number + 1
    next_lesson = Lessons.objects.get(course=lesson_course, sequence_number=next_lesson_sequence_number)
    return next_lesson


def remove_lessons_ids_from_course(course: Courses, ids: Iterable) -> None:
    """
    Given an iterable list of primary keys removes lessons which correspond to those primary keys.
    :param course: The Courses to remove lessons from.
    :param ids: Any generic iterable collection of primary keys.
    """
    # We need to be careful with these kinds of assertions because Django will accept str values "1" and int value 1.
    # To overcome this we use Python list comprehension in conjunction with wrapping variables.
    assert all([str(i).isdigit() and int(i) > 0 for i in ids])
    # pk in allows for list filtering
    Lessons.objects.filter(course=course, pk__in=ids).delete()
    # Sequence the courses lessons once we have performed our update.
    sequence_lessons(course)


def sequence_lessons(course: Courses) -> None:
    """
    For a course, sequences the order of lessons in the database (not for re-order but perform an update to make sure
    there are no "missing" sequences). To illustrate if a lesson is created with a sequence number of 5 and another
    at a sequence number of 6 and 7, and 6 is deleted, then the sequence of lessons reads "5,7" (which is invalid and
    risks violating uniqueness constraints). This operation will perform an operation which updates those kinds of
    sequences to "5,6" without violating uniqueness.
    :param course: The Courses object to sequence the lessons of.
    """

    # Performs update in sequence to prevent uniqueness constraint conflict. For instance if we change 6 to 5 and 5 to
    # 4 then the uniqueness of the value 5 is violated. But given a lesson sequence 1,2,4,5, we can perform a unique
    # update for each value by performing value assignment based on its position in the sequence i.e.
    # updating 4 as 1,2,"3",4. This is performable with a simple for loop.
    lessons = Lessons.objects.filter(course=course).order_by(
        'sequence_number')
    i = 1
    for lesson in lessons:
        if lesson.sequence_number == i:
            pass
        else:
            lesson.sequence_number = i
        lesson.save()
        i = i + 1
