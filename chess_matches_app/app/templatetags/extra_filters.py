from django import template

register = template.Library()

def modulo(arg1, arg2):
    return arg1%arg2

register.filter('modulo', modulo)