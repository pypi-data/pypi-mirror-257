# Autor: jugo

from concurrent.futures import ThreadPoolExecutor
import time, os
import pandas as pd

###############
## MAX Y MIN ##
###############

# Secuencial

def calcular_maximo_minimo_secuencial(df):
    inicio_secuencial = time.time()
    
    ages = df['age'].tolist()
    if len(ages) == 0:
        return None, None, 0
    
    maximo_global = max(ages)
    minimo_global = min(ages)
    
    fin_secuencial = time.time()
    tiempo_secuencial = fin_secuencial - inicio_secuencial
    
    return maximo_global, minimo_global, tiempo_secuencial

# Paralelo

def encontrar_maximo_minimo_subconjunto(df_subconjunto):
    ages = df_subconjunto['age'].tolist()
    if len(ages) == 0:
        return None, None
    return max(ages), min(ages)

def calcular_maximo_minimo_paralelo(df, num_threads):
    inicio_paralelo = time.time()
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

    fin_paralelo = time.time()
    tiempo_paralelo = fin_paralelo - inicio_paralelo

    return maximo_global, minimo_global, tiempo_paralelo

#########
## SUM ##
#########

# Secuencial

def calcular_suma_secuencial(df):
    inicio_secuencial = time.time()
    
    ages = df['age'].tolist()
    suma_total = sum(ages)
    
    fin_secuencial = time.time()
    tiempo_secuencial = fin_secuencial - inicio_secuencial
    
    return suma_total, tiempo_secuencial

# Paralelo

def encontrar_suma_subconjunto(df_subconjunto):
    ages = df_subconjunto['age'].tolist()
    return sum(ages)

def calcular_suma_paralelo(df, num_threads):
    inicio_paralelo = time.time()
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
    fin_paralelo = time.time()
    tiempo_paralelo = fin_paralelo - inicio_paralelo
    
    return suma_total, tiempo_paralelo

##########
## PROM ##
##########

def encontrar_prom_edades(ages):
    if len(ages) == 0:
        return 0
    return sum(ages) / len(ages)

# Secuencial

def calcular_promedio_secuencial(df):
    inicio_secuencial = time.time()
    
    # Utilizando la función ya definida para calcular el promedio de edades directamente.
    promedio_total = encontrar_prom_edades(df['age'].tolist())
    
    fin_secuencial = time.time()
    tiempo_secuencial = fin_secuencial - inicio_secuencial
    
    return promedio_total, tiempo_secuencial

# Paralelo

def encontrar_promedio_subconjunto(ages):
    return encontrar_prom_edades(ages)

def calcular_promedio_paralelo(df, num_threads):
    inicio_paralelo = time.time()

    subconjuntos = [df[i:i + len(df) // num_threads] for i in range(0, len(df), len(df) // num_threads)]

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Calcular el promedio de cada subconjunto de manera recursiva
        promedios_parciales = executor.map(encontrar_promedio_subconjunto, [subconjunto['age'].tolist() for subconjunto in subconjuntos])

    # Calcular el promedio global combinando los promedios parciales
    promedio_global = encontrar_prom_edades(list(promedios_parciales))
    
    fin_paralelo = time.time()
    tiempo_paralelo = fin_paralelo - inicio_paralelo
    
    return promedio_global, tiempo_paralelo

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
        maximo_global, minimo_global = calcular_maximo_minimo_paralelo(df, num_threads)
        fin_paralelo = time.time()
        tiempo_paralelo = fin_paralelo - inicio_paralelo

        print("Máximo edad encontrado en paralelo:", maximo_global)
        print("Mínimo edad encontrado en paralelo:", minimo_global)
        print("Tiempo total en paralelo:", tiempo_paralelo, "segundos")
    else:
        print("No se pudieron cargar los datos del archivo CSV")