--1) Conversion global
-- En SQLite, los booleanos True/False de Pandas se guardan como 1/0,
-- así que SUM(compro) cuenta directamente los que compraron.

SELECT
    COUNT(*) AS total_alcanzados,
    SUM(compro) AS compraron,
    ROUND(
        100.0 * SUM(compro) / COUNT(*),
        2
    ) AS tasa_conversion_pct
FROM campana_verano_clientes;

-- 2) Conversión por CANAL (normalizado)
-- Normalizamos canal_contacto: minúsculas y unificamos variantes de push
SELECT
    CASE
        WHEN LOWER(canal_contacto) LIKE 'push%' THEN 'push'
        ELSE LOWER(canal_contacto)
    END AS canal,
    COUNT(*) AS alcanzados,
    SUM(compro) AS compraron,
    ROUND(
        100.0 * SUM(compro) / COUNT(*),
        2
    ) AS tasa_conversion_pct
FROM campana_verano_clientes
GROUP BY canal
ORDER BY tasa_conversion_pct DESC;