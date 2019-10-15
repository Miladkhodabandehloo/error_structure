from rest_framework.exceptions import APIException as DRFAPIException


class APIException(DRFAPIException):
    def __init__(self, errors, status_code=400):
        self.status_code = status_code
        self.detail = {"errors": [error.__dict__ for error in errors]}

    @staticmethod
    def authorization():
        authorization_specs = ErrorSpec.specs["authorization"]
        return APIException(status_code=authorization_specs["status_code"], errors=[
            Error(code=authorization_specs["code"], type=authorization_specs["type"],
                  message=authorization_specs["message"])])


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
        "authorization": {"code": 403, "status_code": 403, "type": "AuthorizationError", "message": "AccessDenied."}
    }
