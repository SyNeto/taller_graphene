import graphene

from graphene_django.types import DjangoObjectType

from .models import Schedule, Event


class ScheduleType(DjangoObjectType):
    class Meta:
        model = Schedule


class EventType(DjangoObjectType):
    class Meta:
        model = Event


class Query(object):
    hello = graphene.String(name=graphene.String(default_value='World'))
    schedules = graphene.List(ScheduleType)
    schedule = graphene.Field(ScheduleType, id=graphene.ID(required=True))
    events = graphene.List(EventType)
    event = graphene.Field(EventType, id=graphene.ID(required=True))

    def resolve_hello(self, info, name):
        return f'Hello, {name}!'

    def resolve_schedules(self, info, **kwargs):
        return Schedule.objects.all()

    def resolve_schedule(self, info, id, **kwargs):
        return Schedule.objects.get(pk=id)

    def resolve_events(self, info, **kwargs):
        return Event.objects.all()

    def resolve_event(self, info, id, **kwargs):
        return Event.objects.get(pk=id)


class CreateSchedule(graphene.Mutation):
    class Arguments:
        code = graphene.String(required=True)
    
    schedule = graphene.Field(ScheduleType)

    def mutate(self, info, **kwargs):
        schedule = Schedule.objects.create(**kwargs)
        return CreateSchedule(schedule=schedule)

class UpdateSchedule(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        code = graphene.String(required=True)

    schedule = graphene.Field(ScheduleType)

    def mutate(self, info, id, code, **kwargs):
        qs = Schedule.objects.filter(pk=id)
        qs.update(code=code, **kwargs)
        return UpdateSchedule(schedule=qs.first())


class RemoveSchedule(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id, **kwargs):
        try:
            Schedule.objects.get(pk=id).delete()
        except:
            pass
        return RemoveSchedule(ok=True)


class CreateEvent(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        schedule_id = graphene.ID(required=True)
        start = graphene.DateTime(required=True)
        end = graphene.DateTime(required=True)

    event = graphene.Field(EventType)

    def mutate(self, info, **kwargs):
        event = Event.objects.create(**kwargs)
        return CreateEvent(event=event)


class UpdateEvent(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        schedule_id = graphene.ID()
        start = graphene.DateTime()
        end = graphene.DateTime()

    event = graphene.Field(EventType)

    def mutate(self, info, id, **kwargs):
        qs = Event.objects.filter(pk=id)
        qs.update(**kwargs)
        return UpdateEvent(event=qs.first())


class RemoveEvent(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id, **kwargs):
        try:
            Event.object.get(pk=id)
        except:
            pass
        return RemoveEvent(ok=True)



class Mutation(graphene.ObjectType):
    create_schedule = CreateSchedule.Field()
    update_schedule = UpdateSchedule.Field()
    remove_schedule = RemoveSchedule.Field()
    create_event = CreateEvent.Field()
    update_event = UpdateEvent.Field()

