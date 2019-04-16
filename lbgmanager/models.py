from django.db import models
from enum import Enum
# Create your models here.


class Responsibility(Enum):
    PR = "President"
    TR = "Treasurer"
    SEC = "Secretary"
    VP_PR = "Vice President in Public Relations"
    VP_HR = "Vice President in Human Resources"
    VP_FR = "Vice President in Foundraising"


class Member(models.Model):
    id = models.CharField(max_length=10)
    hashed_password = models.CharField(max_length=255)
    auth_key = models.CharField(max_length=20)
    name = models.CharField(max_length=30)
    responsibility = models.CharField(max_length=50, choices=[(tag, tag.value) for tag in Responsibility])
    administrator = models.BooleanField(default=False)
    finished_tasks = models.IntegerField()
    dodged_tasks = models.IntegerField()
    not_respected_tasks = models.IntegerField()


class Task(models.Model):
    id = models.CharField(max_length=10)
    event_id = models.CharField(max_length=10)
    name = models.CharField(max_length=30)
    description = models.TextField()
    deadline = models.DateTimeField()
    """We can use json.dumps(listOfIds) to get a string and json.loads(allIdsInOneString) for the opposite operation"""
    responsibles_ids = models.TextField()
    completed = models.BooleanField()


class Event(models.Model):
    id = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    description = models.TextField()
    date_begin = models.DateTimeField()
    date_end = models.DateTimeField()
    main_organiser_id = models.CharField(max_length=10)
    admins_ids = models.TextField()
    tasks_ids = models.TextField()
    organisers_ids = models.TextField()






