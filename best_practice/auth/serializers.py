from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from ..utils.serializer_utils import DRFSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer, DRFSerializer):
    pass


class CustomTokenRefreshSerializer(TokenRefreshSerializer, DRFSerializer):
    pass
