import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()


TECHSTORE_DATABASE_URL = os.getenv("TECHSTORE_DATABASE_URL")

ETL_DATABASE_URL = os.getenv("ETL_DATABASE_URL")


engine_techstore = create_engine(TECHSTORE_DATABASE_URL)

engine_etl = create_engine(ETL_DATABASE_URL)
