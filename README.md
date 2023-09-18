# Fortify Report Download Automation

This script provides an automated solution for interacting with Fortify Software Security Center (SSC). It streamlines the process of generating, downloading, and subsequently deleting security reports, making it especially valuable for integration into CI/CD pipelines or other automated workflows.

## Overview

1. **Report Generation**: 
   - The script initiates the creation of a security report on Fortify SSC based on predefined parameters such as the application name, version, and specific report details.
   
2. **Status Polling**: 
   - After the report generation request, the script continuously polls Fortify SSC to monitor the status of the report. This ensures that the subsequent steps only proceed once the report is ready.
   
3. **Download Token Creation**: 
   - Before downloading the report, a unique token is generated. This token authorizes the download request, ensuring secure access to the report.
   
4. **Report Download**: 
   - Once the report is ready and the token is generated, the script downloads the report and saves it locally in the specified format (e.g., PDF).
   
5. **Cleanup**: 
   - After successfully downloading the report, the script sends a request to delete the report from Fortify SSC. This ensures that no unnecessary data persists on the server, adhering to good data hygiene practices.

## Benefits

- **Automation**: By automating the report generation and download process, teams can ensure that they always have the latest security reports at their fingertips without manual intervention.
- **Integration**: This script is designed to be easily integrated into CI/CD pipelines, ensuring that security reports are generated and made available as part of the build or deployment process.
- **Security**: The script uses tokens for authentication and authorization, ensuring that interactions with Fortify SSC are secure.
- **Efficiency**: By automatically deleting reports from SSC after downloading, the script ensures efficient use of storage and reduces manual cleanup efforts.

## Usage

To use this script, ensure you have the necessary environment variables set in a `.env` file. These variables include details about the application, its version, and authentication tokens. Once set up, simply run the script to initiate the report generation, download, and cleanup process.
