#Escribir mensaje para #data-team
#Formato slack (texto plano, puedes usar *negritas* y emojis)

Resumen del incidente : Error DAG 19/09/2024

**Que paso**
El DAG fallo el dia 19/09/2024  y los pedidos no se actualizaron por 24hs.

**Causa Raiz**
Infra roto las credenciales del usuario data_readonly de RDS por la noche.
El DAG tenia la contraseña hardcodeada en el codigo y seguia usando la antigua.

**Fix aplicado**
Credencial actualizada. Relanzada la ejecucion caida. Los pedidos ya estan en el lake.

**Impacto**
Entre el 19/09 a las 3:00 hasta hoy los dashboard reflejaron informacion desactualizada. Ya fue solucionado.

**Proximos pasos**
Migrar la conexion a Airflow Connections.
