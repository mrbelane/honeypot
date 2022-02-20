from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib import messages
from datetime import date
import urllib.request
import json
from .models import *


def home(request):
    return render(request, 'app/home.html')


def loginuser(request):
    data = {}

    if request.method == 'GET':
        return render(request, 'app/loginuser.html', {'form': AuthenticationForm()})
    else:

        info = Information()
        try:
            with urllib.request.urlopen("https://geolocation-db.com/json") as url:
                data = json.loads(url.read().decode())
        except IntegrityError:
            print("you are not connected")

        ip = data['IPv4']
        headers = request.headers
        username = request.POST['username']
        password = request.POST['password']
        country = data['country_name']
        user_agent = request.META.get('HTTP_USER_AGENT')
        current_date = date.today()

        info.headers = headers
        info.ip = ip
        info.country = country
        info.password = password
        info.current_date = current_date
        info.user_agent = user_agent
        info.username = username

        info.save()

        # SQL Injection detected
        is_vulnerable = scan_sql_injection(username, password)

        if is_vulnerable:
            print("[+] SQL Injection vulnerability detected:", username, password)
            injection = Sqlinjection()
            injection.ip = ip
            injection.usernameInject = username
            injection.passwordInject = password
            injection.current_date = current_date
            injection.save()
        else:
            print("[+] SQL Injection vulnerability not detected:")

        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

        # if user is None:
        #     messages.error(request, 'the username and password did not match')
        #     return render(request, 'app/loginuser.html',
        #                   {'form': AuthenticationForm(), "error": 'the username and password did not match'})
        # else:
        messages.info(request, 'login is successfully')
        # login(request, user)
    return redirect('home')


def scan_sql_injection(username, password):
    for c in "\"'":
        if username.__contains__(c) or password.__contains__(c):
            return True
    # no error detected
    return False
