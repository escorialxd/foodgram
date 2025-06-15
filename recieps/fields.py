import base64
import uuid

from django.core.files.base import ContentFile
from rest_framework import serializers


class Base64ImageField(serializers.ImageField):
    """Кастомное поле для работы с изображениями в формате base64."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]
            data = ContentFile(
                base64.b64decode(imgstr), name=f"{uuid.uuid4()}.{ext}"
            )
        return super().to_internal_value(data)

    def to_representation(self, value):
        if not value:
            return None
        try:
            with value.open("rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode(
                    "utf-8"
                )
                file_type = value.name.split('.')[-1]
                return f"data:image/{file_type};base64,{encoded_string}"
        except Exception:
            return None
