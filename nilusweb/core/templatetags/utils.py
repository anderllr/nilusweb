from django.template import Library

register = Library()


@register.filter
def format_int(value):
    return '%.2d' %value
