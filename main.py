from fastapi import FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from snowflake.snowpark import Session
from snowflake.snowpark.functions import call_udf, col
from dotenv import load_dotenv
import os

app = FastAPI()
load_dotenv()

connection_parameters = {
    "account": os.getenv("SNOWFLAKE_ACCOUNT"),
    "user": os.getenv("SNOWFLAKE_USER"),
    "password": os.getenv("SNOWFLAKE_PASSWORD"),
    "schema": os.getenv("SNOWFLAKE_SCHEMA"),
    "database": os.getenv("SNOWFLAKE_DATABASE"),
    "role": os.getenv("SNOWFLAKE_ROLE"),
    "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
}

session = Session.builder.configs(connection_parameters).create()
@app.get("/", include_in_schema=False)
def read_root():
    return RedirectResponse(url='/docs')

@app.get("/predict/")
def predict(tv: float, radio: float, newspaper: float):
    try:
        advertising_df = session.create_dataframe([[tv, radio, newspaper]], schema=["TV", "RADIO", "NEWSPAPER"])
        
        predicted_sales_df = advertising_df.select(
            call_udf("predict_sales", col("TV"), col("RADIO"), col("NEWSPAPER")).alias("PREDICTED_SALES")
        )

        result = predicted_sales_df.collect()
        
        return {"predicted_sales": result[0]["PREDICTED_SALES"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
