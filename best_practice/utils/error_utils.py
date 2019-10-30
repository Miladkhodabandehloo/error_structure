from rest_framework.exceptions import APIException as DRFAPIException
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.exceptions import ErrorDetail


class Error:
    def __init__(self, code=None, type=None, sub_type=None,
                 parameter=None, message=None):
        self.code = code
        self.sub_type = sub_type
        self.type = type
        if parameter is not None and "choices" in parameter.keys():
            parameter["choices"] = [choice[0] for choice in parameter["choices"]]
        self.parameter = parameter
        self.message = message

    @classmethod
    def make_by_code(cls, code, message=None, sub_type=None):
        specs = ErrorSpec.specs[code]
        return cls(
            code=specs.get("code"),
            type=specs.get("type"),
            message=message or specs.get("message"),
            sub_type=sub_type or specs.get("sub_type")
        )

    @classmethod
    def authorization_error(cls):
        return cls.make_by_code(code=403)

    @classmethod
    def authentication(cls):
        return cls.make_by_code(code=401)

    @property
    def pretty(self):
        return self.__dict__


class ErrorSpec:
    specs = {
        400: {"code": 400, "status_code": 400, "type": "ValidationError", "message": None},
        403: {"code": 403, "status_code": 403, "type": "AuthorizationError", "message": "Access Denied."},
        401: {"code": 401, "status_code": 401, "type": "AuthenticationError",
              "message": "Authentication Failed."},
        500: {"code": 500, "status_code": 500, "type": "UnknownInternalError", "message": "Unknown Error Occurred."}
    }


def custom_exception_handler(exc, context):
    response = exception_handler(exc=exc, context=context)

    custom_errors = list()
    if hasattr(exc, "fields") and hasattr(exc, "form_errors"):
        validation_specs = ErrorSpec.specs[400]
        for field_name, obj in exc.fields.items():
            custom_errors.append(Error(code=validation_specs["code"],
                                       type=validation_specs["type"],
                                       sub_type=error.code, parameter=dict(name=field_name, **obj._kwargs),
                                       message=str(error)).pretty
                                 for error in exc.form_errors.get(field_name, list()))
        response.data = custom_errors
        return response

    if isinstance(exc.detail, ErrorDetail):
        message = exc.detail
        sub_type = exc.detail.code
    else:
        message = None
        sub_type = None

    if response.status_code and response.status_code in ErrorSpec.specs.keys():
        custom_errors.append(Error.make_by_code(code=response.status_code,
                                                message=message,
                                                sub_type=sub_type).pretty)
    else:
        custom_errors.append(Error.make_by_code(code=500).pretty)

    response.data = custom_errors
    return response
