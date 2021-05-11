from django.http import request
from django.shortcuts import render

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
    