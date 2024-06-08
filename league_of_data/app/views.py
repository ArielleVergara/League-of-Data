from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from .form import summoner_form
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from league_of_data import settings
from django.http import JsonResponse
from .services import save_summoner_matches_and_stats
from .models import Summoner, Time_info, Match, Graphic_data
from .graphs_code.graphs_detail import generate_graphs
import matplotlib.pyplot as plt
from io import BytesIO

def buscarInvc(request):
  form = summoner_form()
  return render(request, 'buscarInvc.html', {'form': form})

def nosotros(request):
    return render(request, 'nosotros.html')

def home(request):
    return render(request, 'home.html')

def get_summoner(request):
    if request.method == "POST":
        form = summoner_form(request.POST)
        if form.is_valid():
            summoner_name = form.cleaned_data['summoner_name']
            summoner_tag = form.cleaned_data['summoner_tag']
            summoner_region = form.cleaned_data['summoner_region']
            
            request.session['summ_info'] = [summoner_name, summoner_tag, summoner_region]
            
            return JsonResponse({'redirectUrl': '/data_visualization'})
        else:
            return JsonResponse(form.errors, status=400)

def data_visualization(request):
    summ_info = request.session.get('summ_info', None)
    
    if summ_info is None:
        return redirect('home')
    
    summoner_name, summoner_tag, summoner_region = summ_info

    api_key = settings.RIOT_API_KEY

    save_summoner_matches_and_stats(summoner_name, summoner_tag, summoner_region, api_key)

    try:
        summoner = Summoner.objects.get(summoner_name=summoner_name, summoner_tag=summoner_tag, region=summoner_region)
    except Summoner.DoesNotExist:
        return redirect('home')

    matches = Match.objects.filter(summoner_id=summoner)
    all_match_details = []
    
    for match in matches:
        graphic_data = Graphic_data.objects.filter(match_id=match).first()
        if graphic_data:
            match_details = {
                'match_id': match.id,
                'championName': graphic_data.championName,
                'kills': graphic_data.kills,
                'assists': graphic_data.assists,
                'deaths': graphic_data.deaths,
                'goldEarned': graphic_data.goldEarned,
                'totalDamageDealt': graphic_data.totalDamageDealt,
                'totalDamageTaken': graphic_data.totalDamageTaken,
                'role': graphic_data.role,
                'lane': graphic_data.lane,
                'win': graphic_data.win,
                'goldSpent': graphic_data.goldSpent,
                'totalHeal': graphic_data.totalHeal,
                'totalHealOnTeammates': graphic_data.totalHealsOnTeammates,
                'totalMinionsKilled': graphic_data.totalMinionsKilled,
                'totalTimeSpentDead': graphic_data.totalTimeSpentDead,
                'visionScore': graphic_data.visionScore,
                'wardKilled': graphic_data.wardKilled,
                'wardPlaced': graphic_data.wardPlaced,
                'doubleKills': graphic_data.doubleKills,
                'tripleKills': graphic_data.tripleKills,
                'firstBloodAssist': graphic_data.firstBloodAssist,
                'firstBloodKill': graphic_data.firstBloodKill,
                'timePlayed': graphic_data.timePlayed,
                'killingSprees': graphic_data.killingSprees,
                'individualPosition': graphic_data.individualPosition,
                'gameEndedInEarlySurrender': graphic_data.gameEndedInEarlySurrender,
                'gameEndedInSurrender': graphic_data.gameEndedInSurrender,
                'time_info': []
            }

        time_info = Time_info.objects.filter(match_id = match)
        for time_data in time_info:
            match_details['time_info'].append({
                'minute': time_data.minute,
                'damageDone': time_data.damageDone,
                'damageTaken': time_data.damageTaken,
                'gold': time_data.gold,
                'xp': time_data.xp,
                'minions': time_data.minions,
                'level': time_data.level
            })
        
        all_match_details.append(match_details)
            
        generate_graphs(match)
        
    
    
    total_wins = summoner.total_wins
    total_losses = summoner.total_losses
    winrate = (total_wins / (total_wins + total_losses)) * 100 if (total_wins + total_losses) > 0 else 0
    
    context = {
        'match_data': all_match_details,
        'summoner': summoner,
        'total_wins': total_wins,
        'total_losses': total_losses,
        'winrate': winrate,
        'rank': summoner.rank,
        'tier': summoner.tier,
        
    }
    return render(request, 'data_visualization.html', context)

def plot_image(request, match_id, graph_type):
    match = Match.objects.get(id=match_id)
    result = generate_graphs(match)
    graph_index = {
        'daño': 0,
        'exp': 1,
        'minions': 2,
        'nivel': 3,
        'oro': 4
    }.get(graph_type, 0)

    fig = result[graph_index]
    buf = BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    response = HttpResponse(buf.getvalue(), content_type="image/png")
    response['Content-Length'] = str(len(response.content))
    return response
