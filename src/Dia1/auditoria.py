import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def auditoria_rapida(df: pd.DataFrame, nombre: str) -> dict:
    #genera un resumen de calidad basico para un dataframe
    total_filas = len(df)
    total_columnas = len(df.columns)
    filas_duplicadas = df.duplicated().sum()
    nulos_totales = df.isnull().sum().sum()
    porcentajes_nulos = (nulos_totales / (total_filas * total_columnas)) * 100 if total_filas > 0 else 0.0

    return {
        "archivo": nombre,
        "total_filas": total_filas,
        "total_columnas": total_columnas,
        "filas_duplicadas": filas_duplicadas,
        "nulos_totales": nulos_totales,
        "porcentaje_nulos": porcentajes_nulos
    }

#cargar los 3 archivos
archivos = {
    "clientes": BASE_DIR / 'data' / 'incoming' / 'campana_verano' / "campana_verano_clientes.csv",
    "ventas": BASE_DIR / 'data' / 'incoming' / 'campana_verano' / "campana_verano_ventas.csv",
    "productos": BASE_DIR / 'data' / 'incoming' / 'campana_verano' / "productos_promo_verano.csv"
}

for nombre, ruta in archivos.items():
    df = pd.read_csv(ruta)
    resumen = auditoria_rapida(df, nombre)
    print(f"\n{'='*40}")
    print(f"  {resumen['archivo'].upper()}")
    print(f"{'='*40}")
    for k, v in resumen.items():
        if k != 'archivo':
            print(f"  {k}: {v}")