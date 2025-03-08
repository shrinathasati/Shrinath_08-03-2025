import pandas as pd
from sqlalchemy import create_engine
from database import StoreStatus, BusinessHours, StoreTimezone, SessionLocal

# Database connection
DATABASE_URL = "sqlite:///./store_monitoring.db"
engine = create_engine(DATABASE_URL)
db = SessionLocal()

def load_csv_to_db():
    # Load store_status.csv
    print("doing 1st")
    store_status_df = pd.read_csv("data/store_status.csv")
    store_status_df["timestamp_utc"] = pd.to_datetime(store_status_df["timestamp_utc"])
    store_status_df.to_sql("store_status", engine, if_exists="replace", index=False)

    print("doing 2nd")
    # Load menu_hours.csv
    menu_hours_df = pd.read_csv("data/menu_hours.csv")
    menu_hours_df.to_sql("business_hours", engine, if_exists="replace", index=False)

    print("doing 3rd")
    # Load timezones.csv
    timezones_df = pd.read_csv("data/timezones.csv")
    timezones_df.to_sql("store_timezone", engine, if_exists="replace", index=False)

    print("Data loaded into the database successfully!")

if __name__ == "__main__":
    load_csv_to_db()