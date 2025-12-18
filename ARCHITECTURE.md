# Swasthya Monitor - Architecture Documentation

## System Overview

Swasthya Monitor is a web-based healthcare screening application built with Streamlit. The system implements a rule-based expert system for health risk assessment using clinical guidelines from the Indian Council of Medical Research (ICMR) and Asian-Indian health standards.

## Project Structure

```
Swasthya-Monitor/
├── .streamlit/
│   ├── config.toml          # UI theme configuration (Medical Teal/White)
│   └── secrets.toml          # Google Sheets connection credentials
├── src/
│   ├── __init__.py          # Package initialization
│   ├── logic.py             # Clinical risk calculation (SCRS algorithm)
│   ├── database.py          # Google Sheets data persistence
│   └── reports.py           # PDF generation and WhatsApp integration
├── app.py                   # Main application entry point
├── requirements.txt         # Python dependencies
└── README.md               # Project documentation
```

## Module Architecture

### Core Modules

#### 1. src/logic.py

**Purpose**: Clinical risk calculation and input validation

**Functions**:

- `calculate_scrs(age, bmi, sugar, sys_bp, dia_bp)`
  - Implements the Swasthya Composite Risk Score algorithm
  - Input: Patient vital signs
  - Output: Risk score (0-10), risk level (Low/Moderate/High), color code, risk factors list
  - Logic: Multi-factor scoring based on BMI, blood sugar, blood pressure, and age

- `validate_inputs(age, weight, height, sugar, sys_bp, dia_bp)`
  - Validates all input parameters against clinical ranges
  - Returns list of error messages
  - Validates: age (1-119), weight (20-200 kg), height (50-250 cm), blood sugar (50-500 mg/dL), blood pressure ranges

**Key Characteristics**:
- Rule-based expert system (no machine learning)
- Deterministic output based on clinical guidelines
- Indian-specific standards (BMI ≥25 obese, ≥23 overweight)
- ICMR diabetes thresholds (<100 normal, 100-126 prediabetic, >126 diabetic)
- AHA blood pressure standards

#### 2. src/database.py

**Purpose**: Data persistence using Google Sheets

**Functions**:

- `get_conn()`
  - Returns Streamlit connection object for Google Sheets
  - Uses `st.connection()` with GSheetsConnection type

- `init_db()`
  - Placeholder function for compatibility
  - Google Sheets connection initialized on first use

- `get_history()`
  - Fetches all patient records from Google Sheet
  - Returns pandas DataFrame
  - Handles connection errors gracefully (returns empty DataFrame)

- `add_record(data)`
  - Appends new patient record to Google Sheet
  - Formats data with timestamp
  - Handles errors without crashing application

**Data Schema**:
```
Date | Name | Age | Gender | Weight | Height | BMI | Sugar | BP | Risk_Score | Label
```

**Design Decisions**:
- Google Sheets chosen for cloud deployment compatibility
- No local file dependencies (works with Streamlit Cloud)
- Real-time data synchronization
- Free tier suitable for educational/prototype use

#### 3. src/reports.py

**Purpose**: Report generation and patient communication

**Functions**:

- `create_pdf(data)`
  - Generates professional PDF health report
  - Includes patient information, vitals, risk score, and recommendations
  - Uses FPDF library
  - Handles special characters in patient names
  - Returns PDF as bytes for download

- `get_whatsapp_link(name, score, label)`
  - Creates WhatsApp sharing link with encoded message
  - Includes Hindi greeting (नमस्ते)
  - Provides patient-friendly summary
  - Returns URL-encoded WhatsApp link

**Report Content**:
- Patient identification
- Composite Risk Score and category
- Vital signs summary
- Clinical recommendations
- Medical disclaimer

### Main Application

#### app.py

**Purpose**: Application orchestrator and UI controller

**Structure**:

1. **Page Configuration**
   - Sets page title, icon, and wide layout
   - Loads custom CSS for medical theme

2. **Sidebar (Input Section)**
   - Patient information form
   - Vital signs input fields
   - Diagnostic trigger button

3. **Main Content Area (Tabs)**
   - Current Analysis Tab: Risk assessment and results
   - Patient Records Tab: Historical data and analytics

**Workflow**:

```
User Input → Validation → SCRS Calculation → Display Results → Save to Database → Export Options
```

## Data Flow

```
User Interface (app.py)
    ↓
Input Validation (logic.validate_inputs)
    ↓
BMI Calculation (app.py)
    ↓
Risk Score Calculation (logic.calculate_scrs)
    ↓
Display Results (app.py UI)
    ↓
Save Record (database.add_record)
    ↓
Generate Reports (reports.create_pdf, reports.get_whatsapp_link)
```

## Design Patterns

### 1. Separation of Concerns

- **Presentation Layer**: `app.py` (UI and user interaction)
- **Business Logic Layer**: `src/logic.py` (clinical calculations)
- **Data Access Layer**: `src/database.py` (data persistence)
- **Output Layer**: `src/reports.py` (report generation)

### 2. Error Handling Strategy

- Validation errors: Displayed to user without saving data
- Database errors: Gracefully handled, app continues to function
- Report generation errors: Error messages shown, app remains stable

### 3. Configuration Management

- Theme settings: `.streamlit/config.toml`
- Secrets: `.streamlit/secrets.toml` (not committed to version control)
- Dependencies: `requirements.txt`

## Clinical Algorithm: Composite Risk Score (SCRS)

### Scoring System

The SCRS combines multiple risk factors on a 0-10 scale:

1. **BMI Component** (0-3 points)
   - BMI ≥25 (Obesity): +3 points
   - BMI ≥23 (Overweight): +2 points
   - BMI <23: 0 points

2. **Blood Sugar Component** (0-3 points)
   - Sugar >126 mg/dL (Diabetic): +3 points
   - Sugar 100-126 mg/dL (Prediabetic): +1 point
   - Sugar <100 mg/dL: 0 points

3. **Blood Pressure Component** (0-3 points)
   - Systolic ≥140 OR Diastolic ≥90 (Hypertension): +3 points
   - Systolic ≥130 OR Diastolic ≥80 (Elevated): +1 point
   - Normal BP: 0 points

4. **Age Synergy** (0-1 point)
   - Age >45 years AND existing risk factors: +1 point

### Risk Categorization

- **Low Risk**: Score = 0
- **Moderate Risk**: Score 1-4
- **High Risk**: Score 5-10

### Clinical Standards Used

- **BMI**: Asian-Indian standards (lower thresholds than WHO general standards)
- **Diabetes**: ICMR (Indian Council of Medical Research) guidelines
- **Hypertension**: AHA (American Heart Association) standards
- **Age Factor**: Based on epidemiological data showing increased risk with age

## Technology Choices

### Frontend Framework: Streamlit

**Rationale**:
- Rapid development for data science applications
- Built-in components (forms, charts, tables)
- Python-based (no HTML/CSS/JavaScript required)
- Automatic reactivity and state management
- Excellent for prototyping and educational projects

**Trade-offs**:
- Less flexible than React/Vue for complex UIs
- Limited customization compared to traditional web frameworks
- Best suited for data-centric applications

### Data Storage: Google Sheets

**Rationale**:
- No database server setup required
- Free tier sufficient for educational use
- Streamlit Cloud compatible (ephemeral file system safe)
- Real-time collaboration possible
- Visual data inspection

**Trade-offs**:
- Performance degrades with large datasets (>10,000 rows)
- Limited query capabilities
- Write conflicts with concurrent users
- Not suitable for production-scale deployment

**Migration Path for Production**:
- PostgreSQL or MySQL for structured data
- Proper indexing and query optimization
- Connection pooling
- Transaction support

### PDF Generation: FPDF

**Rationale**:
- Simple API for basic PDF creation
- No external dependencies
- Lightweight library
- Sufficient for health reports

**Trade-offs**:
- Limited formatting options
- Manual layout positioning
- No advanced graphics capabilities

## Security Considerations

### Current Implementation

- Input validation on all user inputs
- Google Sheets credentials stored in secrets (not in code)
- Error messages don't expose system internals

### Recommendations for Production

- User authentication and authorization
- Data encryption at rest
- Audit logging
- HIPAA/GDPR compliance review
- Regular security audits
- Input sanitization review

## Performance Characteristics

### Response Times

- Risk calculation: < 100ms (CPU-bound, deterministic)
- Database read: 200-500ms (depends on Google Sheets API)
- Database write: 500-1000ms (depends on Google Sheets API)
- PDF generation: < 200ms (CPU-bound)

### Scalability Limits

- Google Sheets: Efficient up to ~10,000 rows
- Concurrent users: Limited by Google Sheets API rate limits
- Memory usage: Low (streaming data processing)

### Optimization Opportunities

- Cache Google Sheets reads (with TTL)
- Async PDF generation (background task)
- Pagination for patient records
- Database indexing (if migrating to SQL)

## Deployment Architecture

### Local Development

```
Developer Machine
    ↓
Python Virtual Environment
    ↓
Streamlit Development Server
    ↓
Local Browser (localhost:8501)
```

### Cloud Deployment (Streamlit Cloud)

```
Streamlit Cloud Infrastructure
    ↓
Containerized Application
    ↓
Google Sheets API (External)
    ↓
User Browser
```

**Requirements**:
- Google Sheets configured with proper permissions
- Secrets configured in Streamlit Cloud dashboard
- No local file system dependencies

## Extensibility

### Adding New Risk Factors

1. Update `calculate_scrs()` in `src/logic.py`
2. Add scoring logic for new factor
3. Update database schema in `src/database.py`
4. Update UI in `app.py` for input
5. Update PDF report in `src/reports.py`

### Adding New Features

1. Create new module in `src/` directory
2. Import in `app.py`
3. Add UI components
4. Update documentation

### Migration to Production Database

1. Replace Google Sheets connection with SQL connection
2. Update `src/database.py` functions
3. Add database migration scripts
4. Update connection configuration
5. Test data migration

## Testing Strategy

### Current State

- Manual testing only
- No automated test suite

### Recommended Testing

**Unit Tests**:
- Test `calculate_scrs()` with known inputs/outputs
- Test `validate_inputs()` with edge cases
- Test score boundaries (0, 4, 5, 10)

**Integration Tests**:
- Test database read/write operations
- Test PDF generation with various inputs
- Test error handling paths

**End-to-End Tests**:
- Complete user workflows
- UI component interactions
- Report generation and download

## Maintenance Considerations

### Code Quality

- Modular structure enables easy maintenance
- Clear separation of concerns
- Comprehensive error handling
- Documentation with docstrings

### Monitoring

- Add application logging
- Monitor Google Sheets API usage
- Track error rates
- Monitor response times

### Updates

- Clinical guidelines may change (ICMR updates)
- Streamlit framework updates
- Dependency updates (security patches)
- Feature enhancements based on feedback

## Conclusion

The Swasthya Monitor architecture prioritizes simplicity, maintainability, and educational value. The modular design allows for easy understanding and extension. While optimized for educational use, the architecture provides a clear path for production deployment with appropriate modifications.

The rule-based approach ensures transparency and explainability, critical for healthcare applications. The cloud-ready design demonstrates modern web application practices while remaining accessible for educational purposes.
