# Autor: antho

import time
from concurrent.futures import ThreadPoolExecutor
import pandas as pd

def encontrar_maximo_minimo_subconjunto(df_subconjunto):
    ages = df_subconjunto['age'].tolist()
    if len(ages) == 0:
        return None, None
    return max(ages), min(ages)

def encontrar_maximo_minimo_paralelo(df, num_threads):
    resultados_maximos = []
    resultados_minimos = []
    tamanio_subconjunto = len(df) // num_threads

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for i in range(num_threads):
            inicio = i * tamanio_subconjunto
            fin = inicio + tamanio_subconjunto if i < num_threads - 1 else None
            df_subconjunto = df.iloc[inicio:fin]
            resultado_maximo, resultado_minimo = executor.submit(encontrar_maximo_minimo_subconjunto, df_subconjunto).result()
            resultados_maximos.append(resultado_maximo)
            resultados_minimos.append(resultado_minimo)

    maximo_global = max(resultados_maximos)
    minimo_global = min(resultados_minimos)

    return maximo_global, minimo_global

def cargar_datos(ruta_archivo):
    try:
        df = pd.read_csv(ruta_archivo)
        return df
    except Exception as e:
        print("Error al cargar el archivo CSV:", e)
        return None

def analizar_datos(ruta_archivo, num_threads):
    df = cargar_datos(ruta_archivo)

    if df is not None:
        inicio_paralelo = time.time()
        maximo_global, minimo_global = encontrar_maximo_minimo_paralelo(df, num_threads)
        fin_paralelo = time.time()
        tiempo_paralelo = fin_paralelo - inicio_paralelo

        print("Máximo edad encontrado en paralelo:", maximo_global)
        print("Mínimo edad encontrado en paralelo:", minimo_global)
        print("Tiempo total en paralelo:", tiempo_paralelo, "segundos")
    else:
        print("No se pudieron cargar los datos del archivo CSV")