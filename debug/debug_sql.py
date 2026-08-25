from pathlib import Path

BASE_DIR = Path.cwd()
ruta_sql = BASE_DIR / "sql" / "tasa_conversion.sql"

print(f"Ruta: {ruta_sql}")
print(f"Existe: {ruta_sql.exists()}")
print(f"Tamaño: {ruta_sql.stat().st_size} bytes")
print("-" * 50)

with open(ruta_sql, 'r', encoding='utf-8') as f:
    contenido = f.read()

print("CONTENIDO RAW:")
print(repr(contenido))  # repr muestra caracteres especiales, saltos de línea, etc.
print("-" * 50)
print("CONTENIDO VISUAL:")
print(contenido)