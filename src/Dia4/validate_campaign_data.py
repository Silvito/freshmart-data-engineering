import pandas as pd

def validate_campaign_data(df: pd.DataFrame) -> dict[str, bool]:
    """Ejecuta 5 validaciones de calidad sobre los datos de campaña.
    
    Returns: dict con nombre_validacion: true/false
    """

    results = {}

    #1. El Dataframe no esta vacio (comprueba que len(df) > 0)
    results["no_vacio"] = len(df) > 0

    #2. Campos obligatorios no tienen NULLs (comprueba .notna().all()
    # en cada obligatorio
    campos_obligatorios = ["venta_id", "producto_id", "fecha_compra",
                           "precio"]
    results["sin_nulls_obligatorios"] = df[campos_obligatorios].notna().all().all()

    #3. Todos los precios son > 0 (positivos)
    results["precios_positivos"] = (df["precio"] > 0).all()

    #4. Fechas dentro del rango de campaña verano (2024-06-15 a 2024-09-15)
    results["fechas_en_rango"] = ((df["fecha_compra"] >= "2024-06-15") & (df["fecha_compra"] <= "2024-09-15")).all()

    #5. No hay filas 100% duplicadas (comprueba que df.duplicated().sum() == 0)
    results["sin_duplicados"] = df.duplicated().sum() == 0

    return results

#test con datos de ejemplo
datos_test = pd.DataFrame({
    "venta_id": [1, 2, 3, 4],
    "producto_id": [101, None, 103, 104],
    "fecha_compra": pd.to_datetime(["2024-06-20", "2024-07-15", "2024-08-10", "2024-09-01"]),
    "cantidad": [1, 2, 1, 3],
    "precio": [10.0, 20.0, 30.0, 40.0]
})

resultados = validate_campaign_data(datos_test)
for nombre, paso in resultados.items():
    print(f"{'✓' if paso else '✗'} {nombre}")