import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns


def extract_data(time_info):
    sorted_time_info = sorted(time_info, key=lambda x: (x.match_id.id, x.minute))
    data_list = []
    for obj in sorted_time_info:
        data = {
            'minuto': obj.minute,
            'damageDone': obj.damageDone,
            'damageTaken': obj.damageTaken, 
            'level': obj.level,
            'minions': obj.minions, 
            'gold': obj.gold,
            'xp': obj.xp, 
            'match_id': obj.match_id 
        }
        data_list.append(data)
    return data_list

def generate_graphs(time_info, match_id):
    data_list = extract_data(time_info)
    if not data_list:
        print(f"No hay datos en time_info para la partida {match_id} ")
        return None
    
    try:
        df = pd.DataFrame(data_list)
        if df.empty:
            print("DataFrame está vacío.")
            return None
        try:
            plt_daño = plt.figure(figsize=(10, 6))
            plt.plot(df['minuto'], df['damageDone'], color="g", label='Daño Hecho')
            plt.plot(df['minuto'], df['damageTaken'], color="r", label='Daño Recibido')
            plt.xlabel('Tiempo (min)')
            plt.ylabel('Daño')
            plt.title('Daño Hecho al Minuto')
            plt.legend()
            plt.grid()
            matplotlib.pyplot.close()
            
        except:
            print(f"No se pudo generar el gráfico de Daño")

        try: 
            plt_nivel = plt.figure(figsize=(10, 6))
            plt.plot(df['minuto'], df['level'], color="g", label='Nivel')
            plt.xlabel('Tiempo (min)')
            plt.ylabel('Nivel de campeón')
            plt.title('Nivel de campeón al minuto')
            plt.grid()
            matplotlib.pyplot.close()
        except:
            print("No se pudo generar el gráfico de Nivel")

        try: 
            plt_minions = plt.figure(figsize=(10, 6))
            plt.plot(df['minuto'], df['minions'], color="r", label='Minions')
            plt.xlabel('Tiempo (min)')
            plt.ylabel('Minions')
            plt.title('Minions al minuto')
            plt.grid()
            matplotlib.pyplot.close()
        except:
            print("No se pudo generar el gráfico de Minions")   

        try: 

            plt_oro = plt.figure(figsize=(10, 6))
            plt.plot(df['minuto'], df['gold'], color="r", label='Oro')
            plt.xlabel('Tiempo (min)')
            plt.ylabel('Oro')
            plt.title('Oro al minuto')
            plt.grid()
            matplotlib.pyplot.close()
        except:
            print("No se pudo generar el gráfico de Oro")

        try: 
            plt_exp = plt.figure(figsize=(10, 6))
            plt.plot(df['minuto'], df['xp'], color="r", label='Experiencia')
            plt.xlabel('Tiempo (min)')
            plt.ylabel('Experiencia')
            plt.title('Experiencia al minuto')
            plt.grid()
            matplotlib.pyplot.close()
        except:
            print("No se pudo generar el gráfico de Experiencia")   
        
    except:
        print(f"No hay datos en time_info_data")
    print(f"League of Data: Los datos están listos para visualizar.")
    return plt_daño, plt_nivel, plt_minions, plt_oro, plt_exp
    
def compare_graphs(info):
    #print(info)
    if info:
        try:
            summonerA_totalLosses = info['summonerA']['summoner'].total_losses
            summonerA_totalWins = info['summonerA']['summoner'].total_wins
            summonerA_matchDetails = info['summonerA']['match_details']
            #print(summoner_a)
            champions_a = []
            roles_a = []
            lanes_a = []
            
            for match in summonerA_matchDetails:
                graphic_data = match['graphic_data']
                champion = graphic_data.championName
                if champion:
                    champions_a.append(champion)
                role = graphic_data.role
                if role:
                    roles_a.append(role)
                lane = graphic_data.lane
                if lane:
                    lanes_a.append(lane)
                
            summonerB_totalLosses = info['summonerB']['summoner'].total_losses
            summonerB_totalWins = info['summonerB']['summoner'].total_wins
            summonerB_matchDetails = info['summonerB']['match_details']
            champions_b = []
            roles_b = []
            lanes_b = []

            for match in summonerB_matchDetails:
                graphic_data = match['graphic_data']
                champion = graphic_data.championName
                if champion:
                    champions_b.append(champion)
                role = graphic_data.role
                if role:
                    roles_b.append(role)
                lane = graphic_data.lane
                if lane:
                    lanes_b.append(lane)
                    
            #all_champions = champions_a + champions_b
            try:
                df_champions_a = pd.DataFrame(champions_a, columns=['Champion'])
                df_champions_b = pd.DataFrame(champions_b, columns=['Champion'])
            

                champion_counts_a = df_champions_a['Champion'].value_counts().reset_index()
                champion_counts_a.columns = ['Champion', 'CountA']
                champion_counts_b = df_champions_b['Champion'].value_counts().reset_index()
                champion_counts_b.columns = ['Champion', 'CountB']
                champion_counts = pd.merge(champion_counts_a, champion_counts_b, on='Champion', how='outer').fillna(0)
                #print(champion_counts)
            
                plt_champions = plt.figure(figsize=(10, 6))
                plt.barh(champion_counts['Champion'], champion_counts['CountA'], color="g", label='Invocador A')
                plt.barh(champion_counts['Champion'], champion_counts['CountB'], color="r", label='Invocador B')
                plt.xlabel('Campeón')
                plt.ylabel('Frecuencia')
                plt.title('Frecuencia de campeones')
                plt.legend()
                plt.grid()
                matplotlib.pyplot.close()
                return plt_champions

            except:
                print(f"No se pudo generar el gráfico de Champions")
        except:
            print("No se pudo acceder a la información de los campeones")
            return None
    else:
        print("La información de los summoners está vacía")
        return None