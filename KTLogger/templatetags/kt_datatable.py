import json

from django import template

register = template.Library()

DATATABLES_LOCALES = {
    "en": "https://cdn.datatables.net/plug-ins/1.12.1/i18n/en-GB.json",
    "default": "https://cdn.datatables.net/plug-ins/1.12.1/i18n/en-GB.json"
}


@register.inclusion_tag('KTLogger/includes/datatables/view_utils.html', takes_context=True)
def render_datatable_view_utils(context: template.Context, table_html_id: str, table_ajax_url: str, table_setup: dict,
                                **kwargs):
    request = context.get('request', None)

    if 'language' not in table_setup:
        try:
            table_setup["language"] = {"url": DATATABLES_LOCALES[request.LANGUAGE_CODE]}
        except AttributeError:
            table_setup["language"] = {"url": DATATABLES_LOCALES["default"]}

    return {
        'table_html_id': table_html_id,
        'table_ajax_url': table_ajax_url,
        'table_setup': json.dumps(table_setup),
        'table_additional_data': json.dumps(dict(**kwargs))
    }


@register.simple_tag
def kwargs_to_dict(**kwargs) -> dict:
    return dict(**kwargs)
