SELECT
    seq::date,
    COUNT(DISTINCT pola_query."client") count_uq_user,
    COUNT(1) count_request
FROM
    generate_series(
        (date_trunc('month', CURRENT_DATE) - INTERVAL '24 months')::timestamp,
        (date_trunc('month', CURRENT_DATE))::timestamp,
        '1 week'::interval
    ) seq,
    {{ source('public', 'pola_query') }}
WHERE
    pola_query.timestamp BETWEEN seq::date AND (seq::date + INTERVAL '1 week')
GROUP BY seq
ORDER BY seq
