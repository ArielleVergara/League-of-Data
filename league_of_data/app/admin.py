from django.contrib import admin
from .models import Summoner, Match, Graphic_data

# Register your models here.
admin.site.register(Summoner)
admin.site.register(Match)
admin.site.register(Graphic_data)

