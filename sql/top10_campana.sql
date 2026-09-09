-- TOP 10 productos por revenue en cada campaña
-- Necesitas: ROW_NUMBER() y filtro WHERE ranking <= 10

WITH producto_revenue AS (
SELECT
    v.campana,
    v.producto_id,
    p.nombre AS producto,
    SUM(v.precio * v.cantidad) AS revenue_total,
    SUM(v.cantidad) AS unidades
FROM silver.campaign_ventas v
JOIN silver.productos p ON v.producto_id = p.producto_id
WHERE v.cantidad > 0
GROUP BY v.campana, v.producto_id, p.nombre
),

rankeados AS (
SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY campana 
            ORDER BY revenue_total DESC
        ) AS ranking
    FROM producto_revenue
)
SELECT campana, ranking, producto, revenue_total, unidades
FROM rankeados
WHERE ranking <= 10
ORDER BY campana, ranking;