import os  # Módulo para interactuar con el sistema de archivos
import pandas as pd  # Librería para manipulación y análisis de datos estructurados

# Ruta de entrada y salida como constantes para facilitar su mantenimiento y reutilización
INPUT_PATH = "files/input/solicitudes_de_credito.csv"
OUTPUT_DIR = "files/output"
OUTPUT_FILE = "solicitudes_de_credito.csv"

def convertir_fecha(fecha):
    """
    Intenta convertir una cadena a un objeto datetime en dos formatos posibles.
    Devuelve NaT si ambos intentos fallan.
    """
    fecha_convertida = pd.to_datetime(fecha, format="%d/%m/%Y", errors="coerce")
    if pd.isna(fecha_convertida):
        fecha_convertida = pd.to_datetime(fecha, format="%Y/%m/%d", errors="coerce")
    return fecha_convertida

def limpiar_texto(df, columnas):
    """
    Aplica limpieza estándar a columnas de texto:
    - Convierte a minúsculas.
    - Reemplaza guiones y guiones bajos por espacios.
    """
    return df[columnas].apply(lambda col: col.str.lower().str.replace(r"[-_]", " ", regex=True))

def normalizar_monto_credito(monto):
    """
    Limpia la columna 'monto_del_credito':
    - Elimina '.00' al final.
    - Elimina caracteres no numéricos como puntos, comas, espacios y símbolos de moneda.
    """
    return monto.str.replace(".00", "").str.replace(r"[,. $]", "", regex=True)

def crear_directorio_si_no_existe(ruta):
    """
    Crea el directorio si no existe, para evitar errores al guardar archivos.
    """
    os.makedirs(ruta, exist_ok=True)

def pregunta_01():
    """
    Limpia el archivo CSV de solicitudes de crédito:
    - Elimina duplicados y registros con datos faltantes.
    - Normaliza campos de texto y fechas.
    - Guarda el resultado limpio en una nueva ruta.
    """

    # Paso 1: Cargar datos con el primer campo como índice y separador ';'
    df = pd.read_csv(INPUT_PATH, index_col=0, sep=";")

    # Paso 2: Columnas que requieren limpieza textual especial
    columnas_texto = ["barrio", "línea_credito", "idea_negocio", "monto_del_credito"]

    # Paso 3: Normalización de columnas específicas
    df["sexo"] = df["sexo"].str.lower()
    df["tipo_de_emprendimiento"] = df["tipo_de_emprendimiento"].str.lower()

    # Paso 4: Limpieza y normalización del monto del crédito
    df["monto_del_credito"] = normalizar_monto_credito(df["monto_del_credito"])

    # Paso 5: Limpieza general de columnas de texto definidas
    df[columnas_texto] = limpiar_texto(df, columnas_texto)

    # Paso 6: Conversión de fechas con distintos formatos
    df["fecha_de_beneficio"] = df["fecha_de_beneficio"].apply(convertir_fecha)

    # Paso 7: Eliminar duplicados exactos
    df.drop_duplicates(inplace=True)

    # Paso 8: Eliminar filas con valores faltantes
    df.dropna(inplace=True)

    # Paso 9: Crear directorio de salida si no existe
    crear_directorio_si_no_existe(OUTPUT_DIR)

    # Paso 10: Guardar archivo limpio como CSV con separador ';' y sin índice
    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
    df.to_csv(output_path, index=False, sep=";")
