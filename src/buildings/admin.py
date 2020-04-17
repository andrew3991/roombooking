from django.contrib import admin
from .models import Building, Room, Interval, RoomFeature


class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'room_number', 'building', 'capacity', 'beamer', 'board')
    list_editable = ('beamer', 'board')
    list_display_links = ('id', 'room_number')
    list_filter = ('building',)
    search_fields = ('room_number', 'capacity', 'description',)


admin.site.register(Building)
admin.site.register(Room, RoomAdmin)
admin.site.register(Interval)
admin.site.register(RoomFeature)
