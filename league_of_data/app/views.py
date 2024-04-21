from django.http import HttpResponse
from django.template import loader


def get_home(request):
  template = loader.get_template('home.html')
  return HttpResponse(template.render())

def get_data_visualization(request):
  if request.method == "POST":
    data_input = request.POST.get(['summoner_name', 'summoner_tag'])
    template = loader.get_template('data_visualization.html')
  return HttpResponse(template.render(), data_input)
