from .serializers import BaseSerializer


def use_custom_error(cls):
    class NEWCLS(cls, BaseSerializer):
        pass

    return NEWCLS



