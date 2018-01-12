from collections import Iterable

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from communicate.exceptions.courses_exceptions import CourseNotFoundException
from communicate.exceptions.learning_resources_exceptions import LearningResourceNotFoundException
from communicate.exceptions.lessons_exceptions import LessonNotFoundException
from courses.manage.courses import get_course_from_id, remove_courses_ids_from_user, \
    generate_next_lesson_sequence_number
from courses.manage.lessons import get_lesson_from_id, remove_lessons_ids_from_course
from courses.manage.lessonslearningstylesresources import remove_lessonlearningstyleresources_ids_from_lesson, \
    get_lessonslearningstyleresource_from_id
from courses.models import Courses, Lessons


def remove_courses_list(user: User, courses: Iterable):
    """
    Given a list of courses and a leader will remove all the courses for that leader.
    :param user: the Leader to remove courses from.
    :param courses: the Courses
    """
    remove_courses_ids_from_user(user, courses)


def remove_lessons_list(course: Courses, lessons: Iterable):
    """
    Given a list of lessons for a course will remove those lessons for that course.
    :param course: The Courses object to remove lessons from.
    :param lessons: The Lessons objects to remove from the course.
    """
    remove_lessons_ids_from_course(course, lessons)


def remove_learning_resources_list(lesson: Lessons, learning_resources: Iterable):
    """
    Given a list of learning resources and a lesson will remove learning resources from that lesson.
    :param lesson: The Lessons object to remove learning resources from
    :param learning_resources: The LearningResources objects to remove.
    """
    remove_lessonlearningstyleresources_ids_from_lesson(lesson, learning_resources)


def get_leaders_course(course_id: int, user: User):
    """
    Given a course id and a leader will return the courses object for that leader.
    :param course_id: The id of the Course
    :param user: The User object representing the leader.
    :return: Returns a Courses object.
    :raises: Raises a CourseNotFoundException if the course cannot be found.
    """
    try:
        course = get_course_from_id(course_id)
        if not course.author == user:
            raise CourseNotFoundException
        return course
    except ObjectDoesNotExist:
        raise CourseNotFoundException


def get_leaders_lesson(lesson_id: int, course: Courses, user: User):
    """
    Given a lesson id and a course and a specified leader, returns the lesson for that course for that leader.
    :param lesson_id: The Lesson id
    :param course: The Courses object.
    :param user: The User object representing the leader.
    :return: Returns a Lessons object.
    :raises: Raises a LessonNotFoundException if the lesson cannot be found.
    """
    try:
        lesson = get_lesson_from_id(lesson_id)
        if not course.author == user:
            raise LessonNotFoundException
        if not lesson.course == course:
            raise LessonNotFoundException
    except ObjectDoesNotExist:
        raise LessonNotFoundException
    return lesson


def get_leaders_learning_resource(learning_resource_id: int, lesson: Lessons, course: Courses, user: User):
    """
     Given a learning resources id, a lesson, a course, and a specified leader, returns the
     learning resource meeting each criteria.
    :param learning_resource_id: The LessonsLearningStyleResources id.
    :param lesson: The Lessons object
    :param course: The Courses object.
    :param user: The User object representing the leader.
    :return: Returns a LessonsLearningStyleResources object.
    """
    try:
        learning_resource = get_lessonslearningstyleresource_from_id(learning_resource_id)
        if not learning_resource.lesson == lesson:
            raise LearningResourceNotFoundException
        if not lesson.course == course:
            raise LearningResourceNotFoundException
        if not course.author == user:
            raise LearningResourceNotFoundException
    except ObjectDoesNotExist:
        raise LearningResourceNotFoundException
    return learning_resource


def get_maximum_lesson_sequence_number(course: Courses) -> int:
    """
    Given a course will return the next projected lesson for that course (between 1 to n).
    :param course: The Courses object to generate the next lesson for.
    :return: Returns the value of the next projected lesson.
    """
    next_lesson_sequence_number = generate_next_lesson_sequence_number(course=course)
    return next_lesson_sequence_number
