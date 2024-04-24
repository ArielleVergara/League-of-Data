from django import forms

region_choices = {
    "AMERICAS": "Americas",
    "ASIA" : "Asia",
    "ESPORTS" : "Esports",
    "EUROPE" : "Europa"
}

class summoner_form(forms.Form):
    summoner_name = forms.CharField(label='Summoner name', max_length=100)
    summoner_tag = forms.CharField(label='Summoner tag', max_length=100)
    summoner_region = forms.ChoiceField(label='Summoner Region', choices= region_choices)