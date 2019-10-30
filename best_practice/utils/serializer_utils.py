from rest_framework import serializers
from .error_utils import Error, ErrorSpec, APIException


class BaseSerializer(serializers.BaseSerializer):
    def is_valid(self, raise_exception=False):
        is_valid = super(BaseSerializer, self).is_valid(raise_exception=False)
        if not raise_exception or is_valid:
            return is_valid

        custom_errors = list()
        validation_specs = ErrorSpec.specs[400]
        for field_name, obj in self.fields.items():
            custom_errors.extend(
                [Error(code=validation_specs["code"],
                       type=validation_specs["type"],
                       sub_type=error.code, parameter=dict(name=field_name, **obj._kwargs),
                       message=str(error))
                 for error in self.errors.get(field_name, list())])
        raise APIException(errors=custom_errors, status_code=validation_specs["status_code"])