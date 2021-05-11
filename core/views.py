from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound
from faunadb import query as q
import pytz
from faunadb.objects import Ref
from faunadb.client import FaunaClient
import hashlib
import datetime
import os

client = FaunaClient(secret=os.environ(FAUNA_SECRET_KEY))
indexes =  client.query(q.paginate(q.indexes()))



# Create your views here.

def login(request):
    return render(request, "login.html")
    
def create_appointment(request):
    return render(request, "appoint/create-appointment.html")
        
def dashboard(request):
    return render(request, "index.html")

def today_appointment(request):
    return render(request, "today-appointment.html")

def all_appointment(request):
    return render(request, "all-appointments.html")

def register(request):
    return render(request, "register.html")
