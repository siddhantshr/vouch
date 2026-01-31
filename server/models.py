from django.contrib.auth.models import User
from django.db import models


class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=100)
    startTime = models.DateTimeField()
    imageURL = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name="reviews", on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "event"], name="one_review_per_user_per_event"
            )
        ]

    def __str__(self):
        return f"{self.rating}⭐ for {self.event.title}"
