import json

from django import forms, template
from django.db.models import Model
from django.template import RequestContext
from django.templatetags.static import static
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def dfv_script():
    return format_html(
        '<script type="text/javascript" defer src="{}"></script>',
        static("../static/dfv.js"),
    )


@register.simple_tag
def hyperpony_behavior_form_state():
    return mark_safe(
        """
        <script type="text/hyperscript">
            behavior FormState
                def form_state()
                    send form_state(state:me as Values)
                end
                init form_state()
                then on input form_state()
            end
        </script>
        """
    )


@register.simple_tag
def hyperpony_script_swap_merge():
    return format_html(
        '<script type="text/javascript" defer src="{}"></script>',
        static("../static/dfv_swap_merge.js"),
    )


def _args_kwargs_to_json_dict(context: RequestContext, args, kwargs):
    for a in args:
        if isinstance(a, Model):
            a = model_to_dict(a)
        if not isinstance(a, dict):
            raise ValueError(
                f"{context.template_name}: positional arguments must be dicts or Django models"
            )
        kwargs = {**a, **kwargs}

    return json.dumps(kwargs)


@register.simple_tag(takes_context=True)
def hx_vals(context: RequestContext, *args, **kwargs):
    j = _args_kwargs_to_json_dict(context, args, kwargs)
    attr = f" hx-vals='{j}' "
    return mark_safe(attr)


@register.filter
def model_to_dict(model):
    return forms.model_to_dict(model)


@register.filter
def to_str(model):
    return str(model)
