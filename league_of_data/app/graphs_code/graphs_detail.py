import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


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
            plt_daño, ax = plt.subplots(figsize=(10, 6))
            ax.plot(df['minuto'], df['damageDone'], color="g", label='Daño Hecho')
            ax.plot(df['minuto'], df['damageTaken'], color="r", label='Daño Recibido')
            ax.set_xlabel('Tiempo (min)')
            ax.set_ylabel('Daño')
            ax.set_title('Daño Hecho al Minuto')
            ax.legend()
            ax.grid()
            plt.close(plt_daño)
            
        except:
            print(f"No se pudo generar el gráfico de Daño")

        try: 
            plt_nivel, ax = plt.subplots(figsize=(10, 6))
            ax.plot(df['minuto'], df['level'], color="g", label='Nivel')
            ax.set_xlabel('Tiempo (min)')
            ax.set_ylabel('Nivel de campeón')
            ax.set_title('Nivel de campeón al minuto')
            ax.grid()
            plt.close(plt_nivel)
        except:
            print("No se pudo generar el gráfico de Nivel")

        try: 
            plt_minions, ax = plt.subplots(figsize=(10, 6))
            ax.plot(df['minuto'], df['minions'], color="r", label='Minions')
            ax.set_xlabel('Tiempo (min)')
            ax.set_ylabel('Minions')
            ax.set_title('Minions al minuto')
            ax.grid()
            plt.close(plt_minions)
        except:
            print("No se pudo generar el gráfico de Minions")   

        try: 

            plt_oro, ax = plt.subplots(figsize=(10, 6))
            ax.plot(df['minuto'], df['gold'], color="r", label='Oro')
            ax.set_xlabel('Tiempo (min)')
            ax.set_ylabel('Oro')
            ax.set_title('Oro al minuto')
            ax.grid()
            plt.close(plt_oro)
        except:
            print("No se pudo generar el gráfico de Oro")

        try: 
            plt_exp, ax = plt.subplots(figsize=(10, 6))
            ax.plot(df['minuto'], df['xp'], color="r", label='Experiencia')
            ax.set_xlabel('Tiempo (min)')
            ax.set_ylabel('Experiencia')
            ax.set_title('Experiencia al minuto')
            ax.grid()
            plt.close(plt_exp)
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
            wins_a = []
            
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
                win = graphic_data.win
                if win == True:
                    wins_a.append('Ganada')
                else:
                    wins_a.append('Perdida')

                
            summonerB_totalLosses = info['summonerB']['summoner'].total_losses
            summonerB_totalWins = info['summonerB']['summoner'].total_wins
            summonerB_matchDetails = info['summonerB']['match_details']
            champions_b = []
            roles_b = []
            lanes_b = []
            wins_b = []

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
                win = graphic_data.win
                if win == True:
                    wins_b.append('Ganada')
                else:
                    wins_b.append('Perdida')
                
                    
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
            
                plt_champions, ax = plt.subplots(figsize=(10, 6))

                ax.bar(champion_counts['Champion'], champion_counts['CountA'], color="g", label='Invocador A')
                ax.bar(champion_counts['Champion'], champion_counts['CountB'], bottom=champion_counts['CountA'], color="r", label='Invocador B')
                ax.set_xlabel('Campeón')
                ax.set_ylabel('Frecuencia')
                ax.set_title('Frecuencia de campeones')
                ax.legend()

                ax.set_xticklabels(champion_counts['Champion'], rotation=45, ha="right")
                
                #return plt_champions

            except:
                print(f"No se pudo generar el gráfico de Champions")
            
            try:
                # Crear DataFrames para los datos de winrate de los invocadores A y B
                df_winrate_a = pd.DataFrame([{'Jugador': 'Invocador A', 'Ganadas': summonerA_totalWins, 'Perdidas': summonerA_totalLosses}])
                df_winrate_b = pd.DataFrame([{'Jugador': 'Invocador B', 'Ganadas': summonerB_totalWins, 'Perdidas': summonerB_totalLosses}])

                # Combinar los DataFrames
                df_winrate = pd.concat([df_winrate_a, df_winrate_b]).reset_index(drop=True)

                # Crear el gráfico
                plt_winrate, ax = plt.subplots(figsize=(10, 6))
                # Posiciones de las barras en el eje x
                x = np.arange(len(df_winrate))
                # Ancho de las barras
                width = 0.35

                # Barras para partidas ganadas
                rects1 = ax.bar(x - width/2, df_winrate['Ganadas'], width, label='Ganadas', color='g')
                # Barras para partidas perdidas
                rects2 = ax.bar(x + width/2, df_winrate['Perdidas'], width, label='Perdidas', color='r')

                # Añadir algunas etiquetas y título
                ax.set_xlabel('Jugador')
                ax.set_ylabel('Partidas')
                ax.set_title('Partidas Ganadas y Perdidas por Jugador')
                ax.set_xticks(x)
                ax.set_xticklabels(df_winrate['Jugador'])
                ax.legend()

                def autolabel(rects):
                    for rect in rects:
                        height = rect.get_height()
                        ax.annotate('{}'.format(height),
                                    xy=(rect.get_x() + rect.get_width() / 2, height),
                                    xytext=(0, 3),  # 3 puntos verticales de offset
                                    textcoords="offset points",
                                    ha='center', va='bottom')

                autolabel(rects1)
                autolabel(rects2)

            except Exception as e:
                print(f"No se pudo generar el gráfico de Winrate: {e}")
        except:
            print("No se pudo acceder a la información de los Summoners")
            return None
        return plt_winrate, plt_champions
    else:
        print("La información de los summoners está vacía")
        return None