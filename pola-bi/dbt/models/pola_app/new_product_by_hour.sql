SELECT
    extract(hour from created_at) as dd,
    COUNT(*) FILTER(WHERE product_product.company_id is NULL) rozpoznaana,
    COUNT(*) FILTER(WHERE product_product.company_id is not NULL) nieroznanaa,
    COUNT(*) wszystkie
FROM
    {{ source('public', 'product_product') }}
WHERE
        product_product.created_at >= NOW() - INTERVAL '1 month'
GROUP BY extract(hour from created_at)
ORDER BY dd DESC
LIMIT 100
