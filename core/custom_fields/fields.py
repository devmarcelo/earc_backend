# core/serializes/fields.py
from rest_framework import serializers

class FileOrUrlField(serializers.Field):
    """
    Campo DRF customizado que aceita um arquivo (upload) OU uma string (URL).
    Use como Field em Serializers, inclusive com ModelSerializer (sobrescreva o field).
    """
    def __init__(self, *args, allowed_types=None, **kwargs):
        self.allowed_types = allowed_types or []
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        # Aceita arquivo ou string
        if hasattr(data, "read"):  # Arquivo tipo InMemoryUploadedFile
            if self.allowed_types and hasattr(data, "content_type"):
                if data.content_type not in self.allowed_types:
                    raise serializers.ValidationError(f"Tipo de arquivo não suportado: {data.content_type}")
            return data
        elif isinstance(data, str):
            # Opcional: pode validar se é URL
            if data and not (data.startswith("http://") or data.startswith("https://") or data.startswith("/")):
                raise serializers.ValidationError("Informe uma URL válida ou realize o upload de um arquivo.")
            return data
        elif data is None or data == "":
            return None
        raise serializers.ValidationError("Campo deve ser um arquivo ou uma URL válida.")

    def to_representation(self, value):
        return str(value) if value else ""
