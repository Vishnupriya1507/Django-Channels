from django.contrib import admin

# Register your models here.
from .models import Room,Problem,Player

admin.site.register(Room)
admin.site.register(Problem)
admin.site.register(Player)