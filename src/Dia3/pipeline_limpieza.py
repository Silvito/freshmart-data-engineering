import pandas as pd
import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(message)s', stream=sys.stdout, force=True)

BASE_DIR = Path.cwd()

#--- Configuracion de Rutas ---
ARCHIVOS = {
    'verano': BASE_DIR / "data" / "incoming" / "campana_verano" / "campana_verano_ventas.csv",
    'primavera': BASE_DIR / "data" / "incoming" / "campana_primavera" / "campana_primavera_ventas.csv",
}

COLUMNAS_OBLIGATORIAS = [
    'venta_id', 'cliente_id', 'producto_id', 'fecha_compra',
    'cantidad', 'precio', 'descuento_pct', 'tienda_id', 'campana'
]

COLUMN_MAPPINGS = {
    'verano': {}, #ya tiene los nombres correctos
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

#------------FUNCIONES DE LIMPIEZA ----------------------

def aplicar_mapping(df: pd.DataFrame, campana: str) -> pd.DataFrame:
    """Renombra columnas segun el mapping de la campaña"""
    mapping = COLUMN_MAPPINGS.get(campana, {})
    if mapping:
        df = df.rename(columns=mapping)

    faltantes = [col for col in COLUMNAS_OBLIGATORIAS if col not in df.columns]
    if faltantes:
        raise ValueError(f"Faltan columnas obligatorias: {faltantes}")

    return df

def limpiar_precio(df: pd.DataFrame) -> pd.DataFrame:
    """Convierte precio de '2,45€' a float. Si ya es numérico, no toca."""
    df = df.copy()
    
    # Solo limpiar si es string (tiene € o coma)
    if df['precio'].dtype == object:
        df['precio'] = (
            df['precio']
            .astype(str)
            .str.replace('€', '', regex=False)
            .str.replace(',', '.', regex=False)
            .astype(float)
        )
    return df

def normalizar_fechas(df: pd.DataFrame) -> pd.DataFrame:
    """Convierte fecha_compra a datetime."""
    df = df.copy()
    df['fecha_compra'] = pd.to_datetime(
        df['fecha_compra'],
        format='mixed',
        dayfirst=True,
    )
    
    nat_count = df['fecha_compra'].isna().sum()
    if nat_count > 0:
        logging.warning(f"  ⚠️  {nat_count} fechas no se pudieron parsear")
    else:
        logging.info("  ✓ Fechas normalizadas correctamente")
    
    return df


def marcar_anonimos(df: pd.DataFrame) -> pd.DataFrame:
    """Crea columna es_anonimo cuando cliente_id es nulo o vacío."""
    df = df.copy()
    df['es_anonimo'] = (
        df['cliente_id'].isna() |
        (df['cliente_id'].astype(str).str.strip() == '') |
        (df['cliente_id'].astype(str).str.lower() == 'nan')
    )
    return df


# ==================== PIPELINE PRINCIPAL ====================

resultados = []

for campana, ruta in ARCHIVOS.items():
    logging.info(f"\n{'='*40}")
    logging.info(f"Procesando: {campana}")
    logging.info(f"{'='*40}")

    # 1. Cargar
    if not ruta.exists():
        logging.warning(f"  ⚠️  No existe: {ruta}")
        continue
        
    df = pd.read_csv(ruta)
    logging.info(f"  Cargadas: {len(df):,} filas")

    # 2. Aplicar mapping
    df = aplicar_mapping(df, campana)
    logging.info("  ✓ Mapping aplicado")

    # 3. Eliminar duplicados
    antes = len(df)
    df = df.drop_duplicates()
    logging.info(f"  Duplicados eliminados: {antes - len(df)}")

    # 4. Normalizar fechas
    df = normalizar_fechas(df)

    # 5. Limpiar precio
    df = limpiar_precio(df)
    logging.info("  ✓ Precios limpios")

    # 6. Marcar anónimos
    df = marcar_anonimos(df)
    anonimos = df['es_anonimo'].sum()
    logging.info(f"  Anónimos detectados: {anonimos}")

    # 7. Filtrar cantidad = 0
    antes_filtro = len(df)
    df = df[df['cantidad'] > 0]
    logging.info(f"  Filtradas (cantidad=0): {antes_filtro - len(df)}")

    resultados.append(df)
    logging.info(f"  Resultado: {len(df):,} filas limpias")

# ==================== UNIFICAR ====================

if resultados:
    unificado = pd.concat(resultados, ignore_index=True)
    
    print(f"\n{'='*40}")
    print(f"RESUMEN FINAL")
    print(f"{'='*40}")
    print(f"Total filas: {len(unificado):,}")
    print(f"Por campaña: {unificado['campana'].value_counts().to_dict()}")
    print(f"Anónimos: {unificado['es_anonimo'].sum():,}")
    print(f"Rango de fechas: {unificado['fecha_compra'].min()} a {unificado['fecha_compra'].max()}")
    
    # Exportar a SILVER
    silver_dir = BASE_DIR / "data" / "silver"
    silver_dir.mkdir(exist_ok=True)
    unificado.to_csv(silver_dir / "ventas_unificado.csv", index=False)
    print(f"\n✅ Exportado a: data/silver/ventas_unificado.csv")
else:
    print("\n❌ No se procesó ningún archivo")