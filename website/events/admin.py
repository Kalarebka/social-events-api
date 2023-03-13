from django.contrib import admin

from .models import Event, Location


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "latitude",
        "longitude",
        "country",
        "city",
        "street",
        "street_number",
        "zip_code",
    )


class EventAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "event_type",
        "status",
        "start_time",
        "end_time",
        "location",
    )
    list_filter = ("event_type", "status")


admin.site.register(Location, LocationAdmin)
admin.site.register(Event, EventAdmin)
