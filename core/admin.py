from django import forms
from django.contrib import admin
from django.utils.html import format_html
from .models import *


class SportsCenterSportInline(admin.TabularInline):
    """Sports in a Sports center"""
    extra = 1
    model = SportsCenterSport


class SportsCenterMediaInline(admin.TabularInline):
    """Media inside sports center admin"""
    extra = 3
    model = SportsCenterMedia
    fields = ('url', 'order')


@admin.register(SportsCenter)
class SportsCenterAdmin(admin.ModelAdmin):
    """Sports center"""
    description = forms.CharField(widget=forms.Textarea)
    inlines = [SportsCenterMediaInline, SportsCenterSportInline]
    list_display = ('name', 'active', 'location', 'has_email')
    search_fields = ('name',)
    # list_per_page = 50

    def has_email(self, obj):
        if obj.email is '':
            return format_html('<img src="/static/admin/img/icon-no.svg" alt="False">')
        else:
            return format_html('<img src="/static/admin/img/icon-yes.svg" alt="True">')


admin.site.register(Owner)
admin.site.register(Location)
admin.site.register(Sport)
admin.site.register(Court)
admin.site.register(Surface)
admin.site.register(BlockedDate)
admin.site.register(Booking)
