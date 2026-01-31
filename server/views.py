from django.conf import settings
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .exceptions import ConflictError
from .models import Event, Review
from .permissions import IsOwnerOrSuperUser
from .serializers import EventSerializer, RegisterSerializer, ReviewSerializer

# from drf_spectacular.utils import extend_schema


@api_view(["GET"])
@permission_classes([AllowAny])
def root(request):
    return Response(
        {"status": "working", "version": settings.SPECTACULAR_SETTINGS["VERSION"]}
    )


class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all().order_by("-date_created")
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [SearchFilter]
    search_fields = ["title"]  # 👈 searchable fields

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        now = timezone.now()

        upcoming = [event for event in queryset if event.startTime >= now]
        past = [event for event in queryset if event.startTime < now]

        return Response(
            {
                "upcoming": self.get_serializer(upcoming, many=True).data,
                "past": self.get_serializer(past, many=True).data,
            }
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EventDestroyView(generics.DestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsOwnerOrSuperUser]


class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        event_id = self.kwargs["event_id"]
        return Review.objects.filter(event_id=event_id)

    def perform_create(self, serializer):
        event_id = self.kwargs["event_id"]
        event = get_object_or_404(Event, id=event_id)

        try:
            serializer.save(event=event, user=self.request.user)
        except IntegrityError:
            raise ConflictError("You have already reviewed this event.")


class ReviewDelete(generics.DestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrSuperUser]

    def get_queryset(self):
        return Review.objects.filter(event_id=self.kwargs["event_id"])


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "user": user.username,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )
