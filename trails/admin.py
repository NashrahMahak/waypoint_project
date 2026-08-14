from django.contrib import admin
from .models import Trail

@admin.register(Trail)
class TrailAdmin(admin.ModelAdmin):
    list_display = ('name', 'distance_km', 'elevation_gain', 'difficulty', 'is_open', 'added')
    list_filter = ('difficulty', 'is_open')
    search_fields = ('name',)
