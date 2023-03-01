from django import template


register = template.Library()

@register.filter(name='zip')
def zip_filter(a,b):
    return zip(a, b)

@register.filter(name='split')
def str_split(text):
    return text.split('img')