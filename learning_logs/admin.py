from django.contrib import admin

from . import models


@admin.register(models.Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("title", "date_added", "public", "owner")
    list_filter = ("public", "date_added")
    search_fields = ("title", "content")
    ordering = ("-date_added",)


@admin.register(models.Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ("content", "date_added", "topic")
    list_filter = (
        "topic",
        "date_added",
    )
    search_fields = ("content",)
    ordering = ("-date_added",)
