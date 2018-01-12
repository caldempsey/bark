from collections import Iterable

from django.contrib.auth.models import User

from courses.models import Lessons
from students_interfaces.exceptions.update_exceptions import InvalidUserLessonProgressRequestException
from students_interfaces.update.student_progress import sequential_update_lesson_complete, global_update_lesson_complete


def update_user_lesson_progress_protocols(student : User, learning_styles: Iterable,
                                          lesson: Lessons):
    # If there are special rules to follow for a learning style when marking a lesson as complete the functions for
    # that learning style should be added as functions and passed by the
    # execute_update_user_lesson_progress_protocols() method. One example where this is useful is to ensure
    # sequential users cannot complete lessons out of bounds of the last lesson they completed).

    # Invalid requests can be handled by the custom exception defined.
    # Define the protocols / rule-sets. Each of these will be executed in turn.
    # Flag to indicate whether statements have been executed (so we know whether to execute the default ruleset).
    statements_executed = False
    for learning_style in learning_styles:
        # Define arguments here
        if learning_style.name == "Sequential":
            sequential_update_lesson_complete(student, lesson=lesson)
            statements_executed = True
        if learning_style.name == "Global":
            global_update_lesson_complete(student, lesson=lesson)
            statements_executed = True
    # If no protocols are executed then the system is not apt to handle the data.
    if not statements_executed:
        raise InvalidUserLessonProgressRequestException
