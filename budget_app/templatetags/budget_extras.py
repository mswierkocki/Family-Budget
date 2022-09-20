from django import template
from django.template.defaultfilters import stringfilter

from budget_app.models import CURRENCY_SIGN

register = template.Library()


@register.filter
@stringfilter
def currency(value):
    return "{}{}".format(value, CURRENCY_SIGN)


@register.filter
def subtract(value, arg):
    value
    return value - arg
