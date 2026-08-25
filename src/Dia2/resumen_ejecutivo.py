import pandas as pd
from pathlib import Path


BASE_DIR = Path.cwd()

#cargamos el csv que exportamos en el ejercicio anterior
ruta_segmentacion = BASE_DIR / 'data' / 'processed' / 'segmentacion_jorge.csv'
resultado = pd.read_csv(ruta_segmentacion)

#generar tabla resumen: segmento, cantidad, porcentaje
resumen = (
    resultado['segmento'].value_counts().reset_index()
)
resumen.columns = ['segmento', 'cantidad']
total = resumen['cantidad'].sum()

#calcular porcentaje de cada segmento y redondeado a 1 decimal
resumen['porcentaje'] = (100 * resumen['cantidad'] / total).round(1)

#ordenar de mayor a menor (value_counts ya lo hace, pero por si acaso)
resumen = resumen.sort_values(by='cantidad', ascending=False)

print("\n📊 Segmentacion de clientes - campaña verano 2024")
print("=" * 50)
print(resumen.to_string(index=False))
print(f"\n Total de clientes: {total:,}")