from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Review(models.Model):
    event = models.ForeignKey(
        Event,
        related_name="reviews",
        on_delete=models.CASCADE
    )
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating}⭐ for {self.event.title}"