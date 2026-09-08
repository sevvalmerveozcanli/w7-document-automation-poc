# IRS Form W-7 Document Automation PoC

A proof-of-concept web application for automating the generation of the official IRS Form W-7 (Rev. December 2024).

The application collects applicant information through a structured web interface, validates the submitted data, maps the values to the corresponding fields of the official IRS W-7 PDF, and generates a completed PDF document.

## Project Purpose

The purpose of this project is to demonstrate how structured user input can be transformed into an official PDF document through a reusable document automation architecture.

Instead of manually entering information into the PDF, the application:

1. Collects data through a web form.
2. Performs input validation.
3. Maps application data to official PDF field identifiers.
4. Handles conditional fields and checkbox/radio selections.
5. Generates a completed W-7 PDF.
6. Returns the generated document to the user.

## Technology Stack

- Python
- FastAPI
- Jinja2
- PyPDF
- Uvicorn
- HTML / CSS / JavaScript

## Project Structure

```text
w7-document-automation-poc/
│
├── data/
│   └── countries.json
│
├── mappings/
│   └── w7_2024.py
│
├── services/
│   ├── country_service.py
│   ├── date_service.py
│   ├── pdf_service.py
│   └── validation_service.py
│
├── templates/
│   └── index.html
│
├── tests/
│
├── fw7.pdf
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Architecture

The project separates document automation responsibilities into different layers.

### Web Layer

`main.py`

Handles HTTP requests, receives submitted form data, runs validation, calls the PDF generation service, and returns the generated PDF.

### Validation Layer

`services/validation_service.py`

Validates submitted form data before document generation.

This includes checks such as required fields and format-specific validation.

### PDF Service Layer

`services/pdf_service.py`

Transforms application-level data into values compatible with the official PDF fields.

Responsibilities include:

- PDF field population
- Checkbox and radio-button handling
- Date normalization
- ITIN / IRSN processing
- Conditional field population

### Mapping Layer

`mappings/w7_2024.py`

Contains the mapping between application field names and the internal AcroForm field identifiers of the official IRS W-7 PDF.

Keeping field mappings separate from business logic makes the document integration easier to maintain.

## Conditional Form Logic

Some W-7 fields depend on previous selections.

Examples include:

- Reason D relationship information
- Reason E name and SSN/ITIN information
- Reason H details
- Other identification document description
- Previous ITIN / IRSN information
- Delegate relationship

The web interface dynamically displays relevant fields, while the backend independently processes and validates the submitted values.

## Running the Project

Create and activate a virtual environment.

Install the dependencies:

```bash
pip install -r requirements.txt
```

Start the development server:

```bash
uvicorn main:app --reload
```

Then open the local application in a web browser.

## Document Generation Flow

```text
User
  ↓
Web Form
  ↓
FastAPI
  ↓
Validation Service
  ↓
PDF Service
  ↓
W-7 Field Mapping
  ↓
Official W-7 PDF
  ↓
Generated PDF
```

## Security and Production Considerations

This repository is a proof of concept and is not intended to process real taxpayer information in production without additional security controls.

A production implementation should include:

- HTTPS
- Authentication and authorization
- Encryption at rest
- Secure temporary document storage
- Automatic document retention and deletion policies
- Audit logging
- Input sanitization and stricter validation
- Access controls for generated documents
- Secrets and configuration management
- Appropriate handling of personally identifiable information (PII)

Generated documents are excluded from version control through `.gitignore`.

## AI Integration

The core document generation process is deterministic.

AI is not required to populate known PDF fields when structured data is already available. This reduces the risk of hallucinated or incorrectly transformed values.

AI could be introduced as an optional layer for tasks such as:

- Extracting structured information from unstructured documents
- Classifying document types
- Assisting with field matching for previously unseen forms
- Flagging potentially inconsistent submissions for human review

Any AI-generated or AI-extracted information should be validated before being written to an official document.

## Extensibility

The architecture is designed so that additional forms can be supported by introducing:

- A new PDF template
- A new field mapping
- Form-specific validation rules
- A form-specific generation service

This allows the same overall automation pipeline to be reused for other document types.

## Disclaimer

This project is a technical proof of concept for document automation. It does not provide tax or legal advice.
