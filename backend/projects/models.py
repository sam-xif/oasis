from django.db import models
from django.urls import reverse
# from django.contrib.auth import User
import uuid
from enum import Enum


class Profile(models.Model):
    # user = models.OneToOneField(User)
    last_login = models.DateTimeField()


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
    # creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    # collaborators = models.ManyToMany(settings.AUTH_USER_MODEL)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    lifecycle = models.CharField(max_length=200, choices=[(tag.name, tag.value) for tag in ProjectLifecycle])
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        ordering = ["-created"]

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
    # creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created = models.DateTimeField(blank=True, auto_now_add=True)
    updated = models.DateTimeField(blank=True, auto_now=True)
    project = models.ForeignKey(
        Project,
        related_name="comments", on_delete=models.CASCADE
    )
    votes = models.IntegerField()

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.text


class Vote(models.Model):
    TYPES = (
        ("U", "Up"),
        ("D", "Down"),
    )
    # user = models.ForeignKey(settings.AUTH_USER_MODEL)
    type = models.CharField(choices=TYPES, max_length=1)
    created_on = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(
        Project,
        related_name="votes", on_delete=models.CASCADE
    )

    # def __str__(self):
    #     return self.user