from django.contrib import admin

from .models import Schedule, Event


class EventInline(admin.StackedInline):
    model = Event
    extra = 0


@admin.register(Schedule)
class ScheduleModelAdmin(admin.ModelAdmin):
    inlines = [EventInline]


@admin.register(Event)
class EventModelAdmin(admin.ModelAdmin):
    pass