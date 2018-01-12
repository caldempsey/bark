from collections import Iterable

from django.template import TemplateDoesNotExist

from students_interfaces.generator.template_contexts import learning_styles_templates


def get_learning_styles_template(learning_styles: Iterable) -> str:
    """
    Returns the template for a specific learning style based on the dict object in template_contexts.
    :param learning_styles:
    :return:
    """
    template = ""
    for learning_style in learning_styles:
        # Get the appropriate learning styles template.
        if learning_style.name in learning_styles_templates:
            template = learning_styles_templates.get(learning_style.name)
    if template == "":
        raise TemplateDoesNotExist
    return template
