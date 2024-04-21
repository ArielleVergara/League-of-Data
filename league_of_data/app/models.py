from django.db import models

class Summoner (models.Model):
    puuid = models.CharField(max_length=255)
    api_summoner_id = models.CharField(max_length=255)
    region = models.CharField(max_length=30, default=None)

class Match (models.Model):
    summoner_id = models.ForeignKey(Summoner, on_delete=models.CASCADE)
    api_match_id = models.CharField(max_length=255)

class Graphic_data (models.Model):
    summoner_id = models.ForeignKey(Summoner, on_delete=models.CASCADE)
    match_id = models.ForeignKey(Match, on_delete=models.CASCADE)
    kills = models.IntegerField (verbose_name= 'asesinatos del jugador', default=None)
    deaths = models.IntegerField (verbose_name= 'muertes del jugador', default=None)
    assists = models.IntegerField (verbose_name= 'asistencias del jugador', default=None)
    gold = models.IntegerField (verbose_name= 'oro del jugador', default=None)
    experience = models.IntegerField (verbose_name= 'experiencia del jugador', default=None)
    damage = models.IntegerField (verbose_name= 'daño del jugador', default=None)