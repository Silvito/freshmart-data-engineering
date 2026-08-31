import pandas as pd
from pathlib import Path

BASE_DIR = Path.cwd()

COLUMNAS_OBLIGATORIAS = [
    'venta_id' , 'cliente_id' , 'producto_id' , 'fecha_compra' ,
    'cantidad', 'precio', 'descuento_pct', 'tienda_id', 'campana'
]

COLUMN_MAPPINGS = {
    'verano': {}, #tiene los nombres correctos
    'primavera': {
        'id_transaccion': 'venta_id',
        'id_cliente': 'cliente_id',
        'id_producto': 'producto_id',
        'fecha_venta': 'fecha_compra',
        'unidades': 'cantidad',
        'importe': 'precio',
        'descuento': 'descuento_pct',
        'almacen': 'tienda_id',
        'promocion': 'campana',
    },
}

def aplicar_mapping(df: pd.DataFrame, campana: str) -> pd.DataFrame:
    """Renombra columnas segun el mapping de la campaña."""
    mapping = COLUMN_MAPPINGS.get(campana, {})

    #renombrar si hay mapping
    if mapping:
        df = df.rename(columns=mapping)

    #validar columnas obligatorias
    faltantes = [col for col in COLUMNAS_OBLIGATORIAS if col not in df.columns]
    if faltantes:
        raise ValueError(f"Faltan columnas obligatorias: {faltantes}")
    return df


#probar con primavera
ruta_primavera = BASE_DIR / "data" / "incoming" / "campana_primavera" / "campana_primavera_ventas.csv"

if ruta_primavera.exists():
    primavera = pd.read_csv(ruta_primavera)
    print("Antes:", list(primavera.columns))

    primavera  = aplicar_mapping(primavera, 'primavera')
    print("Despues:", list(primavera.columns))
    print("\n✓ Mapping aplicado correctamente")
else:
    print(f"⚠️  No existe el archivo: {ruta_primavera}")
    print("Ajustá la ruta si el CSV está en otra carpeta.")



