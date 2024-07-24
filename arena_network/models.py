from django.db import models
from django.conf import settings

from arena_network.constants import COMMUNITY_ROLE_CHOICES


class Community(models.Model):
    name = models.CharField(max_length=255, unique=True)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='communities_created')

    def __str__(self):
        return self.name


class CommunityMember(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='members')
    role = models.CharField(max_length=10, choices=COMMUNITY_ROLE_CHOICES)

    class Meta:
        unique_together = ('user', 'community')

    def __str__(self):
        return f'{self.user.username} in {self.community.name} as {self.role}'
