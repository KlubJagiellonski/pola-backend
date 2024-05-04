{#
To list columns:

cat ./pola-bi/dbt/models/bigquery/staging/sources.yml |  yq e -j  | jq '[.sources[].tables[].name]'

To run:
dbt compile --select pola_app.analysis.pola_backend_bigquery_create_base_models.sql --target staging --debug --profile pola_app_bigquery
#}

{{
codegen.create_base_models(
    source_name='pola_backend',
    tables=[
  "ai_pics_aiattachment",
  "ai_pics_aipics",
  "company_brand",
  "company_company",
  "gpc_brick",
  "gpc_class",
  "gpc_family",
  "gpc_segment",
  "pola_query",
  "pola_searchquery",
  "pola_stats",
  "product_product",
  "report_attachment",
  "report_report"
]
)
}}
