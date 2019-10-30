from rest_framework.exceptions import APIException as DRFAPIException
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.exceptions import ErrorDetail


class APIException(DRFAPIException):
    def __init__(self, errors, status_code=400):
        self.status_code = status_code
        self.detail = {"errors": [error.__dict__ for error in errors]}

    @property
    def response(self):
        return Response(data=self.detail, status=self.status_code)

    @staticmethod
    def make_api_exception_by_code(code, message=None, sub_type=None):
        specs = ErrorSpec.specs[code]
        return APIException(status_code=specs["status_code"], errors=[
            Error(
                code=specs.get("code"),
                type=specs.get("type"),
                message=message or specs.get("message"),
                sub_type=sub_type or specs.get("sub_type"))
        ])

    @staticmethod
    def authorization_exception():
        return APIException.make_api_exception_by_code(code=403)

    @staticmethod
    def authentication():
        return APIException.make_api_exception_by_code(code=401)


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
    if isinstance(exc.detail, ErrorDetail):
        message = exc.detail
        sub_type = exc.detail.code
    elif isinstance(exc.detail, dict):
        message = exc.detail.get("detail")
        sub_type = exc.detail.get("code")
    else:
        message = None
        sub_type = None
    if response.status_code and response.status_code in ErrorSpec.specs.keys():
        return APIException.make_api_exception_by_code(
            code=response.status_code,
            message=message,
            sub_type=sub_type
        ).response if not isinstance(exc, APIException) else response
    else:
        return APIException.make_api_exception_by_code(code=500).response




