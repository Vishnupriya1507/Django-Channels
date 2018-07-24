from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from chat.models import Room,Player
from django.utils.safestring import mark_safe
import json
from django.contrib.auth.models import User

def main(request):
    return HttpResponseRedirect("/accounts/login/")

def logout(request):
    
    return HttpResponseRedirect("/chat/logout/")


def login(request):
    return render(request,'sportzillalogin.html')

