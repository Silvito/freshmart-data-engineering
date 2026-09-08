--- Tabla gold: campaign_performance
--- Granularidad: campaña + dia
-- Fuente: silver.campaign_ventas

SELECT campana,
    fecha_compra::date AS fecha,

    --Revenue bruto (precio * cantidad, sin descuento)
    SUM(precio * cantidad) AS revenue_bruto,

    -- Revenue neto (precio * cantidad - descuento)
    SUM(precio * cantidad * (1 - descuento_pct / 100.0)) AS revenue_neto,

    -- Numero de transacciones
    COUNT(*) AS num_transacciones,

    -- Clientes unicos (excluyendo anonimos → cliente_id IS NOT NULL)
    COUNT(DISTINCT cliente_id) FILTER (WHERE cliente_id IS NOT NULL) AS clientes_unicos,

    -- Ticket medio = revenue neto / numero de transacciones
    SUM(precio * cantidad * (1 - descuento_pct / 100.0))
    / NULLIF(COUNT(*), 0) AS ticket_medio

FROM silver.campaign_ventas
WHERE cantidad > 0
GROUP BY campana, fecha_compra::date
ORDER BY campana, fecha
LIMIT 10;