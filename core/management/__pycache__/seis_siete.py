import os
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "6... 7!"

    def handle(self, *args, **options):
        ruta = os.path.join(settings.BASE_DIR, "static", "audio", "profesora-67.mp3")

        if not os.path.exists(ruta):
            self.stderr.write(f"No encuentro el audio en: {ruta}")
            return

        self.stdout.write("🎵 6... 7!")
        os.startfile(ruta)  # abre el archivo con tu reproductor por defecto (Windows)