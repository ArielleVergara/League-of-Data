from django.db import models

class Summoner (models.Model):
    summoner_id = models.CharField(max_length=255)
    puuid = models.CharField(max_length=255, default=None)
    summoner_name = models.CharField(max_length=255, default=None)
    summoner_tag = models.CharField(max_length=255, default=None)
    region = models.CharField(max_length=30, default=None)
    league_points = models.IntegerField (verbose_name= 'ranked points', default=None)
    total_wins = models.IntegerField (verbose_name= 'total wins', default=None)
    total_losses = models.IntegerField (verbose_name= 'total losses', default=None)
    rank = models.CharField(max_length=255, default=None)
    tier = models.CharField(max_length=255, default=None)
    profile_icon = models.IntegerField (verbose_name= 'ícono de cuenta', default=None)
    server = models.CharField(max_length=255, default=None)

class Match (models.Model):
    summoner_id = models.ForeignKey(Summoner, on_delete=models.CASCADE)
    api_match_id = models.CharField(max_length=255)

class Graphic_data (models.Model):
    summoner_id = models.ForeignKey(Summoner, on_delete=models.CASCADE)
    match_id = models.ForeignKey(Match, on_delete=models.CASCADE)
    kills = models.IntegerField (verbose_name= 'asesinatos del jugador', default=None)
    deaths = models.IntegerField (verbose_name= 'muertes del jugador', default=None)
    assists = models.IntegerField (verbose_name= 'asistencias del jugador', default=None)
    championName = models.CharField(max_length=255, default=None)
    goldEarned = models.IntegerField (verbose_name= 'oro ganado', default=None)
    totalDamageDealt = models.IntegerField (verbose_name= 'daño total', default=None)
    totalDamageTaken = models.IntegerField (verbose_name= 'daño total recibido', default=None)
    role = models.CharField(max_length=255, default=None)
    lane = models.CharField(max_length=255, default=None)
    win = models.BooleanField (verbose_name= 'victoria', default=None)

class Time_info (models.Model):
    match_id = models.ForeignKey(Match, on_delete=models.CASCADE)
    summoner_id = models.ForeignKey(Summoner, on_delete=models.CASCADE, default=None)
    minute = models.IntegerField(verbose_name='minuto de la partida', default=None)
    damageDone = models.IntegerField(verbose_name= 'daño hecho', default=None)
    damageTaken = models.IntegerField(verbose_name= 'daño tomado', default=None)
    gold = models.IntegerField(verbose_name= 'oro', default=None)
    xp = models.IntegerField(verbose_name= 'xp', default=None)
    minions = models.IntegerField(verbose_name= 'farm', default=None)
    level = models.IntegerField(verbose_name= 'nivel', default=None)

