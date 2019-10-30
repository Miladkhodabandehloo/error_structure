from rest_framework import serializers
from .models import Note
from best_practice.utils.patterns import use_custom_error


@use_custom_error
class SomeSerializer(serializers.Serializer):
    some_field = serializers.IntegerField(min_value=1, max_value=10)
    some_choice_field = serializers.ChoiceField(choices=((1, "The One"), (2, "The Two")))


@use_custom_error
class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ("title",)
