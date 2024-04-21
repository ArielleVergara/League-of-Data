import requests

api_key = "RGAPI-6d4b46d7-1bdf-4c33-b16b-823785fb3231"
tag = "ttv"
summoner_name = 'LoboSkoll'
region = 'Americas'


def get_summoner_puuid(summoner_name, tag, region, api_key):
    url_start = "http://"
    url_finish = ".api.riotgames.com/riot/account/v1/accounts/by-riot-id/"
    api_url = url_start + region + url_finish + summoner_name + tag + "?api_key=" + api_key

    try:
        resp_summoner = requests.get(api_url)
        if resp_summoner == 200:
            summoner_info = resp_summoner.json()
            summoner_puuid = summoner_info['puuid']
        else:
            print("No tiene acceso válido a la API Account (response != 200)")
    except:
        print("No se pudo conectar con la API Account")
    return summoner_puuid

def get_match_list(summoner_puuid, region, api_key):
    url_start = "http://"
    url_middle = ".api.riotgames.com/lol/match/v5/matches/by-puuid/"
    url_finish = "/ids?type=ranked&start=0&count=20&api_key="

    try:
        api_url = url_start + region + url_middle + summoner_puuid + url_finish + api_key

        resp_list = requests.get(api_url)
        if resp_list == 200:
            match_list = resp_list.json()
        else:
            print("No se ha podido acceder a la API Match List")
    except:
        print("No se pudo conectar con la API Matches")
    return match_list

def get_match_data (match_list, region, api_key):
    url_start = "http://"
    url_middle = ".api.riotgames.com/lol/match/v5/matches/"
    url_finish = "?api_key="
    
    for match in match_list:
        return match
    
    url_api = url_start + region + url_middle + match + url_finish + api_key

    resp_match = requests.get(url_api)
    if resp_match == 200:
        match_data = resp_match.json()
    else:
        print("No se ha podido acceder a la API Match(1)")
    return match_data

def get_summoner_index(match_data, summoner_puuid):
    summoner_index = match_data['metadata']['participants'].index(summoner_puuid)
    return summoner_index

def get_summoner_data(match_data, summoner_index):
    summoner_data = match_data['info']['participants'][summoner_index]
    return summoner_data

def get_kills(summoner_data):
    summoner_kills = summoner_data['kills']
    return summoner_kills

def get_assists(summoner_data):
    summoner_assists = summoner_data['assists']
    return summoner_assists

def get_deaths(summoner_data):
    summoner_deaths = summoner_data['deaths']
    return summoner_deaths

def get_championId(summoner_data):
    summoner_championId = summoner_data['championId']
    return summoner_championId

def get_championName(summoner_data):
    summoner_championName = summoner_data['championName']
    return summoner_championName

def get_goldEarned(summoner_data):
    summoner_goldEarned = summoner_data['goldEarned']
    return summoner_goldEarned

def get_goldSpent(summoner_data):
    summoner_goldSpent = summoner_data['goldSpent']
    return summoner_goldSpent

def get_totalDamageDealt(summoner_data):
    summoner_totalDamageDealt = summoner_data['totalDamageDealt']
    return summoner_totalDamageDealt

def get_totalDamageTaken(summoner_data):
    summoner_totalDamageTaken = summoner_data['totalDamageTaken']
    return summoner_totalDamageTaken

def get_role(summoner_data):
    summoner_role = summoner_data['role']
    return summoner_role

def get_wardsPlaced(summoner_data):
    summoner_wardsPlaced = summoner_data['wardsPlaced']
    return summoner_wardsPlaced

def get_lane(summoner_data):
    summoner_lane = summoner_data['lane']
    return summoner_lane

def get_participantId(summoner_data):
    summoner_participantId = summoner_data['participantId']
    return summoner_participantId

def get_doubleKills(summoner_data):
    summoner_doubleKills = summoner_data['doubleKills']
    return summoner_doubleKills

def get_firstBloodAssist(summoner_data):
    summoner_firstBloodAssist = summoner_data['firstBloodAssist']
    return summoner_firstBloodAssist

def get_firstBloodKill(summoner_data):
    summoner_firstBloodKill = summoner_data['firstBloodKill']
    return summoner_firstBloodKill

def get_gameEndedInEarlySurrender(summoner_data):
    summoner_gameEndedInEarlySurrender = summoner_data['gameEndedInEarlySurrender']
    return summoner_gameEndedInEarlySurrender

def get_gameEndedInSurrender(summoner_data):
    summoner_gameEndedInSurrender = summoner_data['gameEndedInSurrender']
    return summoner_gameEndedInSurrender

def get_individualPosition(summoner_data):
    summoner_individualPosition = summoner_data['individualPosition']
    return summoner_individualPosition

def get_killingSprees(summoner_data):
    summoner_killingSprees = summoner_data['killingSprees']
    return summoner_killingSprees

def get_longestTimeSpentLiving(summoner_data):
    summoner_longestTimeSpentLiving = summoner_data['longestTimeSpentLiving']
    return summoner_longestTimeSpentLiving

def get_spell1Casts(summoner_data):
    summoner_spell1Casts = summoner_data['spell1Casts']
    return summoner_spell1Casts

def get_spell2Cast(summoner_data):
    summoner_spell2Cast = summoner_data['spell2Cast']
    return summoner_spell2Cast

def get_spell3Cast(summoner_data):
    summoner_spell3Cast = summoner_data['spell3Cast']
    return summoner_spell3Cast

def get_spell4Cast(summoner_data):
    summoner_spell4Cast = summoner_data['spell4Cast']
    return summoner_spell4Cast

def get_timePlayed(summoner_data):
    summoner_timePlayed = summoner_data['timePlayed']
    return summoner_timePlayed

def get_win(summoner_data):
    summoner_win = summoner_data['win']
    return summoner_win

