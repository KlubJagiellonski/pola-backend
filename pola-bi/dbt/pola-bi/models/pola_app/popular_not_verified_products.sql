SELECT *
FROM  {{ source('public', 'product_product') }}
WHERE created_at >= NOW() - INTERVAL '1 month'
  AND company_id IS null
  AND query_count > 0
ORDER BY query_count DESC
LIMIT 10000
