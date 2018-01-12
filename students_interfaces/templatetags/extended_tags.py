# Custom template tag to accomodate a lack of dictionary support for Django templates (see ticket
# https://code.djangoproject.com/ticket/3371) Custom template tag solution sourced from
# https://stackoverflow.com/questions/8000022/django-template-how-to-look-up-a-dictionary-value-with-a-variable
# Installation instructions as to how to register a custom filter can be found here
# https://docs.djangoproject.com/en/1.10/howto/custom-template-tags/#code-layout
from django.template.defaulttags import register


@register.filter()
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def equal_to_zero(arg):
    return arg == 0
