import uuid
from django.contrib.auth.models import User
from django.db import models


class BaseModel(models.Model):
    """Base model that contains shared columns for all models
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True, editable=False)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ('-created',)


class Topic(BaseModel):
    """Topics are sections for related messages
    """

    name = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.name}"


class Message(BaseModel):
    """Messages are comments users can leave on topics
    """

    content = models.TextField(null=True, blank=True)
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.topic} - {str(self.content)[:100]}"
