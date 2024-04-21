import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException


def get_summoner_puuid(summoner_name, tag, region, api_key):
    url_start = "https://"
    url_finish = ".api.riotgames.com/riot/account/v1/accounts/by-riot-id/"
    api_url = f"{url_start}{region}{url_finish}{summoner_name}/{tag}?api_key={api_key}"
    summoner_puuid = None  # Initialize to ensure variable is defined

    try:
        resp_summoner = requests.get(api_url)
        resp_summoner.raise_for_status()  # This will raise an HTTPError for bad responses
        summoner_info = resp_summoner.json()
        summoner_puuid = summoner_info['puuid']
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except RequestException as req_err:
        print(f"Request exception occurred: {req_err}")
    return summoner_puuid

def get_match_list(summoner_puuid, region, api_key):
    url_start = "https://"
    url_middle = ".api.riotgames.com/lol/match/v5/matches/by-puuid/"
    url_finish = "/ids?type=ranked&start=0&count=20&api_key="

    match_list = []  # Initialize match_list as an empty list

    try:
        api_url = f"{url_start}{region}{url_middle}{summoner_puuid}{url_finish}{api_key}"
        resp_list = requests.get(api_url)
        resp_list.raise_for_status()  # This will raise an HTTPError for bad responses
        match_list = resp_list.json()  # Assign the actual list if the request is successful
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except RequestException as req_err:
        print(f"Request exception occurred: {req_err}")
    return match_list

def get_match_data(match_list, region, api_key):
    url_start = "https://"
    url_middle = ".api.riotgames.com/lol/match/v5/matches/"
    url_finish = "?api_key="
    
    all_match_data = []  # Initialize an empty list to store data for all matches

    for match_id in match_list:
        api_url = f"{url_start}{region}{url_middle}{match_id}{url_finish}{api_key}"
        try:
            resp_match = requests.get(api_url)
            resp_match.raise_for_status()  # This will raise an HTTPError for bad responses
            match_data = resp_match.json()
            all_match_data.append(match_data)  # Append the match data to the list
        except HTTPError as http_err:
            print(f"No se ha podido acceder a la API Match para el match ID {match_id} (response != 200): {http_err}")
        except ConnectionError as conn_err:
            print(f"No se pudo conectar con la API Matches para el match ID {match_id}: {conn_err}")
        except Timeout as timeout_err:
            print(f"Timeout error occurred for match ID {match_id}: {timeout_err}")
        except RequestException as req_err:
            print(f"Request exception occurred for match ID {match_id}: {req_err}")

    return all_match_data

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
