from django import forms

region_choices = [
    ("AMERICAS", "Americas"),
    ("ASIA", "Asia"),
    ("ESPORTS", "Esports"),
    ("EUROPE", "Europa")
]

server_choices = [
    ("LA1", "LA1"),
    ("LA2", "LA2"),
    ("BR1", "BR1"),
    ("EUN1", "EUN1"),
    ("JP1", "JP1"),
    ("KR", "KR"),
    ("RU", "RU"),
    ("NA1", "NA1"),
    ("TR1", "TR1"),
    ("OC1", "OC1"),
    ("PH2", "PH2"),
    ("SG2", "SG2"),
    ("TH2", "TH2"),
    ("TW2", "TW2"),
    ("VN2", "VN2")
]

class summoner_form(forms.Form):
    summoner_name = forms.CharField(label='Nombre Invocador', max_length=100)
    summoner_tag = forms.CharField(label='Tag Invocador', max_length=100)
    summoner_region = forms.ChoiceField(label='Región', choices= region_choices)
    summoner_server = forms.ChoiceField(label='Servidor', choices= server_choices)

class summoner_compare_form(forms.Form):
    summoner1_name = forms.CharField(label='Nombre Invocador 1', max_length=100)
    summoner1_tag = forms.CharField(label='Tag Invocador 1', max_length=100)
    summoner1_region = forms.ChoiceField(label='Región 1', choices= region_choices)
    summoner1_server = forms.ChoiceField(label='Servidor 1', choices= server_choices)
    summoner2_name = forms.CharField(label='Nombre Invocador 2', max_length=100)
    summoner2_tag = forms.CharField(label='Tag Invocador 2', max_length=100)
    summoner2_region = forms.ChoiceField(label='Región 2', choices= region_choices)
    summoner2_server = forms.ChoiceField(label='Servidor 2', choices= server_choices)