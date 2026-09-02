# Cierre del Día 3 — Limpieza y Estandarización

## Resumen del día
En el Día 3 se trabajó la **capa SILVER** del pipeline de datos. El foco principal fue la **limpieza y estandarización** de los datos crudos (RAW) para dejarlos consistentes, tipados y listos para análisis.

---

## Ejercicios realizados

| Ejercicio                  | Status | Qué se hizo                                                                 |
|---------------------------|--------|-----------------------------------------------------------------------------|
| **[01] Limpiar precios**  | ✅     | Transformación de precios con formato europeo (`2,45€`) a `float` (`2.45`) |
| **[02] Normalizar fechas**| ✅     | Unificación de 3 formatos de fecha mixtos hacia `datetime64`               |
| **[03] Column mapping**   | ✅     | Mapeo de nombres de campaña al esquema estándar de la capa SILVER          |
| **[04] Pipeline completo**| ✅     | Construcción del flujo end-to-end: **RAW → SILVER**                        |

---

## Pipeline completo (RAW → SILVER)

El ejercicio 04 integró todos los pasos anteriores en un único flujo de transformación:

1. **Column mapping** → Alineación con el esquema estándar SILVER  
2. **Deduplicación** → Eliminación de registros duplicados  
3. **Normalización de fechas** → Conversión a `datetime64`  
4. **Limpieza de precios** → Conversión a tipo numérico (`float`)  
5. **Anonimización** → Tratamiento de datos sensibles  
6. **Filtrado** → Aplicación de reglas de calidad / negocio  
7. **Unificación** → Consolidación final del dataset limpio  

---

## Resultado del día
Se completó exitosamente la transformación de datos desde la capa **RAW** hasta la capa **SILVER**, dejando los datos limpios, tipados y estandarizados.
