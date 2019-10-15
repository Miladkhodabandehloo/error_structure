# Django Error Response Structure
This project represents structure for passing errors to clients and implements this structure in django and [django REST
framework](https://www.django-rest-framework.org/ "django REST framework Home Page").

### Validation error response sample:
You can raise validation error with this structure like this example:
 ```python
from rest_framework import serializers
from best_practice.utils import use_custom_error


@use_custom_error
class SomeSerializer(serializers.Serializer):
    some_field = serializers.IntegerField(min_value=1, max_value=10)
    some_choice_field = serializers.ChoiceField(choices=((1, "The One"), (2, "The Two")))
```
If you sent invalid date response would be like this:
```json
{
    "errors": [
        {
            "code": 400,
            "sub_type": "required",
            "type": "ValidationError",
            "parameter": {
                "name": "some_field",
                "min_value": 1,
                "max_value": 10
            },
            "message": "This field is required."
        },
        {
            "code": 400,
            "sub_type": "required",
            "type": "ValidationError",
            "parameter": {
                "name": "some_choice_field",
                "choices": [
                    1,
                    2
                ]
            },
            "message": "This field is required."
        }
    ]
}
```

#### other error response samples:
other errors can be created this way:
```python
from best_practice.errors import APIException, Error
raise APIException(status_code=403, errors=[
            Error(code=403, type="AuthorizationError", message="Access Denied.")])
```
```json
{
    "errors": [
        {
            "code": 403,
            "sub_type": null,
            "type": "AuthorizationError",
            "parameter": null,
            "message": "AccessDenied."
        }
    ]
}
```
