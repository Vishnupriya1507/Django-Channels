from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from chat.models import Room,Player
from django.utils.safestring import mark_safe
import json
from django.contrib.auth.models import User
from django.contrib.auth import logout

def main(request):
    return HttpResponseRedirect("/sportzilla/")

def logoutview(request):
    logout(request)
    return HttpResponseRedirect('https://www.google.com/accounts/Logout?continue=https://appengine.google.com/_ah/logout?continue=localhost:8000/')

    #return HttpResponseRedirect("/chat/logout/")


def login(request):
    return render(request,'sportzillalogin.html')

