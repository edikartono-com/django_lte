from django.template import Library
from django.contrib.admin.templatetags.admin_list import result_list
from django.contrib.admin.templatetags.base import InclusionAdminNode
from django.contrib.admin.views.main import (
    ALL_VAR, PAGE_VAR,
)
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.text import slugify

register = Library()

@register.tag(name='custom_result_list')
def result_list_tag(parser, token):
    return InclusionAdminNode(
        parser, token,
        func=result_list,
        template_name='custom_change_list_results.html',
        takes_context=False,
    )

@register.simple_tag
def str_slug(value):
    s = slugify(value)
    return s

@register.simple_tag
def paginator_number(cl, i):
    """
    Generate an individual page index link in a paginated list.
    """
    if i == cl.paginator.ELLIPSIS:
        return format_html(
            f'''
            <li class="page-item disabled" aria-current="page">
            <a class="page-link" href="#">{cl.paginator.ELLIPSIS}</a>
            </li>
            '''
        )
    elif i == cl.page_num:
        return format_html(
            f'''
            <li class="page-item active" aria-current="page">
            <a class="page-link" href="#">{i}</a> 
            </li>
            '''
        )
    else:
        return format_html(
            '<li class="page-item"><a class="page-link" href="{}"{}>{}</a></li>',
            cl.get_query_string({PAGE_VAR: i}),
            mark_safe(' class="end"' if i == cl.paginator.num_pages else ''),
            i,
        )


def pagination(cl):
    """
    Generate the series of links to the pages in a paginated list.
    """
    pagination_required = (not cl.show_all or not cl.can_show_all) and cl.multi_page
    page_range = cl.paginator.get_elided_page_range(cl.page_num) if pagination_required else []
    need_show_all_link = cl.can_show_all and not cl.show_all and cl.multi_page
    return {
        'cl': cl,
        'pagination_required': pagination_required,
        'show_all_url': need_show_all_link and cl.get_query_string({ALL_VAR: ''}),
        'page_range': page_range,
        'ALL_VAR': ALL_VAR,
        '1': 1,
    }


@register.tag(name='pagination')
def pagination_tag(parser, token):
    return InclusionAdminNode(
        parser, token,
        func=pagination,
        template_name='pagination.html',
        takes_context=False,
    )

@register.tag(name='object_tools')
def change_list_object_tools_tag(parser, token):
    """Display the row of change list object tools."""
    return InclusionAdminNode(
        parser, token,
        func=lambda context: context,
        template_name='includes/object_tools.html',
    )