import graphene
from graphene_django import DjangoObjectType

from .models import Project

class ProjectType(DjangoObjectType):
    class Meta:
        model = Project

class Query(graphene.ObjectType):
    project = graphene.List(ProjectType)

    def resolve_project(self, info, **kwargs):
        return Project.objects.all()

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