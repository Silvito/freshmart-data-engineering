-- Clientes cuya PRIMERA compra fue durante la campaña
-- Esto mide la efectividdad de captacion de cada campaña

WITH primera_compra AS (
    -- 1. Primera fecha de compra de cada cliente (en toda la historia)
    SELECT
        cliente_id,
        MIN(fecha_pedido)::date AS fecha_primera_compra
    FROM pedidos
    WHERE cliente_id IS NOT NULL          -- excluimos anónimos
    GROUP BY cliente_id
),
clientes_nuevos_por_campana AS (
    -- 2. Clasificamos esa primera compra según el rango de cada campaña
    SELECT
        CASE
            WHEN fecha_primera_compra BETWEEN '2024-06-15' AND '2024-09-15'
                THEN 'verano'
            WHEN fecha_primera_compra BETWEEN '2024-03-01' AND '2024-05-31'
                THEN 'primavera'
            ELSE 'fuera_de_campana'
        END AS campana,
        COUNT(*) AS clientes_nuevos
    FROM primera_compra
    GROUP BY 1
)
SELECT campana, clientes_nuevos
FROM clientes_nuevos_por_campana
WHERE campana IN ('primavera', 'verano')   -- solo las dos campañas
ORDER BY campana;