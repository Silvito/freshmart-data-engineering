# 📚 Resumen de la Sesión — DATA-147: Ingesta y Exploración

> Tutoría de Ingeniería de Datos — FreshMart Data Engineering  
> Fecha: 2026-08-24

---

## 1️⃣ Instalación y Entorno (Windows)

| Concepto | Qué aprendimos |
|---|---|
| **Python 3.11** | Descargar el `.exe` de python.org, marcar ✅ *"Add to PATH"*. |
| **Entorno virtual** | `py -3.11 -m venv .venv` → crea el entorno. |
| **Activación** | `.\.venv\Scripts\Activate.ps1` (PowerShell). |
| **Problema común** | Si falla la activación: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`. |
| **Rutas con `pathlib`** | `Path(__file__).resolve().parent.parent` para apuntar siempre a la raíz del proyecto, sin importar desde dónde ejecutes. |

---

## 2️⃣ Ejercicio [01] — Exploración de Datos

**Archivo:** `campana_verano_clientes.csv`

### Funciones de Pandas clave

```python
len(df)                          # Total de filas
df['columna'].nunique()          # Valores únicos en una columna
df.isnull().sum()                # Nulos por columna
df.head()                        # Primeras 5 filas
```

### Lecciones importantes

- **Duplicados ≠ Filas extra:** `total_filas - ids_unicos` te da las filas repetidas, pero no cuántos clientes distintos están afectados.
- **Los nulos tienen significado:** No siempre son "datos rotos". En este caso, los nulos en `clickeo_link` o `primer_compra_campana` significaban *"el cliente no interactuó/no compró"*.
- **Inconsistencias de texto:** `email` vs `Email` son el mismo canal escrito de formas distintas. Hay que estandarizar en SILVER.

---

## 3️⃣ Ejercicio [02] — Detección de Formatos de Fecha

**Archivo:** `campana_verano_ventas.csv`

### Regex con Pandas

```python
mascara = df['columna'].str.match(r'^\d{4}-\d{2}-\d{2}')  # True/False por fila
mascara.sum()                                               # Contar cuántas coinciden
df[mascara]['columna'].head(3).tolist()                    # Mostrar ejemplos
```

### Lecciones importantes

- **Siempre verificá que la suma de categorías cierre con el total.** Acá faltaban **645 filas** que ninguna regex capturó.
- **Nulos vs Datos sucios:** Las 645 filas no eran `NaN` (solo había 847 nulos en todo el dataset). Eran **valores con formato inesperado** o corrupto.
- **Un buen Data Engineer no avanza a limpiar sin investigar primero qué hay en los datos que no encajan.**

---

## 4️⃣ Ejercicio [03] — Estructura del Data Lake (RAW)

### Concepto: ¿Qué es un Data Lake?

Un repositorio que guarda los datos en su **forma original**, organizados por convención, para poder reconstruir todo el pipeline desde cero si es necesario.

### Zonas del Lake

| Zona | Propósito |
|---|---|
| **RAW** | Datos originales, inmutables, sin tocar. |
| **SILVER** | Datos limpios, validados, tipados correctamente. |
| **GOLD** | Tablas finales listas para negocio (dashboards, ML, reportes). |

### Código clave

```python
from pathlib import Path
import shutil

destino = Path("data/raw/...") / fuente / tabla / anio / mes / dia
destino.mkdir(parents=True, exist_ok=True)     # Crea toda la jerarquía
shutil.copy(origen, destino / archivo)          # Copia sin modificar
```

### Lecciones importantes

- **RAW es inmutable:** Nunca modificás el archivo original. Siempre copiás.
- **Particionar por fecha** (`año/mes/día`) permite ingestar la misma tabla múltiples veces sin sobrescribir.
- **Usá `pathlib` en vez de strings** para que tu código funcione en Windows, Linux y macOS.

---

## 5️⃣ Ejercicio [04] — Auditoría Rápida de Calidad

### Función reutilizable

```python
def auditoria_rapida(df: pd.DataFrame, nombre: str) -> dict:
    total_filas = len(df)
    total_columnas = len(df.columns)
    filas_duplicadas = df.duplicated().sum()           # Filas 100% idénticas
    nulos_totales = df.isnull().sum().sum()            # Suma de todos los NaN
    porcentaje_nulos = (nulos_totales / (total_filas * total_columnas)) * 100
    return {...}
```

### Hallazgos clave del análisis

| Archivo | Filas | Duplicados (100%) | % Nulos | Observación |
|---|---|---|---|---|
| **Clientes** | 15.247 | 2 | 23.59% | Nulos esperables (no todos compran/clickean). |
| **Ventas** | 42.891 | 155 | 0.22% | 155 filas clonadas → posible bug de ingestión. |
| **Productos** | 312 | 0 | 0% | Tabla maestra limpia. |

### Lecciones importantes

- **`df.duplicated()`** detecta filas donde **todas las columnas** son iguales. Es diferente de duplicados en una sola columna (ej: `cliente_id` repetido).
- **El % de nulos solo tiene sentido con contexto:** 23% en clientes no es malo si los nulos representan "no aplica".
- **Compará siempre con el total:** 155 duplicados en 42.891 filas es poco, pero en transacciones financieras **ninguna duplicación es aceptable sin explicación**.

---

## 🧠 Mindset del Data Engineer (lo más importante)

> **"Antes de limpiar, no tocamos absolutamente nada."**

1. **Explorá primero.** Nunca asumas que los datos están limpios.
2. **Validá que los números cierren.** Si sumás categorías y no da el total, investigá qué falta.
3. **Los nulos no siempre son errores.** Preguntate: ¿significa "dato faltante" o "no aplica"?
4. **Documentá todo.** RAW existe para que puedas volver atrás y demostrar qué encontraste.
5. **Estandarizá en SILVER, no en RAW.** En RAW guardás lo que recibiste. En SILVER aplicás reglas de negocio.

---

## 📁 Archivos generados en esta sesión

- `src/explorar_campana.py` — Ejercicio [01]
- `src/auditoria_rapida.py` — Ejercicio [04]
- `src/estructura_datalake.py` — Ejercicio [03]
- `data/raw/campana_verano/marketing/...` — Zona RAW del Data Lake

---

*Generado durante la tutoría de Ingeniería de Datos — FreshMart*
