import streamlit as st
import pandas as pd
from datetime import datetime
import hashlib

# Try to import Google Sheets connection, with fallback
try:
    from streamlit_gsheets import GSheetsConnection
    HAS_GSHEETS = True
except ImportError:
    HAS_GSHEETS = False
    st.warning("Google Sheets connection not available. Using fallback mode.")

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
                                         "BMI", "Sugar", "BP", "Risk_Score", "Label", "Phone"])
        df = conn.read(worksheet="Sheet1", usecols=list(range(13)), ttl=0)  # ttl=0 means no caching (real-time)
        return df.dropna(how="all")
    except Exception as e:
        # Log error but don't crash the app
        return pd.DataFrame(columns=["Date", "Patient_ID", "Name", "Age", "Gender", "Weight", "Height", 
                                     "BMI", "Sugar", "BP", "Risk_Score", "Label", "Phone"])

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
        
        # Prepare new row with all required fields
        new_row = pd.DataFrame([{
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Name": str(data.get('name', 'Unknown')),
            "Age": int(data.get('age', 0)),
            "Gender": str(data.get('gender', 'Unknown')),
            "Weight": float(data.get('weight', 0)),
            "Height": float(data.get('height', 0)),
            "BMI": float(data.get('bmi', 0)),
            "Sugar": int(data.get('sugar', 0)),
            "BP": f"{data.get('sys', 0)}/{data.get('dia', 0)}",
            "Risk_Score": int(data.get('score', 0)),
            "Label": str(data.get('label', 'Unknown'))
        }])
        
        # Combine and Update
        updated_df = pd.concat([existing_data, new_row], ignore_index=True)
        conn.update(worksheet="Sheet1", data=updated_df)
    except KeyError as e:
        st.error(f"Missing required field in record data: {str(e)}")
    except Exception as e:
        # If Google Sheets connection fails, log error but don't crash app
        st.error(f"Failed to save record to database: {str(e)}. Please check your Google Sheets connection.")

