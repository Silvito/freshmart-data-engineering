import os
import json

#Simular AWS Secrets Manager (en produccion usarias boto3)
FAKE_SECRETS_MANAGER = {
    "freshmart/prod/rds/data_readonly": json.dumps({
        "host": "freshmart-prod.xxxxx.eu-west-1.rds.amazonaws.com",
        "port": 5432,
        "dbname": "orders",
        "user": "data_readonly",
        "password": "NEW_FrM4rt_R0_Q4_2024!"
    })
}

def get_secret(secret_id: str) -> dict:
    """Simula boto3 secretsmanager.get_secret_value()"""
    raw = FAKE_SECRETS_MANAGER.get(secret_id)
    if raw:
        return json.loads(raw)
    raise Exception(f"Secret not found: {secret_id}")

def get_db_connection_params() -> dict:
    """Obtiene los parametros de conexion de forma SEGURA.
    Prioridad:
    1. AWS Secrets Manager
    2. Variables de entorno (fallback)
    3. Error si ninguna esta disponible
    """

    #--- Prioridad 1: Secrets Manager ----

    try:
        secret = get_secret("freshmart/prod/rds/data_readonly")
        return {
            "host": secret["host"],
            "port": secret["port"],
            "dbname": secret["dbname"],
            "user": secret["user"],
            "password": secret["password"],
        }
    except Exception:
        #Si el secreto no existe o hay un error de red,
        # no rompemos el flujo: pasamos al fallback.
        pass

    #--- Prioridad 2: Variables de entorno ----
    host = os.environ.get("DB_HOST")
    port = os.environ.get("DB_PORT")
    dbname = os.environ.get("DB_NAME")
    user = os.environ.get("DB_USER")
    password = os.environ.get("DB_PASSWORD")

    # Solo devolvemos si TODAS las variables existen
    if all([host, port, dbname, user, password]):
        return {
            "host": host,
            "port": int(port),
            "dbname": dbname,
            "user": user,
            "password": password,
        }

    #--- Prioridad 3: Error claro ---
    raise RuntimeError(
        "No se encontraron credenciales. "
        "Configura Secrets Manager o las variables de entorno: "
        "DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD"
    )