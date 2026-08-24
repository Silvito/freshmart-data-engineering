import pandas as pd
from pathlib import Path

#setear la ruta base para encontrar archivo csv
BASE_DIR = Path(__file__).resolve().parent.parent
ruta_clientes = BASE_DIR / 'data' / 'incoming' / 'campana_verano' / "campana_verano_clientes.csv"

#cargar el csv de clientes con parametro de la ruta del archivo
clientes = pd.read_csv(ruta_clientes)
print(f"CSV cargado desde : {ruta_clientes}")

#ejercicio 1: cuantas filas tiene?
total_filas = len(clientes)

#ejercicio 2: cuantos cliente_id unicos hay?
ids_unicos = clientes['cliente_id'].nunique()

#ejercicio 3: cuantas filas duplicadas (por cliente id) hay?
duplicados = total_filas - ids_unicos

#ejercicio 4: nulos por columna
nulos = clientes.isnull().sum()


print(clientes.head())
print(f"Total de filas: {total_filas}")
print(f"Cliente IDs únicos: {ids_unicos}")
print(f"Filas duplicadas: {duplicados}")
print(f"Nulos por columna:\n{nulos}")