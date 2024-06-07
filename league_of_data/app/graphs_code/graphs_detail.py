import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
from app.models import Time_info
import os

import pandas as pd
import matplotlib.pyplot as plt
from app.models import Time_info

def generate_graphs(match):
    try:
        
        time_info_data = Time_info.objects.filter(match_id = match).values()
        # Paso 2: Convierte los datos a un DataFrame de pandas
        match_id = (time_info_data[0]['match_id_id'])

        """if not os.path.exists(f"./app/static/graphs/match_{match_id}/damage_{match_id}.png"):
                os.makedirs(f"./app/static/graphs/match_{match_id}/damage_{match_id}.png")"""
        
        df = pd.DataFrame(time_info_data)
        try: 
            # Paso 4: Crea gráficos con matplotlib
            plt_daño = plt.figure(figsize=(10, 6))

            # Ejemplo: Gráfico de daño hecho por minuto
            plt.plot(df['minute'], df['damageDone'], color="g", label='Daño Hecho')
            plt.plot(df['minute'], df['damageTaken'], color="r", label='Daño Recibido')

            plt.xlabel('Tiempo (min)')
            plt.ylabel('Daño')
            plt.title('Daño Hecho por Minuto')
            plt.legend()
            plt.grid()          
            """plt.savefig(f"./app/static/graphs/match_{match_id}/damage_{match_id}.png")"""
            matplotlib.pyplot.close()
        except:
            print("No se pudo generar el gráfico de Daño")

        try: 
            # Paso 4: Crea gráficos con matplotlib
            plt_nivel = plt.figure(figsize=(10, 6))

            # Ejemplo: Gráfico de daño hecho por minuto
            plt.plot(df['minute'], df['level'], color="g", label='Nivel')

            plt.xlabel('Tiempo (min)')
            plt.ylabel('Nivel de campeón')
            plt.title('Nivel de campeón al minuto')
            plt.grid()
            """plt.savefig(f"./app/static/graphs/match_{match_id}/level_{match_id}.png")"""
            matplotlib.pyplot.close()
        except:
            print("No se pudo generar el gráfico de Nivel")

        try: 
            # Paso 4: Crea gráficos con matplotlib
            plt_minions = plt.figure(figsize=(10, 6))

            # Ejemplo: Gráfico de daño hecho por minuto
            plt.plot(df['minute'], df['minions'], color="r", label='Minions')

            plt.xlabel('Tiempo (min)')
            plt.ylabel('Minions')
            plt.title('Minions al minuto')
            plt.grid()
            """plt.savefig(f"./app/static/graphs/match_{match_id}/minions_{match_id}.png")"""
            matplotlib.pyplot.close()
        except:
            print("No se pudo generar el gráfico de Minions")   

        try: 
            # Paso 4: Crea gráficos con matplotlib
            plt_oro = plt.figure(figsize=(10, 6))

            # Ejemplo: Gráfico de daño hecho por minuto
            plt.plot(df['minute'], df['gold'], color="r", label='Oro')

            plt.xlabel('Tiempo (min)')
            plt.ylabel('Oro')
            plt.title('Oro al minuto')
            plt.grid()
            """plt.savefig(f"./app/static/graphs/match_{match_id}/gold_{match_id}.png")"""
            matplotlib.pyplot.close()
        except:
            print("No se pudo generar el gráfico de Oro")

        try: 
            # Paso 4: Crea gráficos con matplotlib
            plt_exp = plt.figure(figsize=(10, 6))

            # Ejemplo: Gráfico de daño hecho por minuto
            plt.plot(df['minute'], df['xp'], color="r", label='Experiencia')

            plt.xlabel('Tiempo (min)')
            plt.ylabel('Experiencia')
            plt.title('Experiencia')
            plt.grid()
            """plt.savefig(f"./app/static/graphs/match_{match_id}/xp_{match_id}.png")"""
            matplotlib.pyplot.close()
        except:
            print("No se pudo generar el gráfico de Experiencia")   
        
    except:
        print(f"No hay datos en time_info_data")
    
    return plt_daño, plt_exp, plt_minions, plt_nivel, plt_oro
    
