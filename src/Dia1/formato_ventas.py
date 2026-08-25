import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ruta_ventas = BASE_DIR / 'data' / 'incoming' / 'campana_verano' / "campana_verano_ventas.csv"

#cargamos el archivo csv
ventas = pd.read_csv(ruta_ventas)

#detectar formato ISO de fecha_compra: YYYY-MM-DD (ej: 2024-07-15)
formato_iso = ventas['fecha_compra'].str.match(r'^\d{4}-\d{2}-\d{2}$')

#detectar formato europeo de fecha_compra: DD/MM/YYYY (ej: 15/07/2024)
formato_eu = ventas['fecha_compra'].str.match(r'^\d{2}/\d{2}/\d{4}$')

#detectar formato americano: Mon DD, YYYY (ej: Jul 15, 2024)
formato_us = ventas['fecha_compra'].str.match(r'^[A-Za-z]{3} \d{2}, \d{4}$')

#contar cada uno
print(f"Formato ISO (YYYY-MM-DD): {formato_iso.sum()} filas")
print(f"Formato Europeo (DD/MM/YYYY): {formato_eu.sum()} filas")
print(f"Formato Americano (Mon DD, YYYY): {formato_us.sum()} filas")
print (f"Total de filas: {len(ventas)}")

#mostrar ejemplos de cada uno
print("\n Ejemplos ISO:", ventas[formato_iso]['fecha_compra'].head(3).tolist())
print("Ejemplos Eu:", ventas[formato_eu]['fecha_compra'].head(3).tolist())
print("Ejemplos US:", ventas[formato_us]['fecha_compra'].head(3).tolist())