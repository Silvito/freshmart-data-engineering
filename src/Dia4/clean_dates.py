import pandas as pd
import logging
import sys

logging.basicConfig(
    level=logging.WARNING,
    format="%(levelname)s: %(message)s",
    stream=sys.stdout,
    force=True
)

logger = logging.getLogger(__name__)

def clean_dates(df: pd.DataFrame, has_mixed_formats: bool) -> pd.DataFrame:
    """Normaliza fecha_compra a datetime.
    -Si has_mixed_formats es true, usa formats ='mixed'
    - Si alguna fecha no se puede parsear, usa errors='coerce'
    - Loggea cuantas fechas quedaron como nat
    """

    try:
        if has_mixed_formats:
            df["fecha_compra"] = pd.to_datetime(
                df["fecha_compra"], format='mixed', dayfirst=True
            )
        else:
            df["fecha_compra"] = pd.to_datetime(
                df["fecha_compra"], dayfirst=True
            )
    except Exception as e:
        logger.warning(f"Fechas no parseables ({type(e).__name__}). Reintento con errors='coerce'.")
        df["fecha_compra"] = pd.to_datetime(
            df["fecha_compra"], format="mixed", dayfirst=True, errors="coerce"
        )
        nulas = df["fecha_compra"].isna().sum()
        logger.warning(f"{nulas} fechas convertidas a NaT")
    
    return df

#test con datos de ejemplo
datos = pd.DataFrame({
    "fecha_compra": [
        "2024-07-15",
        "15/07/2024",
        "Jul 15, 2024",
        "esto-no-es-fecha"
    ]
})

resultado = clean_dates(datos, has_mixed_formats=True)
print(resultado["fecha_compra"])
print(f"NaT count: {resultado['fecha_compra'].isna().sum()}")
