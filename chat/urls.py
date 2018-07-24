from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^create_room/$', views.create_room,name = 'create_room'),
    url(r'^$', views.index, name='index'),
    url(r'^(?P<room_name>[^/]+)/$', views.room, name='room'),
    #url(r'^login/$', views.login,name = 'login'),
    url(r'^logout/$', views.logout,name = 'logout'),                # FOR CHECKING DJANGO PROJECT
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


