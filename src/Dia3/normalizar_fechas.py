import pandas as pd
from pathlib import Path

BASE_DIR = Path.cwd()

#cargar csv ventas

ruta_ventas = BASE_DIR / "data" / "incoming" / "campana_verano" / "campana_verano_ventas.csv"
ventas = pd.read_csv(ruta_ventas)

print("Tipo original:", ventas['fecha_compra'].dtype)
print("Ejemplo formatos:")
print("  Primera fila:", ventas.loc[0, 'fecha_compra'])


def normalizar_fechas(df: pd.DataFrame) -> pd.DataFrame:
    """Convierte fecha_compra de 3 formatos a datetime."""
    df = df.copy()

    # pd.to_datetime con format='mixed' maneja múltiples formatos
    df['fecha_compra'] = pd.to_datetime(
        df['fecha_compra'],
        format='mixed',
        dayfirst=True,   # <-- TODO completado: DD/MM/YYYY es día primero
    )

    # Verificar que no quedaron NaT (Not a Time = fecha inválida)
    nat_count = df['fecha_compra'].isna().sum()
    if nat_count > 0:
        print(f"⚠️  {nat_count} fechas no se pudieron parsear")
        # Mostrar ejemplos de las que fallaron
        print("Ejemplos de fechas inválidas:")
        print(df.loc[df['fecha_compra'].isna(), 'fecha_compra'].head())
    else:
        print("✓ Todas las fechas parseadas correctamente")

    return df


ventas = normalizar_fechas(ventas)
print(f"\nTipo después: {ventas['fecha_compra'].dtype}")
print(f"Rango: {ventas['fecha_compra'].min()} a {ventas['fecha_compra'].max()}")
