from django.db import transaction
from .models import Summoner, Match, Graphic_data, Time_info
from league_of_data import settings
from .graphs_code.fn_data_api import (
    get_summoner_puuid, get_account_info, get_summoner_name, get_summoner_info, get_match_minutes, get_list_ranked_info, get_ranked_info,
    get_match_list, get_match_data, get_summoner_index, get_summoner_data,
    get_summoner_id, get_league_points, get_total_wins, get_total_losses, get_rank, get_tier,
    get_kills, get_deaths, get_assists, get_goldEarned, get_totalDamageDealt, get_championId, get_championName,
    get_goldSpent, get_totalDamageTaken, get_totalHeal, get_totalHealsOnTeammates, get_totalMinionsKilled,
    get_totalTimeSpentDead, get_unitsHealed, get_visionScore, get_spell1Cast, get_spell2Cast, get_spell3Cast, get_spell4Cast,
    get_doubleKills, get_tripleKills, get_firstBloodAssist, get_firstBloodKill, get_individualPosition, 
    get_gameEndedInEarlySurrender, get_gameEndedInSurrender, get_wardKilled, get_wardsPlaced, get_role, get_lane, 
    get_participantId, get_win, get_timePlayed, get_killingSprees, get_longestTimeSpentLiving, get_match_minutes, get_time_info, 
    get_participants, get_participants_info
)
from django.core.exceptions import ValidationError
import requests


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
        
def validate_match_data(match_details):
    required_fields = ['match_id', 'kills', 'deaths', 'assists', 'championName', 'goldEarned',
                        'totalDamageDealt', 'totalDamageTaken', 'role', 'lane','win']
    
    if not match_details:
        raise ValidationError("Summoner match data is missing.")
    
    for field in required_fields:
        if field not in match_details:
            raise ValidationError(f"Missing required match field: {field}")
        
        if isinstance(match_details[field], (list, dict)) and not match_details[field]:
            raise ValidationError(f"Empty value for required match field: {field}")
        if field == 'participantId' and match_details[field] < 0:
            raise ValidationError("Invalid participant ID.")

def validate_time_info(time_info):
    required_fields = ['xp', 'gold', 'level', 'minions', 'damageTaken', 'damageDone']

    if not time_info:
        raise ValidationError("Time info is missing.")
    
    for field in required_fields:
        if field not in time_info:
            raise ValidationError(f"Missing required match field: {field}")
    if not time_info[field]:
            raise ValidationError(f"Empty value for required time_info field: {field}")
            
    

def validate_summoner(summoner_name, summoner_tag, summoner_region, api_key):
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

    validate_summoner_data(summ_info)

    return summ_info

def save_summoner_info(summoner_puuid, summ_info):
    try:
        existing_summoner = Summoner.objects.get(puuid=summoner_puuid)
        needs_update = any([
            existing_summoner.summoner_name != summ_info['summoner_name'],
            existing_summoner.summoner_tag != summ_info['summoner_tag'],
            existing_summoner.region != summ_info['region'],
            existing_summoner.summoner_id != summ_info['summoner_id'],
            existing_summoner.puuid != summ_info['puuid'],
            existing_summoner.league_points != summ_info['league_points'],
            existing_summoner.total_wins != summ_info['total_wins'],
            existing_summoner.total_losses != summ_info['total_losses'],
            existing_summoner.rank != summ_info['rank'],
            existing_summoner.tier != summ_info['tier'],
        ])
    except Summoner.DoesNotExist:
        existing_summoner = None
        needs_update = True

    if needs_update:
        summoner, _ = Summoner.objects.update_or_create(
            puuid=summoner_puuid,
            defaults=summ_info
        )
        return summoner
    else:
        return existing_summoner

def get_summoner_stats(summoner, match_id, api_key):
    #print(match_id)
    match_data = get_match_data(match_id, summoner.region, api_key)
    #print(match_data)
    if match_data:
        participants = get_participants(match_data)
        #print(participants)
        participant_info = get_participants_info(match_data)
        #print(participant_info)
        summoner_index = get_summoner_index(participants, summoner.puuid)
        #print(summoner_index)
        summoner_data = get_summoner_data(participant_info, summoner_index)
        #print(summoner_data)
        
        try:
            match_details = {
                'match_id': match_id,
                'championName': get_championName(summoner_data),
                'kills': get_kills(summoner_data),
                'assists': get_assists(summoner_data),
                'deaths': get_deaths(summoner_data),
                'goldEarned': get_goldEarned(summoner_data),
                'totalDamageDealt': get_totalDamageDealt(summoner_data),
                'totalDamageTaken': get_totalDamageTaken(summoner_data),
                'role': get_role(summoner_data),
                'lane': get_lane(summoner_data),
                'win': get_win(summoner_data),
            }
            #print(match_details)
            validate_match_data(match_details)
            if match_details:
                return match_details
                #print(all_match_details)
            else:
                print(f"No match_details for match {match_id}")
        except ValidationError as e:
            print(f"Validation error for match {match_id}: {str(e)}")
    

def send_time_info(match_id, api_key, summoner_name):
    #print(match_id)
    #print(api_key)
    #print(summoner_name)
    try:
        summoner = Summoner.objects.filter(summoner_name=summoner_name).first()
        if not summoner:
            print(f"No summoner found with name {summoner_name}")
    except Exception as e:
        print(f"Error retrieving summoner: {str(e)}")
    try:
        time_info = get_time_info(match_id, api_key, summoner.region)
        #print(time_info)
        if not time_info:
            print(f"No time info available for match {match_id}")
            return None
    except Exception as e:
        print(f"Error retrieving time info: {str(e)}")
        return None

    try:
        match_data = get_match_data(match_id, summoner.region, api_key)
        if not match_data:
            print(f"No match data available for match {match_id}")
            return None
        participants = get_participants(match_data)
        if not participants:
            print(f"No participants available for match {match_id}")
            return None
        summoner_index = get_summoner_index(participants, summoner.puuid)
        if not summoner_index:
            print(f"No summoner index available for match {match_id}")
            return None
        minutes = [int(minute) for minute in get_match_minutes(time_info)]
        if not minutes:
            print(f"No minutes available for match {match_id}")
            return None
    except Exception as e:
        print(f"Error processing match data: {str(e)}")
    
    match = Match.objects.filter(api_match_id=match_id).first() 
    all_match_time_info = []
    try:
        for min in minutes:
            try:
                summoner_time_info = time_info[min]['participantFrames'][str(summoner_index)]
                #print(summoner_time_info)
                #print(summoner_time_info['damageStats']['totalDamageDone'])
                match_time_info = {
                    'match_id': match.id,
                    'damageDone': summoner_time_info['damageStats']['totalDamageDone'],
                    'damageTaken': summoner_time_info['damageStats']['totalDamageTaken'],
                    'gold': summoner_time_info['totalGold'],
                    'xp': summoner_time_info['xp'],
                    'minions': summoner_time_info['minionsKilled'],
                    'level': summoner_time_info['level'],
                    'minuto': min
                }
                #print(match_time_info)
                validate_time_info(match_time_info)
                all_match_time_info.append(match_time_info)
            except Exception as e:
                print(f"Error during processing time info for minuto {min}: {str(e)}")
                continue
    except Exception as e:
        print(f"General error in processing time data: {str(e)}")
        return None

    if all_match_time_info:
        try:
            save_time_info(match, all_match_time_info)
        except Exception as e:
            print(f"Error saving time info: {str(e)}")
            return None

    return all_match_time_info


def save_matches_stats(summoner, match_id, summoner_data):
    #print(summoner_data)
    #print(summoner)
    #print(match_id)
    match_instance, _ = Match.objects.update_or_create(
        summoner_id=summoner, api_match_id=match_id
    )

    Graphic_data.objects.update_or_create(
        summoner_id=summoner,
        match_id=match_instance,
        defaults={
            'kills': summoner_data['kills'],
            'deaths': summoner_data['deaths'],
            'assists': summoner_data['assists'],
            'championName': summoner_data['championName'],
            'goldEarned': summoner_data['goldEarned'],
            'totalDamageDealt': summoner_data['totalDamageDealt'],
            'totalDamageTaken': summoner_data['totalDamageTaken'],
            'role': summoner_data['role'],
            'lane': summoner_data['lane'],
            'win': summoner_data['win'],
        }
    )

def save_time_info(match_instance, time_info):
    for minute_info in time_info:
        Time_info.objects.update_or_create(
            match_id=match_instance,
            minute=minute_info['minuto'],
            defaults={
                'damageDone': minute_info['damageDone'],
                'damageTaken': minute_info['damageTaken'],
                'gold': minute_info['gold'],
                'xp': minute_info['xp'],
                'minions': minute_info['minions'],
                'level': minute_info['level']
            }
        )


    
    
   
    

        

        
        