# Swasthya Monitor

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**AI-Powered Health Screening System for Indian Population**

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Documentation](#documentation) • [Contributing](#contributing)

</div>

---

## Overview

Swasthya Monitor is a comprehensive web-based healthcare screening application designed specifically for the Indian population. It implements a rule-based expert system combined with machine learning and AI to provide accurate health risk assessment using Indian Council of Medical Research (ICMR) guidelines and Asian-Indian health standards.

### Key Highlights

- 🏥 **Clinical Standards**: ICMR guidelines and Asian-Indian BMI classifications
- 🤖 **AI-Powered**: Personalized health advice using Groq API (Llama-3)
- 📊 **ML Integration**: Trend prediction using Linear Regression
- 🌐 **Bilingual**: English and Hindi support for rural accessibility
- 📱 **Cloud-Ready**: Google Sheets integration for seamless deployment
- ⚡ **High Performance**: O(1) time complexity for instant results

## Features

### Core Functionality

- **Real-time Risk Assessment**: Composite Risk Score (SCRS) calculation from patient vitals
- **Multi-factor Analysis**: BMI, blood sugar, blood pressure, and age-based risk evaluation
- **Trend Prediction**: ML-based forecasting of health trends using patient history
- **AI Health Advice**: Personalized care plans with Indian food recommendations
- **Patient History Tracking**: Unique Patient ID system for accurate record management
- **Follow-up Management**: Automated follow-up date calculation for high-risk patients
- **Chronotype Detection**: Sleep pattern analysis for comprehensive health assessment

### Clinical Standards

- **BMI Classification**: Asian-Indian standards (Normal: 18.5-22.9, Overweight: ≥23, Obese: ≥25)
- **Diabetes Screening**: ICMR thresholds (Normal: <100, Prediabetic: 100-126, Diabetic: >126 mg/dL)
- **Hypertension Detection**: AHA standards with Indian population considerations
- **Age-Adjusted Scoring**: Synergy factors for age-related risk assessment

### Reporting & Export

- **PDF Reports**: Professional health reports with bilingual support
- **WhatsApp Integration**: Direct sharing of results with patients
- **Population Analytics**: Aggregate statistics and trend visualization

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Frontend | Streamlit 1.29+ |
| Backend | Python 3.8+ |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn |
| AI/LLM | Groq API (Llama-3-8b) |
| Database | Google Sheets |
| PDF Generation | FPDF2 |
| Visualization | Plotly |

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Google account (for Google Sheets)
- Groq API key (free tier available at [console.groq.com](https://console.groq.com))

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Swasthya-Monitor
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure secrets**
   
   Create `.streamlit/secrets.toml`:
   ```toml
   [connections.gsheets]
   spreadsheet = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID"
   
   GROQ_API_KEY = "gsk_your_groq_api_key_here"
   ```

5. **Set up Google Sheet**
   
   - Create a Google Sheet named `Swasthya_DB`
   - Add headers: `Date`, `Patient_ID`, `Name`, `Age`, `Gender`, `Weight`, `Height`, `BMI`, `Sugar`, `BP`, `Risk_Score`, `Label`, `Phone`, `Followup_Date`, `Advice`
   - Share with appropriate permissions

6. **Run the application**
   ```bash
   streamlit run app.py
   ```

   The app will open at `http://localhost:8501`

## Usage

### Patient Screening Workflow

1. **Enter Patient Information**
   - Select language (English/Hindi)
   - Enter patient name and phone number
   - Input age, gender, and vital signs
   - Optionally add medications and sleep patterns

2. **Run Diagnostics**
   - Click "Run Diagnostics" to calculate risk score
   - Review composite risk score and identified risk factors
   - View trend predictions (if history available)
   - Read AI-generated personalized advice

3. **Export & Share**
   - Download PDF report
   - Share results via WhatsApp
   - Review follow-up recommendations

### Patient Records

- View all historical records in the "Patient Records" tab
- Track individual patient history using Patient ID
- Analyze population-level statistics and trends

## Project Structure

```
Swasthya-Monitor/
├── .streamlit/
│   ├── config.toml          # UI theme configuration
│   └── secrets.toml          # API keys and credentials (not in repo)
├── src/
│   ├── __init__.py
│   ├── logic.py              # SCRS algorithm & validation
│   ├── database.py           # Google Sheets integration
│   ├── reports.py           # PDF & WhatsApp reports
│   ├── prediction.py        # ML trend prediction
│   └── ai_advice.py         # AI-powered health advice
├── app.py                   # Main application entry point
├── requirements.txt         # Python dependencies
├── README.md                # This file
├── LICENSE                  # MIT License
├── .gitignore              # Git ignore rules
├── ARCHITECTURE.md          # System architecture documentation
├── CODEBASE_ANALYSIS.md     # Comprehensive codebase analysis
└── TEST_CASES.md           # Test cases documentation
```

## Algorithm: Composite Risk Score (SCRS)

The SCRS algorithm combines multiple risk factors on a 0-10 scale:

| Component | Points | Threshold |
|-----------|--------|-----------|
| BMI (Obesity) | +3 | BMI ≥ 25 |
| BMI (Overweight) | +2 | BMI ≥ 23 |
| Diabetes | +3 | Sugar > 126 mg/dL |
| Prediabetes | +1 | Sugar 100-126 mg/dL |
| Hypertension | +3 | BP ≥ 140/90 |
| Elevated BP | +1 | BP ≥ 130/80 |
| Age Synergy | +1 | Age >45 with comorbidities |

**Risk Categories:**
- **Low Risk**: Score = 0
- **Moderate Risk**: Score 1-4
- **High Risk**: Score 5-10

## Clinical Standards Reference

### BMI Classification (Asian-Indian)

| Category | BMI Range |
|----------|----------|
| Underweight | < 18.5 kg/m² |
| Normal | 18.5 - 22.9 kg/m² |
| Overweight | 23.0 - 24.9 kg/m² |
| Obese | ≥ 25.0 kg/m² |

### Blood Sugar (ICMR Guidelines)

| Category | Fasting Blood Sugar |
|----------|---------------------|
| Normal | < 100 mg/dL |
| Prediabetic | 100 - 126 mg/dL |
| Diabetic | > 126 mg/dL |

### Blood Pressure (AHA Standards)

| Category | Systolic/Diastolic |
|----------|-------------------|
| Normal | < 120/80 mmHg |
| Elevated | 120-139/80-89 mmHg |
| Hypertension Stage 1 | 140-159/90-99 mmHg |
| Hypertension Stage 2 | ≥ 160/100 mmHg |

## Performance Characteristics

- **Time Complexity**: O(1) for SCRS calculation (constant time)
- **Space Complexity**: O(1) for SCRS algorithm
- **Response Time**: < 1ms for risk calculation
- **Suitable for**: Low-resource hardware in rural PHCs

## Documentation

- **[ARCHITECTURE.md](ARCHITECTURE.md)**: System architecture and design patterns
- **[CODEBASE_ANALYSIS.md](CODEBASE_ANALYSIS.md)**: Comprehensive codebase analysis
- **[TEST_CASES.md](TEST_CASES.md)**: Test cases and validation scenarios

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 style guide
- Add docstrings to all functions
- Include error handling
- Write clear, descriptive commit messages

## Limitations & Disclaimers

⚠️ **Important Medical Disclaimer**

This application is a **screening tool**, not a diagnostic system. It should not replace professional medical consultation. Always consult qualified healthcare professionals for medical diagnosis and treatment.

- Designed for educational and screening purposes
- Uses standard guidelines; individual cases may vary
- Not intended for emergency medical situations
- Ensure proper data security for patient information

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **Indian Council of Medical Research (ICMR)** for clinical guidelines
- **American Heart Association (AHA)** for blood pressure standards
- **Streamlit** team for the excellent framework
- **Groq** for fast AI inference API

## Support

For issues, questions, or contributions:

1. Check the [documentation](ARCHITECTURE.md)
2. Review [test cases](TEST_CASES.md)
3. Open an issue on GitHub

---

<div align="center">

**Built with ❤️ for healthcare accessibility in India**

[⬆ Back to Top](#swasthya-monitor)

</div>
