from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

urlpatterns = [
    path("", views.root, name="root"),
    path("events/", views.EventListCreateView.as_view()),
    path("events/<int:event_id>/reviews/", views.ReviewListCreateView.as_view()),
    path("register/", views.RegisterView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("events/<int:pk>/delete/", views.EventDestroyView.as_view()),
    path(
        "events/<int:event_id>/reviews/<int:pk>/delete/", views.ReviewDelete.as_view()
    ),
]
