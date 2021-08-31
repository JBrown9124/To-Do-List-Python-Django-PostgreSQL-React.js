from django.shortcuts import render
from django.http import HttpResponse
import json
from django.core import serializers
from .models import *
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseServerError
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import hashlib
import uuid

# Create your views here.


def get_tasks_by_user(request, user):
    u = Users.objects.get(pk=user)
    # tasks = u.tasks_set.order_by('task_priority')
    # tasks = Tasks.objects.filter(user=u).order_by('task_priority')
    # data = serializers.serialize('json',tasks)
    # return HttpResponse(data, content_type='application/json')
    # return JsonResponse(tasks, safe=False)

    data = list(Tasks.objects.filter(
        user=u).order_by('task_priority').values())

    return JsonResponse({'user': data})
def order_tasks_by_date(request, user):
    u = Users.objects.get(pk=user)
    # tasks = u.tasks_set.order_by('task_priority')
    # tasks = Tasks.objects.filter(user=u).order_by('task_priority')
    # data = serializers.serialize('json',tasks)
    # return HttpResponse(data, content_type='application/json')
    # return JsonResponse(tasks, safe=False)

    data = list(Tasks.objects.filter(
        user=u).order_by('task_date_time').values())

    return JsonResponse({'user': data})  
def order_tasks_by_name(request, user):
    u = Users.objects.get(pk=user)
    # tasks = u.tasks_set.order_by('task_priority')
    # tasks = Tasks.objects.filter(user=u).order_by('task_priority')
    # data = serializers.serialize('json',tasks)
    # return HttpResponse(data, content_type='application/json')
    # return JsonResponse(tasks, safe=False)

    data = list(Tasks.objects.filter(
        user=u).order_by('task_name').values())

    return JsonResponse({'user': data})    


@csrf_exempt
def get_task_by_task_id(request, user):
    u = Users.objects.get(pk=user)
    if request.method == 'GET':
        json_data = json.loads(request.body)
        t = Tasks.objects.filter(user=u, pk=json_data['task_id'])
        data = list(t.values())
        return JsonResponse({'task': data})


@csrf_exempt
def edit_task(request, user):
    u = Users.objects.get(pk=user)
    if request.method == 'POST':
        json_data = json.loads(request.body)
        d = datetime.datetime.strptime(
            json_data["date_time"], '%d. %B %Y %H:%M')
        t = Tasks(pk=json_data['id'], user=u, task_name=json_data['name'], task_priority=json_data['priority'],
                  task_description=json_data['description'], task_attendees=json_data['attendees'], task_date_time=d)
        t.save()
        return HttpResponse("nice")


def get_user(request, user):
    return HttpResponse(user)
# def register(request, login, password, first_name, email, registered=True):
#     u = Users(user_login=login, user_password=password, user_first_name=first_name, user_email=email, user_registered=registered)
#     u.save()
#     return HttpResponse(reverse(f"{user_first_name} created successfully!"))


@csrf_exempt
def add_task(request, user):
    u = Users.objects.get(pk=user)
    if request.method == 'POST':
        json_data = json.loads(request.body)

        # d = datetime.datetime.strptime('12. June 2017 10:17', '%d. %B %Y %H:%M')
        d = datetime.datetime.strptime(
            json_data["date_time"], '%d. %B %Y %H:%M')
        # d = datetime.datetime.strptime(json_data['date_time'], '%Y-%B-%d %H:%M:%S')
        t = Tasks(user=u, task_name=json_data['name'], task_priority=json_data['priority'],
                  task_description=json_data['description'], task_attendees=json_data['attendees'], task_date_time=d)
        t.save()
        return HttpResponse(f"{user} tasks saved")


@csrf_exempt
def delete_task(request, user):
    u = Users.objects.get(pk=user)
    if request.method == 'DELETE' or request.method == 'POST':
        json_data = json.loads(request.body)

        t = Tasks.objects.filter(user=u, pk=json_data['task_id'])
        t.delete()

        return HttpResponse(f"{user} tasks deleted")


@csrf_exempt
def log_in(request):
    if request.method == "POST":
        json_data = json.loads(request.body)

        # data = json_data['data']

        try:
            user_salt = Users.objects.get(
                user_email=json_data['email']).user_salt
            hashed_password = hashlib.sha512(json_data['password'].encode(
                'utf-8') + user_salt.encode('utf-8')).hexdigest()
            user = Users.objects.get(
                user_email=json_data['email'], user_hash=hashed_password)

            return HttpResponse(user.user_id)
        except:
            return HttpResponseServerError


@csrf_exempt
def register(request):
    if request.method == "POST" or request.method == "OPTIONS":
        json_data = json.loads(request.body)

        # data = json_data['data']
        try:

            if Users.objects.get(user_email=json_data['email']).user_registered:
                return HttpResponseServerError
        except:
            salt = uuid.uuid4().hex
            hashed_password = hashlib.sha512(json_data['password'].encode(
                'utf-8') + salt.encode('utf-8')).hexdigest()
            u = Users(user_hash=hashed_password, user_salt=salt,
                      user_first_name=json_data['name'], user_email=json_data['email'], user_registered=True)
            u.save()
            return HttpResponse(u.user_id)


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
