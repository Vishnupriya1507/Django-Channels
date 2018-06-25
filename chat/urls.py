from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^create_room/$', views.create_room,name = 'create_room'),
    #url(r'^join_room/$', views.join_room,name = 'join_room'),
    url(r'^$', views.index, name='index'),
    url(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),
]
