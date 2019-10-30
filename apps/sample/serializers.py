from best_practice.utils.serializer_utils import DRFSerializer, DRFModelSerializer
from rest_framework import serializers
from .models import Note


class SomeSerializer(DRFSerializer):
    some_field = serializers.IntegerField(min_value=1, max_value=10)
    some_choice_field = serializers.ChoiceField(choices=((1, "The One"), (2, "The Two")))


class NoteSerializer(DRFModelSerializer):
    class Meta:
        model = Note
        fields = ("title",)
