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
        # Paso 1: Consulta los datos desde la base de 
        time_info_data = Time_info.objects.filter(match_id = match).values()
        # Paso 2: Convierte los datos a un DataFrame de pandas
        df = pd.DataFrame(time_info_data)
        try: 
            # Paso 4: Crea gráficos con matplotlib
            plt.figure(figsize=(10, 6))

            # Ejemplo: Gráfico de daño hecho por minuto
            plt.plot(df['minute'], df['damageDone'], color="g", label='Daño Hecho')
            plt.plot(df['minute'], df['damageTaken'], color="r", label='Daño Recibido')

            plt.xlabel('Tiempo (min)')
            plt.ylabel('Daño')
            plt.title('Daño Hecho por Minuto')
            plt.legend()
            plt.grid()
            plt.savefig(f"./app/static/graphs/daño/{match}.png")
            matplotlib.pyplot.close()
        except:
            print("No se pudo generar el gráfico de Daño Hecho")

        try: 
            # Paso 4: Crea gráficos con matplotlib
            plt.figure(figsize=(10, 6))

            # Ejemplo: Gráfico de daño hecho por minuto
            plt.plot(df['minute'], df['level'], color="g", label='Nivel')

            plt.xlabel('Tiempo (min)')
            plt.ylabel('Nivel de campeón')
            plt.title('Nivel de campeón al minuto')
            plt.grid()
            plt.savefig(f"./app/static/graphs/level/{match}.png")
            matplotlib.pyplot.close()
        except:
            print("No se pudo generar el gráfico de Nivel")

        try: 
            # Paso 4: Crea gráficos con matplotlib
            plt.figure(figsize=(10, 6))

            # Ejemplo: Gráfico de daño hecho por minuto
            plt.plot(df['minute'], df['minions'], color="r", label='Minions')

            plt.xlabel('Tiempo (min)')
            plt.ylabel('Minions')
            plt.title('Minions al minuto')
            plt.grid()
            plt.savefig(f"./app/static/graphs/minions/{match}.png")
            matplotlib.pyplot.close()
        except:
            print("No se pudo generar el gráfico de Minions")   

        try: 
            # Paso 4: Crea gráficos con matplotlib
            plt.figure(figsize=(10, 6))

            # Ejemplo: Gráfico de daño hecho por minuto
            plt.plot(df['minute'], df['gold'], color="r", label='Oro')

            plt.xlabel('Tiempo (min)')
            plt.ylabel('Oro')
            plt.title('Oro al minuto')
            plt.grid()
            plt.savefig(f"./app/static/graphs/oro/{match}.png")
            matplotlib.pyplot.close()
        except:
            print("No se pudo generar el gráfico de Oro")

        try: 
            # Paso 4: Crea gráficos con matplotlib
            plt.figure(figsize=(10, 6))

            # Ejemplo: Gráfico de daño hecho por minuto
            plt.plot(df['minute'], df['xp'], color="r", label='Experiencia')

            plt.xlabel('Tiempo (min)')
            plt.ylabel('Experiencia')
            plt.title('Experiencia')
            plt.grid()
            plt.savefig(f"./app/static/graphs/xp/{match}.png")
            matplotlib.pyplot.close()
        except:
            print("No se pudo generar el gráfico de Experiencia")   
        
    except:
        print(f"No hay datos en time_info_data")
    
    
