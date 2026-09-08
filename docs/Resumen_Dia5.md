# Cierre — Diagnóstico de DAGs y Lectura Segura de Credenciales

## Resumen del día
Se trabajó el lado **operacional** de un pipeline: cómo diagnosticar un fallo en producción a partir de logs de Airflow y cómo implementar la lectura segura de credenciales (sin hardcodear passwords).

---

## Actividades realizadas

| Ejercicio | Status | Qué se hizo |
|-----------|--------|-------------|
| **[01] Diagnosticar fallo de DAG** | ✅ | Análisis de logs de Airflow, identificación del error exacto y clasificación del tipo de problema |
| **[02] Lectura segura de credenciales** | ✅ | Función que prioriza Secrets Manager y usa variables de entorno como fallback |
| **Razonamiento de diseño** | ✅ | Entender el *por qué* detrás de cada decisión (prioridad, fallback, error explícito) |

---

## Ejercicio 01 — Leer logs y diagnosticar un fallo

### Qué ocurrió
Un DAG de Airflow falló al intentar conectarse a PostgreSQL. Los logs mostraban:

```
ERROR - Connection failed: psycopg2.OperationalError: 
FATAL: password authentication failed for user "data_readonly"
```

### Análisis realizado

| Pregunta | Respuesta |
|----------|-----------|
| **Error exacto** | `password authentication failed for user "data_readonly"` |
| **Tipo de problema** | **Credenciales** (no es código ni red) |
| **Hipótesis** | La contraseña del usuario fue rotada o expiró y no se actualizó en la conexión de Airflow |
| **A quién preguntar** | Equipo de infraestructura / DevOps |

### Aprendizaje clave
Saber leer logs y clasificar el error (código / red / credenciales) es una de las habilidades más importantes en producción. Un buen diagnóstico evita perder horas investigando en el lugar equivocado.

---

## Ejercicio 02 — Lectura segura de credenciales

### Problema que se resolvía
Las credenciales hardcodeadas son una de las causas más comunes de fallos y de riesgos de seguridad.

### Solución implementada

Orden de prioridad:

1. **AWS Secrets Manager** (primera opción, profesional)
2. **Variables de entorno** (fallback para local/desarrollo)
3. **Error claro** si ninguna fuente está disponible

### Código conceptual

```python
def get_db_connection_params() -> dict:
    # 1. Intentar Secrets Manager
    try:
        secret = get_secret("freshmart/prod/rds/data_readonly")
        return { ... }
    except Exception:
        pass  # no tumbar el flujo, pasar al fallback

    # 2. Fallback a variables de entorno
    if all([os.environ.get(k) for k in ["DB_HOST", "DB_PORT", ...]]):
        return { ... }

    # 3. Error explícito
    raise RuntimeError("No se encontraron credenciales...")
```

### Por qué este diseño es profesional

| Práctica | Motivo |
|----------|--------|
| No hardcodear passwords | Evita filtraciones y facilita rotar claves |
| Secrets Manager primero | Estándar en producción (AWS, GCP, Azure) |
| Variables de entorno como fallback | Permite trabajar en local sin depender de la nube |
| Error explícito | Facilita el diagnóstico cuando algo falta |
| Función reutilizable | Cualquier DAG puede usarla |

---

## Lo que aprendí

### 1. Diagnóstico de fallos en producción
- Leer logs de forma sistemática
- Clasificar el error: **código**, **red** o **credenciales**
- Formular una hipótesis clara y saber a quién preguntar

### 2. Seguridad de credenciales
- Nunca poner passwords en el código
- Usar un sistema de secretos (Secrets Manager)
- Tener un plan B (fallback) bien diseñado
- Fallar de forma clara y temprana cuando faltan datos

### 3. Diseño de funciones robustas
- `try/except` para no romper el flujo cuando una fuente no está disponible
- Comprobar que **todas** las variables existen antes de devolverlas
- Mensajes de error que ayuden a quien lea el log

### 4. Mentalidad de producción
> Preferible que el pipeline falle con un mensaje claro  
> a que intente conectarse con credenciales incompletas o incorrectas.

---

## Conceptos clave del día

| Concepto | Definición corta |
|----------|------------------|
| **Hardcodear** | Poner valores sensibles directamente en el código |
| **Secrets Manager** | Servicio que guarda y rota secretos de forma segura |
| **Fallback** | Plan B cuando la opción principal no está disponible |
| **RuntimeError** | Error que se lanza cuando no se pueden obtener las credenciales |
| **Diagnóstico** | Proceso de leer logs, clasificar el error e hipotetizar la causa |

---

## Resultado del día
Se aprendió a diagnosticar un fallo real de producción a partir de logs y a implementar una función profesional de lectura de credenciales con prioridad clara, fallback y manejo de errores.
