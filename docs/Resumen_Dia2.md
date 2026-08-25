# 📚 Resumen del Día 2 — DATA-147: Cruce y Segmentación para Jorge

> Tutoría de Ingeniería de Datos — FreshMart Data Engineering  
> Fecha: 2024-09-17 (Día 2)

---

## 🎯 Contexto del Día

Después de explorar los datos (Día 1), el stakeholder **Jorge Ruiz** pidió segmentar a los 15K clientes de la campaña de verano según su actividad de compra reciente. El objetivo: entender quiénes son premium, quiénes regulares y quiénes no compraron — para tomar decisiones de marketing.

**Fuentes cruzadas:**
- `campana_verano_clientes.csv` — Lista de 15,247 clientes de la campaña
- `clientes.csv` — Tabla maestra del CRM (nombre, email, fecha_registro)
- `pedidos.csv` — Historial de pedidos del warehouse

---

## 1️⃣ Ejercicio [01] — Query de Segmentación SQL

### Conceptos clave aplicados

| Concepto | Uso en la query | Por qué importa |
|---|---|---|
| **CTE (`WITH`)** | Dividir la query en pasos lógicos | Legibilidad y mantenimiento |
| **LEFT JOIN** | Cruzar campaña con clientes y pedidos | Mantiene a todos los clientes de la campaña, incluso los que nunca compraron |
| **COALESCE(p.pedidos_3m, 0)** | Convertir NULL en 0 | Un cliente sin pedidos aparece como NULL en el JOIN; COALESCE lo convierte en 0 para poder clasificarlo |
| **CASE WHEN** | Clasificar en premium/regular/nuevo | Lógica de negocio: >6 = premium, 2-6 = regular, <2 = nuevo |
| **filtrar cancelados** | `estado != 'cancelado'` | Un pedido cancelado no es una venta real |

### Query SQL completa

```sql
WITH pedidos_recientes AS (
    SELECT
        cliente_id,
        COUNT(*) AS pedidos_3m
    FROM pedidos
    WHERE fecha_pedido >= '2024-06-16'
      AND estado != 'cancelado'
    GROUP BY cliente_id
),
segmentacion AS (
    SELECT
        c.cliente_id,
        m.nombre,
        m.fecha_registro,
        COALESCE(p.pedidos_3m, 0) AS pedidos_ultimos_3m,
        CASE
            WHEN COALESCE(p.pedidos_3m, 0) > 6 THEN 'premium'
            WHEN COALESCE(p.pedidos_3m, 0) >= 2 THEN 'regular'
            ELSE 'nuevo'
        END AS segmento
    FROM campana_verano_clientes c
    LEFT JOIN clientes m ON c.cliente_id = m.cliente_id
    LEFT JOIN pedidos_recientes p ON c.cliente_id = p.cliente_id
)
SELECT * FROM segmentacion
ORDER BY pedidos_ultimos_3m DESC;
```

### Arquitectura: SQLite sobre CSVs

Como trabajamos en local, usamos **Python + SQLite** para simular una base de datos:

```python
import sqlite3
import pandas as pd

conn = sqlite3.connect("freshmart.db")
pd.read_csv("campana_verano_clientes.csv").to_sql("campana_verano_clientes", conn, if_exists="replace")
# ... cargar las otras tablas
resultado = pd.read_sql_query(query, conn)
```

> **Lección:** Cuando los datos están en archivos locales, SQLite es la forma más rápida de ejecutar SQL real sin instalar servidores.

---

## 2️⃣ Ejercicio [02] — Resumen Ejecutivo de Segmentos

### Cálculo en Pandas

```python
resumen = resultado['segmento'].value_counts().reset_index()
resumen.columns = ['segmento', 'cantidad']
resumen['porcentaje'] = round(100 * resumen['cantidad'] / resumen['cantidad'].sum(), 1)
```

### Resultados obtenidos

| Segmento | Cantidad | Porcentaje |
|---|---|---|
| **Nuevo** (0-1 pedidos) | 10,944 | 70.4% |
| **Premium** (>6 pedidos) | 2,505 | 16.1% |
| **Regular** (2-6 pedidos) | 2,107 | 13.5% |
| **Total** | **15,556** | 100% |

> ⚠️ **Nota de calidad:** El total es 15,556 en vez de 15,247 porque `campana_verano_clientes.csv` contiene aproximadamente 309 `cliente_id` duplicados. En la etapa SILVER se debería deduplicar.

---

## 3️⃣ Ejercicio [03] — Investigación: ¿Quiénes son los 7.032 clientes sin pedidos?

### Hallazgo clave

Jorge preguntó si los clientes sin pedidos eran "captación reciente que no convirtió". El análisis reveló lo contrario:

| Grupo | Cantidad | % del total sin pedidos | Interpretación |
|---|---|---|---|
| **Sin pedidos** | 7,032 | 100% | Clientes de la campaña que no compraron en 3 meses |
| **Recientes** (registrados post-junio 2024) | 401 | **5.7%** | Nuevos que llegaron por la campaña y no compraron |
| **Antiguos** (registrados pre-junio 2024) | 6,631 | **94.3%** | Clientes históricos que **se fugaron** |

### Conclusión para el negocio

> **"La campaña de verano no falló en captar nuevos clientes. Falló en retener a los que ya tenía."**

- Solo **401** clientes nuevos se registraron después de junio y no compraron.
- **6,631 clientes antiguos** dejaron de comprar en los últimos 3 meses.
- Esto sugiere un problema de **fuga de clientes históricos**, no de captación.

### Código de análisis

```python
sin_pedidos = resultado[resultado['pedidos_ultimos_3m'] == 0].copy()
sin_pedidos['fecha_registro'] = pd.to_datetime(sin_pedidos['fecha_registro'])

fecha_corte = pd.Timestamp('2024-06-01')
recientes = sin_pedidos[sin_pedidos['fecha_registro'] >= fecha_corte]
antiguos = sin_pedidos[sin_pedidos['fecha_registro'] < fecha_corte]

pct_recientes = round(100 * len(recientes) / len(sin_pedidos), 1)
pct_antiguos = round(100 * len(antiguos) / len(sin_pedidos), 1)
```

---

## 4️⃣ Ejercicio [04] — Tasa de Conversión por Canal

### Trampa de datos: canal_contacto sucio

El CSV venía con variantes del mismo canal:
- `"email"` vs `"Email"`
- `"push"` vs `"push_notification"` vs `"Push"`

**Solución SQL:**
```sql
CASE
    WHEN LOWER(canal_contacto) LIKE 'push%' THEN 'push'
    ELSE LOWER(canal_contacto)
END AS canal
```

### Resultados de conversión

| Métrica | Valor |
|---|---|
| **Conversión global** | **19.65%** |

| Canal | Alcanzados | Compraron | Tasa de conversión |
|---|---|---|---|
| **SMS** | 1,537 | 586 | **38.13%** 🥇 |
| **Push** | 3,821 | 1,298 | **33.97%** 🥈 |
| **Email** | 9,889 | 1,112 | **11.24%** 🥉 |

### Insight de negocio

> **"Email alcanzó al 65% de la campaña pero solo convirtió al 11%. SMS alcanzó solo al 10% pero convirtió al 38%."**

- **Email** = barato, masivo, pero frío.
- **SMS** = caro, limitado, pero caliente.
- **Estrategia óptima:** segmentar — email para volumen, SMS para clientes de alto valor o ofertas urgentes.

### Query SQL completa

```sql
-- Conversión global
SELECT
    COUNT(*) AS total_alcanzados,
    SUM(compro) AS compraron,
    ROUND(100.0 * SUM(compro) / COUNT(*), 2) AS tasa_conversion_pct
FROM campana_verano_clientes;

-- Conversión por canal (normalizado)
SELECT
    CASE
        WHEN LOWER(canal_contacto) LIKE 'push%' THEN 'push'
        ELSE LOWER(canal_contacto)
    END AS canal,
    COUNT(*) AS alcanzados,
    SUM(compro) AS compraron,
    ROUND(100.0 * SUM(compro) / COUNT(*), 2) AS tasa_conversion_pct
FROM campana_verano_clientes
GROUP BY canal
ORDER BY tasa_conversion_pct DESC;
```

> **Nota técnica:** En SQLite, los booleanos `True/False` de Pandas se almacenan como `1/0`. Por eso `SUM(compro)` cuenta directamente los que compraron.

---

## 🧠 Lecciones del Día 2

### SQL
| Concepto | Cuándo usarlo |
|---|---|
| `LEFT JOIN` | Cuando necesitás **todos** los registros de la tabla izquierda, aunque no tengan match en la derecha. Esencial para no perder clientes sin pedidos. |
| `COALESCE(valor, 0)` | Cuando un `LEFT JOIN` devuelve `NULL` y necesitás tratarlo como 0 para matemáticas o clasificaciones. |
| `CASE WHEN` | Para aplicar reglas de negocio (segmentación, categorización) directamente en la query. |
| `LOWER()` + `LIKE 'prefijo%'` | Para normalizar texto sucio antes de agrupar. |
| `SUM(booleano)` | Para contar cuántos `True` hay en una columna booleana (en SQLite/PostgreSQL). |

### Python / Pandas
| Patrón | Uso |
|---|---|
| `value_counts()` | Contar ocurrencias de categorías. |
| `round(100 * parte / total, 1)` | Calcular porcentajes con 1 decimal. |
| `pd.to_datetime()` | Convertir strings de fecha a objetos datetime para comparar. |
| `df[df['col'] == 0]` | Filtrar filas con boolean mask. |
| `Path.cwd()` | Obtener la raíz del proyecto cuando ejecutás desde ahí. |

### Comunicación con stakeholders
- **Siempre comunicar el hallazgo, no solo el archivo.** Jorge no quería el CSV; quería saber qué significaban los 6,852 clientes sin pedidos.
- **Nunca asumir que un dato raro es un error.** Los "datos raros" a veces son exactamente lo que el negocio quiere analizar.
- **Iterar:** Jorge pidió agregar `fecha_registro` después de ver el primer resultado. Esto es normal en la vida real.

---

## 📁 Archivos generados en el Día 2

```
src/
├── Dia2/
│   ├── segmentacion_sql.sql           -- Query SQL de segmentación
│   ├── ejecutar_segmentacion.py       -- Orquestador SQLite + SQL
│   ├── resumen_segmentos.py           -- Ejercicio [02] en Pandas
│   ├── investigar_pedidos.py          -- Ejercicio [03] análisis sin pedidos
│   ├── tasa_conversion.sql            -- Query SQL de conversión por canal
│   └── ejecutar_tasa_conversion.py    -- Orquestador SQLite + SQL
├── sql/
│   └── tasa_conversion.sql            -- Query SQL pura (alternativa)
output/
└── segmentacion_jorge.csv             -- Resultado del cruce para el stakeholder
```

---

## 🔗 Relación con el Día 1

| Día 1 (Exploración) | Día 2 (Análisis) |
|---|---|
| Detectamos ~301 duplicados en clientes | El cruce SQL retornó 15,556 filas en vez de 15,247 |
| Detectamos 645 filas de ventas sin formato de fecha | Pendiente para limpieza en SILVER |
| Detectamos nulos en `abrio_email` y `clickeo_link` | En el Día 3 se deberán decidir reglas de imputación |
| Creamos la estructura RAW del data lake | Los datos crudos siguen intactos en `data/raw/...` |

---

## 🚀 Próximos pasos sugeridos

1. **Deduplicar** `campana_verano_clientes` antes de pasar a SILVER.
2. **Investigar** las 645 filas de ventas sin formato de fecha detectadas en el Día 1.
3. **Normalizar** `canal_contacto` a minúsculas en la capa SILVER para evitar el problema de limpieza en cada query.
4. **Documentar** el hallazgo de la fuga de clientes antiguos (6,631) como un ticket separado para el equipo de retención.

---

*Resumen generado durante la tutoría de Ingeniería de Datos — FreshMart*
