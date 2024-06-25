from django.db import transaction
from .models import Summoner, Match, Graphic_data, Time_info
from .graphs_code.fn_data_api import (
    get_summoner_puuid, get_account_info, get_summoner_info, get_match_minutes, get_list_ranked_info, get_ranked_info,
    get_match_data, get_summoner_index, get_summoner_data,
    get_summoner_id, get_league_points, get_total_wins, get_total_losses, get_rank, get_tier,
    get_kills, get_deaths, get_assists, get_goldEarned, get_totalDamageDealt, get_championName,
    get_totalDamageTaken, get_role, get_lane, get_win, get_match_minutes, get_time_info, 
    get_participants, get_participants_info, get_profile_icon
)
from django.core.exceptions import ValidationError
import requests
import logging

logger = logging.getLogger(__name__)

def validate_summoner_data(summ_info):


    required_fields = ['summoner_name', 'puuid', 'summoner_tag', 'region', 'summoner_id',
                        'league_points', 'total_wins', 'total_losses', 'rank', 'tier', 'profile_icon', 'server']
    
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
    required_fields = ['match_id', 'xp', 'gold', 'level', 'minions', 'damageTaken', 'damageDone', 'minute', 'summoner_id']

    if not time_info:
        raise ValidationError("Time info is missing.")

    for field in required_fields:
        if field not in time_info:
            raise ValidationError(f"Missing required time info field: {field}")
        if time_info[field] is None or (isinstance(time_info[field], (list, dict)) and not time_info[field]):
            raise ValidationError(f"Empty or invalid value for required time_info field: {field}")        
    

def validate_summoner(request, summoner_name, summoner_tag, summoner_region, api_key, summoner_server):
    try:
        account_info = get_account_info(request, summoner_name, summoner_tag, summoner_region, api_key)
        #print(account_info)
        if not account_info:
            raise ValidationError("Account info could not be retrieved.")
        #print(account_info)
        summoner_puuid = get_summoner_puuid(account_info)
        if not summoner_puuid:
            raise ValidationError("Summoner PUUID not found.")

        summoner_info = get_summoner_info(summoner_puuid, api_key, summoner_server)
        if not summoner_info:
            raise ValidationError("Account information could not be retrieved.")

        summoner_id = get_summoner_id(summoner_info)
        #print(summoner_id)
        if not summoner_id:
            raise ValidationError("Summoner ID not found.")
        
        profile_icon = get_profile_icon(summoner_info) if summoner_info else None
        if not profile_icon:
            raise ValidationError("Summoner profile icon not found.")
        #print(profile_icon)

        list_ranked_info = get_list_ranked_info(summoner_id, api_key, summoner_server)
        if not list_ranked_info:
            raise ValidationError("List ranked info could not be retrieved.")

        ranked_info = get_ranked_info(list_ranked_info) if list_ranked_info else None
        #print(ranked_info)
        if not ranked_info:
            raise ValidationError("Ranked info could not be retrieved.")

        tier = get_tier(ranked_info) if ranked_info else None
        #print(tier)
        if not tier:
            raise ValidationError("Summoner tier not found.")

        rank = get_rank(ranked_info) if ranked_info else None
        #print(rank)
        if not rank:
            raise ValidationError("Summoner rank not found.")

        league_points = get_league_points(ranked_info) if ranked_info else None
        #print(league_points)
        if not league_points:
            raise ValidationError("Summoner league points not found.")

        total_wins = get_total_wins(ranked_info) if ranked_info else None
        #print(total_wins)
        if not total_wins:
            raise ValidationError("Summoner total wins not found.")

        total_losses = get_total_losses(ranked_info) if ranked_info else None
        #print(total_losses)
        if not total_losses:
            raise ValidationError("Summoner total losses not found.")
        
        
    
    except requests.exceptions.RequestException as e:
        # This captures any network related errors
        raise ValidationError(f"Network error occurred: {str(e)}")

    except Exception as e:
        # General exception for any other errors
        raise ValidationError(f"An unexpected error occurred: {str(e)}")

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
        'tier': tier,
        'profile_icon': profile_icon,
        'server': summoner_server
    }
    #print(summ_info)
    validate_summoner_data(summ_info)

    return summ_info

def save_summoner_info(summoner_puuid, summ_info):
    with transaction.atomic():
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
                existing_summoner.profile_icon != summ_info['profile_icon']
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
    #print(summoner)
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
    try:
        summoner = Summoner.objects.get(summoner_name=summoner_name)
        match_data = get_match_data(match_id, summoner.region, api_key)
        participants = get_participants(match_data)
        summoner_index = get_summoner_index(participants, summoner.puuid)
        summoner_index = f"{summoner_index +1}"
        time_info = get_time_info(match_id, api_key, summoner.region)

        if not time_info:
            logger.error(f"No time info available for match {match_id}")
            raise ValueError("No time info available for match {}".format(match_id))

        minutes = [int(minute) for minute in get_match_minutes(time_info)]
        match = Match.objects.filter(api_match_id = match_id).first()
        all_match_time_info = []

        with transaction.atomic():
            for min in minutes:
                summoner_time_info = time_info[min]['participantFrames'][summoner_index]
                match_time_info = {
                    'match_id': int(match.id),
                    'summoner_id': summoner.id,
                    'damageDone': summoner_time_info['damageStats']['totalDamageDone'],
                    'damageTaken': summoner_time_info['damageStats']['totalDamageTaken'],
                    'gold': summoner_time_info['totalGold'],
                    'xp': summoner_time_info['xp'],
                    'minions': summoner_time_info['minionsKilled'],
                    'level': summoner_time_info['level'],
                    'minute': min
                }
                logger.debug(f"Processing minute {min}: {match_time_info}")
                validate_time_info(match_time_info)
                all_match_time_info.append(match_time_info)
        #print(all_match_time_info)
        return all_match_time_info

    except Summoner.DoesNotExist:
        logger.exception("Summoner not found with name {}".format(summoner_name))
        raise ValueError("Summoner not found with name {}".format(summoner_name))
    except KeyError as e:
        logger.exception("Key error in processing time info: {}".format(e))
        raise ValueError("Key error in processing time info: {}".format(e))
    except Exception as e:
        logger.exception("An unexpected error occurred: {}".format(e))
        raise SystemError("An unexpected error occurred: {}".format(e))


def save_matches_stats(summoner, match_id, summoner_data):
    print(f"League of Data: Guardando los datos de {summoner.summoner_name} en la base de datos.")
    with transaction.atomic():
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

def save_time_info(match_id, time_data, summoner):
    for time in time_data:
        with transaction.atomic():
            match_instance = Match.objects.get(api_match_id=match_id)
            if not match_instance:
                raise ValueError(f"No Match found with id {match_id}")
            Time_info.objects.update_or_create(
                match_id=match_instance,
                minute=time['minute'],
                defaults={
                    'damageDone': time['damageDone'],
                    'damageTaken': time['damageTaken'],
                    'gold': time['gold'],
                    'xp': time['xp'],
                    'minions': time['minions'],
                    'level': time['level'],
                    'summoner_id': summoner
                }
            )

def calculate_winrate(summoner):
    if summoner.total_wins + summoner.total_losses == 0:
        return 0  # Evita la división por cero si no hay partidas jugadas
    winrate = (summoner.total_wins / (summoner.total_wins + summoner.total_losses)) * 100
    return winrate


    
    
   
    

        

        
        