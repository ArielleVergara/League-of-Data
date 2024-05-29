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
        """print('time_info_data', time_info_data)"""
        """for i in time_info_data:
            print(i)"""
        # Paso 2: Convierte los datos a un DataFrame de pandas
        df = pd.DataFrame(time_info_data)
        """print(df)"""
            
        min = df.loc[:,['minute']]
        """print('min', min)"""

        # Paso 4: Crea gráficos con matplotlib
        plt.figure(figsize=(10, 6))

        # Ejemplo: Gráfico de daño hecho por minuto
        plt.plot(df['minute'], df['damageDone'], label='Daño Hecho')
        
        plt.xlabel('Minuto')
        plt.ylabel('Daño')
        plt.title('Daño Hecho por Minuto')
        plt.legend()
        plt.grid()
        plt.savefig(f"./app/static/graphs/{match}.png")

    except Exception as e:
        print(f"Error al generar el gráfico: {e}")
