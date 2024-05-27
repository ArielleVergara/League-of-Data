"""
import matplotlib
matplotlib.use('Agg')  # Usa el backend 'Agg' para evitar problemas de GUI
import pandas as pd
import matplotlib.pyplot as plt
from app.models import Time_info
import os

import pandas as pd
import matplotlib.pyplot as plt
from app.models import Time_info

def generate_graphs():
    try:
        # Paso 1: Consulta los datos desde la base de datos
        time_info_data = Time_info.objects.all().values()

        # Paso 2: Convierte los datos a un DataFrame de pandas
        df = pd.DataFrame(time_info_data)

        # Paso 3: Asegúrate de que los datos están en el formato correcto
        # Por ejemplo, si necesitas convertir algún campo a un tipo específico:
        df['minute'] = df['minute'].astype(int)
        df['damageDone'] = df['damageDone'].astype(int)
        df['damageTaken'] = df['damageTaken'].astype(int)
        df['gold'] = df['gold'].astype(int)
        df['xp'] = df['xp'].astype(int)
        df['minions'] = df['minions'].astype(int)
        df['level'] = df['level'].astype(int)

        # Paso 4: Crea gráficos con matplotlib
        plt.figure(figsize=(10, 6))

        # Ejemplo: Gráfico de daño hecho por minuto
        plt.plot(df['minute'], df['damageDone'], label='Daño Hecho')
        plt.plot(df['minute'], df['damageTaken'], label='Daño Recibido')

        plt.xlabel('Minuto')
        plt.ylabel('Daño')
        plt.title('Daño Hecho y Recibido por Minuto')
        plt.legend()
        plt.grid(True)

        # Guarda el gráfico como una imagen
        graph_dir = os.path.join('static', 'graphs')
        if not os.path.exists('static/graphs'):
            os.makedirs(graph_dir)
        plt.savefig(os.path.join(graph_dir, 'damage_graph.png'))
        plt.close()
    except Exception as e:
        print(f"Error al generar el gráfico: {e}")
        """