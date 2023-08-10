from django import template

register = template.Library()


@register.inclusion_tag("registration/tags/select_meno.html")
def link(request, link_name, content, classes):
    return {
        "request": request,
        "link_name": link_name,
        "link": "account:{0}".format(link_name),
        "content": content,
        "classes": classes
    }
