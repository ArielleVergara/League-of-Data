from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from .form import summoner_form
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from league_of_data import settings
from django.http import JsonResponse
from .services import save_summoner_info, save_matches_stats, send_time_info, validate_summoner, validate_time_info, get_summoner_stats
from .models import Summoner, Time_info, Match, Graphic_data
from .graphs_code.graphs_detail import generate_graphs
import matplotlib.pyplot as plt
from io import BytesIO
import traceback
from django.core.cache import cache
from django.core.exceptions import ValidationError
from .graphs_code.fn_data_api import get_match_list, get_match_data, get_summoner_data, get_summoner_index, get_championName, get_kills, get_assists, get_deaths, get_goldEarned, get_totalDamageDealt, get_totalDamageTaken, get_role, get_lane, get_win, get_participants, get_summoner_data, get_participants_info

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
            try:
                summoner_info = validate_summoner(summoner_name, summoner_tag, summoner_region, api_key)
                summoner = save_summoner_info(summoner_info['puuid'], summoner_info)
                #print(summoner)
                return JsonResponse({'redirectUrl': f'/data_visualization/{summoner.summoner_name}/{summoner.summoner_tag}/{summoner.region}/'})
            except ValidationError as e:
                return JsonResponse({'error': str(e)}, status=400)
        else:
            return JsonResponse(form.errors, status=400)

def display_matches(request, summoner_name, summoner_tag, summoner_region):
    api_key = settings.RIOT_API_KEY
    match_data = None
    try:
        summoner = Summoner.objects.filter(summoner_name=summoner_name).first()
        #print(summoner.id)
        if not summoner:
            #print(summoner)
            lista_match_id = get_match_list(summoner.summoner_puuid, summoner.region, api_key)
            if lista_match_id:
                for match_id in lista_match_id:
                    #print(match_id)
                    match_info = get_summoner_stats(summoner, match_id, api_key)
                    #print(match_info)
                    if match_info:
                        save_matches_stats(summoner, match_id, match_info)
                    else:
                        return HttpResponse("No se pudo obtener la información del invocador.", status=404)
            else:
                print(f"No se pudo obtener la lista de partidos de {summoner.summoner_name}")
            
        else:
            api_match_ids = get_match_list(summoner.puuid, summoner.region, api_key)
            #print(api_match_ids)
            if api_match_ids:
                existing_match_ids = set(Match.objects.filter(summoner_id=summoner.id).values_list('api_match_id', flat=True))
                new_match_ids = [mid for mid in api_match_ids if mid not in existing_match_ids]
                #(new_match_ids)
                for match_id in new_match_ids:
                    print(match_id)
                    match_info = get_summoner_stats(summoner, match_id, api_key)
                    #print(match_data)
                    if not match_info:
                        print(f"No se pudo obtener la información del partido {match_id} de {summoner.summoner_name}")
                    else:
                        save_matches_stats(summoner, match_id, match_info)
            else:
                print(f"No se pudo obtener la lista de partidos de {summoner.summoner_name}")
        # Continuar con la lógica para mostrar los partidos, etc.
        if match_data is None:
            all_match_data = []
            graphic_data = Graphic_data.objects.filter(summoner_id=summoner.id).all()
            for num in graphic_data:
                match_data = {
                    'match_id': num.match_id.api_match_id,
                    'assists': num.assists,
                    'deaths': num.deaths,
                    'kills': num.kills,
                    'total_damage_dealt': num.totalDamageDealt,
                    'total_damage_taken': num.totalDamageTaken,
                    'gold_earned': num.goldEarned,
                    'lane': num.lane,
                    'win': num.win,
                    'role': num.role,
                    'champion': num.championName,
                }
                #print(match_data)
                if match_data:
                    all_match_data.append(match_data)
                else:
                    print(f"No se pudo obtener la información del partido {num.match_id} de {summoner.summoner_name}")
        #print(match_data)
        context = {
            'summoner': summoner,
            'match_data': all_match_data,
            'total_wins': summoner.total_wins,
            'total_losses': summoner.total_losses,
            'winrate': (summoner.total_wins / (summoner.total_wins + summoner.total_losses)) * 100 if (summoner.total_wins + summoner.total_losses) > 0 else 0,
            'rank': summoner.rank,
            'tier': summoner.tier,
        }
        return render(request, 'data_visualization.html', context)
    except Exception as e:
        import traceback
        traceback.print_exc()  # Esto imprimirá el traceback en la consola del servidor
        return HttpResponse(f"An error occurred: {str(e)}", status=500)


def compare_summoners(request):
    if request.method == "POST":
        form = summoner_form(request.POST)
        if form.is_valid():
            summoner1_name = form.cleaned_data['summoner1_name']
            summoner2_name = form.cleaned_data['summoner2_name']
            summoner1_region = form.cleaned_data['summoner1_region']
            summoner2_region = form.cleaned_data['summoner2_region']
            summoner1_tag = form.cleaned_data['summoner1_tag']
            summoner2_tag = form.cleaned_data['summoner2_tag']
            
            try:
                # Validar y obtener información de los invocadores
                summoner1_info = validate_summoner(summoner1_name, summoner1_tag, summoner1_region, settings.RIOT_API_KEY)
                summoner2_info = validate_summoner(summoner2_name, summoner2_tag, summoner2_region, settings.RIOT_API_KEY)
                
                # Guardar o actualizar la información en la base de datos
                summoner1 = save_summoner_info(summoner1_info['puuid'], summoner1_info)
                summoner2 = save_summoner_info(summoner2_info['puuid'], summoner2_info)
                
                # Obtener estadísticas adicionales si es necesario
                summoner1_stats = get_summoner_stats(summoner1)
                summoner2_stats = get_summoner_stats(summoner2)
                
                # Generar gráficos para la comparación
                graph1 = generate_graphs(summoner1)
                graph2 = generate_graphs(summoner2)
                
                context = {
                    'summoner1': summoner1_stats,
                    'summoner2': summoner2_stats,
                    'graph1': graph1,
                    'graph2': graph2
                }
                return render(request, 'compare_summoners.html', context)
            except ValidationError as e:
                return error_view(request, str(e))
            except Exception as e:
                return error_view(request, "An unexpected error occurred: " + str(e))
        else:
            return error_view(request, "Invalid form data.")
    else:
        form = summoner_form()
        return render(request, 'compare_form.html', {'form': form})
    
def time_info_to_plot_image(request, match_id, graph_type, summoner_name):
    #print(match_id)
    api_key = settings.RIOT_API_KEY
    try:
        time_info = send_time_info(match_id, api_key, summoner_name)
        #print(time_info)
        if not time_info:
            return HttpResponse("No time information available.", status=404)
    except:
        print("No se se encontró time_info")
    # Llamar a plot_image pasando los datos directamente
    return plot_image(request, graph_type, time_info, summoner_name, match_id)

def plot_image(request, graph_type, time_info, summoner_name, match_id):
    
    try:      
        result = generate_graphs(time_info)
        graph_index = {
            'daño': 0,
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
        #return response
        pass
    except Exception as e:
        trace = traceback.format_exc()
        return HttpResponse(f"An error occurred: {str(e)}\nTraceback:\n{trace}", status=500)
