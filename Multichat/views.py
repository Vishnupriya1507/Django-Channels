from django.http import HttpResponseRedirect
from django.shortcuts import render

def main(request):
	return HttpResponseRedirect("/accounts/login/")