from django.http import HttpResponse
import json, hashlib, random, string
from lbgmanager.models import *


def generate_token(user):
    """ Generates a authentication token and sets it to the user"""
    while True:
        random_token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        try:  # Checks if no user already has this random generated token (it's highly improbable)
            Member.objects.get(auth_key=random_token)
            continue
        except Member.DoesNotExist:
            break
    user.auth_key = random_token
    user.save()
    return random_token


def parserequest(request):
    """At this point we assume the request is a dictionary from a json file"""

    def get_model(response):
        """Returns a json file with all the Members, Events and Task descriptions"""
        task_list = Task.objects.all()
        event_list = Event.objects.all()
        member_list = Member.objects.all()
        task_elements = []
        event_elements = []
        member_elements = []
        for task in task_list:
            task_dictionary = {"id": str(task.id), "event_id": str(task.event_id), "name": str(task.name),
                               "description": str(task.description), "deadline": str(task.deadline),
                               "responsibles_ids": json.loads(str(task.responsibles_ids)), "completed": str(task.completed)}
            task_elements.append(task_dictionary)
        response["tasks"] = task_elements
        for event in event_list:
            event_dictionary = {"id": str(event.id), "name": str(event.name), "description": str(event.description),
                                "date_begin": str(event.date_begin), "date_end": str(event.date_end),
                                "main_organiser_id": str(event.main_organiser_id), "admins_ids": json.loads(event.admins_ids),
                                "tasks_ids": json.loads(event.tasks_ids), "organisers_ids": json.loads(event.organisers_ids)}
            event_elements.append(event_dictionary)
        response["events"] = event_elements
        for member in member_list:
            member_dictionary = {"id": str(member.id), "name": str(member.name),
                                 "responsibility": str(member.responsibility),
                                 "administrator": str(member.administrator)}
            member_elements.append(member_dictionary)
        response["members"] = member_elements
        return HttpResponse(json.dumps(response))

    def get_authentication(request, response):
        """Checks if the username and the password is good and sets a new token to the user"""
        try:
            user_id = request["id"]
            user_pass = request["password"]
            user = Member.objects.get(id=user_id)
            if user.hashed_password.upper() == hashlib.sha256(user_pass.encode()).hexdigest().upper():
                generated_token = generate_token(user)
                response["request_status"] = "ok"
                response["password"] = "ok"
                response["token"] = generated_token
                return HttpResponse(json.dumps(response))
            else:
                return HttpResponse(json.dumps({"request_status": "ok", "password": "wrong"}))
        except (KeyError, Member.DoesNotExist):
            return HttpResponse(json.dumps({"request_status": "ok", "password": "wrong"}))  # Override the response

    def check_token(request, response):
        try:
            auth_key = request["auth_key"]
            member = Member.objects.get(auth_key=auth_key)
            return HttpResponse(json.dumps({"request_status": "ok", "id": str(member.id), "name": str(member.name),
                                 "responsibility": str(member.responsibility),"administrator": str(member.administrator)}))
        except (KeyError, Member.DoesNotExist):
            return HttpResponse(json.dumps({"request_status": "wrong_auth"}))

    request_type = request["request_type"]
    response = {}
    if request_type != "get_authentication_key":
        try:
            Member.objects.get(auth_key=request["auth_key"])
        except Member.DoesNotExist:
            return HttpResponse(json.dumps({"request_status": "wrong_auth"}))
        except KeyError:
            return HttpResponse(json.dumps({"request_status": "no_auth"}))
    if request_type == "get_model":
        response["request_status"] = "ok"
        return get_model(response)
    elif request_type == "get_authentication_key":
        return get_authentication(request, response)
    elif request_type == "check_token":
        return check_token(request, response)

