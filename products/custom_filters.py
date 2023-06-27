from django import template

register = template.Library()

@register.filter
def has_extension(filename, extension):
    return filename.lower().endswith(extension.lower())
