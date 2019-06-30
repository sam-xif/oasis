import graphene
from graphene_django import DjangoObjectType
from users.schema import UserType
from graphql import GraphQLError


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
    class Arguments:
        vote_type = graphene.Argument(graphene.Enum('vote_types', [('U', 'Up'), ('D', 'Down')]))
        project_id = graphene.Int()


    id = graphene.Int()
    type = graphene.String()
    project = graphene.Field(ProjectType)
    creator = graphene.Field(UserType)
    created_on = graphene.types.datetime.DateTime()

    def mutate(self, info, vote_type, project_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('User must be logged in to vote')

        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
                raise Exception('Could not find the specified project.')

        vote = Vote(
            creator=user,
            type=vote_type,
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
    class Arguments:
         name = graphene.String()
         description = graphene.String()
         lifecycle = graphene.Argument(graphene.Enum('project_lifecycle', [('IDEA', 'Idea stage'), ('PROTOTYPE', 'Prototype'), ('BETA', 'Beta version'), ('DEPLOY', 'Deployment')]))


    id = graphene.Int()
    name = graphene.String()
    description = graphene.String()
    votes = graphene.Int()
    lifecycle = graphene.String()


    def mutate(self, info, name, description, lifecycle):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('User must be logged in to create a project')

        project = Project(name=name, description=description, creator=user, lifecycle=lifecycle)
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