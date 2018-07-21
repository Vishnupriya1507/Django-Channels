from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from chat.models import Room
from django.utils.safestring import mark_safe
import json

def main(request):
    return HttpResponseRedirect("/accounts/login/")

def logout(request):
    return HttpResponseRedirect("/chat/logout/")

