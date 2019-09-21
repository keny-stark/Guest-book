from django.contrib import admin
from webapp.models import BookGuest


class ListAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'updated_at', 'created_at']


admin.site.register(BookGuest, ListAdmin)
