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
