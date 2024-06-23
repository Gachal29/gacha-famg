import json

from django import template
from django.db.models.query import QuerySet
from django.core.serializers import serialize
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter("jsonify")
def jsonify(obj):
    """オブジェクトをJSON化するDjangoテンプレートフィルタ
    """
    if isinstance(obj, QuerySet):
        return mark_safe(serialize('json', obj))
    return mark_safe(json.dumps(obj))
