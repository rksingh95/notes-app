import uuid

from django.contrib.auth.models import User
from django.db import models


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Note(UUIDModel):
    title = models.TextField(max_length=200)
    body = models.TextField()
    tag = models.TextField(max_length=60)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = ["updated"]

    def __str__(self) -> str:
        return "New note" + " - " + self.tag[0:60] + " by " + self.user.first_name
