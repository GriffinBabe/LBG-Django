from django.shortcuts import render
from django.http import HttpResponse

from lbgmanager.requesthandler import *
import json
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def api(request):
    if request.method == "POST":
        try:
            print(request.body)
            json_request = json.loads(request.body)
            return parserequest(json_request)
        except json.JSONDecodeError:
            response = {"request_status": "error"}
            json_response = json.dumps(response)
            return HttpResponse(json_response)
    return HttpResponse("error")