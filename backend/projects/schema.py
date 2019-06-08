import graphene
from graphene_django import DjangoObjectType
from users.schema import UserType

from .models import Project, Vote, Comment

class ProjectType(DjangoObjectType):
    class Meta:
        model = Project

class VoteType(DjangoObjectType):
    class Meta:
        model = Vote

class Query(graphene.ObjectType):
    projects = graphene.List(ProjectType)
    votes = graphene.List(VoteType)

    def resolve_projects(self, info, **kwargs):
        return Project.objects.all()

    def resolve_votes(self, info, **kwargs):
        return Vote.objects.all()

class CreateVote(graphene.Mutation):
    id = graphene.Int()
    type = graphene.String()
    project = graphene.Field(ProjectType)
    creator = graphene.Field(UserType)

    class Arguments:
        type = graphene.String()
        project_id = graphene.Int()

    def mutate(self, info, type, project_id):
        user = info.context.user
        project = Project.objects.get(pk=project_id)

        vote = Vote(
            creator=user,
            type=type,
            project=project,
        )
        vote.save()

        return Vote(
            id=vote.id,
            type=vote.type,
            project=vote.project,
            creator=vote.creator,
            created_on=vote.created_on,
        )

class CreateProject(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()
    description = graphene.String()
    votes = graphene.Int()
    lifecycle = graphene.String()

    class Arguments:
         name = graphene.String()
         description = graphene.String()
         lifecycle = graphene.String()


    def mutate(self, info, name, description, lifecycle):
        project = Project(name=name, description=description, lifecycle=lifecycle)
        project.save()

        return CreateProject(
            id=project.id,
            name=project.name,
            description=project.description,
            lifecycle=project.lifecycle,
        )


class Mutation(graphene.ObjectType):
    create_project = CreateProject.Field()
    create_vote = CreateVote.Field()