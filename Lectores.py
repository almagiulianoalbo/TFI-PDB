import pandas as pd

# Crear una carpeta data donde se encuentren los archivos de MIT

def PrintTxt(ruta_archivo): # ruta_archivo debe ser un str seguido de annotations
    with open(f"data/mitbih_database/{ruta_archivo}.txt", "r", encoding="utf-8") as archivo:
        for linea in archivo:
            print(linea.strip())  # .strip() para quitar saltos de línea

def PrintCsv(ruta_archivo): # ruta_archivo debe ser un str
    df = pd.read_csv(f"data/mitbih_database/{ruta_archivo}.csv")
    print(df.head())  # Muestra las primeras 5 filas

def ReadTxt(ruta_archivo):
    try:
        ruta_completa = f"data/mitbih_database/{ruta_archivo}.txt"

        with open(ruta_completa, "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()

    except FileNotFoundError: # Si no encuentro el archivo
        print(f"El archivo {ruta_archivo}.txt no existe.")
        return None

    datos = []
    for linea in lineas[1:]:
        partes = linea.strip().split()
        if len(partes) >= 6:
            datos.append(partes[:6])

    columnas = ['Time', 'Sample', 'Type', 'Sub', 'Chan', 'Num']
    df = pd.DataFrame(datos, columns=columnas)

    df['Sample'] = pd.to_numeric(df['Sample'], errors='coerce')
    df['Num'] = pd.to_numeric(df['Num'], errors='coerce')

    return df

def ReadCsv(ruta_archivo):
    try:
        df = pd.read_csv(f"data/mitbih_database/{ruta_archivo}.csv")
        return df
    except FileNotFoundError: # Si no encuentro el archivo
        print(f"El archivo {ruta_archivo}.csv no existe.")
        return None