from django.urls import path
from .views import CommunityCreateView

urlpatterns = [
    path('create_community/', CommunityCreateView.as_view(), name='create_community'),
    path('create-event/', views.create_event, name='create_event'),
]
