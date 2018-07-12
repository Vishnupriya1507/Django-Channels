from django.http import HttpResponseRedirect
from django.shortcuts import render

def main(request):
	return HttpResponseRedirect("/accounts/login/")

def logout(request):
	return HttpResponseRedirect("/chat/logout/")