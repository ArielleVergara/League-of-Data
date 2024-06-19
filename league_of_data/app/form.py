from django import forms

region_choices = {
    "AMERICAS": "Americas",
    "ASIA" : "Asia",
    "ESPORTS" : "Esports",
    "EUROPE" : "Europa"
}

class summoner_form(forms.Form):
    summoner_name = forms.CharField(label='Nombre Invocador', max_length=100)
    summoner_tag = forms.CharField(label='Tag Invocador', max_length=100)
    summoner_region = forms.ChoiceField(label='Región', choices= region_choices)

class summoner_compare_form(forms.Form):
    summoner1_name = forms.CharField(label='Nombre Invocador 1', max_length=100)
    summoner1_tag = forms.CharField(label='Tag Invocador 1', max_length=100)
    summoner1_region = forms.ChoiceField(label='Región 1', choices= region_choices)
    summoner2_name = forms.CharField(label='Nombre Invocador 2', max_length=100)
    summoner2_tag = forms.CharField(label='Tag Invocador 2', max_length=100)
    summoner2_region = forms.ChoiceField(label='Región 2', choices= region_choices)