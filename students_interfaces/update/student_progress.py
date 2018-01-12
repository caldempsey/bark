from django.contrib.auth.models import User

from communicate.students import has_next_lesson, get_next_lesson
from communicate.students import has_student_completed_lesson, get_student_completed_lessons_sorted, \
    has_student_completed_any_course_lessons, add_student_completed_lesson
from courses.models import Lessons
from students_interfaces.exceptions.update_exceptions import InvalidUserLessonProgressRequestException


def sequential_update_lesson_complete(student: User, lesson: Lessons):
    # If the lesson is already complete then do nothing.
    if has_student_completed_lesson(student, lesson):
        return True

    # Otherwise validate that this is the next lesson in their sequence (if one exists). If it is not then throw an
    # error, likely that someone is trying to abuse POST).
    else:
        # Get the save data for the user sorted by sequence number (a QuerySet of UserLessonsCompleted objects
        # indicating which lessons are completed).
        lesson_save_data = get_student_completed_lessons_sorted(student,
                                                                lesson.course)
        # Since our queryset has defined ordering we can use the reverse method to get the last item in the set.
        # https://docs.djangoproject.com/en/dev/ref/models/querysets/#reverse.

        # If the user has completed lessons in the past from the course the lesson is on, then get the last completed
        #  lesson from the users save data as a lesson object. If the next lesson exists we need to check that this
        # lesson is the one the user is trying to mark as complete.
        if has_student_completed_any_course_lessons(student, lesson.course):
            last_completed_lesson = lesson_save_data.reverse()[0].lesson
            if has_next_lesson(last_completed_lesson):
                next_lesson = get_next_lesson(last_completed_lesson)
                # Succeeding this we can create the save data (the == operator checks object's for logical
                # equivalence).
                if next_lesson == lesson:
                    add_student_completed_lesson(student, lesson)
                    return True
                # If the course has the next lesson but this is not the lesson we are trying to mark completed then
                # raise the custom InvalidUserLessonProgressRequestException exception (handled by the except clause
                # of the calling statement).
                else:
                    raise InvalidUserLessonProgressRequestException()
        else:
            # If the user has not completed a lesson on the specified course before then check the lessons sequence
            # number is equal to 1. If they have not completed a course lesson before then raise the custom
            # InvalidUserLessonProgressRequestException exception (handled by the except clause of the calling
            # statement).
            if lesson.sequence_number == 1:
                add_student_completed_lesson(student, lesson)
            else:
                raise InvalidUserLessonProgressRequestException()


def global_update_lesson_complete(student: User, lesson: Lessons):
    if has_student_completed_lesson(student, lesson):
        return True
    else:
        add_student_completed_lesson(student, lesson)
        return True
