from django import template
import math

register = template.Library()


@register.inclusion_tag("Products/temtag/ratings-templatetags.html")
def ratings_show(objects):
    return {
        "object": objects.rate
    }


@register.inclusion_tag("Products/temtag/ratings-templatetags-ltr.html")
def average_rate(objects, direction="ltr", star_width=None):
    try:
        num = 0
        sums = 0
        for i in objects:
            num += 1
            sums += i.rate
        objects = math.floor((sums / num) + 0.5)
        return {
            "object": objects,
            "dire": direction,
            "star_width": star_width
        }
    except ZeroDivisionError:
        return {
            "object": 1,
            "dire": direction,
            "star_width": star_width
        }
