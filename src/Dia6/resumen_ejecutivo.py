import pandas as pd

def generar_resumen_ejecutivo(gold: pd.DataFrame) -> str:
    """Genera un resumen de texto para stakeholders no-técnicos.
    
    Args:
        gold: DataFrame con columnas [campana, fecha, revenue_neto, 
              num_transacciones, clientes_unicos]
    
    Returns:
        String con el resumen formateado
    """

    resumen = []
    resumen.append("=" * 50)
    resumen.append("RESUMEN DE CAMPAÑAS - Preview para presentacion")
    resumen.append("=" * 50)
    resumen.append("")

    # 1. Revenue total por campaña
    revenue_por_campana = gold.groupby("campana")["revenue_neto"].sum().to_dict()

    resumen.append("Revenue total por campaña:")
    for campana, revenue in revenue_por_campana.items():
        resumen.append(f"  • {campana.title()}: €{revenue:,.0f}")
    resumen.append("")

    # 2. Diferencia porcentual entre ambas
    if "verano" in revenue_por_campana and "primavera" in revenue_por_campana:
        rev_verano = revenue_por_campana["verano"]
        rev_primavera = revenue_por_campana["primavera"]
        diferencia_pct = ((rev_verano - rev_primavera) / rev_primavera) * 100
        
        if diferencia_pct > 0:
            resumen.append(
                f"Verano superó a Primavera en un {diferencia_pct:.1f}%."
            )
        else:
            resumen.append(
                f"Primavera superó a Verano en un {abs(diferencia_pct):.1f}%."
            )
        resumen.append("")

    # 3. Día pico de cada campaña
    resumen.append("Día con más ventas por campaña:")
    for campana in gold["campana"].unique():
        df_camp = gold[gold["campana"] == campana]
        idx_max = df_camp["revenue_neto"].idxmax()
        dia_pico = df_camp.loc[idx_max, "fecha"]
        revenue_pico = df_camp.loc[idx_max, "revenue_neto"]
        resumen.append(
            f"  • {campana.title()}: {dia_pico} (€{revenue_pico:,.0f})"
        )

    resumen.append("")
    resumen.append("=" * 50)

    return "\n".join(resumen)


# Test con datos de ejemplo
datos = pd.DataFrame({
    "campana": ["verano"]*3 + ["primavera"]*3,
    "fecha": ["2024-07-01", "2024-07-02", "2024-07-03",
              "2024-04-01", "2024-04-02", "2024-04-03"],
    "revenue_neto": [5000, 8000, 6000, 3000, 4500, 3500],
    "num_transacciones": [100, 160, 120, 60, 90, 70],
    "clientes_unicos": [80, 130, 95, 50, 72, 58],
})

print(generar_resumen_ejecutivo(datos))



