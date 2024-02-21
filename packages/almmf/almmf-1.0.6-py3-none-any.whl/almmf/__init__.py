# Autor: jugo

import time
from concurrent.futures import ThreadPoolExecutor
import os
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

def encontrar_suma_subconjunto(df_subconjunto):
    ages = df_subconjunto['age'].tolist()
    return sum(ages)

def encontrar_suma_paralelo(df):
    num_threads = os.cpu_count() or 1  # Obtener el número de CPU o establecer a 1 si no se puede determinar
    resultados_suma = []
    tamanio_subconjunto = len(df) // num_threads

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for i in range(num_threads):
            inicio = i * tamanio_subconjunto
            fin = inicio + tamanio_subconjunto if i < num_threads - 1 else len(df)
            df_subconjunto = df.iloc[inicio:fin]
            resultado_suma = executor.submit(encontrar_suma_subconjunto, df_subconjunto).result()
            resultados_suma.append(resultado_suma)

    suma_total = sum(resultados_suma)
    return suma_total

def calcular_prom_edades(ages):
    if len(ages) == 0:
        return 0
    return sum(ages) / len(ages)

# Función para calcular el promedio de edades
def calcular_promedio_subconjunto(df_subconjunto):
    ages = df_subconjunto['age'].tolist()
    return calcular_prom_edades(ages)

# Función para calcular promedios en paralelo
def calcular_promedio_paralelo(df, num_threads):
    resultados_parciales = []
    tamanio_subconjunto = len(df) // num_threads

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for i in range(num_threads):
            inicio = i * tamanio_subconjunto
            fin = inicio + tamanio_subconjunto if i < num_threads - 1 else None
            df_subconjunto = df.iloc[inicio:fin]
            resultado_parcial = executor.submit(calcular_promedio_subconjunto, df_subconjunto)
            resultados_parciales.append(resultado_parcial)

    promedios_parciales = [resultado.result() for resultado in resultados_parciales]
    promedio_global = calcular_prom_edades(promedios_parciales)

    return promedio_global

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