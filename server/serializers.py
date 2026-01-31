from django.contrib.auth.models import User
from django.db.models import Avg
from rest_framework import serializers

from .models import Event, Review


class EventSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if not reviews.exists():
            return None
        return reviews.aggregate(Avg("rating"))["rating__avg"]

    class Meta:
        model = Event
        fields = [
            "id",
            "user",
            "title",
            "content",
            "date_created",
            "rating",
            "location",
            "startTime",
            "imageURL",
        ]
        read_only_fields = ["id", "user", "date_created", "rating"]


class ReviewSerializer(serializers.ModelSerializer):
    def validate_rating(self, value):
        if value not in (1, 2, 3, 4, 5):
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value

    class Meta:
        model = Review
        fields = ["id", "user", "rating", "comment", "created_at"]
        read_only_fields = ["id", "user", "created_at"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"], password=validated_data["password"]
        )
        return user
