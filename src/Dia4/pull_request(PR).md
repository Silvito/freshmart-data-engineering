## Qué hace

- Pipeline de ingesta de campañas de Marketing (raw → silver)
- Mapping configurable para diferentes formatos de CSV (verano, primavera)
- Limpieza: normalización de fechas (3 formatos), precios (€ + coma), duplicados
- Validaciones de calidad: vacío, NULLs, precios positivos, rango fechas, unicidad

## Cómo probar
```bash
cd pipelines/campaign_ingestion
python run.py --campaign verano --input data/raw/ --output data/silver/
pytest tests/ -v
```

## Decisiones de diseño
- **Enum para campañas:** Evita typos silenciosos. Si escribes Campaign.VERAMO
  te da un error inmediato en vez de devolver un dict vacío.
- **Ventas anónimas no se eliminan:** Guest checkout es un caso de uso válido.
  Se marcan con es_anonimo=True para que el analista decida si filtrarlas.
- **errors='coerce' como fallback en fechas:** Prefiero perder 1 fecha (NaT)
  antes que tumbar el pipeline entero por un registro corrupto.

## Contexto de negocio
María necesita los datos para la presentación del jueves a dirección.
Los datos de primavera se añadirán mañana con el mismo pipeline (solo requiere
añadir una entrada al mapping en config.py).