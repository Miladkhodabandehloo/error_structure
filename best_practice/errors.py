from rest_framework.exceptions import APIException as DRFAPIException
from rest_framework.views import exception_handler
from rest_framework.response import Response


class APIException(DRFAPIException):
    def __init__(self, errors, status_code=400):
        self.status_code = status_code
        self.detail = {"errors": [error.__dict__ for error in errors]}

    @property
    def response(self):
        return Response(data=self.detail, status=self.status_code)

    @staticmethod
    def authorization():
        authorization_specs = ErrorSpec.specs["authorization"]
        return APIException(status_code=authorization_specs["status_code"], errors=[
            Error(code=authorization_specs["code"], type=authorization_specs["type"],
                  message=authorization_specs["message"])])

    @staticmethod
    def authentication():
        authentication_specs = ErrorSpec.specs["authentication"]
        return APIException(status_code=authentication_specs["status_code"], errors=[
            Error(code=authentication_specs["code"], type=authentication_specs["type"],
                  message=authentication_specs["message"])])


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
        "validation": {"code": 400, "status_code": 400, "type": "ValidationError", "message": None},
        "authorization": {"code": 403, "status_code": 403, "type": "AuthorizationError", "message": "Access Denied."},
        "authentication": {"code": 401, "status_code": 401, "type": "AuthenticationError",
                           "message": "Not Authenticated."}
    }


def custom_exception_handler(exc, context):
    response = exception_handler(exc=exc, context=context)
    if response.status_code == 401:
        return APIException.authentication().response
    if response.status_code == 403:
        return APIException.authorization().response
    return response
