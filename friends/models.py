from django.contrib.auth.models import User
from django.db import models


class Friendship(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')
    since = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')


class FriendshipRequest(models.Model):
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requester')
    requested = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requested')
    message = models.TextField()

    class Meta:
        unique_together = ('requester', 'requested')
