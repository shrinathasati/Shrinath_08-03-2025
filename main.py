from fastapi import FastAPI, BackgroundTasks
import uuid
import logging
from report_generator import generate_report

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory storage for reports
reports = {}

@app.post("/trigger_report")
def trigger_report(background_tasks: BackgroundTasks):
    """
    Trigger report generation and return a report ID.
    """
    report_id = str(uuid.uuid4())
    reports[report_id] = {"status": "Running", "data": None}
    background_tasks.add_task(generate_report_and_update_status, report_id)
    return {"report_id": report_id}

@app.get("/get_report")
def get_report(report_id: str):
    """
    Get the status of the report or the generated CSV file.
    """
    report = reports.get(report_id)
    if not report:
        return {"error": "Report not found"}
    if report["status"] == "Running":
        return {"status": "Running"}
    return {"status": "Complete", "data": report["data"]}

def generate_report_and_update_status(report_id):
    """
    Generate the report and update the report status.
    """
    try:
        logger.info(f"Generating report {report_id}...")
        report_path = generate_report(report_id)
        reports[report_id]["status"] = "Complete"
        reports[report_id]["data"] = report_path
        logger.info(f"Report {report_id} generated successfully.")
    except Exception as e:
        logger.error(f"Error generating report {report_id}: {e}")
        reports[report_id]["status"] = "Failed"
        reports[report_id]["data"] = None