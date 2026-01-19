from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('', views.root, name='root'),
    path('events/', views.EventListCreateView.as_view()),
    path('events/<int:event_id>/reviews/', views.ReviewListCreateView.as_view()),
    path('register/', views.RegisterView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('login/refresh/', TokenObtainPairView.as_view())
]