from django.http import HttpResponse
from django.template import loader

def app(request):
  template = loader.get_template('home.html')
  return HttpResponse(template.render())