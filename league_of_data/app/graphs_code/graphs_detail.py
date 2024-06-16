import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt


def generate_graphs(match):
    try:
        time_info_data = match
        #print(time_info_data)
        for time_info in time_info_data:
            print(time_info)   
            df = pd.DataFrame(time_info)
            try: 
                # Paso 4: Crea gráficos con matplotlib
                plt_daño = plt.figure(figsize=(10, 6))

                # Ejemplo: Gráfico de daño hecho por minuto
                plt.plot(df['minuto'], df['damageDone'], color="g", label='Daño Hecho')
                plt.plot(df['minuto'], df['damageTaken'], color="r", label='Daño Recibido')

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
                plt.plot(df['minuto'], df['level'], color="g", label='Nivel')

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
                plt.plot(df['minuto'], df['minions'], color="r", label='Minions')

                plt.xlabel('Tiempo (min)')
                plt.ylabel('Minions')
                plt.title('Minions por minuto')
                plt.grid()
                """plt.savefig(f"./app/static/graphs/match_{match_id}/minions_{match_id}.png")"""
                matplotlib.pyplot.close()
            except:
                print("No se pudo generar el gráfico de Minions")   

            try: 
            # Paso 4: Crea gráficos con matplotlib
                plt_oro = plt.figure(figsize=(10, 6))

            # Ejemplo: Gráfico de daño hecho por minuto
                plt.plot(df['minuto'], df['gold'], color="r", label='Oro')

                plt.xlabel('Tiempo (min)')
                plt.ylabel('Oro')
                plt.title('Oro por minuto')
                plt.grid()
                """plt.savefig(f"./app/static/graphs/match_{match_id}/gold_{match_id}.png")"""
                matplotlib.pyplot.close()
            except:
                print("No se pudo generar el gráfico de Oro")

        try: 
            # Paso 4: Crea gráficos con matplotlib
            plt_exp = plt.figure(figsize=(10, 6))

            # Ejemplo: Gráfico de daño hecho por minuto
            plt.plot(df['minuto'], df['xp'], color="r", label='Experiencia')

            plt.xlabel('Tiempo (min)')
            plt.ylabel('Experiencia')
            plt.title('Experiencia por minuto')
            plt.grid()
            """plt.savefig(f"./app/static/graphs/match_{match_id}/xp_{match_id}.png")"""
            matplotlib.pyplot.close()
        except:
            print("No se pudo generar el gráfico de Experiencia")   
        
    except:
        print(f"No hay datos en time_info_data")
    
    return plt_daño, plt_nivel, plt_minions, plt_oro,plt_exp
    
