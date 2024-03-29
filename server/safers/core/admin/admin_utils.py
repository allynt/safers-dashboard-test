from django.urls import reverse
from django.utils.html import format_html

from django.utils.translation import gettext_lazy as _

####################
# list_display fns #
####################


def get_clickable_m2m_for_list_display(model_class, queryset):
    """
    Prints a pretty (clickable) representation of a m2m field for an Admin's `list_display`.
    Note that when using this it is recommended to call `prefetch_related` in the Admin's
    `get_queryset` fn in order to avoid the "n+1" problem.
    """
    admin_change_url_name = f"admin:{model_class._meta.db_table}_change"
    list_display = [
        f"<a href='{reverse(admin_change_url_name, args=[obj.id])}'>{str(obj)}</a>"
        for obj in queryset
    ]
    return format_html(", ".join(list_display))


def get_clickable_fk_for_list_display(obj):
    """
    Prints a pretty (clickable) representation of a fk field for an Admin's `list_display`.
    """
    model_class = type(obj)
    admin_change_url_name = f"admin:{model_class._meta.db_table}_change"
    list_display = f"<a href='{reverse(admin_change_url_name, args=[obj.pk])}'>{str(obj)}</a>"
    return format_html(list_display)
