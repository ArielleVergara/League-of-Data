import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt

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
            plt.title('Daño Hecho por Minuto')
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
            plt.title('Minions por minuto')
            plt.grid()
            matplotlib.pyplot.close()
        except:
            print("No se pudo generar el gráfico de Minions")   

        try: 

            plt_oro = plt.figure(figsize=(10, 6))
            plt.plot(df['minuto'], df['gold'], color="r", label='Oro')
            plt.xlabel('Tiempo (min)')
            plt.ylabel('Oro')
            plt.title('Oro por minuto')
            plt.grid()
            matplotlib.pyplot.close()
        except:
            print("No se pudo generar el gráfico de Oro")

        try: 
            plt_exp = plt.figure(figsize=(10, 6))
            plt.plot(df['minuto'], df['xp'], color="r", label='Experiencia')
            plt.xlabel('Tiempo (min)')
            plt.ylabel('Experiencia')
            plt.title('Experiencia por minuto')
            plt.grid()
            matplotlib.pyplot.close()
        except:
            print("No se pudo generar el gráfico de Experiencia")   
        
    except:
        print(f"No hay datos en time_info_data")
    print(f"League of Data: Los datos están listos para visualizar.")
    return plt_daño, plt_nivel, plt_minions, plt_oro,plt_exp
    
