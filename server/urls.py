from django.urls import path
from . import views

urlpatterns = [
    path('', views.root, name='root'),
    path('events/', views.EventListCreateView.as_view()),
    path('events/<int:event_id>/reviews/', views.ReviewListCreateView.as_view()),
]