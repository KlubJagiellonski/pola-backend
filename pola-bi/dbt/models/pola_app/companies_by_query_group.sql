SELECT
    CASE
        WHEN company_company.query_count > 75000 THEN '00. 75000>'
        WHEN company_company.query_count > 50000 THEN '01. 50000>'
        WHEN company_company.query_count > 30000 THEN '02. 30000>'
        WHEN company_company.query_count > 25000 THEN '03. 25000>'
        WHEN company_company.query_count > 20000 THEN '04. 20000>'
        WHEN company_company.query_count > 15000 THEN '05. 15000>'
        WHEN company_company.query_count > 10000 THEN '06. 10000>'
        WHEN company_company.query_count > 7500 THEN '07. 7500>'
        WHEN company_company.query_count > 5000 THEN '08. 5000>'
        WHEN company_company.query_count > 2500 THEN '09. 2500>'
        WHEN company_company.query_count > 1000 THEN '10. 1000>'
        WHEN company_company.query_count > 500 THEN '11. 500>'
        WHEN company_company.query_count > 250 THEN '12. 250>'
        WHEN company_company.query_count > 100 THEN '13. 100>'
        WHEN company_company.query_count > 50 THEN '14. 50>'
        WHEN company_company.query_count > 10 THEN '15. 10>'
        WHEN company_company.query_count > 5 THEN '16. 5>'
        ELSE '17. other'
    END query_count_group,
    SUM(query_count) sum_query_count,
    SUM(1) sum_total,
    SUM(company_company.verified::int) sum_verified,
    CASE
        WHEN SUM(1) = 0 THEN 0
        ELSE SUM(company_company.verified::int)::float / SUM(1)::float
    END percentage_verified,
    CASE
        WHEN (SELECT SUM(company_company.query_count) FROM company_company) = 0 THEN 0
        ELSE SUM(query_count)::float / (SELECT SUM(company_company.query_count) FROM company_company)
    END percentage_query_count
FROM
    {{ source('public', 'company_company') }}
GROUP BY query_count_group
ORDER BY query_count_group ASC
