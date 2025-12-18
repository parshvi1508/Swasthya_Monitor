# Setup Instructions

## Installation Steps

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Fix PDF Library Conflict (if needed)

If you see a warning about PyFPDF and fpdf2:

```bash
pip uninstall --yes pypdf
pip install --upgrade fpdf2
```

### 3. Configure Secrets

Create `.streamlit/secrets.toml`:

```toml
[connections.gsheets]
spreadsheet = "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID"

GROQ_API_KEY = "your_groq_api_key_here"
```

### 4. Set Up Google Sheet

1. Create a Google Sheet named `Swasthya_DB`
2. Add headers in Row 1:
   ```
   Date | Patient_ID | Name | Age | Gender | Weight | Height | BMI | Sugar | BP | Risk_Score | Label | Phone | Followup_Date | Advice
   ```
3. Share the sheet with appropriate permissions

### 5. Run the Application

```bash
streamlit run app.py
```

## Troubleshooting

### Import Errors

If you see import errors:
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again
- Check Python version (requires 3.8+)

### Google Sheets Connection

If Google Sheets doesn't work:
- App will run in fallback mode (no data saving)
- Check `secrets.toml` configuration
- Verify Google Sheet permissions

### Groq API Issues

If AI advice doesn't work:
- App will use fallback advice
- Check `GROQ_API_KEY` in `secrets.toml`
- Verify API key is valid at console.groq.com

