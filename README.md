# Store Monitoring System

Backend system to monitor restaurant uptime/downtime. Generates reports based on store activity, business hours, and timezone data.

---

## **Features**
- **APIs**:
  - `/trigger_report`: Triggers report generation.
  - `/get_report`: Returns report status or CSV.

---

**Improvement Ideas**
- Use async DB operations.

- Add caching for frequent data.

- Implement parallel processing.

- Add robust error handling.

- Use a more efficient DB (e.g., PostgreSQL).

- Add API rate limiting.

- Add logging and monitoring.

- Write unit tests.
## **File Structure**
- store-monitoring
 - main.py # FastAPI app
 - database.py # DB setup
 - report_generator.py # Report logic
 - data_loader.py # Load CSV data
 - requirements.txt # Dependencies
 - data/ # CSV files
 - reports/ # Generated reports

Sampal output: [Drive Link](https://drive.google.com/file/d/1Y6RAIfMHa_USzqNamHDmlLYQKQaq3CCr/view?usp=sharing)

Live Recording: [Recording](https://www.loom.com/share/890861854ca34fdfb2f22c1f81dc0f13?sid=cf25c744-0ff5-4d2e-bbb5-78d36218fb83) 

## **How to Run**
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
Load data:

bash
Copy
python data_loader.py
Run the app:

bash
Copy
uvicorn main:app --reload
Trigger report:

bash
Copy
curl -X POST http://127.0.0.1:8000/trigger_report
Get report:

bash
Copy
curl -X GET "http://127.0.0.1:8000/get_report?report_id=<report_id>"



