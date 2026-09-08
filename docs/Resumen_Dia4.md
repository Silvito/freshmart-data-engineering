# Cierre del Día 4 — Pipeline Completo, Tests y Pull Request

## Resumen del día
En este día se ensambló el **pipeline profesional RAW → SILVER**, se escribieron validaciones de calidad, tests unitarios y se preparó la descripción del primer Pull Request. También se practicó la negociación de scope con Elena y se corrigió código según code review.

---

## Actividades realizadas

| Ejercicio / Actividad                        | Status | Qué se hizo                                                                 |
|---------------------------------------------|--------|-----------------------------------------------------------------------------|
| **Standup y negociación de scope**          | ✅     | Se mantuvo el deadline de verano y se pospuso primavera                     |
| **Estructura profesional del pipeline**     | ✅     | Organización modular: `config.py`, `clean.py`, `validate.py`, `run.py`     |
| **[02] Corregir `clean_dates`**             | ✅     | Se eliminó `infer_datetime_format` (deprecated) y se usó `format="mixed"` + try/except con `errors="coerce"` |
| **Validaciones de calidad**                 | ✅     | 5 dimensiones: completitud, unicidad, validez, consistencia y no vacío     |
| **[03] Tests unitarios**                    | ✅     | 4 tests para `validate_positive_prices` y `validate_no_duplicates`         |
| **[04] Descripción del PR**                 | ✅     | Markdown profesional con secciones Qué hace / Cómo probar / Decisiones de diseño |

---

## Pipeline completo (RAW → SILVER)

El flujo final quedó estructurado así:

1. **Leer** CSV desde `data/raw/`
2. **Aplicar column mapping** según la campaña
3. **Eliminar duplicados**
4. **Limpiar fechas** (`format="mixed"` + fallback con `errors="coerce"`)
5. **Limpiar precios** (quitar `€`, cambiar coma por punto)
6. **Marcar anónimos** (sin eliminar las filas)
7. **Filtrar filas inválidas** (`cantidad <= 0`)
8. **Ejecutar validaciones** de calidad
9. **Escribir** solo si todas las validaciones pasan → `data/silver/*.parquet`

---

## Lo que aprendí

### 1. Negociación de scope
Cuando los requisitos crecen a mitad de sprint, no se responde con un “sí” automático.  
La forma profesional es:

> “Puedo entregar A para el miércoles o A+B para el jueves. ¿Qué prefieres?”

### 2. Código modular y responsabilidades claras
- `config.py` → solo configuración
- `clean.py` → solo transformaciones (funciones puras)
- `validate.py` → solo validaciones
- `run.py` → solo orquestación

Cada archivo tiene **una sola responsabilidad**.

### 3. Validaciones de calidad de datos
Un pipeline profesional no solo limpia: **verifica** el resultado.  
Las 5 dimensiones clave:
- Completitud
- Unicidad
- Validez
- Consistencia (fechas en rango)
- Existencia (DataFrame no vacío)

### 4. Tests unitarios
Los tests no verifican los datos, verifican que **las funciones de validación funcionen correctamente**.  
Se aprendió la importancia de convertir `numpy.bool_` a `bool` de Python para evitar asserts confusos.

### 5. Code review y código mantenible
- No usar parámetros deprecated (`infer_datetime_format`)
- Preferir `format="mixed"` + `dayfirst=True`
- Usar `try/except` + `errors="coerce"` para que una fecha rota no tumbe todo el pipeline
- Loggear cuántas fechas quedaron como `NaT`

### 6. Pull Request
Un PR no es solo código: es una **propuesta de cambio** que debe explicar:
- Qué hace
- Cómo probarlo
- Por qué se tomaron ciertas decisiones de diseño

---

## Decisiones de diseño clave

| Decisión | Motivo |
|----------|--------|
| Usar `Enum` para campañas | Evita typos y facilita añadir nuevas campañas |
| No eliminar ventas anónimas | Son transacciones reales; se marcan con `es_anonimo` |
| No escribir en silver si falla una validación | Preferible no tener dato a tener un dato en el que nadie confía |
| Funciones puras en `clean.py` | Fáciles de testear y reutilizar |

---

## Resultado del día
Se entregó un pipeline profesional, testeado y documentado, listo para code review y merge. Se pasó de “funciones sueltas” a un flujo completo, configurable y mantenible.
