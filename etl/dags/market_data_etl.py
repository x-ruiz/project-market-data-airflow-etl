from airflow.sdk import dag, task, chain
from airflow.sdk.definitions.asset import Asset

from datetime import datetime, timedelta
import requests # for making api request
import os
import pandas as pd
import pendulum

@dag(
    dag_id="market_data_etl",
    start_date=pendulum.datetime(2024, 1, 1, 9, tz="America/Chicago"),  # 9:00 AM Central Time
    schedule="@daily",
    catchup=True,
    max_active_runs=1,
    default_args={
        "retries": 3,
        "retry_delay": timedelta(minutes=5)
    }
)
def market_data_etl():
    
    @task # probably wraps the funciton with functionality specific to dag tasks
    def extract_polygon_api(**context): # context is a dictionary that contains metadata about the task and DAG.
        """
        Returns the api response from polygon. 
        Example response:
        {"status":"OK","from":"2025-04-25","symbol":"AMZN","open":187.62,"high":189.94,"low":185.49,"close":188.99,"volume":3.641333e+07,"afterHours":189.2,"preMarket":189.84}
        """

        stock_ticker = "AMZN"
        polygon_api_key = os.environ.get("POLYGON_API_KEY")

        # Run extract on previous day
        ds = context.get("ds") # retrieves data_interaval_end in the format YYYY-mm-dd
        print("Processing data for", ds)

        # Create URL
        url = f"https://api.polygon.io/v1/open-close/{stock_ticker}/{ds}?/adjusted=true&apiKey={polygon_api_key}"

        response = requests.get(url)

        return response.json()
    
    @task
    def print_market_data_response(response: dict):
        print(f"Extract Response: {response}")

    @task
    def flatten_market_data(response: dict, **context):
        columns = { # provides default values if response.get returns null
            "status": "closed", # market is closed if there is no valid response
            "from": context.get("ds"), # still want to keep track of the date even if no valid response
            "symbol": "AMZN",
            "open": None,
            "high": None,
            "low": None,
            "close": None,
            "volume": None
        }

        flattened_record = []
        for key, default in columns.items():
            flattened_record.append(response.get(key, default))

        # convert to pandas dataframe
        flattened_df = pd.DataFrame([flattened_record], columns=columns.keys())
        return flattened_df
    
    ## Define task dependencies and pass data between tasks
    raw_market_data = extract_polygon_api()
    print_market_data_response(raw_market_data)
    flatten_market_data(raw_market_data)
    
market_data_etl() # call the dag, needed for dag to show up in UI"
