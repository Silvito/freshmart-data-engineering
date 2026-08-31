import pandas as pd
from pathlib import Path

BASE_DIR = Path.cwd()

#cargar csv de ventas

ruta_ventas = BASE_DIR / "data" / "incoming" / "campana_verano" / "campana_verano_ventas.csv"
ventas = pd.read_csv(ruta_ventas)

#Antes de limpiar
print("Tipo Original:", ventas['precio'].dtype)
print ("Ejemplo:", ventas['precio'].head(3).tolist())

def limpiar_precio(df: pd.DataFrame) -> pd.DataFrame:
    """Convierte precio de '2,45 euros a float 2.45"""
    df = df.copy()
    df['precio'] = (
        df['precio'].astype(str).str.replace('€', '', regex=False)
        .str.replace(',', '.', regex=False)
        .astype(float)
    )
    return df

ventas = limpiar_precio(ventas)

# despues de limpiar

print("\nTipo después:", ventas['precio'].dtype)
print(f"Mínimo: {ventas['precio'].min():.2f}€")
print(f"Máximo: {ventas['precio'].max():.2f}€")
print(f"Media: {ventas['precio'].mean():.2f}€")
print(f"Mediana: {ventas['precio'].median():.2f}€")
