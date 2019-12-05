# Skittle-Sorter

## Overview ##

Skittle Sorter powered by AWS IOT

This project is broken into its components as follows:

- Web UI as a control panel
- Cognito for Authentication
- API Gateway
- Lambda : IOT shadow update/fetch
- Raspberry pi: python code that runs locally on the PI which detects colours and controls the servo accordingly
- lambda for AWS IoT Greengrass

## Architecture ##

For the architecture see the PDF file "docs/SkittlerSorterArchitecture.pdf".
For the physical build and software setup instructions see the file "docs/SkittleSorterPhysicalArchitecture.pdf"

Good luck!

## Authors ##
- Vinay Nadig nadvinay@amazon.com
- Vijay Menon vijaym@amazon.com 


