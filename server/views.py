from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from .models import Event, Review
from .serializers import EventSerializer, ReviewSerializer
from django.shortcuts import get_object_or_404

@api_view(["GET"])
def root(request):
    return Response({
        "status": "working",
        "version": "0.1.0-dev"
    })

class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all().order_by("-date_created")
    serializer_class = EventSerializer

class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        event_id = self.kwargs["event_id"]
        return Review.objects.filter(event_id=event_id)
    
    def perform_create(self, serializer):
        event_id = self.kwargs["event_id"]
        event = get_object_or_404(Event, id=event_id)
        serializer.save(event=event)
