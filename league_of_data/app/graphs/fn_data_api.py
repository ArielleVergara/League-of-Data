import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException


def get_summoner_puuid(summoner_name, tag, region, api_key):
    url_start = "https://"
    url_finish = ".api.riotgames.com/riot/account/v1/accounts/by-riot-id/"
    api_url = f"{url_start}{region}{url_finish}{summoner_name}/{tag}?api_key={api_key}"
    summoner_puuid = None

    try:
        resp_summoner = requests.get(api_url)
        resp_summoner.raise_for_status()
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

def get_account_info (summoner_puuid, api_key):
    url_start = "https://"
    url_middle = "la2.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/"
    url_finish = "?api_key="

    api_url = f"{url_start}{url_middle}{summoner_puuid}{url_finish}{api_key}"
    account_info = None

    try:
        resp_account = requests.get(api_url)
        resp_account.raise_for_status()
        account_info = resp_account.json()
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except RequestException as req_err:
        print(f"Request exception occurred: {req_err}")
    return account_info

def get_summoner_id (account_info):
    summoner_id = account_info['id']
    return summoner_id

def get_list_ranked_info (summoner_id, api_key):
    url_start = "https://"
    url_middle = "la2.api.riotgames.com/lol/league/v4/entries/by-summoner-id/"
    url_finish = "?api_key="

    api_url = f"{url_start}{url_middle}{summoner_id}{url_finish}{api_key}"

    list_ranked_info = None

    try:
        resp_ranked = requests.get(api_url)
        resp_ranked.raise_for_status()
        list_ranked_info = resp_ranked.json()
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except RequestException as req_err:
        print(f"Request exception occurred: {req_err}")
    return list_ranked_info

def get_ranked_info (list_ranked_info):
    ranked_info = list_ranked_info[0]
    return ranked_info

def get_tier (ranked_info):
    tier = ranked_info['tier']
    return tier

def get_rank (ranked_info):
    rank = ranked_info['rank']
    return rank

def get_league_points (ranked_info):
    league_points = ranked_info['leaguePoints']
    return league_points

def get_total_wins (ranked_info):
    total_wins = ranked_info['wins']
    return total_wins

def get_total_losses (ranked_info):
    total_losses = ranked_info['losses']
    return total_losses

def get_match_list(summoner_puuid, region, api_key):
    url_start = "https://"
    url_middle = ".api.riotgames.com/lol/match/v5/matches/by-puuid/"
    url_finish = "/ids?type=ranked&start=0&count=20&api_key="

    match_list = []

    try:
        api_url = f"{url_start}{region}{url_middle}{summoner_puuid}{url_finish}{api_key}"
        resp_list = requests.get(api_url)
        resp_list.raise_for_status()
        match_list = resp_list.json()
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
    
    all_match_data = []

    for match_id in match_list:
        api_url = f"{url_start}{region}{url_middle}{match_id}{url_finish}{api_key}"
        try:
            resp_match = requests.get(api_url)
            resp_match.raise_for_status()
            match_data = resp_match.json()
            all_match_data.append(match_data)
        except HTTPError as http_err:
            print(f"No se ha podido acceder a la API Match para el match ID {match_id} (response != 200): {http_err}")
        except ConnectionError as conn_err:
            print(f"No se pudo conectar con la API Matches para el match ID {match_id}: {conn_err}")
        except Timeout as timeout_err:
            print(f"Timeout error occurred for match ID {match_id}: {timeout_err}")
        except RequestException as req_err:
            print(f"Request exception occurred for match ID {match_id}: {req_err}")

    return all_match_data

def get_summoner_index(all_match_data, summoner_puuid):
    summoner_index = all_match_data['metadata']['participants'].index(summoner_puuid)
    return summoner_index

def get_summoner_data(all_match_data, summoner_index):
    summoner_data = all_match_data['info']['participants'][summoner_index]
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

def get_totalHeal (summoner_data):
    summoner_totalHeal = summoner_data['totalHeal']
    return summoner_totalHeal

def get_totalHealsOnTeammates (summoner_data):
    summoner_totalHealsOnTeammates = summoner_data['totalHealsOnTeammates']
    return summoner_totalHealsOnTeammates

def get_totalMinionsKilled (summoner_data):
    summoner_totalMinionsKilled = summoner_data['totalMinionsKilled']
    return summoner_totalMinionsKilled

def get_totalTimeSpentDead (summoner_data):
    summoner_totalTimeSpentDead = summoner_data['totalTimeSpentDead']
    return summoner_totalTimeSpentDead

def get_unitsHealed (summoner_data):
    summoner_unitsHealed = summoner_data['unitsHealed']
    return summoner_unitsHealed

def get_visionScore (summoner_data):
    summoner_visionScore = summoner_data['visionScore']
    return summoner_visionScore

def get_wardKilled (summoner_data):
    summoner_wardKilled = summoner_data['wardKilled']
    return summoner_wardKilled

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

def get_tripleKills(summoner_data):
    summoner_tripleKills = summoner_data['tripleKills']
    return summoner_tripleKills

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

def get_spell1Cast(summoner_data):
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
