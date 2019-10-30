from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import SomeSerializer, NoteSerializer


class SampleApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = SomeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(data=["some_data"])

    def get(self, request):
        return Response("some thing for get.")
