import google.generativeai as genai
import os
import re
#from IPython.display import Markdown

API_KEY = ''

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

def comparacion_gemini(context):
    summonerA_name = context['summonerA']['summoner'].summoner_name
    summonerB_name = context['summonerB']['summoner'].summoner_name
    summonerA_winrate = context['summonerA']['winrate']
    summonerB_winrate = context['summonerB']['winrate']
    summonerA_totalwins = context['summonerA']['summoner'].total_wins
    summonerB_totalwins = context['summonerB']['summoner'].total_wins
    summonerA_totalLosses = context['summonerA']['summoner'].total_losses
    summonerB_totalLosses = context['summonerB']['summoner'].total_losses
    summonerA_champions = []
    summonerB_champions = []
    summonerA_lanes = []
    summonerB_lanes = []
    summonerA_roles = []
    summonerB_roles = []
    summonerA_wins = []
    summonerB_wins = []

    
    for match in context['summonerA']['match_details']:
        champion = match['graphic_data'].championName
        summonerA_champions.append(champion)
        lane = match['graphic_data'].lane
        summonerA_lanes.append(lane)
        role = match['graphic_data'].role
        summonerA_roles.append(role)
        wins = match['graphic_data'].win
        if wins == True:
            summonerA_wins.append('Ganada')
        else:
            summonerA_wins.append('Perdida')
        
    for match in context['summonerB']['match_details']:
        champion = match['graphic_data'].championName
        summonerB_champions.append(champion)
        lane = match['graphic_data'].lane
        summonerB_lanes.append(lane)
        role = match['graphic_data'].role
        summonerB_roles.append(role)
        wins = match['graphic_data'].win
        if wins == True:
            summonerB_wins.append('Ganada')
        else:
            summonerB_wins.append('Perdida')
    
    consejo = {}
    context.keys()
    
    try:
        for key in context:
            genai.configure(api_key=API_KEY)
            
            model = genai.GenerativeModel('gemini-1.5-flash')
            if key == 'summonerA':
                prompt = ('Dame un análisis acotado de los siguientes gráficos de un jugador de League of Legends.'
                          f'En el primer gráfico de barras, el eje X representa al jugador {summonerA_name} '
                          f'y el eje Y representa la cantidad de partidas ganadas {summonerA_totalwins} o perdidas {summonerA_totalLosses},'
                          f'graficando así, el ratio de victorias de un {summonerA_winrate}. '
                          f'En el segundo gráfico de barras apiladas, el eje X representa el campeón utilizado {summonerA_champions}, '
                          f'y el eje Y representa el número de partidas jugadas con esos campeones. '
                          f'Cada barra está dividida en dos secciones: la parte superior representa las '
                          f'partidas ganadas y la parte inferior representa las partidas perdidas {summonerA_wins}. '
                          f'los siguientes resultados {summonerA_wins}. '
                          f'El tercer gráfico grafica las partidas gandas y perdidas según la linea jugada. '
                          f'El eje X representa la línea jugada {summonerA_lanes} y el eje Y '
                          f'representa el ratio de victorias {summonerA_wins}. '
                          f'Cada línea está divida en dos secciones: la parte superior representa las '
                          f'partidas ganadas y la parte inferior representa las partidas perdidas. '
                          )
                response = model.generate_content(prompt)
                html_response = markdown_to_html(response.text)
                consejo['summonerA'] = html_response
            else:
                prompt = ('Dame un análisis acotado de los siguientes gráficos de un jugador de League of Legends. '
                          f'En el primer gráfico de barras, el eje X representa al jugador {summonerB_name} '
                          f'y el eje Y representa la cantidad de partidas ganadas {summonerA_totalwins} o perdidas {summonerA_totalLosses}, '
                          f'graficando así, el ratio de victorias de un {summonerB_winrate}. '
                          f'En el segundo gráfico de barras apiladas, el eje X representa el campeón utilizado {summonerB_champions}, '
                          f'y el eje Y representa el número de partidas jugadas con esos campeones. '
                          f'Cada barra está dividida en dos secciones: la parte superior representa las '
                          f'partidas ganadas y la parte inferior representa las partidas perdidas {summonerB_wins}. '
                          f'los siguientes resultados {summonerB_wins}. '
                          f'El tercer gráfico grafica las partidas gandas y perdidas según la linea jugada. '
                          f'El eje X representa la línea jugada {summonerB_lanes} y el eje Y '
                          f'representa el ratio de victorias {summonerB_wins}. '
                          f'Cada línea está divida en dos secciones: la parte superior representa las '
                          f'partidas ganadas y la parte inferior representa las partidas perdidas. '
                          )
                response = model.generate_content(prompt)
                html_response = markdown_to_html(response.text)
                consejo['summonerB'] = html_response
        return consejo      
    except Exception as e:
        print(f"Error al obtener respuesta de OpenAI: {e}")
        return None