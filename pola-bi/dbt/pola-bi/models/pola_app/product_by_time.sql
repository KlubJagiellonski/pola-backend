SELECT
    seq,
    SUM(1) count_total,
    SUM((company_id IS NOT NULL)::int) count_with_company,
    SUM((code LIKE '590%')::int) count_590,
    SUM((company_id IS NOT NULL AND code LIKE '590%')::int) count_with_company_and_590,
    SUM((company_id IS NULL AND code LIKE '590%')::int) count_without_company_and_590,
    SUM((company_id IS NOT NULL)::int)::float / SUM(1) percentage_with_company,
    SUM((code LIKE '590%')::int)::float / SUM(1) percentage_590,
    SUM((company_id IS NOT NULL AND code LIKE '590%')::int)::float / SUM(1) percentage_wtih_company_and_590,
    SUM((company_id IS NULL AND code LIKE '590%')::int)::float / SUM(1) percentage_wtihout_company_and_590
FROM
    generate_series(
        (CURRENT_DATE - INTERVAL '24 months')::timestamp,
        (CURRENT_DATE)::timestamp,
        '1 week'::interval
    ) seq
    LEFT JOIN
        {{ source('public', 'product_product') }}
    ON
        product_product.created_at BETWEEN seq AND (seq + INTERVAL '1 week')
GROUP BY seq
ORDER BY seq
