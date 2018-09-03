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
    return HttpResponseRedirect('https://accounts.google.com/Logout?&continue=https://www.google.com')
    #https://accounts.google.com/ServiceLogin/signinchooser?service=mail&passive=true&rm=false&continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&ss=1&scc=1&ltmpl=default&ltmplcache=2&emr=1&osid=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin
    #return HttpResponseRedirect("https://www.google.com/accounts/Logout?continue=https://appengine.google.com/_ah/logout?continue=localhost:8000//")


def login(request):
    return render(request,'sportzillalogin.html')

