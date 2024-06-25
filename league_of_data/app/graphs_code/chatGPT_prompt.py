import google.generativeai as genai
import os
import textwrap
import re
import pathlib
from IPython.display import Markdown

def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def markdown_to_html(text):
    text = re.sub(r'## (.+)', r'<h2>\1</h2>', text)
    text = re.sub(r'# (.+)', r'<h1>\1</h1>', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\* ([^*]+)', r'<li>\1</li>', text)
    text = re.sub(r'(\<li\>.*?\<\/li\>)+', r'<ul>\g<0></ul>', text)
    text = re.sub(r'\n\n', r'</p><p>', text)
    text = f'<p>{text}</p>'
    
    return text

def get_chatgpt_response(context):
    API_KEY = ''
    summoner = context['summoner'].summoner_name
    winrate = context['winrate']
    tier = context['summoner'].tier
    rango = context['summoner'].rank
    match_list = context['match_details']
    total_champs = []
    total_roles = []
    total_lanes = []
    total_kills = []
    total_deaths = []
    total_assists = []
    total_winrate = []
    for match in match_list:
        match_data = match['graphic_data']
        champ = match_data.championName
        if champ:
            total_champs.append(champ)
        role = match_data.role
        if role:
            total_roles.append(role)
        lane = match_data.lane
        if lane:
            total_lanes.append(lane)
        kills = match_data.kills
        if kills:
            total_kills.append(kills)
        deaths = match_data.deaths
        if deaths:
            total_deaths.append(deaths)
        assists = match_data.assists
        if assists:
            total_assists.append(assists)
        win = match_data.win
        if win == True:
            total_winrate.append('Ganada')
        else:
            total_winrate.append('Perdida')
        
    try:
        genai.configure(api_key=API_KEY)
        
        model = genai.GenerativeModel('gemini-1.5-flash')
             
        prompt = (
        f'Eres un experto en análisis de jugadores de League of Legends.' 
        f'Da consejos que permitan al jugador {summoner} entender sus fortalezas y debilidades'
        'con los siguientes datos generales de su cuenta y de sus últimas 10 partidas.'
        f'El jugador es {tier} {rango}, con un porcentaje de victorias de {winrate}.'
        f'En sus últimas 10 partidas, utilizó los siguientes campeones {total_champs},'
        f'se desempeñó en los siguientes roles {total_roles},'
        f'jugando en las siguientes líneas {total_lanes}.'
        f'En las últimas 10 partidas, obtuvo la siguiente cantidad de asesitanos {total_kills},'
        f'la siguiente cantidad de muertes {total_deaths} y'
        f'la siguiente cantidad de asistencias {total_assists}.'
        )
        
        response = model.generate_content(prompt)
        #print(model.count_tokens(response))
        html_response = markdown_to_html(response.text)
        return html_response
        
    except Exception as e:
        print(f"Error al obtener respuesta de OpenAI: {e}")
        return None