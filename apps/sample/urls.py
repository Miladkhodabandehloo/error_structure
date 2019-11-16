from django.urls import path
from .views import *

urlpatterns = [
    path("notes/", NotesList.as_view()),
    path("something/", SomeAPIView.as_view())
]
