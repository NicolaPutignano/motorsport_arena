from django.urls import path
from .views import CommunityCreateView, CommunityDeleteView, JoinCommunityView, LeaveCommunityView, RemoveMemberView

urlpatterns = [
    path('community/create/', CommunityCreateView.as_view(), name='create_community'),
    path('community/delete/<str:community_name>/', CommunityDeleteView.as_view(), name='delete_community'),
    path('community/join/<str:community_name>/', JoinCommunityView.as_view(), name='join_community'),
    path('community/leave/<str:community_name>/', LeaveCommunityView.as_view(), name='leave_community'),
    path('community/remove/<str:community_name>/<str:username>/', RemoveMemberView.as_view(), name='remove_member'),
]
