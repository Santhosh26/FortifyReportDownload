import requests
import time
import json
from decouple import config

# Extract environment variables from .env file
APP_NAME = config('SSC_APP_NAME')
APP_ID = config('SSC_APP_NAME_ID')
APP_VERSION = config('SSC_APP_VER_NAME')
APP_VERSION_ID = config('SSC_APP_VER_ID')
SSC_URL = config('SSC_URL')
API_URI = f"{SSC_URL}/api/v1"
SSC_AUTH_TOKEN = config('SSC_AUTH_TOKEN')
REPORT_NAME = f"{APP_NAME} Developer Report"
REPORT_FORMAT = "PDF"
SSC_REPORT_TOKEN = config('SSC_REPORT_TOKEN')


# Define the report details and parameters
request_body = {
    "name": REPORT_NAME,
    "note": "Created Automatically via Pipleine",
    "format": "PDF",
    "inputReportParameters": [
        {"name": "Key Terminology", "identifier": "IncludeSectionDescriptionOfKeyTerminology", "paramValue": True, "type": "BOOLEAN"},
        {"name": "About Fortify Solutions", "identifier": "IncludeSectionAboutFortifySecurity", "paramValue": True, "type": "BOOLEAN"},
        {"name": "Application Version", "identifier": "projectversionid", "paramValue": int(APP_VERSION_ID), "type": "SINGLE_PROJECT"}
    ],
    "reportDefinitionId": 9,
    "type": "ISSUE",
    "project": {"id": int(APP_VERSION_ID), "name": APP_VERSION, "version": {"id": int(APP_ID), "name": APP_NAME}}
}

headers = {
    'Accept': "application/json",
    'Content-Type': "application/json",
    'Authorization': f"FortifyToken {SSC_AUTH_TOKEN}"
}

# Create the report on the server
print("Creating Report")
response = requests.post(f"{API_URI}/reports", headers=headers, json=request_body)
response.raise_for_status()

# Retrieve the id of the report
report_id = response.json()['data']['id']
print(f"Report Id: {report_id}")

# Poll the server to check the status of the report until it's ready
print("Polling status of report")
while True:
    response = requests.get(f"{API_URI}/reports/{report_id}?fields=status", headers=headers)
    response.raise_for_status()
    report_status = response.json()['data']['status']
    print(f"Report id: '{report_id}' current status: {report_status}")
    if report_status in ["PROCESSING", "SCHED_PROCESSING"]:
        time.sleep(10)
    else:
        break

if report_status == "ERROR_PROCESSING":
    raise Exception("There was an error processing the report...")

# Create a token to download the report
print("Creating Download Token")
body = {"fileTokenType": "3"}
response = requests.post(f"{API_URI}/fileTokens", headers=headers, json=body)
response.raise_for_status()
transfer_token = response.json()['data']['token']


# Download the report using the token
print("Downloading Report")
response = requests.get(f"{SSC_URL}/transfer/reportDownload.html?mat={transfer_token}&id={report_id}", headers=headers)
with open(f"{REPORT_NAME}.{REPORT_FORMAT.lower()}", "wb") as f:
    f.write(response.content)

#special header for deletion of report
report_headers = {
    'Authorization': f"FortifyToken {SSC_REPORT_TOKEN}",
    'Accept': "application/json",
    'Content-Type': "application/json"
}
# Delete the report from the server
print("Deleting Report from SSC")
response = requests.delete(f"{API_URI}/reports/{report_id}", headers=report_headers)
response.raise_for_status()

print("Reported deleted from SSC")
