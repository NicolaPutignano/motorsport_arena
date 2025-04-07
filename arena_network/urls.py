from django.urls import path
from .views import (
    CommunityCreateView,
    CommunityDeleteView,
    JoinCommunityView,
    LeaveCommunityView,
    RemoveMemberView,
    CommunityRetrieveView,
    CommunityListView)

urlpatterns = [
    path('community-create/', CommunityCreateView.as_view(), name='create_community'),
    path('communities/', CommunityListView.as_view(), name='community_list'),
    path('community/<str:community_name>', CommunityRetrieveView.as_view(), name='community_detail'),
    path('community/<str:community_name>/delete/', CommunityDeleteView.as_view(), name='delete_community'),
    path('community/<str:community_name>/join/', JoinCommunityView.as_view(), name='join_community'),
    path('community/<str:community_name>/leave/', LeaveCommunityView.as_view(), name='leave_community'),
    path('community/<str:community_name>/remove/<str:username>/', RemoveMemberView.as_view(), name='remove_member'),

]
