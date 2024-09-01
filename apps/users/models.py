from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.users.managers import UserManager
from apps.utils.common_model import CommonModel


class User(AbstractUser, CommonModel):
    username = None
    email = models.EmailField(unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    friends = models.ManyToManyField(
        "self", related_name="friend_set", blank=True, symmetrical=False
    )

    # add more field

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class FriendRequestStatus(models.TextChoices):
    PENDING = "pending", _("Pending")
    ACCEPTED = "accepted", _("Accepted")
    REJECTED = "rejected", _("Rejected")


class FriendRequest(CommonModel):
    sender = models.ForeignKey(
        "User", related_name="sent_requests", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        "User", related_name="received_requests", on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=20,
        choices=FriendRequestStatus.choices,
        default=FriendRequestStatus.PENDING,
    )

    class Meta:
        unique_together = ("sender", "receiver")

    def __str__(self):
        return f"{self.sender.email} -> {self.receiver.email} ({self.status})"
