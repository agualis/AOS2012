from django import template
register = template.Library()

@register.filter
def index(value, arg1):
    if value:
        return value[arg1]
    else:
        return ""
    