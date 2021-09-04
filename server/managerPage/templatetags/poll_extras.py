from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def getdimName(obj,number):
    print(number)
    print(obj)
    return obj.filter(amwayNumber=int(number)).first().main