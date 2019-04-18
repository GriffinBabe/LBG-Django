from django.http import HttpResponse
import json
from lbgmanager.models import Member, Task, Event


def parserequest(request):
    """At this point we assume the request is a dictionnary from a json file"""
    def get_model(response):
        task_list = Task.objects.all()
        event_list = Event.objects.all()
        member_list = Member.objects.all()
        task_elements = []
        event_elements = []
        member_elements = []
        for task, event, member in zip(task_list, member_list, event_list):
            task_dictionary = {"id": str(task.id), "event_id": str(task.event_id), "name": str(task.name),
                               "description": str(task.description), "deadline": str(task.deadline),
                               "responsibles_ids": str(task.responsibles_ids), "completed": str(task.completed)}
            task_elements.append(task_dictionary)
        response["tasks"] = task_elements
        return HttpResponse(json.dumps(response))

    request_type = request["request_type"]
    response = {}
    if request_type == "get_model":
        response["request_status"] = "ok"
        return get_model(response)

