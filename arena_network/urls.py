from django.urls import path
from .views import CommunityCreateView, CommunityDeleteView, JoinCommunityView

urlpatterns = [
    path('community/create/', CommunityCreateView.as_view(), name='api_create_community'),
    path('community/delete/<int:pk>/', CommunityDeleteView.as_view(), name='api_delete_community'),
    path('community/join/<int:pk>/', JoinCommunityView.as_view(), name='api_join_community'),
]
