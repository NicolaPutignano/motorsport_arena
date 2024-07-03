from django.urls import path
from .views import CommunityCreateView, CommunityDeleteView

urlpatterns = [
    path('create_community/', CommunityCreateView.as_view(), name='create_community'),
    path('delete_community/<int:pk>/', CommunityDeleteView.as_view(), name='api_delete_community'),
]
