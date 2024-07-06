from django.urls import path
from .views import CommunityCreateView, CommunityDeleteView, JoinCommunityView, LeaveCommunityView, RemoveMemberView

urlpatterns = [
    path('community/create/', CommunityCreateView.as_view(), name='api_create_community'),
    path('community/delete/<str:community_name>/', CommunityDeleteView.as_view(), name='api_delete_community'),
    path('community/join/<str:community_name>/', JoinCommunityView.as_view(), name='api_join_community'),
    path('community/leave/<str:community_name>/', LeaveCommunityView.as_view(), name='api_leave_community'),
    path('community/remove/<str:community_name>/<str:username>/', RemoveMemberView.as_view(), name='api_remove_member'),
]
