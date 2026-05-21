# =============================================
# Script de analisis estadistico del torneo
# =============================================
# Autor original : Paco (P2 - Desarrollador)
# Revisado por   : Luis (P3 - Revisor QA)
# Jira           : TORNEO-2 / TORNEO-3
#
# Por que usamos pandas:
#   Permite filtrar filas por condicion de forma
#   simple sin recorrer el archivo manualmente.
#
# Por que usamos rutas relativas:
#   Para que el script funcione en cualquier
#   computadora sin necesidad de modificaciones.
#
# Por que ordenamos por PTS descendente:
#   Para respetar el formato estandar de una
#   tabla de posiciones de torneo de futbol.
# =============================================

import pandas as pd
import matplotlib.pyplot as plt
import os

# Creamos la carpeta resultados si no existe
os.makedirs('resultados', exist_ok=True)

# Cargamos el archivo CSV con los resultados
df = pd.read_csv('datos/resultados_partidos.csv')
print('Partidos cargados:', len(df))

# Obtenemos la lista de equipos sin repetir
equipos = list(set(df['local'].tolist() + df['visitante'].tolist()))
equipos.sort()

# Lista vacia donde guardamos los datos de cada equipo
resultados = []

# Recorremos cada equipo y calculamos sus estadisticas
for equipo in equipos:

    # Filtramos partidos de local y visitante
    como_local     = df[df['local'] == equipo]
    como_visitante = df[df['visitante'] == equipo]

    # Total de partidos jugados
    partidos_jugados = len(como_local) + len(como_visitante)

    # Goles a favor y en contra
    goles_favor  = como_local['goles_local'].sum()     + como_visitante['goles_visitante'].sum()
    goles_contra = como_local['goles_visitante'].sum() + como_visitante['goles_local'].sum()

    # Partidos ganados
    ganados  = (como_local['goles_local']         > como_local['goles_visitante']).sum()
    ganados += (como_visitante['goles_visitante'] > como_visitante['goles_local']).sum()

    # Partidos empatados
    empatados  = (como_local['goles_local']         == como_local['goles_visitante']).sum()
    empatados += (como_visitante['goles_visitante'] == como_visitante['goles_local']).sum()

    # Partidos perdidos y puntos totales
    perdidos = partidos_jugados - ganados - empatados
    puntos   = ganados * 3 + empatados

    resultados.append({
        'Equipo' : equipo,
        'PJ'     : partidos_jugados,
        'PG'     : ganados,
        'PE'     : empatados,
        'PP'     : perdidos,
        'GF'     : goles_favor,
        'GC'     : goles_contra,
        'DG'     : goles_favor - goles_contra,
        'PTS'    : puntos
    })

# Convertimos la lista en tabla y ordenamos por puntos
tabla = pd.DataFrame(resultados)
tabla = tabla.sort_values('PTS', ascending=False)
tabla = tabla.reset_index(drop=True)
tabla.index += 1

# Mostramos la tabla en pantalla
print('')
print('TABLA DE POSICIONES')
print(tabla.to_string())

# Calculamos promedio de goles por partido
total_goles    = (df['goles_local'] + df['goles_visitante']).sum()
promedio_goles = round(total_goles / len(df), 2)
print('')
print('Promedio de goles por partido:', promedio_goles)

# Guardamos la tabla en CSV dentro de resultados
tabla.to_csv('resultados/tabla_posiciones.csv')
print('Tabla guardada en resultados/tabla_posiciones.csv')

# Creamos el grafico de barras comparando puntos por equipo
plt.figure(figsize=(10, 5))
plt.bar(tabla['Equipo'], tabla['PTS'], color='steelblue')
plt.title('Puntos por Equipo - Campeonato 2026')
plt.xlabel('Equipo')
plt.ylabel('Puntos')
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig('resultados/grafico_resultados.png')
plt.show()
print('Grafico guardado en resultados/grafico_resultados.png')
