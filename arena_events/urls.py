from django.urls import path
from .views import EventCreateView, EventDeleteView

urlpatterns = [
    path('create-event/', EventCreateView.as_view(), name='create_event'),
    path('delete-event/', EventDeleteView.as_view(), name='delete_event'),
]
