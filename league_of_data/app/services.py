from django.db import transaction
from .models import Summoner, Match, Graphic_data, Time_info
from .graphs_code.fn_data_api import (
    get_summoner_puuid, get_account_info, get_summoner_name, get_summoner_info, get_summoner_tag, get_list_ranked_info, get_ranked_info,
    get_match_list, get_match_data, get_summoner_index, get_summoner_data,
    get_summoner_id, get_league_points, get_total_wins, get_total_losses, get_rank, get_tier,
    get_kills, get_deaths, get_assists, get_goldEarned, get_totalDamageDealt, get_championId, get_championName,
    get_goldSpent, get_totalDamageTaken, get_totalHeal, get_totalHealsOnTeammates, get_totalMinionsKilled,
    get_totalTimeSpentDead, get_unitsHealed, get_visionScore, get_spell1Cast, get_spell2Cast, get_spell3Cast, get_spell4Cast,
    get_doubleKills, get_tripleKills, get_firstBloodAssist, get_firstBloodKill, get_individualPosition, 
    get_gameEndedInEarlySurrender, get_gameEndedInSurrender, get_wardKilled, get_wardsPlaced, get_role, get_lane, 
    get_participantId, get_win, get_timePlayed, get_killingSprees, get_longestTimeSpentLiving, get_match_minutes, get_time_info,
)
from django.core.exceptions import ValidationError

def validate_summoner_data(summ_info):


    required_fields = ['summoner_name', 'puuid', 'summoner_tag', 'region', 'summoner_id',
                        'league_points', 'total_wins', 'total_losses', 'rank', 'tier']
    
    if not summ_info:
        raise ValidationError("Account info is missing.")
    
    for field in required_fields:
        if field not in summ_info:
            raise ValidationError(f"Missing required summoner field: {field}")
        
        if not summ_info[field]:
            raise ValidationError(f"Empty value for required summoner field: {field}")
        
def validate_match_data(mtch_info):
    required_fields = ['participantId','summoner_id', 'match_id', 'championId', 'spell1Casts',
                        'spell2Casts', 'spell3Casts', 'spell4Casts', 'kills', 'deaths', 'assists',
                        'championName', 'goldEarned', 'goldSpent', 'totalDamageDealt', 'totalDamageTaken',
                        'totalHeal', 'totalHealsOnTeammates', 'totalMinionsKilled', 'totalTimeSpentDead',
                        'totalUnitsHealed', 'visionScore', 'wardKilled', 'wardPlaced', 'role', 'lane',
                        'doubleKills', 'tripleKills', 'firstBloodAssist', 'firstBloodKill', 'individualPosition',
                        'gameEndedInEarlySurrender', 'gameEndedInSurrender', 'win', 'timePlayed', 'killingSprees',
                        'longestTimeSpentLiving']
    
    if not mtch_info:
        raise ValidationError("Summoner match data is missing.")
    
    for field in required_fields:
        if field not in mtch_info:
            raise ValidationError(f"Missing required match field: {field}")
        
        if isinstance(mtch_info[field], (list, dict)) and not mtch_info[field]:
            raise ValidationError(f"Empty value for required match field: {field}")
        
        if field == 'participantId' and mtch_info[field] < 0:
            raise ValidationError("Invalid participant ID.")

def validate_time_info(time_info):
    required_fields = ['xp', 'gold', 'level', 'minions', 'damageTaken', 'damageDone', 'minuto']

    if not time_info:
        raise ValidationError("Time info is missing.")
    
    for field in required_fields:
        if field not in time_info:
            raise ValidationError(f"Missing required match field: {field}")
    if not time_info[field]:
            raise ValidationError(f"Empty value for required time_info field: {field}")
            
    

def save_summoner_matches_and_stats(summoner_name, summoner_tag, summoner_region, api_key):

    summ_info = {}

    account_info = get_account_info(summoner_name, summoner_tag, summoner_region, api_key)
    if not account_info:
        raise ValidationError("Account info could not be retrieved.")
    
    
    summoner_puuid = get_summoner_puuid(account_info)
    if not summoner_puuid:
        raise ValidationError("Summoner PUUID not found.")
    
    
    summoner_info = get_summoner_info(summoner_puuid, api_key)
    if not summoner_info:
        raise ValidationError("Account information could not be retrieved.")
    
    
    summoner_id = get_summoner_id(summoner_info)
    if not summoner_id:
        raise ValidationError("Summoner ID not found.")
    
    
    list_ranked_info = get_list_ranked_info(summoner_id, api_key)
    if not list_ranked_info:
        raise ValidationError("List ranked info could not be retrieved.")
    

    ranked_info = get_ranked_info(list_ranked_info) if list_ranked_info else None
    if not ranked_info:
        raise ValidationError("Ranked info could not be retrieved.")
    

    tier = get_tier(ranked_info) if ranked_info else None
    if not tier:
        raise ValidationError("Summoner tier not found.")
    

    rank = get_rank(ranked_info) if ranked_info else None
    if not rank:
        raise ValidationError("Summoner rank not found.")
    

    league_points = get_league_points(ranked_info) if ranked_info else None
    if not league_points:
        raise ValidationError("Summoner league points not found.")
    

    total_wins = get_total_wins(ranked_info) if ranked_info else None
    if not total_wins:
        raise ValidationError("Summoner total wins not found.")
    

    total_losses = get_total_losses(ranked_info) if ranked_info else None
    if not total_losses:
        raise ValidationError("Summoner total losses not found.")
    

    match_list = get_match_list(summoner_puuid, summoner_region, api_key)
    if not match_list:
        raise ValidationError("Match list could not be retrieved.")
    

    summ_info = {
        'summoner_name': summoner_name,
        'summoner_tag': summoner_tag,
        'region': summoner_region,
        'summoner_id': summoner_id,
        'puuid': summoner_puuid,
        'league_points': league_points,
        'total_wins': total_wins,
        'total_losses': total_losses,
        'rank': rank,
        'tier': tier
    }

    with transaction.atomic():
        
        validate_summoner_data(summ_info)

        summoner, _ = Summoner.objects.update_or_create(
            puuid=summoner_puuid,
            defaults={
                'summoner_id': summoner_id,
                'puuid': summoner_puuid,
                'summoner_name': summoner_name,
                'summoner_tag': summoner_tag,
                'region': summoner_region,
                'league_points': league_points,
                'total_wins': total_wins,
                'total_losses': total_losses,
                'rank': rank,
                'tier': tier,
            }
        )


        for match_id in match_list[:5]:
            match_data = get_match_data([match_id], summoner_region, api_key)
            if not match_data:
                print(f"No data found for match ID {match_id}")
                continue
            
            for match in match_data:
                summoner_index = get_summoner_index(match, summoner_puuid)
                
                summoner_data = get_summoner_data(match, summoner_index)

                kills = get_kills(summoner_data)
                deaths = get_deaths(summoner_data)
                assists = get_assists(summoner_data)
                champion_id = get_championId(summoner_data)
                champion_name = get_championName(summoner_data)
                gold_earned = get_goldEarned(summoner_data)
                gold_spendt = get_goldSpent(summoner_data)
                totalDamageDealt = get_totalDamageDealt(summoner_data)
                totalDamageTaken = get_totalDamageTaken(summoner_data)
                totalHeal = get_totalHeal(summoner_data)
                totalHealsOnTeammates = get_totalHealsOnTeammates(summoner_data)
                totalMinionsKilled = get_totalMinionsKilled(summoner_data)
                totalTimeSpentDead = get_totalTimeSpentDead(summoner_data)
                totalUnitsHealed = get_unitsHealed(summoner_data)
                visionScore = get_visionScore(summoner_data)
                wardKilled = get_wardKilled(summoner_data)
                wardPlaced = get_wardsPlaced(summoner_data)
                role = get_role(summoner_data)
                lane = get_lane(summoner_data)
                participantId = get_participantId(summoner_data)
                doubleKills = get_doubleKills(summoner_data)
                tripleKills = get_tripleKills(summoner_data)
                firstBloodAssist = get_firstBloodAssist(summoner_data)
                firstBloodKill = get_firstBloodKill(summoner_data)
                individualPosition = get_individualPosition(summoner_data)
                gameEndedInEarlySurrender = get_gameEndedInEarlySurrender(summoner_data)
                gameEndedInSurrender = get_gameEndedInSurrender(summoner_data)
                killingSprees = get_killingSprees(summoner_data)
                longestTimeSpentLiving = get_longestTimeSpentLiving(summoner_data)
                timePlayed = get_timePlayed(summoner_data)
                win = get_win(summoner_data)
                spell1Casts = get_spell1Cast(summoner_data)
                spell2Casts = get_spell2Cast(summoner_data)
                spell3Casts = get_spell3Cast(summoner_data)
                spell4Casts = get_spell4Cast(summoner_data)
                
                mtch_info = {
                    'match_id': match_id,
                    'summoner_id': summoner_id,
                    'participantId': participantId,
                    'championId': champion_id,
                    'championName': champion_name,
                    'win': win,
                    'timePlayed': timePlayed,
                    'spell1Casts': spell1Casts,
                    'spell2Casts': spell2Casts,
                    'spell3Casts': spell3Casts,
                    'spell4Casts': spell4Casts,
                    'longestTimeSpentLiving': longestTimeSpentLiving,
                    'killingSprees': killingSprees,
                    'individualPosition': individualPosition,
                    'gameEndedInEarlySurrender': gameEndedInEarlySurrender,
                    'gameEndedInSurrender': gameEndedInSurrender,
                    'kills': kills,
                    'deaths': deaths,
                    'assists': assists,
                    'goldSpent': gold_spendt,
                    'goldEarned': gold_earned,
                    'totalDamageDealt': totalDamageDealt,
                    'totalDamageTaken': totalDamageTaken,
                    'totalHeal': totalHeal,
                    'totalHealsOnTeammates': totalHealsOnTeammates,
                    'totalMinionsKilled': totalMinionsKilled,
                    'totalTimeSpentDead': totalTimeSpentDead,
                    'totalUnitsHealed': totalUnitsHealed,
                    'visionScore': visionScore,
                    'wardKilled': wardKilled,
                    'wardPlaced': wardPlaced,
                    'role': role,
                    'lane': lane,
                    'doubleKills': doubleKills,
                    'tripleKills': tripleKills,
                    'firstBloodAssist': firstBloodAssist,
                    'firstBloodKill': firstBloodKill,
                }

                
                validate_match_data(mtch_info)

                match_instance, _ = Match.objects.update_or_create(
                    summoner_id=summoner, api_match_id=match_id
                )

                Graphic_data.objects.update_or_create(
                    summoner_id=summoner,
                    match_id=match_instance,
                    defaults={
                        'kills': get_kills(summoner_data),
                        'deaths': get_deaths(summoner_data),
                        'assists': get_assists(summoner_data),                  
                        'championId': get_championId(summoner_data),
                        'championName': get_championName(summoner_data),
                        'goldEarned': get_goldEarned(summoner_data),
                        'goldSpent': get_goldSpent(summoner_data),
                        'totalDamageDealt': get_totalDamageDealt(summoner_data),
                        'totalDamageTaken': get_totalDamageTaken(summoner_data),
                        'totalHeal': get_totalHeal(summoner_data),
                        'totalHealsOnTeammates': get_totalHealsOnTeammates(summoner_data),
                        'totalMinionsKilled': get_totalMinionsKilled(summoner_data),
                        'totalTimeSpentDead': get_totalTimeSpentDead(summoner_data),
                        'totalUnitsHealed': get_unitsHealed(summoner_data),
                        'visionScore': get_visionScore(summoner_data),
                        'wardKilled': get_wardKilled(summoner_data),
                        'wardPlaced': get_wardsPlaced(summoner_data),
                        'role': get_role(summoner_data),
                        'lane': get_lane(summoner_data),
                        'participantId': get_participantId(summoner_data),
                        'doubleKills': get_doubleKills(summoner_data),
                        'tripleKills': get_tripleKills(summoner_data),
                        'firstBloodAssist': get_firstBloodAssist(summoner_data),
                        'firstBloodKill': get_firstBloodKill(summoner_data),
                        'win': get_win(summoner_data),
                        'timePlayed': get_timePlayed(summoner_data),
                        'spell1Casts': get_spell1Cast(summoner_data),
                        'spell2Casts': get_spell2Cast(summoner_data),
                        'spell3Casts': get_spell3Cast(summoner_data),
                        'spell4Casts': get_spell4Cast(summoner_data),
                        'longestTimeSpentLiving': get_longestTimeSpentLiving(summoner_data),
                        'killingSprees': get_killingSprees(summoner_data),
                        'individualPosition': get_individualPosition(summoner_data),
                        'gameEndedInEarlySurrender': get_gameEndedInEarlySurrender(summoner_data),
                        'gameEndedInSurrender': get_gameEndedInSurrender(summoner_data)
                    }
                )
                
                time_info = get_time_info(match_id, api_key, summoner_region,)
                if not time_info:
                    print(f"No time data found for match ID {match_id}")
                    continue

                minutes = get_match_minutes(time_info)
                minutes_list = range(minutes)
                summoner_position = f"{summoner_index + 1}"
                time_damageDone = 0
                time_damageTaken = 0
                time_level = 0
                time_minions = 0
                time_gold = 0
                time_xp = 0
                min = 0

                for i in minutes_list:
                    summoner_time_info = time_info[i]['participantFrames'][summoner_position]
                    min = i+1
                    time_damageDone = summoner_time_info['damageStats']['totalDamageDoneToChampions']
                    time_damageTaken = summoner_time_info['damageStats']['totalDamageTaken']
                    time_level = summoner_time_info['level']
                    time_minions = summoner_time_info['minionsKilled']
                    time_gold = summoner_time_info['totalGold']
                    time_xp = summoner_time_info['xp']

                    tm_info = {
                        'minuto': min,
                        'damageDone': time_damageDone,
                        'damageTaken': time_damageTaken,
                        'level': time_level,
                        'minions': time_minions,
                        'gold': time_gold,
                        'xp': time_xp
                    }
                    validate_time_info(tm_info)

                    time_info_instance, _ = Time_info.objects.update_or_create(
                    match_id = match_instance,
                    minute = min,
                    defaults={
                        'damageDone': time_damageDone,
                        'damageTaken': time_damageTaken,
                        'gold': time_gold,
                        'xp': time_xp,
                        'minions': time_minions,
                        'level': time_level
                    }
                )


    
    
   
    

        

        
        