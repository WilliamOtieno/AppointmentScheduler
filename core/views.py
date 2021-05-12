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
    if request.method == "POST":
        username = request.POST.get("username").strip().lower()
        password = request.POST.get("password")

        try:
            user = client.query(q.get(q.match(q.index("users_index"), username)))
            if hashlib.sha512(password.encode()).hexdigest() == user["data"]["password"]:
                request.session["user"] = {
                    "id": user["ref"].id(),
                    "username": user["data"]["username"]
                }
                return redirect("core:dashboard")
            else:
                raise Exception()
        except:
            messages.add_message(request, messages.INFO, 'Invalid credentials! Please try again.', "danger")
            return redirect("core:login")

    return render(request, "login.html")
    
def create_appointment(request):
    if "user" in request.session:
        if request.method == "POST":
            name = request.POST.get("name")
            description = request.POST.get("description")
            time = request.POST.get("time")
            date = request.POST.get("date")
            try:
                user = client.query(q.get(q.match(q.index("events_index"), date, time)))
                messages.add_message(request, messages.INFO, 'An Event is already scheduled for the specified time.')
                return redirect("core:create-appointment")
            except:
                user = client.query(q.create(q.collection("Events"), {
                    "data": {
                        "name": name,
                        "description": description,
                        "time": time,
                        "date": date,
                        "user": request.session["user"]["username"],
                        "status": 'False',
                    }
                }))
                messages.add_message(request, messages.INFO, 'Appointment Scheduled Successfully.')
                return redirect("core:create-appointment")
        return render(request, "appoint/create-appointment.html")
    else:
        return HttpResponseNotFound("Page not found! Check the url.")

    
        
def dashboard(request):
    return render(request, "index.html")

def today_appointment(request):
    if "user" in request.session:
        


    return render(request, "today-appointment.html")

def all_appointment(request):
    return render(request, "all-appointments.html")

def register(request):
    if request.method == "POST":
        username = request.POST.get("username").strip().lower()
        email = request.POST.get("email").strip().lower()
        password = request.POST.get("password")

        try:
            user = client.query(q.get(q.match(q.index("users_index"), username)))
            messages.add_message(request, messages.INFO, 'User with that username already exists.')
            return redirect("core:register")
        except:
            user = client.query(q.create(q.collection("users"), {
                "data": {
                    "username": username,
                    "email": email,
                    "password": hashlib.sha512(password.encode()).hexdigest(),
                    "date": datetime.datetime.now(pytz.UTC)
                }
            }))
            messages.add_message(request, messages.INFO, 'Registration successful.')
            return redirect("core:login")

    return render(request, "register.html")
