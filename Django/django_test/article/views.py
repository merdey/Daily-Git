from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response

def hello(request):
	name = "Michael"
	html = "<html><body> Hi %s.</body></html>" % name
	return HttpResponse(html)
	
def hello_template(request):
	return render_to_response('hello.html', {'name': 'Michael'})