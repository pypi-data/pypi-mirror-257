from django import template

register = template.Library()


@register.filter
def template_names(obj):
    template_names = ["django_action_logger/logentry.html"]
    if obj.content_type:
        template_names.append(
            f"django_action_logger/{obj.content_type.app_label}_logentry.html"
        )
        template_names.append(
            f"django_action_logger/{obj.content_type.app_label}.{obj.content_type.model}_logentry.html"
        )
    return template_names
