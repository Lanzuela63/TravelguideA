#apps/ar/management/commands/seed_ar_data.py

from django.core.files import File
from django.core.management.base import BaseCommand
from apps.ar.models import ARScene
import os

class Command(BaseCommand):
    help = 'Seed ARScene data for testing'

    def handle(self, *args, **kwargs):
        base_path = os.path.join('media', 'ar')  # adjust if needed

        scenes = [
            {
                "name": "Mayon Volcano",
                "latitude": 13.2575,
                "longitude": 123.6856,
                "marker_image_path": os.path.join(base_path, "markers", "mayon.patt"),
                "model_path": os.path.join(base_path, "models", "mayon.glb"),
                "info_html": "<h1>Mayon Volcano</h1><p>Perfect cone shape.</p>",
            },
        ]

        for data in scenes:
            with open(data["marker_image_path"], "rb") as m_img:
                marker_file = File(m_img, name=os.path.basename(data["marker_image_path"]))

                if os.path.exists(data["model_path"]):
                    with open(data["model_path"], "rb") as mdl:
                        model_file = File(mdl, name=os.path.basename(data["model_path"]))
                    scene, created = ARScene.objects.get_or_create(
                        title=data["title"],
                        latitude=data["latitude"],
                        longitude=data["longitude"],
                        info_html=data["info_html"],
                        defaults={
                            "marker_image": marker_file,
                            "model_url": model_file,
                        }
                    )
                else:
                    scene, created = ARScene.objects.get_or_create(
                        title=data["title"],
                        latitude=data["latitude"],
                        longitude=data["longitude"],
                        info_html=data["info_html"],
                        defaults={
                            "marker_image": marker_file,
                        }
                    )

        self.stdout.write(self.style.SUCCESS("ARScene data seeded successfully."))

