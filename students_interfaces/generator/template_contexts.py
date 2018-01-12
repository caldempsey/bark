from django.contrib.auth.models import User

from communicate.students import has_next_lesson, get_next_lesson, \
    get_first_lesson_in_course
from communicate.students import has_student_completed_any_course_lessons, \
    get_student_completed_lessons_sorted
from courses.models import Courses

# Templates
courses_lessons_global_template = "students/courses_lessons_global.html"
courses_lessons_sequential_template = "students/courses_lessons_sequential.html"
# Template Learning Style
learning_styles_templates = {
    "Global": courses_lessons_global_template,
    "Sequential": courses_lessons_sequential_template,
}


# Arguments to interface the Template Context

def sequential_template_context(user: User, course: Courses):
    """
    Defines the sequential template context ruleset.
    :param user:
    :param course:
    :return:
    """

    context = {}
    if has_student_completed_any_course_lessons(user, course):
        # Get the completed lessons data for the user sorted by sequence number (a QuerySet of UserLessonsCompleted
        # objects indicating which lessons are completed).
        user_completed_lessons = get_student_completed_lessons_sorted(user,
                                                                      course)
        # Update the context with completed lessons data
        context.update({"user_completed_lessons": user_completed_lessons})
        # Since our queryset has defined ordering we can use the reverse method to get the last item in the set.
        # https://docs.djangoproject.com/en/dev/ref/models/querysets/#reverse.

        # Get the last completed lesson from the users save data as a lesson object.
        last_completed_lesson = user_completed_lessons.reverse()[0].lesson

        # Get the users next lesson and append it to the context only if one exists.
        if has_next_lesson(last_completed_lesson):
            next_lesson = get_next_lesson(last_completed_lesson)
            context.update(
                {"next_lesson": next_lesson})
        return context
    # If otherwise the user has not completed any lessons in the course then get the courses first lesson (will raise
    #  an exception if a course cannot be found).
    next_lesson = get_first_lesson_in_course(course)
    context.update(
        {"next_lesson": next_lesson})
    return context


def global_template_context(user: User, course: Courses):
    """
    Defines the global template context ruleset.

    :param user:
    :param course:
    :return:
    """
    # Return completed lessons
    context = {}
    user_completed_lessons = get_student_completed_lessons_sorted(user, course)
    lessons_completed_tuples = []
    for lesson in course.lessons_set.all():
        if user_completed_lessons.filter(lesson=lesson).exists():
            lesson_completed_tuple = (lesson, True)
        else:
            lesson_completed_tuple = (lesson, False)
        lessons_completed_tuples.append(lesson_completed_tuple)
    context.update({"lessons_completed_tuples": lessons_completed_tuples})
    return context
