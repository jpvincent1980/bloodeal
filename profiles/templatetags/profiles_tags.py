from django import template

register = template.Library()


@register.filter
def get_obj_attr(obj, attr):
    return getattr(obj, attr)


@register.filter
def get_obj_class(obj):
    return obj.__class__.__name__
