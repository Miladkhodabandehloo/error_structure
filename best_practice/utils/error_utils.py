from rest_framework.views import exception_handler
from rest_framework.exceptions import ErrorDetail, APIException
import logging
from rest_framework import status
from rest_framework.response import Response


class Error:
    def __init__(self, error_type, message, parameter=None):
        self.error_type = error_type
        self.message = message
        self.parameter = parameter

    ERROR_STATUS_GLOSSARY = {
        status.HTTP_500_INTERNAL_SERVER_ERROR: dict(error_type="InternalError", message="Internal server error."),
        status.HTTP_401_UNAUTHORIZED: dict(error_type="AuthenticationError", message="Authentication failed."),
        status.HTTP_403_FORBIDDEN: dict(error_type="AuthorizationError", message="Access denied.")}


class ErrorResponse(Response):
    def __init__(self, errors, *args, **kwargs):
        super(ErrorResponse, self).__init__(*args, **kwargs)
        self.errors = [errors] if not isinstance(errors, list) else errors


def custom_exception_handler(exc, context):
    if hasattr(exc, "form_data") and hasattr(exc, "form_errors"):
        errors = list()
        for field_name, validation_errors in exc.form_errors.items():
            errors.extend([
                Error(error_type="ValidationError",
                      message=str(error),
                      parameter=dict(name=field_name, sent_data=exc.form_data.get(field_name))
                      ) for error in validation_errors
            ])
        response = ErrorResponse(errors=errors, status=status.HTTP_400_BAD_REQUEST)
        return response

    if hasattr(exc, "status_code"):
        if exc.status_code in Error.ERROR_STATUS_GLOSSARY.keys():
            message = exc.detail if hasattr(exc, "detail") and isinstance(exc.detail, ErrorDetail) else None
            error_detail = Error.ERROR_STATUS_GLOSSARY[exc.status_code]
            return ErrorResponse(
                errors=Error(
                    error_type=error_detail["error_type"],
                    message=message or error_detail["message"]),
                status=exc.status_code)

    logger = logging.getLogger(__name__)
    logger.exception(exc)
    unknown_error_detail = Error.ERROR_STATUS_GLOSSARY[status.HTTP_500_INTERNAL_SERVER_ERROR]
    return ErrorResponse(
        errors=Error(error_type=unknown_error_detail["error_type"],
                     message=unknown_error_detail["message"]),
        status=status.HTTP_500_INTERNAL_SERVER_ERROR)