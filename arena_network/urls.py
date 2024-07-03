from django.urls import path
from .views import CommunityCreateView, CommunityDeleteView, JoinCommunityView, LeaveCommunityView, RemoveMemberView

urlpatterns = [
    path('community/create/', CommunityCreateView.as_view(), name='api_create_community'),
    path('community/delete/<int:pk>/', CommunityDeleteView.as_view(), name='api_delete_community'),
    path('community/join/<int:pk>/', JoinCommunityView.as_view(), name='api_join_community'),
    path('leave/<int:pk>/', LeaveCommunityView.as_view(), name='api_leave_community'),
    path('remove/<int:community_pk>/<int:member_pk>/', RemoveMemberView.as_view(), name='api_remove_member'),
]
