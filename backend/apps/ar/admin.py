# backend/apps/ar/admin.py
from django.contrib import admin
from .models import ARScene, ARObject

@admin.register(ARScene)
class ARSceneAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude', 'created_at')
    search_fields = ('name', 'description')

@admin.register(ARObject)
class ARObjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'scene', 'offset_x', 'offset_y', 'offset_z')
    list_filter = ('scene',)
    search_fields = ('name', 'info')