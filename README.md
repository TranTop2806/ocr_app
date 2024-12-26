# PDF OCR and translator Application

## Overview

`TranTop2806-ocr_app` is a Streamlit-based web application designed to perform Optical Character Recognition (OCR) on PDF documents. It supports both Han (Chinese) and Nom (Vietnamese demotic script) OCR, allowing users to extract text from scanned documents and manage the results.

## Features

*   **Directory Management**: Create, browse, and manage directories for organizing PDF documents.
*   **PDF Upload and Processing**: Upload PDF files, view them, and initiate OCR processing.
*   **Han and Nom OCR**: Supports OCR for both Han and Nom scripts, using a custom OCR API.
*   **OCR Result Preview**: Display the extracted text alongside the original image, formatted for easy reading.
*   **File Management**: Delete uploaded PDF files.
*   **Settings**: Basic settings are available through the side bar.
*   **Memory Management:** Allows users to manage the files and folders within memory.
*   **Proxy Support**: Use proxy in Nom OCR.

## Directory Structure
TranTop2806-ocr_app/
├── .env.example # Example environment variables
├── docker.txt # Docker information
├── docs/ # Documentation (if any, including images)
│ └── image/
├── gui/ # Streamlit GUI components
│ ├── sidebar.py # Sidebar component
│ ├── pycache/ # Cache files
│ ├── page.py # Main page configuration
│ ├── .streamlit/ # Streamlit configuration
│ │ └── pages_sections.toml # Page sections configuration
│ └── preview_pdf.py # PDF preview component
├── app.py # Main application logic
├── init.py # Initialization file
├── Makefile # Makefile for development
├── images/ # General images folder
│ └── file/
├── data/ # Sample data
│ ├── image/ # Sample images for testing
│ │ └── TQDN_1/
│ ├── TQDN_1/
│ ├── json/ # Sample json data
│ │ └── TQDN_1/
│ │ └── page_1.json
│ └── file/
├── event/ # Event-driven architecture for OCR processing
│ ├── config.py # Configuration settings
│ ├── logger.py # Logging module
│ ├── dtype.py # Data classes and types
│ ├── consumer.py # Message consumer
│ ├── api_han.py # Han OCR API integration
│ ├── app.py # Main application for event loop
│ ├── init.py # Initialization
│ ├── producer.py # Message producer
│ ├── proxy.py # Proxy support class
│ ├── id.py # ID generation module
│ ├── pycache/
│ ├── app_sync.py # App sync
│ ├── test.py # Utility for text cleaning
│ ├── gg_api.py # Google API integration
│ ├── extract.py # PDF extraction module
│ ├── image.py # Image utilities
│ ├── api_nom.py # Nom OCR API integration
│ └── ui_event.py # UI event handling
├── requirements.txt # Python dependencies
├── Dockerfile # Docker configuration
├── credential/ # Credentials for Google Cloud API
│ └── possible-post-445216-g0-3dfc09bfa20f.json
└── memories/ # Storage for user data (OCR results, files)
├── <UUID>/ # User Directory
│ ├── map.json
│ └── <UUID>/ # PDF Directory
│ ├── txt/ # Extracted text files
│ │ ├── page_1.txt
│ │ └── ...
│ ├── images/ # Extracted images
│ ├── ocr/ # OCR output images
│ └── pdf/ # Uploaded PDF files
└── map.json # mapping folder name : folder id

## Environment Variables

The application uses the following environment variables, which should be set in a `.env` file (see `.env.example`):

*   `GOOGLE_APPLICATION_CREDENTIALS`: Path to your Google Cloud service account credentials JSON file.
*   `EMAIL`: Email address for API access.
*   `TOKEN`: API access token.

## Getting Started

### Prerequisites

*   Python 3.9 or higher.
*   Docker (optional, for containerized deployment).

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/TranTop2806-ocr_app.git
    cd TranTop2806-ocr_app
    ```
2.  Create a virtual environment (optional, but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```
3.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Create a `.env` file in the root directory, based on the `.env.example` file, and set the necessary environment variables.

### Running the Application

#### Using Streamlit directly:

```bash
make run
``` 
