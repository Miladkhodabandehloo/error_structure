from django.urls import path
from .views import SampleApiView

urlpatterns = [
    path("some_url/", SampleApiView.as_view())
]
