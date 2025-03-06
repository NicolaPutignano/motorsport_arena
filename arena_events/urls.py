from django.urls import path
from .views import EventCreateView, JoinEventView, EventDetailView

urlpatterns = [
    path('create-event/', EventCreateView.as_view(), name='create_event'),
    path('join/<str:event_name>/', JoinEventView.as_view(), name='join_event'),
    path('details/<str:event_name>/', EventDetailView.as_view(), name='details_event'),
]
