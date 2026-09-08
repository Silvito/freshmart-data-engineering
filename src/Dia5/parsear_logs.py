# Simular logs de Airflow como texto
logs = """
[2024-09-19 03:00:05] INFO - Starting task extract_orders
[2024-09-19 03:00:05] INFO - Execution date: 2024-09-18
[2024-09-19 03:00:06] INFO - Connecting to PostgreSQL at freshmart-prod.rds.amazonaws.com:5432
[2024-09-19 03:00:06] ERROR - Connection failed: psycopg2.OperationalError: FATAL: password authentication failed for user "data_readonly"
[2024-09-19 03:05:06] ERROR - Connection failed (retry 2/3): password authentication failed
[2024-09-19 03:10:06] ERROR - Connection failed (retry 3/3): password authentication failed
[2024-09-19 03:10:06] ERROR - Max retries reached. Task FAILED.
"""

#1. Extraer solamente las lineas que contienen "ERROR"
errores = [linea.strip() for linea in logs.strip().split("\n") if "ERROR" in linea]
print("Lineas de error:")
for e in errores:
    print(f" {e}")

#2. Identificar el tipo de error
tipo_error = "credenciales" 
# password authentication failed → problema de autenticación

print(f"\nTipo de error: {tipo_error}")

#3. Que preguntarias para verificar?
hipotesis = "La contraseña del usuario 'data_readonly' es incorrecta, expiro o fue rotada y no se actualizo en la conexion de Airflow."

print(f"Hipotesis: {hipotesis}")
print(f"Preguntaria a : el equipo de infraestructura / devops")

