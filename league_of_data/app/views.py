from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from .form import summoner_form
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from league_of_data import settings
from django.http import JsonResponse
from .services import save_summoner_info, save_matches_stats, send_time_info, validate_summoner, save_time_info, get_summoner_stats, calculate_winrate
from .models import Summoner, Time_info, Match, Graphic_data
from .graphs_code.graphs_detail import generate_graphs
import matplotlib.pyplot as plt
from io import BytesIO
import traceback
from django.core.cache import cache
from django.core.exceptions import ValidationError
from .graphs_code.fn_data_api import get_match_list, get_match_data, get_summoner_data, get_summoner_index, get_championName, get_kills, get_assists, get_deaths, get_goldEarned, get_totalDamageDealt, get_totalDamageTaken, get_role, get_lane, get_win, get_participants, get_summoner_data, get_participants_info
import logging

logger = logging.getLogger(__name__)

def error_view(request, error_message):
    return render(request, 'error.html', {'error_message': error_message})

def buscarInvc(request):
  form = summoner_form()
  return render(request, 'buscarInvc.html', {'form': form})

def nosotros(request):
    return render(request, 'nosotros.html')

def home(request):
    return render(request, 'home.html')

def get_summoner(request):
    api_key = settings.RIOT_API_KEY
    if request.method == "POST":
        form = summoner_form(request.POST)
        if form.is_valid():
            summoner_name = form.cleaned_data['summoner_name']
            summoner_tag = form.cleaned_data['summoner_tag']
            summoner_region = form.cleaned_data['summoner_region']
            cache_key = f"{summoner_name}_{summoner_tag}_{summoner_region}"
            try:
                print(f"League of Data: Buscando datos de cuenta de summoner {summoner_name}")
                summoner_info = validate_summoner(summoner_name, summoner_tag, summoner_region, api_key)
                #print(summoner_info)
                cache.set(cache_key, summoner_info, timeout=3600)
                summoner = save_summoner_info(summoner_info['puuid'], summoner_info)
                return JsonResponse({'redirectUrl': f'/data_visualization/{summoner.summoner_name}/{summoner.summoner_tag}/{summoner.region}/'})
            except Exception as e:
                return render(request, 'error.html', {'error_message': "No se pudo acceder a la API. Revise las credenciales de la API."})
            
        else:
            return JsonResponse(form.errors, status=400)

def display_matches(request, summoner_name, summoner_tag, summoner_region):
    try:
        
        summoner = get_or_create_summoner(summoner_name, summoner_tag, summoner_region)
        #print(summoner)
        handle_new_matches_and_time_info(summoner)
        context = build_display_context(summoner)
        return render(request, 'data_visualization.html', context)
    except ValidationError as e:
        return render(request, 'error.html', {'error_message': str(e)})

    except Exception as e:
        logger.error(f"An error occurred in display_matches: {e}", exc_info=True)
        return render(request, 'error.html', {'error_message': "Ocurrió un error inesperado. Intente de nuevo."})

def get_or_create_summoner(summoner_name, summoner_tag, summoner_region):
    print(f"League of Data: Actualizando datos de summoner {summoner_name}.")
    api_key = settings.RIOT_API_KEY
    summoner_info = validate_summoner(summoner_name, summoner_tag, summoner_region, api_key)
    return save_summoner_info(summoner_info['puuid'], summoner_info)

def handle_new_matches_and_time_info(summoner):
    print(f"League of Data: Buscando datos de partidas de summoner {summoner.summoner_name}.")
    api_key = settings.RIOT_API_KEY
    new_matches = get_match_list(summoner.puuid, summoner.region, api_key)
    existing_match_ids = set(Match.objects.filter(summoner_id=summoner).values_list('api_match_id', flat=True))
    for match_id in new_matches:
        if match_id not in existing_match_ids:
            try:
                match_data = get_summoner_stats(summoner, match_id, api_key)
                save_matches_stats(summoner, match_id, match_data)
                time_data = send_time_info(match_id, api_key, summoner.summoner_name)
                #print(time_data)
                save_time_info(match_id, time_data, summoner)
            except Exception as e:
                logger.error(f"Error handling new matches and time info: {e}", exc_info=True)
                raise ValidationError("Error al procesar las nuevas partidas. Intente de nuevo.")

def build_display_context(summoner):
    print(f"League of Data: Compilando todos los datos de summoner {summoner.summoner_name} para visualización.")
    winrate = calculate_winrate(summoner)
    matches = Match.objects.filter(summoner_id=summoner)
    
    match_details = []
    for match in matches:
        graphic_data = Graphic_data.objects.filter(match_id=match).first()

        cache_key = f"time_info_{match.id}"
        time_info = cache.get(cache_key)

        if not time_info:
            time_info = list(Time_info.objects.filter(match_id=match))
            cache.set(cache_key, time_info, timeout=3600)      
        
        match_details.append({
            'match': match,
            'graphic_data': graphic_data,
            'time_info': time_info
        })   
    
    return {
        'summoner': summoner,
        'match_details': match_details,
        'winrate': winrate
    }


def plot_image(request, graph_type, summoner_name, match_id):
    #print(match_id)
    cache_key = f"time_info_{match_id}"
    time_info = cache.get(cache_key)
    #print(time_info)
    if not time_info:
        time_info = list(Time_info.objects.filter(match_id_id=match_id))
        cache.set(cache_key, time_info, timeout=3600)
    try:
        #print(time_info)      
        result = generate_graphs(time_info, match_id)
        graph_index = {
            'dano': 0,
            'nivel': 1,
            'minions': 2,
            'oro': 3,
            'exp': 4
        }.get(graph_type, None)

        if graph_index is None:
            print("Invalid graph type")
            return HttpResponse("Invalid graph type.", status=400)

        fig = result[graph_index]
        buf = BytesIO()
        fig.savefig(buf, format="png")
        plt.close(fig)
        response = HttpResponse(buf.getvalue(), content_type="image/png")
        response['Content-Length'] = str(len(response.content))
        return response
        #pass
    except Exception as e:
        trace = traceback.format_exc()
        return HttpResponse(f"An error occurred: {str(e)}\nTraceback:\n{trace}", status=500)
