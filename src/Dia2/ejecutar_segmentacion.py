import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path.cwd()

#ruta a los csv
ruta_campana = BASE_DIR / 'data' / 'incoming' / 'campana_verano' /'campana_verano_clientes.csv'
ruta_clientes = BASE_DIR / 'data' / 'incoming' / 'clientes.csv'
ruta_pedidos = BASE_DIR / 'data' / 'incoming' / 'pedidos.csv'

#crear base de datos sqlite (un archivo .db)
db_dir = BASE_DIR / 'sql'
db_dir.mkdir(exist_ok=True)
conn = sqlite3.connect(db_dir / 'freshmart.db')
print(f"✅ Conexión a SQLite creada en: {db_dir / 'freshmart.db'}")

#cargar los CSVs como tablas SQlite
pd.read_csv(ruta_campana).to_sql('campana_verano_clientes',
conn, if_exists='replace', index=False)
pd.read_csv(ruta_clientes).to_sql('clientes',
conn, if_exists='replace', index=False)
pd.read_csv(ruta_pedidos).to_sql('pedidos', 
conn, if_exists='replace', index=False)

print("✅ Tablas creadas en SQLite: campana_verano_clientes, clientes, pedidos")

#Leer archivo SQL
ruta_sql = BASE_DIR / 'sql' / 'segmentacion_sql.sql'
with open(ruta_sql, 'r') as f:
    query = f.read()
print(f"\n📄 Ejecutando query desde: {ruta_sql}")
print("-" * 50)

#ejecutar query
df_resultado = pd.read_sql_query(query, conn)

#Mostrar resultado
print(f"\n📊 Total de filas: {len(df_resultado)}")
print("\nPrimeras 10 filas:")
print(df_resultado.head(10))
print("\nDistribución de segmentos:")
print(df_resultado['segmento'].value_counts())
print(f"\nClientes sin pedidos: {(df_resultado['pedidos_ultimos_3m'] == 0).sum()}")

#guardar resultado
df_resultado.to_csv(BASE_DIR / 'data' / 'processed' / 'segmentacion_jorge.csv', index=False)
print(f"\n💾 Resultado guardado en: {BASE_DIR / 'data' / 'processed' / 'segmentacion_jorge.csv'}")

#cerrar conexión a DB
conn.close()
print("\n✅ Conexión a SQLite cerrada")