# Project Structure Documentation

## Current Structure

```
Swasthya-Monitor/
├── .streamlit/                    # Streamlit configuration
│   ├── config.toml               # UI theme (Medical Teal/White)
│   └── secrets.toml              # API keys (not in repo, user-specific)
│
├── src/                           # Source code modules
│   ├── __init__.py               # Package initialization
│   ├── logic.py                  # SCRS algorithm, validation, chronotype
│   ├── database.py               # Google Sheets integration, Patient ID
│   ├── reports.py                # PDF generation, WhatsApp sharing
│   ├── prediction.py             # ML trend prediction (Linear Regression)
│   └── ai_advice.py              # AI health advice (Groq API)
│
├── archive/                       # Legacy/old files (not used)
│   ├── app_old_backup.py
│   ├── calculations.py
│   ├── config.py
│   ├── database.py
│   ├── input_validators.py
│   ├── pdf_generator.py
│   ├── recommendations.py
│   ├── tab_*.py                  # Old tab modules
│   └── ui_components.py
│
├── app.py                         # Main application entry point
├── requirements.txt               # Python dependencies
│
├── README.md                      # Main project documentation
├── LICENSE                        # MIT License
├── .gitignore                     # Git ignore rules
│
├── ARCHITECTURE.md                # System architecture docs
├── CODEBASE_ANALYSIS.md          # Comprehensive codebase analysis
├── TEST_CASES.md                 # Test cases documentation
├── CONTRIBUTING.md               # Contribution guidelines
├── IMPLEMENTATION_SUMMARY.md     # Feature implementation summary
└── PROJECT_STRUCTURE.md          # This file
│
└── Data Files (optional)
    ├── sample_patient_data.csv   # Sample data for testing
    └── swasthya_database.csv     # Local backup (if used)
```

## Module Responsibilities

### Core Modules (`src/`)

#### `logic.py`
- **Purpose**: Clinical risk calculation and validation
- **Functions**:
  - `calculate_scrs()`: Composite Risk Score algorithm
  - `validate_inputs()`: Input validation
  - `detect_chronotype()`: Sleep pattern classification
- **Dependencies**: None (pure Python)

#### `database.py`
- **Purpose**: Data persistence and patient management
- **Functions**:
  - `get_conn()`: Google Sheets connection
  - `get_history()`: Fetch all records
  - `get_patient_history()`: Fetch patient-specific history
  - `add_record()`: Save new record
  - `generate_patient_id()`: Create unique patient ID
- **Dependencies**: streamlit, pandas, streamlit_gsheets

#### `reports.py`
- **Purpose**: Report generation and sharing
- **Functions**:
  - `create_pdf()`: Generate PDF health report
  - `get_whatsapp_link()`: Create WhatsApp share link
- **Dependencies**: fpdf2, urllib

#### `prediction.py`
- **Purpose**: Machine learning trend prediction
- **Functions**:
  - `predict_trends()`: Linear Regression prediction
  - `calculate_followup_date()`: Follow-up date calculation
- **Dependencies**: scikit-learn, pandas, numpy

#### `ai_advice.py`
- **Purpose**: AI-powered health advice
- **Functions**:
  - `get_holistic_advice()`: Generate AI advice via Groq
  - `get_fallback_advice()`: Standard advice when API fails
- **Dependencies**: groq, streamlit

### Main Application

#### `app.py`
- **Purpose**: Application orchestrator and UI
- **Responsibilities**:
  - Page configuration
  - UI layout and components
  - User input handling
  - Integration of all modules
  - Error handling and user feedback

## File Organization Principles

1. **Separation of Concerns**: Each module has a single, clear purpose
2. **Modularity**: Functions are reusable and testable
3. **Clean Structure**: Old files archived, not deleted (for reference)
4. **Documentation**: Each module well-documented
5. **Dependencies**: Minimal external dependencies, clearly defined

## Data Flow

```
User Input (app.py)
    ↓
Validation (logic.py)
    ↓
Risk Calculation (logic.py)
    ↓
Patient ID Generation (database.py)
    ↓
History Retrieval (database.py)
    ↓
Trend Prediction (prediction.py)
    ↓
AI Advice Generation (ai_advice.py)
    ↓
Report Generation (reports.py)
    ↓
Data Persistence (database.py)
    ↓
User Display (app.py)
```

## Adding New Features

1. **New Module**: Create in `src/` directory
2. **Update Imports**: Add to `app.py` imports
3. **Update Documentation**: Add to relevant docs
4. **Update Requirements**: Add dependencies if needed
5. **Test**: Verify functionality

## Best Practices

- Keep modules focused (single responsibility)
- Maximum file length: 300 lines (aim for <200)
- Add docstrings to all functions
- Include error handling
- Follow PEP 8 style guide
- Update documentation with changes

