from django.contrib import admin
from django.utils.safestring import mark_safe
from django.db.models.functions import Trunc, TruncMonth, TruncDay, TruncYear
# Local imports
from githubUsers.models import *


@admin.register(UserDetail)
class UserDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'login', 'avatar_image', 'db_entry_creation_date',)
    readonly_fields = ["avatar_image"]
    list_filter = ('email','db_entry_creation_date','type','public_repos','created_at','location','followers')

    def avatar_image(self, obj):
        """
        If user image url is present, it displays the user image in Admin panel.
        """
        if obj.avatar_url:
            return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
                url=obj.avatar_url,
                width=100,
                height=100,
            )
            )
        else:
            return ''


@admin.register(UserSummary)
class UserSummaryAdmin(admin.ModelAdmin):
    """
    It creates a report in admin panel about the number of users added in database in a day, month and year.
    """
    change_list_template = 'admin/user_track_list.html'
    date_hierarchy = 'db_entry_creation_date'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response
        response.context_data['summary'] = list(qs.annotate(period=TruncMonth('db_entry_creation_date')).values('period').annotate(idCount=Count('id')).order_by())
        return response


@admin.register(ApiUsageSummary)
class ApiUsageSummaryAdmin(admin.ModelAdmin):
    """
    It creates a report in admin panel about the count of user-search API usage in a day, month and year.
    """
    change_list_template = 'admin/api_track_list.html'
    date_hierarchy = 'api_usage_date'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        response.context_data['summary'] = list(qs.annotate(period=TruncMonth('api_usage_date')).values('period').annotate(hitCount=Count('search_entry')).order_by())
        return response
