from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import SomeSerializer, NoteSerializer
from best_practice.errors import APIException


class SampleApiView(APIView):
    def post(self, request):
        # raise APIException.authorization()
        serializer = SomeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(data=["some_data"])
