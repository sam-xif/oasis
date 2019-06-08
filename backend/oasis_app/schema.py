import graphene

import projects.schema
import users.schema

class Query(users.schema.Query, projects.schema.Query, graphene.ObjectType):
    pass

class Mutation(projects.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)