from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from .form import summoner_info
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .graphs.fn_data_api import (get_summoner_puuid, get_match_list, get_match_data, 
    get_summoner_index, get_summoner_data, get_kills, get_assists, get_deaths, 
    get_championName, get_goldEarned, get_totalDamageDealt, get_totalDamageTaken, 
    get_role, get_lane, get_win)
from league_of_data import settings
from django.http import JsonResponse

def get_home(request):
  form = summoner_info()
  return render(request, 'home.html', {'form': form})

@csrf_exempt
def get_summoner_info(request):
    if request.method == "POST":
        form = summoner_info(request.POST)
        if form.is_valid():
            # Process the form data and set session variables or perform other actions as needed
            
            # Then return the JsonResponse with the redirect URL
            return JsonResponse({'redirectUrl': '/data_visualization'})
        else:
            return JsonResponse(form.errors, status=400)

def data_visualization(request):
    summ_info = request.session.get('summ_info', None)
    if summ_info is None:
        return redirect('get_home')
    
    summoner_name, summoner_tag, summoner_region = summ_info
    api_key = settings.RIOT_API_KEY

    summoner_puuid = get_summoner_puuid(summoner_name, summoner_tag, summoner_region, api_key)
    match_list = get_match_list(summoner_puuid, summoner_region, api_key)

    all_match_details = []
    if match_list:
        for match_id in match_list[:5]:  # Limit to 5 matches for brevity
            match_data = get_match_data([match_id], summoner_region, api_key)
            for match in match_data:
                summoner_index = get_summoner_index(match, summoner_puuid)
                summoner_data = get_summoner_data(match, summoner_index)
                
                match_details = {
                    'match_id': match_id,
                    'championName': get_championName(summoner_data),
                    'kills': get_kills(summoner_data),
                    'assists': get_assists(summoner_data),
                    'deaths': get_deaths(summoner_data),
                    'goldEarned': get_goldEarned(summoner_data),
                    'totalDamageDealt': get_totalDamageDealt(summoner_data),
                    'totalDamageTaken': get_totalDamageTaken(summoner_data),
                    'role': get_role(summoner_data),
                    'lane': get_lane(summoner_data),
                    'win': get_win(summoner_data)
                }
                all_match_details.append(match_details)

    context = {
        'match_data': all_match_details,
        'summoner_name': summoner_name
    }
    return render(request, 'data_visualization.html', context)
