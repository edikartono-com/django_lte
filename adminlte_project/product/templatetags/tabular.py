from django import template
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.utils.safestring import mark_safe


register = template.Library()

