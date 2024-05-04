SELECT
    seq,
    COUNT(*) request_total,
    COUNT(*) FILTER(WHERE was_590 = true) request_was_590,
    COUNT(*) FILTER(WHERE "was_plScore" = true) request_was_plScore,
    COUNT(*) FILTER(WHERE was_verified = true) request_was_verified,
    COUNT(*) FILTER(WHERE was_590 = true)::float / COUNT(*) percetage_request_was_590,
    COUNT(*) FILTER(WHERE "was_plScore" = true)::float / COUNT(*) percetage_request_was_plScore,
    COUNT(*) FILTER(WHERE was_verified = true)::float / COUNT(*) percetage_request_was_verified,
    COUNT(DISTINCT client) uq_user
FROM
    generate_series(
        (CURRENT_DATE - INTERVAL '24 months')::timestamp,
        (CURRENT_DATE)::timestamp,
        '1 week'::interval
    ) seq
    LEFT JOIN
        {{ source('public', 'pola_query') }}
    ON
        pola_query.timestamp BETWEEN seq AND (seq + INTERVAL '1 week')
GROUP BY seq
ORDER BY seq
