import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns
import numpy as np
from math import pi


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
    
def compare_graphs(info, summoner_a, summoner_b):
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
            assists_a = []
            deaths_a = []
            gold_a = []
            kills_a = []
            damageDealt_a = []
            damageTaken_a = []
            minions_a =[]            
            
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
                assists = graphic_data.assists
                if assists:
                    assists_a.append(assists)
                deaths = graphic_data.deaths
                if deaths:
                    deaths_a.append(deaths)
                gold = graphic_data.goldEarned
                if gold:
                    gold_a.append(gold)
                kills = graphic_data.kills
                if kills:
                    kills_a.append(kills)
                damageDealt = graphic_data.totalDamageDealt
                if damageDealt:
                    damageDealt_a.append(damageDealt)
                damageTaken = graphic_data.totalDamageTaken
                if damageTaken:
                    damageTaken_a.append(damageTaken)
                
            for match in summonerA_matchDetails:
                time_info = match['time_info']
                time = time_info[-1]
                minion = time.minions
                minions_a.append(minion)
                    

                
            summonerB_totalLosses = info['summonerB']['summoner'].total_losses
            summonerB_totalWins = info['summonerB']['summoner'].total_wins
            summonerB_matchDetails = info['summonerB']['match_details']
            champions_b = []
            roles_b = []
            lanes_b = []
            wins_b = []
            assists_b = []
            deaths_b = []
            gold_b = []
            kills_b = []
            damageDealt_b = []
            damageTaken_b = []
            minions_b =[]

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
                assists = graphic_data.assists
                if assists:
                    assists_b.append(assists)
                deaths = graphic_data.deaths
                if deaths:
                    deaths_b.append(deaths)
                gold = graphic_data.goldEarned
                if gold:
                    gold_b.append(gold)
                kills = graphic_data.kills
                if kills:
                    kills_b.append(kills)
                damageDealt = graphic_data.totalDamageDealt
                if damageDealt:
                    damageDealt_b.append(damageDealt)
                damageTaken = graphic_data.totalDamageTaken
                if damageTaken:
                    damageTaken_b.append(damageTaken)
                
            for match in summonerA_matchDetails:
                time_info = match['time_info']
                time = time_info[-1]
                minion = time.minions
                minions_b.append(minion)
            
            """ kda_a = [(k + a) / d if d != 0 else (k + a) for k, a, d in zip(kills_a, assists_a, deaths_a)]
            kda_b = [(k + a) / d if d != 0 else (k + a) for k, a, d in zip(kills_b, assists_b, deaths_b)]
            
            avg_kda_a = sum(kda_a) / len(kda_a)
            avg_kda_b = sum(kda_b) / len(kda_b)
            avg_minions_a = sum(minions_a) / len(minions_a)
            avg_minions_b = sum(minions_b) / len(minions_b)
            avg_gold_a = sum(gold_a) / len(gold_a)
            avg_gold_b = sum(gold_b) / len(gold_b)
            avg_damageDealt_a = sum(damageDealt_a) / len(damageDealt_a)
            avg_damageDealt_b = sum(damageDealt_b) / len(damageDealt_b)
            avg_damageTaken_a = sum(damageTaken_a) / len(damageTaken_a)
            avg_damageTaken_b = sum(damageTaken_b) / len(damageTaken_b)
            
            max_kda = max(avg_kda_a, avg_kda_b)
            max_minions = max(avg_minions_a, avg_minions_b)
            max_gold = max(avg_gold_a, avg_gold_b)
            max_damageDealt = max(avg_damageDealt_a, avg_damageDealt_b)
            max_damageTaken = max(avg_damageTaken_a, avg_damageTaken_b)
            
            player_a_stats = [
            avg_kda_a / max_kda,
            avg_minions_a / max_minions,
            avg_gold_a / max_gold,
            avg_damageDealt_a / max_damageDealt,
            avg_damageTaken_a / max_damageTaken
            ]
            
            player_b_stats = [
                avg_kda_b / max_kda,
                avg_minions_b / max_minions,
                avg_gold_b / max_gold,
                avg_damageDealt_b / max_damageDealt,
                avg_damageTaken_b / max_damageTaken
            ]
            
            try:
                categories = ['KDA', 'Minions', 'Oro', 'Daño hecho', 'Daño recibido']
                player_a_stats = [sum(kda_a) / len(kda_a), sum(minions_a) / len(minions_a), sum(gold_a) / len(gold_a), sum(damageDealt_a) / len(damageDealt_a), sum(damageTaken_a) / len(damageTaken_a)]
                player_b_stats = [sum(kda_b) / len(kda_b), sum(minions_b) / len(minions_b), sum(gold_b) / len(gold_b), sum(damageDealt_b) / len(damageDealt_b), sum(damageTaken_b) / len(damageTaken_b)]
                
                num_vars = len(categories)
                angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
                angles += angles[:1]

                plt_radar, ax = plt.subplots(figsize=(10, 6), subplot_kw=dict(polar=True))

                values_a = player_a_stats + player_a_stats[:1]
                ax.plot(angles, values_a, linewidth=1, linestyle='solid', label=f'{summoner_a}')
                ax.fill(angles, values_a, 'b', alpha=0.1)

                values_b = player_b_stats + player_b_stats[:1]
                ax.plot(angles, values_b, linewidth=1, linestyle='solid', label=f'{summoner_b}')
                ax.fill(angles, values_b, 'r', alpha=0.1)

                plt.xticks(angles[:-1], categories)

                ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
                plt.close(plt_radar)
            except Exception as e:
                print(f"No se pudo generar el gráfico de Radar: {e}") """
                
                    
            try:
                df_winrate_a = pd.DataFrame([{'Jugador': f'{summoner_a}', 'Ganadas': summonerA_totalWins, 'Perdidas': summonerA_totalLosses}])
                df_winrate_b = pd.DataFrame([{'Jugador': f'{summoner_b}', 'Ganadas': summonerB_totalWins, 'Perdidas': summonerB_totalLosses}])

                df_winrate = pd.concat([df_winrate_a, df_winrate_b]).reset_index(drop=True)

                plt_winrate, ax = plt.subplots(figsize=(10, 6))
                x = np.arange(len(df_winrate))
                width = 0.35

                rects1 = ax.bar(x - width/2, df_winrate['Ganadas'], width, label='Ganadas', color='g')
                rects2 = ax.bar(x + width/2, df_winrate['Perdidas'], width, label='Perdidas', color='b')

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
                                    xytext=(0, 3),
                                    textcoords="offset points",
                                    ha='center', va='bottom')

                autolabel(rects1)
                autolabel(rects2)
                plt.close(plt_winrate)

            except Exception as e:
                print(f"No se pudo generar el gráfico de Winrate: {e}")
                
            try:
                df_a = pd.DataFrame({'Champion': champions_a, 'Resultado': wins_a})
                df_b = pd.DataFrame({'Champion': champions_b, 'Resultado': wins_b})

                champion_counts_a = df_a.groupby(['Champion', 'Resultado']).size().unstack(fill_value=0)
                champion_counts_b = df_b.groupby(['Champion', 'Resultado']).size().unstack(fill_value=0)

                champion_counts = pd.concat([champion_counts_a, champion_counts_b], keys=[summoner_a, summoner_b], axis=1).fillna(0)

                plt_champ, ax = plt.subplots(figsize=(10, 6))

                x = np.arange(len(champion_counts))

                width = 0.35

                rects1 = ax.bar(x - width/2, champion_counts[(summoner_a, 'Ganada')], width, label=f'{summoner_a} Ganadas', color='g')
                rects2 = ax.bar(x - width/2, champion_counts[(summoner_a, 'Perdida')], width, bottom=champion_counts[(summoner_a, 'Ganada')], label=f'{summoner_a} Perdidas', color='lightgreen')

                rects3 = ax.bar(x + width/2, champion_counts[(summoner_b, 'Ganada')], width, label=f'{summoner_b} Ganadas', color='b')
                rects4 = ax.bar(x + width/2, champion_counts[(summoner_b, 'Perdida')], width, bottom=champion_counts[(summoner_b, 'Ganada')], label=f'{summoner_b} Perdidas', color='lightblue')

                ax.set_xlabel('Campeón')
                ax.set_ylabel('Número de Partidas')
                ax.set_title('Comparación de Campeones según Victorias y Derrotas')
                ax.set_xticks(x)
                ax.set_xticklabels(champion_counts.index, rotation=45, ha="right")
                ax.legend()
                
                def autolabel(rects):
                    for rect in rects:
                        height = rect.get_height()
                        ax.annotate('{}'.format(height),
                                    xy=(rect.get_x() + rect.get_width() / 2, height),
                                    xytext=(0, 3),
                                    textcoords="offset points",
                                    ha='center', va='bottom')

                autolabel(rects1)
                autolabel(rects2)
                autolabel(rects3)
                autolabel(rects4)
                plt.close(plt_champ)
            except:
                print("No se pudo general el gráfico de winrate por campeones")
            
            try:
                df_a = pd.DataFrame({'Lane': lanes_a, 'Resultado': wins_a})
                df_b = pd.DataFrame({'Lane': lanes_b, 'Resultado': wins_b})

                lane_counts_a = df_a.groupby(['Lane', 'Resultado']).size().unstack(fill_value=0)
                lane_counts_b = df_b.groupby(['Lane', 'Resultado']).size().unstack(fill_value=0)

                lane_counts = pd.concat([lane_counts_a, lane_counts_b], keys=[summoner_a, summoner_b], axis=1).fillna(0)
                
                plt_lane, ax = plt.subplots(figsize=(10, 6))

                x = np.arange(len(lane_counts))

                width = 0.35

                rects1 = ax.bar(x - width/2, lane_counts[(summoner_a, 'Ganada')], width, label=f'{summoner_a} Ganadas', color='g')
                rects2 = ax.bar(x - width/2, lane_counts[(summoner_a, 'Perdida')], width, bottom=lane_counts[(summoner_a, 'Ganada')], label=f'{summoner_a} Perdidas', color='lightgreen')
                rects3 = ax.bar(x + width/2, lane_counts[(summoner_b, 'Ganada')], width, label=f'{summoner_b} Ganadas', color='b')
                rects4 = ax.bar(x + width/2, lane_counts[(summoner_b, 'Perdida')], width, bottom=lane_counts[(summoner_b, 'Ganada')], label=f'{summoner_b} Perdidas', color='lightblue')

                ax.set_xlabel('Línea')
                ax.set_ylabel('Ratio de Victorias')
                ax.set_title('Comparación de Partidas Ganadas y Perdidas por Lane')
                ax.set_xticks(x)
                ax.set_xticklabels(lane_counts.index, rotation=45, ha="right")
                ax.legend()
                
                def autolabel(rects):
                    for rect in rects:
                        height = rect.get_height()
                        ax.annotate('{}'.format(height),
                                    xy=(rect.get_x() + rect.get_width() / 2, height),
                                    xytext=(0, 3),
                                    textcoords="offset points",
                                    ha='center', va='bottom')
                autolabel(rects1)
                autolabel(rects2)
                autolabel(rects3)
                autolabel(rects4)
                plt.close(plt_lane)
            except:
                print(f"No se pudo generar el gráfico de Champions")
        except:
            print("No se pudo acceder a la información de los Summoners")
            return None
        return plt_winrate, plt_champ, plt_lane
    else:
        print("La información de los summoners está vacía")
        return None