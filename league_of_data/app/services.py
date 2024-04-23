from django.db import transaction
from .models import Summoner, Match, Graphic_data
from .graphs.fn_data_api import (
    get_summoner_puuid, get_account_info, get_list_ranked_info, get_ranked_info,
    get_match_list, get_match_data, get_summoner_index, get_summoner_data,
    get_summoner_id, get_league_points, get_total_wins, get_total_losses, get_rank, get_tier,
    get_kills, get_deaths, get_assists, get_goldEarned, get_totalDamageDealt, get_championId, get_championName,
    get_goldSpent, get_totalDamageTaken, get_totalHeal, get_totalHealsOnTeammates, get_totalMinionsKilled,
    get_totalTimeSpentDead, get_unitsHealed, get_visionScore, get_spell1Cast, get_spell2Cast, get_spell3Cast, get_spell4Cast,
    get_doubleKills, get_tripleKills, get_firstBloodAssist, get_firstBloodKill, get_individualPosition, 
    get_gameEndedInEarlySurrender, get_gameEndedInSurrender, get_wardKilled, get_wardsPlaced, get_role, get_lane, 
    get_participantId, get_win, get_timePlayed, get_killingSprees, get_longestTimeSpentLiving
)
from django.core.exceptions import ValidationError

def validate_summoner_data(account_info):
    required_fields = ['id', 'accountId', 'puuid', 'name', 'summonerLevel']
    
    if not account_info:
        raise ValidationError("Account info is missing.")
    
    for field in required_fields:
        if field not in account_info:
            raise ValidationError(f"Missing required summoner field: {field}")
        
        if not account_info[field]:
            raise ValidationError(f"Empty value for required summoner field: {field}")
        
def validate_match_data(summoner_data):
    required_fields = ['participantId', 'championId', 'spell1Id', 'spell2Id', 'stats', 'teamId']
    
    if not summoner_data:
        raise ValidationError("Summoner match data is missing.")
    
    for field in required_fields:
        if field not in summoner_data:
            raise ValidationError(f"Missing required match field: {field}")
        
        if isinstance(summoner_data[field], (list, dict)) and not summoner_data[field]:
            raise ValidationError(f"Empty value for required match field: {field}")
        
        if field == 'participantId' and summoner_data[field] < 0:
            raise ValidationError("Invalid participant ID.")


def save_summoner_matches_and_stats(summoner_name, summoner_tag, summoner_region, api_key):
    summoner_puuid = get_summoner_puuid(summoner_name, summoner_tag, summoner_region, api_key)
    if not summoner_puuid:
        raise ValidationError("Summoner PUUID not found.")
    account_info = get_account_info(summoner_puuid, api_key)
    if not account_info:
        raise ValidationError("Account information could not be retrieved.")

    summoner_id = get_summoner_id(account_info)
    if not summoner_id:
        raise ValidationError("Summoner ID not found.")
    list_ranked_info = get_list_ranked_info(summoner_id, api_key)
    if not list_ranked_info:
        raise ValidationError("List ranked info could not be retrieved.")
    ranked_info = get_ranked_info(list_ranked_info) if list_ranked_info else None
    if not ranked_info:
        raise ValidationError("Ranked info could not be retrieved.")

    match_list = get_match_list(summoner_puuid, summoner_region, api_key)
    if not match_list:
        raise ValidationError("Match list could not be retrieved.")

    with transaction.atomic():
        
        validate_summoner_data(account_info)

        summoner, _ = Summoner.objects.update_or_create(
            puuid=summoner_puuid,
            defaults={
                'summoner_name': summoner_name,
                'summoner_tag': summoner_tag,
                'region': summoner_region,
                # Update with ranked info if available
                'league_points': get_league_points(ranked_info) if ranked_info else 0,
                'total_wins': get_total_wins(ranked_info) if ranked_info else 0,
                'total_losses': get_total_losses(ranked_info) if ranked_info else 0,
                'rank': get_rank(ranked_info) if ranked_info else '',
                'tier': get_tier(ranked_info) if ranked_info else '',
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

                validate_match_data(summoner_data)

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
                        'gold': get_goldEarned(summoner_data),
                        'damage': get_totalDamageDealt(summoner_data),                   
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
                        'spell2Casts': get_spell2Cast(summoner_data),  # Ensure this matches your function name
                        'spell3Casts': get_spell3Cast(summoner_data),
                        'spell4Casts': get_spell4Cast(summoner_data),
                        'longestTimeSpentLiving': get_longestTimeSpentLiving(summoner_data),
                        'killingSprees': get_killingSprees(summoner_data),
                        'individualPosition': get_individualPosition(summoner_data),
                        'gameEndedInEarlySurrender': get_gameEndedInEarlySurrender(summoner_data),
                        'gameEndedInSurrender': get_gameEndedInSurrender(summoner_data),
                    }
                )