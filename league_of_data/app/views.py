from django.http import HttpResponse
from django.template import loader
from .form import summoner_form, summoner_compare_form
from django.shortcuts import render
from league_of_data import settings
from django.http import JsonResponse
from .services import save_summoner_info, save_matches_stats, send_time_info, validate_summoner, save_time_info, get_summoner_stats, calculate_winrate
from .models import Time_info, Match, Graphic_data
from .graphs_code.graphs_detail import generate_graphs, compare_graphs
import matplotlib.pyplot as plt
from io import BytesIO
import traceback
from django.core.cache import cache
from django.core.exceptions import ValidationError
from .graphs_code.fn_data_api import get_match_list
from .graphs_code.chatGPT_prompt import get_chatgpt_response
import logging

logger = logging.getLogger(__name__)

def error_view(request, error_message):
    return render(request, 'error.html', {'error_message': error_message})

def comparar(request):
    form = summoner_compare_form(prefix='summoner2')
    return render(request, 'comparacion.html', {'form': form})

def buscarInvc(request):
    form = summoner_form(prefix='summoner1')
    return render(request, 'buscarInvc.html', {'form': form})

def nosotros(request):
    return render(request, 'nosotros.html')

def home(request):
    return render(request, 'home.html')

    
def view_single_summoner(request):
    form = summoner_form(request.POST, prefix='summoner1')
    if form.is_valid():
        summoner_name = form.cleaned_data['summoner_name']
        #print(summoner_name)
        summoner_tag = form.cleaned_data['summoner_tag']
        #print(summoner_tag)
        summoner_region = form.cleaned_data['summoner_region']
        #print(summoner_region)
        summoner_server = form.cleaned_data['summoner_server']
        try:
            context = display_matches(request, summoner_name, summoner_tag, summoner_region, summoner_server)
            chatgpt_graphic_data = get_chatgpt_response(context)
            context['chatgpt_graphic_data'] = chatgpt_graphic_data
        except:
            return render(request, 'error.html', {'error_message': "Hubo un error con la extracción de información de la API. Intente de nuevo."})
        
        return render(request, 'data_visualization.html', context)
    else:
        return render(request, 'error.html', {'error_message': "Hubo un error con el envío de información. Intente de nuevo."})
    
def compare_summoners(request):
    form = summoner_compare_form(request.POST, prefix='summoner2')
    if form.is_valid():
        summoner_a = {
            'name': form.cleaned_data['summoner1_name'],
            'tag': form.cleaned_data['summoner1_tag'],
            'region': form.cleaned_data['summoner1_region'],
            'server': form.cleaned_data['summoner1_server']
        }
        summoner_b = {
            'name': form.cleaned_data['summoner2_name'],
            'tag': form.cleaned_data['summoner2_tag'],
            'region': form.cleaned_data['summoner2_region'],
            'server': form.cleaned_data['summoner2_server']
        }
        #print(summoner_a)
        #print(summoner_b)
        cache_key = f"compare_{summoner_a['name']}_{summoner_b['name']}"
        context = cache.get(cache_key)
        try:
            summoner_a = display_matches(request, summoner_a['name'], summoner_a['tag'], summoner_a['region'], summoner_a['server'])
            #print(summoner_a)
            summoner_b = display_matches(request, summoner_b['name'], summoner_b['tag'], summoner_b['region'], summoner_b['server'])
            #print(summoner_b)
            if 'error_message' in summoner_a:
                raise Exception(summoner_a['error_message'])
            if 'error_message' in summoner_b:
                raise Exception(summoner_b['error_message'])
            
            context = {
                'summonerA': summoner_a,
                'summonerB': summoner_b
            }
            #print(context)
            cache.set(cache_key, context, timeout=3600)
            return render(request, 'ver_comparacion.html', context)
        except Exception as e:
            return render(request, 'error.html', {'error_message': str(e)})
    else:
                return JsonResponse({'error': 'Ambos formularios deben ser válidos.'}, status=400)
    

def display_matches(request, summoner_name, summoner_tag, summoner_region, summoner_server):
    try:
        summoner = get_or_create_summoner(request, summoner_name, summoner_tag, summoner_region, summoner_server)
        #print(summoner)
        handle_new_matches_and_time_info(summoner)
        context = build_display_context(summoner)
        if not context:
            context['error_message'] = "No se pudo construir el contexto para la visualización."
    except ValidationError as e:
        context['error_message'] = str(e)
    except Exception as e:
        logger.error(f"An error occurred in display_matches: {e}", exc_info=True)
        context['error_message'] = "Ocurrió un error inesperado. Intente de nuevo."
    return context

def get_or_create_summoner(request, summoner_name, summoner_tag, summoner_region, summoner_server):
    print(f"League of Data: Actualizando datos de summoner {summoner_name}.")
    api_key = settings.RIOT_API_KEY
    summoner_info = validate_summoner(request, summoner_name, summoner_tag, summoner_region, api_key, summoner_server)
    #print(summoner_info)
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
    #print(winrate)
    matches = Match.objects.filter(summoner_id=summoner)[:10]
    
    match_details = []
    for match in matches:
        graphic_data = Graphic_data.objects.filter(match_id=match).first()

        cache_key = f"time_info_{match.id}"
        time_info = cache.get(cache_key)

        if not time_info:
            time_info = list(Time_info.objects.filter(match_id=match))
            cache.set(cache_key, time_info, timeout=3600)
        #chatgpt_graphic_data = get_chatgpt_response(graphic_data)
        #chatgpt_time_info = get_chatgpt_response(time_info)    
        
        match_details.append({
            'match': match,
            'graphic_data': graphic_data,
            'time_info': time_info,
            #'chatgpt_graphic_data': chatgpt_graphic_data,
            #'chatgpt_time_info': chatgpt_time_info
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
    
def plot_compare(request, summoner_a, summoner_b, graph_type):
    cache_key = f"compare_{summoner_a}_{summoner_b}"
    context = cache.get(cache_key)
    #print(context)
    if context is None:
        return HttpResponse("No se encontró información en caché para estos summoners.", status=404)
    try:
        result = compare_graphs(context, summoner_a, summoner_b)
        graph_index = {
            'winrate': 0,
            'champion': 1,
            'lane': 2
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
    except Exception as e:
        trace = traceback.format_exc()
        return HttpResponse(f"An error occurred: {str(e)}\nTraceback:\n{trace}", status=500)
    return request
