from django import template

register = template.Library()

@register.filter
def truncate_with_dots(value, max_length=100):

    if len(value) > max_length:
        return value[:max_length - 3] + '...'
    return value
