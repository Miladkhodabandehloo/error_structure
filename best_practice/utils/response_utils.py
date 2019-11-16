from rest_framework.response import Response


class APIResponse(Response):
    def __init__(self, errors=None, pagination=None, *args, **kwargs):
        super(APIResponse, self).__init__(*args, **kwargs)
        if errors is None:
            errors = list()
        self.errors = [errors] if not isinstance(errors, list) else errors
        self.pagination = pagination
