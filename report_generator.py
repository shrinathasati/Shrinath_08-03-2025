

import pandas as pd
from datetime import datetime, timedelta, time
import pytz
from sqlalchemy import text
from database import SessionLocal

def calculate_uptime_downtime(store_id, business_hours, status_data, timezone_str):
    """
    Calculate uptime and downtime for a store based on business hours and status data.
    """
    print("calculations:.........")
    uptime_last_hour = 0
    downtime_last_hour = 0
    uptime_last_day = 0
    downtime_last_day = 0
    uptime_last_week = 0
    downtime_last_week = 0

    # Convert timestamps to local time
    status_data["timestamp_local"] = status_data["timestamp_utc"].apply(
        lambda x: pytz.utc.localize(x).astimezone(pytz.timezone(timezone_str)))
    
    # Filter observations within business hours
    for _, row in business_hours.iterrows():
        day = row["dayOfWeek"]
        start_time = row["start_time_local"]
        end_time = row["end_time_local"]

        # Filter data for the current day and within business hours
        filtered_data = status_data[
            (status_data["timestamp_local"].dt.dayofweek == day) &
            (status_data["timestamp_local"].dt.time >= start_time) &
            (status_data["timestamp_local"].dt.time <= end_time)
        ]

        # Skip if no data is available for the current business hours
        if len(filtered_data) == 0:
            continue

        # Calculate uptime and downtime
        active_periods = filtered_data[filtered_data["status"] == "active"]
        inactive_periods = filtered_data[filtered_data["status"] == "inactive"]

        # Extrapolate uptime and downtime
        total_time = (end_time.hour - start_time.hour) * 60  # Total minutes in business hours
        uptime = len(active_periods) / len(filtered_data) * total_time
        downtime = len(inactive_periods) / len(filtered_data) * total_time

        # Update uptime and downtime for last hour, day, and week
        uptime_last_hour += uptime / 60  # Convert to hours
        downtime_last_hour += downtime / 60
        uptime_last_day += uptime
        downtime_last_day += downtime
        uptime_last_week += uptime * 7
        downtime_last_week += downtime * 7

    return {
        "store_id": store_id,
        "uptime_last_hour": uptime_last_hour,
        "uptime_last_day": uptime_last_day,
        "uptime_last_week": uptime_last_week,
        "downtime_last_hour": downtime_last_hour,
        "downtime_last_day": downtime_last_day,
        "downtime_last_week": downtime_last_week
    }

def generate_report(report_id):
    """
    Generate a report for all stores.
    """
    db = SessionLocal()
    print("report id: ", report_id)
    # Fetch data from the database using SQLAlchemy text() for raw SQL
    status_data = pd.read_sql(text("SELECT * FROM store_status"), db.connection())
    business_hours = pd.read_sql(text("SELECT * FROM business_hours"), db.connection())
    timezones = pd.read_sql(text("SELECT * FROM store_timezone"), db.connection())

    # Convert timestamp_utc to datetime
    status_data["timestamp_utc"] = pd.to_datetime(status_data["timestamp_utc"])

    # Convert start_time_local and end_time_local to datetime.time
    business_hours["start_time_local"] = pd.to_datetime(business_hours["start_time_local"], format="%H:%M:%S").dt.time
    business_hours["end_time_local"] = pd.to_datetime(business_hours["end_time_local"], format="%H:%M:%S").dt.time

    # Merge data
    merged_data = pd.merge(status_data, timezones, on="store_id", how="left")
    merged_data["timezone_str"].fillna("America/Chicago", inplace=True)

    # Generate report for each store
    report = []
    for store_id, group in merged_data.groupby("store_id"):
        store_business_hours = business_hours[business_hours["store_id"] == store_id]
        
        # Get the timezone for the store (default to "America/Chicago" if not found)
        store_timezone = timezones[timezones["store_id"] == store_id]["timezone_str"]
        if len(store_timezone) == 0:
            store_timezone = "America/Chicago"
        else:
            store_timezone = store_timezone.values[0]

        report.append(calculate_uptime_downtime(store_id, store_business_hours, group, store_timezone))

    # Save report to CSV
    report_df = pd.DataFrame(report)
    report_path = f"reports/{report_id}.csv"
    report_df.to_csv(report_path, index=False)

    return report_path