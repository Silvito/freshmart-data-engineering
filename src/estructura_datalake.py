import shutil
from pathlib import Path

BASE_DIR = Path.cwd()

#Origen: donde estan los csv originales enviados
ORIGEN = BASE_DIR / 'data' / 'incoming' / 'campana_verano'
#Destino: tu zona RAW del data lake
LAKE_RAW = BASE_DIR / 'data' / 'raw' / 'campana_verano'
FUENTE = "marketing"
#fecha de INGESTION
ANIO, MES, DIA = "2024", "09", "16"

archivos = [
    "campana_verano_clientes.csv",
    "campana_verano_ventas.csv",
    "productos_promo_verano.csv"
]

print(f"📂 Origen: {ORIGEN}")
print(f"📂 Destino RAW: {LAKE_RAW}\n")

for archivo in archivos:
    #Extraer nombre de la tabla (sin extension .csv)
    tabla = Path(archivo).stem
    #construir ruta de destino: raw/marketing/{tabla}/2024/09/16/
    destino = LAKE_RAW / FUENTE / tabla / ANIO / MES / DIA
    #crear directorios (incluyendo padres si no existen)
    destino.mkdir(parents=True, exist_ok=True)
    print(f"Crear: {destino}")

    #copiar archivo original sin modificar
    shutil.copy(ORIGEN / archivo, destino / archivo)
    print(f"✓ {archivo} → {destino}\n")