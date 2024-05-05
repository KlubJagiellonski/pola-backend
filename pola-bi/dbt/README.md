Welcome to your new dbt project!

### Using the starter project

Try running the following commands:
- dbt run
- dbt test


### Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [chat](http://slack.getdbt.com/) on Slack for live discussions and support
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices


# Command

## Run full refresh for postgres

```shell
./run_dbt.sh dbt run --full-refresh --profile pola_app_postgres
```

We have two target: `dev` and `prod`

## Run full refresh for BigQuery

```shell
gcloud auth login --update-adc
./run_dbt.sh dbt run --full-refresh --profile pola_app_bigquery
```

For now, we have one target: `staging`

## ``docs``

```shell
./run_dbt.sh dbt docs generate
./run_dbt.sh dbt docs serve --port 8081
```
