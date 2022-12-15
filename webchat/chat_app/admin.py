from django.contrib import admin
from django.contrib.auth.models import User

from.models import Room


class RoomUsersInline(admin.TabularInline):
    model = User
    extra = 1


class RoomAdmin(admin.ModelAdmin):
    fields = ['name', 'invite', 'users', 'owner']


admin.site.register(Room, RoomAdmin)
