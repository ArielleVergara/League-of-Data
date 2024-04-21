from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from .form import summoner_info
from django.http import HttpResponseRedirect
from django.shortcuts import render

def get_home(request):
  template = loader.get_template('home.html')
  return HttpResponse(template.render())

@csrf_exempt
def get_summoner_info(request):
  if request.method == "POST":
    form = summoner_info(request.POST)
    if form.is_valid():
      summoner_name = form.cleaned_data["summoner_name"]
      summoner_tag = form.cleaned_data["summoner_tag"]
      summoner_region = form.cleaned_data["region"]
      summ_info = list.append(summoner_name, summoner_tag, summoner_region)
      return HttpResponseRedirect("/data_visualization", summ_info)
    else:
      form = summoner_info()
  else:
    print("No se pudo enviar información")
  return render(request, "data_visualization.html", {"form": form})
