{#
To run:
dbt compile --select pola_app.analysis.pola_backend_bigquery_generate_source --target staging --debug --profile pola_app_bigquery
#}
{{ codegen.generate_source(
    schema_name=target.schema,
    generate_columns=True,
    exclude='stg_%'
) }}
