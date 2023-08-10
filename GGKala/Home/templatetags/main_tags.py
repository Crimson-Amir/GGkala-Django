from django import template
from django.db.models import Count, Avg
from django.db.models.functions import Round

register = template.Library()


@register.simple_tag
def fa_number(number):
    farsi_num = {
        '0': '۰', '1': '۱', '2': '۲', '3': '۳', '4': '۴', '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹',
    }

    for a, b in farsi_num.items():
        number = str(number).replace(a, b)

    return number


@register.simple_tag
def rate_avg(objects, number):
    return


@register.inclusion_tag("Category/templatetage_star.html")
def rate_avg(objects, number, toys_score):
    diactiv_star = 5 - number
    avg = objects.annotate(res_off=Round(Avg('review__rate'))).filter(res_off=number).count()
    return {
        "number": number,
        "number_str": str(number),
        "number_range": range(number),
        "toys_score": toys_score,
        "diactiv_star": range(diactiv_star),
        "avg": avg
    }
