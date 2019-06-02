from django.contrib import admin

from projects.models import Project, Tag, Comment, Vote, Resource

admin.site.register(Project)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Resource)
admin.site.register(Vote)

