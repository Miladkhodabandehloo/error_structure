from .paginators import CustomPagination
from rest_framework.generics import ListAPIView
from .models import Note
from .serializers import NoteSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class NotesList(ListAPIView):
    pagination_class = CustomPagination
    serializer_class = NoteSerializer

    def get_queryset(self):
        return Note.objects.all()


class SomeAPIView(APIView):
    def get(self, request):
        return Response("some thing.")
