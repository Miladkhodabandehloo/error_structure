from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from best_practice.utils.patterns import use_custom_error


@use_custom_error
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    pass


@use_custom_error
class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    pass
