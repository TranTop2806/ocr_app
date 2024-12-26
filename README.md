# PDF OCR and Translator Application

## Overview

`TranTop2806-ocr_app` is a Streamlit-based web application designed to perform Optical Character Recognition (OCR) and Translator on PDF documents. It supports both Han (Chinese) and Nom (Vietnamese demotic script) OCR, allowing users to extract text from scanned documents and manage the results.

## Features

*   **Directory Management**: Create, browse, and manage directories for organizing PDF documents.
*   **PDF Upload and Processing**: Upload PDF files, view them, and initiate OCR processing.
*   **Han and Nom OCR**: Supports OCR for both Han and Nom scripts, using a custom OCR API.
*   **OCR Result Preview**: Display the extracted text alongside the original image, formatted for easy reading.
*   **File Management**: Delete uploaded PDF files.
*   **Settings**: Basic settings are available through the side bar.
*   **Memory Management:** Allows users to manage the files and folders within memory.
*   **Proxy Support**: Use proxy in Nom OCR.

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
    git clone https://github.com/TranTop2806/ocr_app.git
    cd ocr_app
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

#### Using Streamlit directly (Build Docker):

```bash
make run
``` 
