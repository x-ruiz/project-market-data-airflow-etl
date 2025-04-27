# project-market-data-airflow-etl
Simple project to learn Airflow to process market data. Based on tutorial: https://www.datacamp.com/tutorial/building-an-etl-pipeline-with-airflow

Using tutorial as a base to learn Airflow but building on top of it.

## SetUp

### Environment Variables
POLYGON_API_KEY=<KEY>
AIRFLOW__CORE__DEFAULT_TIMEZONE=America/Chicago

### Airflow
1. [Installation](https://www.astronomer.io/docs/astro/cli/install-cli/?tab=mac#install-the-astro-cli)
2. ```astro dev init```
3. ```astro dev start```

### Polygon
1. [Create API Key](https://polygon.io/)

## Architecture Diagram

![project-airflow-etl](https://github.com/user-attachments/assets/15f3a5d9-b924-4347-a739-5f65180f7db1)

## TroubleShooting
**Port Already Allocated**
1. ```lsof -i tcp:5432``` -> retrieve the PID
1. ```kill -9 <PID>```

## Documentation
https://www.astronomer.io/docs/learn/dags/?tab=taskflow#writing-dags-with-the-taskflow-api
