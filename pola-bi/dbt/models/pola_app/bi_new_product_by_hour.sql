SELECT
    extract(hour from created) as dd,
    COUNT(*) FILTER(WHERE product_product.company_id is NULL) rozpoznaana,
    COUNT(*) FILTER(WHERE product_product.company_id is not NULL) nieroznanaa,
    COUNT(*) wszystkie
FROM
    {{ source('public', 'product_product') }}
WHERE
        product_product.created >= NOW() - INTERVAL '1 month'
GROUP BY extract(hour from created)
ORDER BY dd DESC
LIMIT 100
