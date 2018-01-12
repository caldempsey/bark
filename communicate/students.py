from collections import Iterable

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet

from communicate.exceptions.courses_exceptions import CourseNotFoundException, NoCoursesExistException
from communicate.exceptions.learning_resources_exceptions import NoLearningResourcesExistException, \
    LearningResourceNotFoundException
from communicate.exceptions.learning_styles_exceptions import NoLearningStylesException
from communicate.exceptions.lessons_exceptions import LessonNotFoundException
from communicate.exceptions.lessons_exceptions import NoLessonsExistException
from courses.manage.courses import get_course_from_id, has_course_sequence_number, \
    get_all, get_course_lesson_from_sequence_number
from courses.manage.lessons import get_lesson_from_id
from courses.manage.lessonslearningstylesresources import get_all_learning_styles_lesson_resources, \
    get_excluded_learning_styles_lesson_resources, get_lessonslearningstyleresource_from_id
from courses.manage.userlessonscompleted import get_user_completed_lessons_sorted, \
    has_user_completed_lesson, has_user_completed_course_lessons, get_user_course_completion_percentages, \
    purge_user_course_progress, add_user_completed_lesson, purge_user_progress
from courses.models import Courses, Lessons
from courses.models import LessonsLearningStylesResources
from learning_styles.manage.userlearningstyles import get_user_learning_styles_from_user, purge_user_userlearningstyles, \
    add_to_user_userlearningstyles_collection


def has_next_lesson(lesson: Lessons) -> bool:
    """
    Identifies if a Lessons object has a next lesson.
    :param lesson: the Lessons object.
    """
    course = lesson.course
    lesson_sequence_number = lesson.sequence_number
    next_lesson_sequence_number = lesson_sequence_number + 1
    has_next = has_course_sequence_number(course, next_lesson_sequence_number)
    return has_next


def get_next_lesson(lesson: Lessons) -> Lessons:
    """
    Gets the next lesson of a Lessons object
    :param lesson: the Lessons object.
    :raises: Raises LessonNotFoundException if the lesson does not exist.
    """
    lesson_course = lesson.course
    lesson_sequence_number = lesson.sequence_number
    next_lesson_sequence_number = lesson_sequence_number + 1
    try:
        next_lesson = get_course_lesson_from_sequence_number(course=lesson_course,
                                                             sequence_number=next_lesson_sequence_number)
    except ObjectDoesNotExist:
        raise LessonNotFoundException
    return next_lesson


def get_course(course_id: int):
    """
    Gets a course from an id.
    :param course_id: An integer representing the course id.
    :return: Returns the Courses object.
    :raises: Raises CourseNotFoundException if the course does not exist.
    """
    try:
        return get_course_from_id(course_id)
    except ObjectDoesNotExist:
        raise CourseNotFoundException


def get_all_courses():
    """
    Returns all Courses objects (if there are any).
    :return: Returns all courses.
    :raises: Raises NoCoursesExistException if no courses exist.
    """
    courses = get_all()
    if not courses:
        raise NoCoursesExistException
    return courses


def get_learning_resources(learning_styles: Iterable, lesson: Lessons) -> QuerySet:
    """
    Given a list of learning styles and a Lessons returns all associable learning resources for that Lesson.
    :param learning_styles: Input list of LearningStyles.
    :param lesson: Lessons objects.
    :return: Returns a QuerySet of Learning Resources.
    :raises: Raises a NoLearningResourcesExistException if none are found.
    """
    learning_resources = get_all_learning_styles_lesson_resources(learning_styles, lesson)
    if not learning_resources:
        raise NoLearningResourcesExistException
    return learning_resources


def get_all_learning_resources_except_learningstyles_from_list(learning_styles: Iterable,
                                                               lesson: Lessons) -> Iterable:
    """
    Given any iterable of learning styles and a lesson will return all the lesson's resources except for
    those learning styles (from the list.)
    :param learning_styles: A list of LearningStyles objects to check.
    :param lesson: The lesson in question.
    :return: Returns an iterable list of all learning resources except those passed.
    :raises: Raises a NoLearningResourcesExistException if the learning resource does not exist.
    """
    learning_resources = get_excluded_learning_styles_lesson_resources(learning_styles, lesson)
    if not learning_resources:
        raise NoLearningResourcesExistException
    return learning_resources


def get_course_lesson(lesson_id: int, course: Courses) -> Lessons:
    """
    Gets a lesson for a course given its id.
    :param lesson_id: The lesson for the course.
    :param course: The Courses object to check.
    :return: Returns the Lessons object queried.
    :raises: Raises a LessonNotFound exception if the course does not have the lesson.
    """
    try:
        lesson = get_lesson_from_id(lesson_id)
        if not lesson.course == course:
            raise LessonNotFoundException
        return lesson
    except ObjectDoesNotExist:
        raise LessonNotFoundException


def get_lesson_resource(learning_resource_id: int, lesson: Lessons, course: Courses) -> LessonsLearningStylesResources:
    """
    Gets a lesson resource given a LessonsLearningStyleResources id.
    :param learning_resource_id: LessonsLearningStyleResource id.
    :param lesson: The lesson to retrieve it from.
    :param course: The course to retrieve it from.
    :return: Returns the learning_resource.
    :raises: Raises a LearningResourceNotFound exception in the event of error.
    """
    try:
        learning_resource = get_lessonslearningstyleresource_from_id(learning_resource_id)
        if not learning_resource.lesson == lesson:
            raise LearningResourceNotFoundException
        if not lesson.course == course:
            raise LearningResourceNotFoundException
        return learning_resource
    except ObjectDoesNotExist:
        raise LearningResourceNotFoundException


def get_first_lesson_in_course(course: Courses):
    """
    Given a course returns its first lesson.
    :param course: The Courses object.
    :return: Returns the first lesson.
    """
    try:
        lesson = get_course_lesson_from_sequence_number(course, 1)
        return lesson
    except ObjectDoesNotExist:
        raise CourseNotFoundException


def add_student_completed_lesson(student: User, lesson: Lessons):
    """
    Adds a student has completed a lesson.
    :param student: The Users object representing the student.
    :param lesson: The Lessons object representing the lesson.
    """
    add_user_completed_lesson(student, lesson)


def update_student_learning_styles(student: User, learning_styles: Iterable):
    """
    Given a list of learning styles will remove all student learning styles and update with the new ones.
    :param student: The User object representing the student.
    :param learning_styles: an iterable of LearningStyles objects.
    """
    # Delete existing settings.
    purge_user_userlearningstyles(student)
    # Populate the many to many relationship.
    add_to_user_userlearningstyles_collection(student, learning_styles)


def get_student_completed_lessons_sorted(student: User, course: Courses):
    """
    Get a sorted list of the student's completed lessons.
    :param student: The User object representing the student.
    :param course: The Courses object.
    :return: Returns a sorted set of the students completed lessons.
    """
    lessons = get_user_completed_lessons_sorted(student, course)
    if not Lessons:
        raise NoLessonsExistException
    return lessons

def delete_course_student_progress(course: Courses, student: User):
    """
    Deletes all a students progress for a course.
    :param course: The Courses object.
    :param student: The User object representing the student.
    """
    purge_user_course_progress(student, course)


def delete_all_student_progress(student):
    """
    Deletes all student progress.
    :param student: The User object representing the student.
    """
    purge_user_progress(student)


def has_student_completed_lesson(student: User, lesson: Lessons) -> bool:
    """
    Provided a student and a lesson will return whether the student has completed it.
    :param student: The User object representing the student.
    :param lesson: The Lessons object.
    :return: Returns whether the student has completed the course
    """

    return has_user_completed_lesson(student, lesson)


def has_student_completed_any_course_lessons(student: User, course: Courses):
    """
    Provided a student will return whether the student has completed any lessons.
    :param student: The User object representing the student.
    :param course: The Courses object.
    :return: Returns whether the student has completed any lessons of the course.
    """

    return has_user_completed_course_lessons(student, course)


def get_student_course_completion_percentages(student: User, courses) -> dict:
    """
    Provided a student will return the percentages of courses they have completed as a dictionary object
    :param student: The User object representing the student.
    :param courses: Th
    :return: Returns the students course completion percentages.
    """
    return get_user_course_completion_percentages(user=student, courses=courses)


def get_student_learning_styles(student: User) -> []:
    """
    Provided a student will return the student's LearningStyles.
    :param student: the User object representing the student.
    :return: Returns the students learning styles as a list.
    """
    learning_styles = get_user_learning_styles_from_user(student)
    if len(learning_styles) == 0:
        raise NoLearningStylesException
    return learning_styles
