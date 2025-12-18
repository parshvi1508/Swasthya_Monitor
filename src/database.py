import streamlit as st
import pandas as pd
from datetime import datetime
import hashlib

# Try to import Google Sheets connection, with fallback
HAS_GSHEETS = False
try:
    from streamlit_gsheets import GSheetsConnection
    HAS_GSHEETS = True
except ImportError:
    # Google Sheets connection not available - app will work in fallback mode
    pass

# Initialize Connection
def get_conn():
    if HAS_GSHEETS:
        try:
            return st.connection("gsheets", type=GSheetsConnection)
        except Exception:
            return None
    return None

def init_db():
    """Initialize database connection (placeholder for compatibility)"""
    pass

def get_history():
    """
    Fetch all patient records from Google Sheet.
    
    Returns:
        pandas.DataFrame: DataFrame containing all patient records, or empty DataFrame if error occurs.
    """
    try:
        conn = get_conn()
        if conn is None:
            return pd.DataFrame(columns=["Date", "Patient_ID", "Name", "Age", "Gender", "Weight", "Height", 
                                         "BMI", "Sugar", "BP", "Risk_Score", "Label", "Phone", "Followup_Date", "Advice"])
        df = conn.read(worksheet="Sheet1", usecols=list(range(15)), ttl=0)  # ttl=0 means no caching (real-time)
        return df.dropna(how="all")
    except Exception as e:
        # Log error but don't crash the app
        return pd.DataFrame(columns=["Date", "Patient_ID", "Name", "Age", "Gender", "Weight", "Height", 
                                     "BMI", "Sugar", "BP", "Risk_Score", "Label", "Phone", "Followup_Date", "Advice"])

def get_patient_history(patient_id):
    """
    Get history for a specific patient by Patient ID.
    
    Args:
        patient_id: Unique patient identifier
    
    Returns:
        pandas.DataFrame: Patient's historical records
    """
    df = get_history()
    if df.empty or 'Patient_ID' not in df.columns:
        return pd.DataFrame()
    return df[df['Patient_ID'] == patient_id].sort_values('Date')

def generate_patient_id(name, phone):
    """
    Generate a unique patient ID from name and phone.
    Format: First 2 letters of name + Last 4 digits of phone + Current year
    
    Args:
        name: Patient name
        phone: Patient phone number (string)
    
    Returns:
        str: Patient ID (e.g., "Ra9876-2024")
    """
    if not name or not phone:
        # Fallback to hash if name/phone missing
        combined = f"{name or 'Unknown'}{phone or '0000'}"
        hash_id = hashlib.md5(combined.encode()).hexdigest()[:8]
        return f"PAT-{hash_id}"
    
    # First 2 letters of name (uppercase)
    name_part = name[:2].upper()
    
    # Last 4 digits of phone
    phone_str = str(phone).replace(" ", "").replace("-", "")
    phone_part = phone_str[-4:] if len(phone_str) >= 4 else phone_str.zfill(4)
    
    # Current year
    year = datetime.now().strftime("%Y")
    
    return f"{name_part}{phone_part}-{year}"

def add_record(data):
    """
    Append a new patient record to the Google Sheet.
    
    Args:
        data: Dictionary containing patient information and health metrics
    """
    try:
        conn = get_conn()
        existing_data = get_history()
        
        # Generate Patient ID if not provided
        patient_id = data.get('patient_id') or generate_patient_id(
            data.get('name', 'Unknown'),
            data.get('phone', '0000')
        )
        
        # Prepare new row with all required fields
        new_row = pd.DataFrame([{
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Patient_ID": patient_id,
            "Name": str(data.get('name', 'Unknown')),
            "Age": int(data.get('age', 0)),
            "Gender": str(data.get('gender', 'Unknown')),
            "Weight": float(data.get('weight', 0)),
            "Height": float(data.get('height', 0)),
            "BMI": float(data.get('bmi', 0)),
            "Sugar": int(data.get('sugar', 0)),
            "BP": f"{data.get('sys', 0)}/{data.get('dia', 0)}",
            "Risk_Score": int(data.get('score', 0)),
            "Label": str(data.get('label', 'Unknown')),
            "Phone": str(data.get('phone', '')),
            "Followup_Date": data.get('followup_date', ''),
            "Advice": str(data.get('advice', ''))[:500]  # Limit length
        }])
        
        # Combine and Update
        if conn is None:
            st.warning("⚠️ Database connection not available. Record not saved. Please configure Google Sheets connection.")
            return
        
        # Try to save using update method (requires write access)
        try:
            updated_df = pd.concat([existing_data, new_row], ignore_index=True)
            conn.update(worksheet="Sheet1", data=updated_df)
            st.success("✅ Record saved successfully!")
        except Exception as update_error:
            error_msg = str(update_error)
            if "Public Spreadsheet cannot be written" in error_msg or "Service Account" in error_msg or "cannot be written" in error_msg.lower():
                st.warning("""
                ⚠️ **Google Sheets Write Access Required**
                
                Your Google Sheet is set to read-only mode. To enable saving records:
                
                **Quick Fix (Recommended for Testing):**
                1. Open your Google Sheet
                2. Click **"Share"** button (top right)
                3. Change from **"Viewer"** to **"Editor"** 
                4. Or select **"Anyone with the link can edit"**
                5. Refresh this app and try again
                
                **For Production (More Secure):**
                See `GOOGLE_SHEETS_SETUP.md` for Service Account setup instructions.
                
                **Note:** The app works normally - all features function. Only data saving is disabled.
                """)
            else:
                st.warning(f"⚠️ Could not save record: {error_msg}. The app continues to work normally.")
    except KeyError as e:
        st.error(f"Missing required field in record data: {str(e)}")
    except Exception as e:
        # If Google Sheets connection fails, log error but don't crash app
        error_msg = str(e)
        if "Public Spreadsheet cannot be written" in error_msg:
            st.warning("⚠️ Google Sheets is read-only. Please enable edit access or use Service Account authentication.")
        else:
            st.warning(f"⚠️ Could not save record: {error_msg}. Records will still be displayed.")

