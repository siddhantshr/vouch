from rest_framework import serializers
from .models import Event, Review

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "title", "content", "date_created"]
        read_only_fields = ["id", "date_created"]

class ReviewSerializer(serializers.ModelSerializer):
    def validate_rating(self, value):
        if not value in (1,2,3,4,5):
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value

    class Meta:
        model = Review
        fields = ["id", "rating", "comment", "created_at"]
        read_only_fields = ["id", "created_at"]