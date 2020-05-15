import graphene

import schedules.schema


class Query(schedules.schema.Query, graphene.ObjectType):
    pass

class Mutation(schedules.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)