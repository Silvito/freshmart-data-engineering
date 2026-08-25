import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path.cwd()

# --- 1. Cargar el CSV en SQLite ---
ruta_csv = BASE_DIR / "data" / "incoming" / "campana_verano" / "campana_verano_clientes.csv"
conn = sqlite3.connect(BASE_DIR / "freshmart.db")

print("Cargando campana_verano_clientes en SQLite...")
df = pd.read_csv(ruta_csv)

print(f"Tipo de 'compro': {df['compro'].dtype}")

if df['compro'].dtype == object:
    df['compro'] = df['compro'].map({'True': 1, 'False': 0})
    print("✅ Convertido 'compro' a 1/0")

df.to_sql("campana_verano_clientes", conn, if_exists="replace", index=False)
print("✅ Tabla cargada.\n")

# --- 2. Leer y limpiar el archivo .sql ---
ruta_sql = BASE_DIR / "sql" / "tasa_conversion.sql"

with open(ruta_sql, 'r', encoding='utf-8') as f:
    lineas = f.readlines()

# Eliminar líneas que empiezan con -- (comentarios)
lineas_limpias = [linea for linea in lineas if not linea.strip().startswith('--')]
sql_limpio = '\n'.join(lineas_limpias)

# Dividir por ';' y filtrar solo las queries SELECT
queries = [q.strip() for q in sql_limpio.split(';') if q.strip()]
selects = [q for q in queries if q.upper().startswith('SELECT')]

print(f"📄 SQL leído: {ruta_sql}")
print(f"Queries SELECT encontradas: {len(selects)}")

if len(selects) < 2:
    print("❌ ERROR: No se encontraron 2 queries SELECT")
    conn.close()
    exit(1)

# --- 3. Ejecutar cada SELECT ---
resultados = []

for i, query in enumerate(selects):
    df_result = pd.read_sql_query(query, conn)
    resultados.append(df_result)
    
    if i == 0:
        print("\n" + "=" * 50)
        print("CONVERSIÓN GLOBAL")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("CONVERSIÓN POR CANAL")
        print("=" * 50)
    
    print(df_result.to_string(index=False))

# --- 4. Conclusión ---
df_canal = resultados[1]
mejor = df_canal.iloc[0]

print("\n" + "=" * 50)
print("CONCLUSIÓN PARA JORGE")
print("=" * 50)
print(f"Canal ganador: {mejor['canal'].upper()}")
print(f"Tasa: {mejor['tasa_conversion_pct']}% ({int(mejor['compraron'])} de {int(mejor['alcanzados'])})")

conn.close()
print("\n✅ Proceso finalizado.")