from django.urls import path
from .views import EventCreateView

urlpatterns = [
    path('create-event/', EventCreateView.as_view(), name='create_event'),
]
