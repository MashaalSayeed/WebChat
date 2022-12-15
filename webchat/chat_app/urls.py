from django.urls import path, re_path

from . import views

app_name= 'chat_app'
urlpatterns = [
    # Main home page
    path('', views.index, name='index'),

    # User profile
    path('chat/profile', views.profile, name='profile'),

    # Default view upon login, lists all rooms
    path('chat/room/', views.chat_default, name='chat_default'),

    path('chat/new', views.new_chat, name='new_chat'),

    # For viewing an existing chat room
    re_path(r'chat/room/(?P<invite>[A-Z|\d]{8})/$', views.chat, name='chat'),
]
