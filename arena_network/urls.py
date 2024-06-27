from django.urls import path
from .views import CommunityCreateView

urlpatterns = [
    path('create_community/', CommunityCreateView.as_view(), name='create_community'),
]
