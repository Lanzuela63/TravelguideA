# backend/apps/ar/models.py
from django.db import models

class ARScene(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    model_file = models.FileField(upload_to='ar/models/', null=True, blank=True)
    marker_image = models.ImageField(upload_to='ar/markers/', blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ARObject(models.Model):
    scene = models.ForeignKey(ARScene, on_delete=models.CASCADE, related_name='objects')
    name = models.CharField(max_length=100)
    info = models.TextField(blank=True)
    image = models.ImageField(upload_to='ar/objects/', blank=True, null=True)
    offset_x = models.FloatField(default=0)
    offset_y = models.FloatField(default=0)
    offset_z = models.FloatField(default=0)
    description = models.TextField(blank=True)
    objects = models.Manager()

    def __str__(self):
       return self.name
