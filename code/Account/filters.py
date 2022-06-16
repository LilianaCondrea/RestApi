from datetime import datetime, date, timedelta
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class AgeStatusListFilter(admin.SimpleListFilter):
    title = 'Age'
    parameter_name = 'age'

    def lookups(self, request, model_admin):
        return (
            ('-1999', _('Born below 1999s')),
            ('+2000', _('Born above 1999s')),
        )

    def queryset(self, request, queryset):
        if self.value() == '-1999':
            return queryset.filter(
                date_of_birth__lte=date(1999, 12, 31)
            )
        if self.value() == '+2000':
            return queryset.filter(
                date_of_birth__gte=date(2000, 1, 1)
            )


class UpdateStatusListFilter(admin.SimpleListFilter):
    title = 'Updates'
    parameter_name = 'u'

    def lookups(self, request, model_admin):
        return (
            ('1', _('Last 24 hours')),
            ('7', _('Past 7 days')),
            ('30', _('This month')),
            ('365', _('This year')),
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(
                last_update__gte=datetime.now() - timedelta(days=1),
                last_update__lte=datetime.now()
            )
        if self.value() == '7':
            return queryset.filter(
                last_update__gte=datetime.now() - timedelta(days=7),
                last_update__lte=datetime.now()
            )
        if self.value() == '30':
            return queryset.filter(
                last_update__gte=datetime.now() - timedelta(days=30),
                last_update__lte=datetime.now()
            )
        if self.value() == '365':
            return queryset.filter(
                last_update__gte=datetime.now() - timedelta(days=365),
                last_update__lte=datetime.now()
            )
