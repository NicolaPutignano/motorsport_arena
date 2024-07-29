from django.urls import path

from .views import EventCreateView, JoinEventView, EventDetailView, EventUpdateView

urlpatterns = [
    path('create-event/', EventCreateView.as_view(), name='create_event'),
    path('join/<str:event_name>/', JoinEventView.as_view(), name='join_event'),
    path('details/<str:event_name>/', EventDetailView.as_view(), name='details_event'),
    path('update/<str:event_name>/', EventUpdateView.as_view(), name='update_event'),
]
