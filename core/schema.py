import graphene
from api.schema import (Query as ApiQuery, Mutation as ApiMutation)
from users.schema import (Query as UserQuery, Mutation as UserMutation)


class Query(
    UserQuery, ApiQuery,
    graphene.ObjectType
):
    pass


class Mutation(
    ApiMutation, UserMutation,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
