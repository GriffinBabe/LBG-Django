from django.shortcuts import render

from django.http import HttpResponse

# Create your views here.
def api(request):
    if request.is_ajax():
        if request.method=="POST":
            print(request.body)
    return HttpResponse("OK")

