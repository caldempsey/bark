from django.contrib.auth.models import User

from courses.models import Courses
from students_interfaces.exceptions.context_exceptions import UndefinedContextException
from students_interfaces.generator.template_contexts import courses_lessons_sequential_template, \
    courses_lessons_global_template, sequential_template_context, global_template_context


def generate_template_context(template: str, user: User, course: Courses):
    """
    Generates a template context based on the rule-set defined in template contexts.
    :param template: The template to get the context for.
    :param user: The student.
    :param course: The course to generate the context for.
    :return: Returns the context as a dictionary object.
    """
    context = {}
    context_set = False

    # Your context arguments here.
    # If the template is the courses lessons sequential template, then replace the
    # context with the context appropriated. Logic to get the context for each template should be placed in
    # "template_contexts.py".

    if template == courses_lessons_sequential_template:
        context = sequential_template_context(user, course)
        context_set = True
    if template == courses_lessons_global_template:
        context = global_template_context(user, course)
        context_set = True
    # You must provide a context or specify exceptions to the rule using the context_set argument.
    if not context_set:
        raise UndefinedContextException
    return context
