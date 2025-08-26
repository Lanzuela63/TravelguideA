from rest_framework import serializers
from .models import  ARScene, ARObject

class ARObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ARObject
        fields = ["id", "name", "info", "image", "offset_x", "offset_y", "offset_z"]


class ARSceneSerializer(serializers.ModelSerializer):
    marker_image = serializers.SerializerMethodField()
    model_url = serializers.SerializerMethodField()

    class Meta:
        model = ARScene
        fields = ["id", "name", "description", "latitude", "longitude", "marker_image", "model_url"]

    def get_marker_image(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.marker_image.url) if obj.marker_image else None

    def get_model_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.model_url.url) if obj.model_url else None
