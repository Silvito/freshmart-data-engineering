import pandas as pd
from pathlib import Path

BASE_DIR = Path.cwd()

#Cargamos resultado de la segmentacion
ruta = BASE_DIR / "data" / "processed" / "segmentacion_jorge.csv"
resultado = pd.read_csv(ruta)

#filtrar clientes sin pedidos
sin_pedidos = resultado[resultado['pedidos_ultimos_3m'] == 0].copy()
print(f"Clientes sin pedidos: {len(sin_pedidos)}")

#convertir fecha_registro a datetime
sin_pedidos['fecha_registro'] = pd.to_datetime(sin_pedidos['fecha_registro'])

#cuantos se registraron despues del 2024-06-01? (captacion reciente)
fecha_captacion = pd.Timestamp('2024-06-01')
recientes = sin_pedidos[sin_pedidos['fecha_registro'] >= fecha_captacion]
antiguos = sin_pedidos[sin_pedidos['fecha_registro'] < fecha_captacion]

print(f"Registros recientes(post junio 2024): {len(recientes)}")
print(f"Registros antiguos(pre junio 2024): {len(antiguos)}")

total_sin_pedidos = len(sin_pedidos)
pct_recientes = round(100 * len(recientes) / total_sin_pedidos, 1)
pct_antiguos = round(100 * len(antiguos) / total_sin_pedidos, 1)

print(f"\n% captacion reciente: {pct_recientes}")
print(f"antiguos que dejaron de comprar: {pct_antiguos}")

#conclusion para jorge:
print("\n" + "=" * 50)
print("Conclusión para Jorge:")
print("=" * 50)

if pct_recientes > 50:
    print(f"La mayoría de los clientes sin pedidos ({pct_recientes}%) son")
    print("captación reciente (se registraron post-junio 2024).")
    print("Esto sugiere que la campaña de verano atrajo nuevos registros")
    print("pero no logró convertirlos en compradores.")
else:
    print(f"La mayoría de los clientes sin pedidos ({pct_antiguos}%) son")
    print("clientes antiguos que dejaron de comprar en los últimos 3 meses.")
    print("Esto sugiere fuga de clientes históricos, no falla en captación.")
