from django.db import models
from django.urls import reverse
from django.conf import settings
# from django.contrib.auth import User
import uuid
from enum import Enum


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    last_login = models.DateTimeField()
    # profile_picture = models.ImageField()



class ProjectLifecycle(Enum):
    IDEA = 'Idea stage'
    PROTOTYPE = 'Prototype'
    BETA = 'Beta version'
    DEPLOY = 'Deployment'


class Tag(models.Model):
    # creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier')
    name = models.CharField(max_length=50)
    summary = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    creator = models.ForeignKey(UserProfile, blank=True, on_delete=models.PROTECT, related_name='projects_created')
    collaborators = models.ManyToManyField(UserProfile, blank=True, related_name='project_collaborated_on')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    lifecycle = models.CharField(max_length=200, choices=[(tag.name, tag.value) for tag in ProjectLifecycle])
    tags = models.ManyToManyField(Tag, blank=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.name

    def get_comments(self):
        comments = Comment.objects.filter(topic=self)
        return comments


class Resource(models.Model):
    """ Represents any related resources to a project """
    choices = ("url", "image")
    project = models.ForeignKey(
        Project,
        related_name="resources", on_delete=models.CASCADE
    )


class Comment(models.Model):
    text = models.CharField(max_length=200)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, on_delete=models.PROTECT)
    created_on = models.DateTimeField(blank=True, auto_now_add=True)
    updated_on = models.DateTimeField(blank=True, auto_now=True)
    project = models.ForeignKey(
        Project,
        related_name="comments", on_delete=models.CASCADE
    )
    votes = models.IntegerField()

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.text


class Vote(models.Model):
    TYPES = (
        ("U", "Up"),
        ("D", "Down"),
    )
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, on_delete=models.CASCADE)
    type = models.CharField(max_length=1)  # Do custom validation on choices=TYPES https://github.com/graphql-python/graphene-django/issues/185#issuecomment-388469296
    project = models.ForeignKey(
        Project,
        related_name="votes", on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)


