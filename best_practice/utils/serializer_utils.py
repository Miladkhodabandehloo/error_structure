from rest_framework import serializers
from rest_framework.serializers import ValidationError


class DRFSerializer(serializers.Serializer):
    def is_valid(self, raise_exception=False):
        try:
            super(DRFSerializer, self).is_valid(raise_exception=raise_exception)
        except ValidationError as exc:
            exc.form_errors = self.errors
            exc.form_data = self.data
            raise exc


class DRFModelSerializer(serializers.ModelSerializer, DRFSerializer):
    pass
