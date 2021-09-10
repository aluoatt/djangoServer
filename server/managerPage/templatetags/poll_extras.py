from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def getdimName(obj,number):

    return obj.filter(amwayNumber=int(number)).first().main