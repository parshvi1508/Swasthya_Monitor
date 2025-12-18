import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from src import logic, database, reports, prediction, ai_advice

# 1. Page Config (Must be first)
st.set_page_config(page_title="Swasthya Monitor", page_icon="🏥", layout="wide")

database.init_db()

# 2. Custom CSS for "Clean Minimal UI"
st.markdown("""
<style>
    .block-container {
        padding-top: 1.5rem; 
        padding-bottom: 1rem;
        max-width: 100%;
    }
    h1 {color: #008080;}
    h2 {color: #008080; margin-top: 1.5rem;}
    h3 {color: #2C3E50; margin-top: 1rem;}
    .stButton button {
        width: 100%; 
        border-radius: 5px;
        margin-top: 0.5rem;
    }
    div[data-testid="stMetricValue"] {
        font-size: 24px;
    }
    [data-testid="stMetric"] {
        padding: 0.5rem;
    }
    .stMarkdown {
        margin-bottom: 0.5rem;
    }
    /* Prevent overlapping on mobile */
    @media (max-width: 768px) {
        [data-testid="column"] {
            width: 100% !important;
            margin-bottom: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# 3. Sidebar (Inputs)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966327.png", width=50)
    st.title("Patient Entry")
    
    # Language Toggle
    language = st.radio("Language / भाषा", ["English", "Hindi"], horizontal=True)
    
    # Patient Identification
    name = st.text_input("Full Name / पूरा नाम" if language == "Hindi" else "Full Name")
    phone = st.text_input("Phone Number / फोन नंबर" if language == "Hindi" else "Phone Number", 
                          placeholder="10 digits", help="Used to generate unique Patient ID")
    
    age = st.number_input("Age / उम्र" if language == "Hindi" else "Age", 1, 120, 45)
    gender = st.radio("Gender / लिंग" if language == "Hindi" else "Gender", ["Male", "Female"], horizontal=True)
    
    st.subheader("Vitals / महत्वपूर्ण संकेत" if language == "Hindi" else "Vitals")
    weight = st.number_input("Weight (kg) / वजन (किलो)" if language == "Hindi" else "Weight (kg)", 30, 150, 70)
    height = st.number_input("Height (cm) / ऊंचाई (सेंटीमीटर)" if language == "Hindi" else "Height (cm)", 100, 250, 170)
    sugar = st.number_input("Fasting Sugar (mg/dL) / रक्त शर्करा" if language == "Hindi" else "Fasting Sugar (mg/dL)", 50, 500, 90)
    sys_bp = st.number_input("Systolic BP / सिस्टोलिक बीपी" if language == "Hindi" else "Systolic BP", 90, 250, 120)
    dia_bp = st.number_input("Diastolic BP / डायस्टोलिक बीपी" if language == "Hindi" else "Diastolic BP", 50, 150, 80)
    
    # Optional: Medications
    meds = st.text_input("Current Medications (Optional) / वर्तमान दवाएं (वैकल्पिक)" if language == "Hindi" else "Current Medications (Optional)", 
                         placeholder="e.g., Metformin, Amlodipine")
    
    # Optional: Chronotype Detection
    bedtime = None
    waketime = None
    with st.expander("Sleep Pattern / नींद का पैटर्न (Optional)"):
        bedtime = st.number_input("Bedtime Hour / सोने का समय (24hr)", 0, 23, 22, 
                                   help="e.g., 22 for 10 PM", key="bedtime")
        waketime = st.number_input("Wake Time Hour / जागने का समय (24hr)", 0, 23, 6,
                                    help="e.g., 6 for 6 AM", key="waketime")
    
    analyze_btn = st.button("Run Diagnostics / निदान चलाएं" if language == "Hindi" else "Run Diagnostics", 
                            type="primary")

# 4. Main Area (Tabs)
tab1, tab2 = st.tabs(["🏥 Current Analysis", "📂 Patient Records"])

with tab1:
    if analyze_btn:
        # A. Validation
        if not name or not name.strip():
            st.error("Please enter a patient name.")
        else:
            errs = logic.validate_inputs(age, weight, height, sugar, sys_bp, dia_bp)
            if errs:
                for e in errs: 
                    st.error(e)
            else:
                # B. Processing
                # Generate Patient ID
                patient_id = database.generate_patient_id(name, phone)
                
                bmi = round(weight / ((height/100)**2), 1)
                score, label, color, factors = logic.calculate_scrs(age, bmi, sugar, sys_bp, dia_bp)
                
                # Chronotype Detection (if provided)
                chronotype = None
                if bedtime is not None and waketime is not None:
                    try:
                        chronotype = logic.detect_chronotype(bedtime, waketime)
                    except Exception:
                        chronotype = None
                
                # C. Prediction Logic (ML)
                history_df = database.get_patient_history(patient_id)
                future_pred = None
                trend = "stable"
                
                if not history_df.empty and len(history_df) >= 2:
                    # Prepare history for prediction
                    history_for_pred = history_df.copy()
                    # Extract BP values if stored as "140/90" format
                    if 'BP' in history_for_pred.columns:
                        history_for_pred['Systolic_BP'] = history_for_pred['BP'].apply(
                            lambda x: int(str(x).split('/')[0]) if '/' in str(x) else None
                        )
                    future_pred = prediction.predict_trends(history_for_pred)
                    
                    # Determine trend
                    if future_pred and 'Sugar' in future_pred:
                        if future_pred['Sugar'] < sugar:
                            trend = "positive"
                        elif future_pred['Sugar'] > sugar:
                            trend = "negative"
                
                # D. AI Advice Generation
                advice_text = None
                try:
                    with st.spinner("🤖 Generating personalized advice..." if language == "English" else "🤖 व्यक्तिगत सलाह तैयार की जा रही है..."):
                        advice_text = ai_advice.get_holistic_advice(name, age, label, trend, meds, language)
                except Exception as e:
                    advice_text = ai_advice.get_fallback_advice(label, language)
                
                # E. Follow-up Date Calculation
                followup_date = prediction.calculate_followup_date(score)
                
                # F. Display - Responsive Grid
                title_text = f"### निदान: **{name}**" if language == "Hindi" else f"### Diagnosis for: **{name}**"
                st.markdown(title_text)
                
                # Patient ID Display
                st.caption(f"Patient ID: {patient_id}")
                
                # Row 1: Key Metrics - Responsive columns
                col1, col2, col3, col4 = st.columns(4, gap="medium")
                with col1:
                    st.metric("Composite Risk", f"{score}/10", delta=label, delta_color="inverse")
                with col2:
                    st.metric("BMI", f"{bmi}")
                with col3:
                    st.metric("Sugar", f"{sugar} mg/dL")
                with col4:
                    st.metric("BP", f"{sys_bp}/{dia_bp}")
                
                # Chronotype Display (if available)
                if chronotype:
                    st.info(f"**Chronotype / नींद का प्रकार:** {chronotype}")
                
                # Row 2: Detailed Factors
                factors_text = f"**पहचाने गए जोखिम कारक:** {', '.join(factors) if factors else 'कोई नहीं - महत्वपूर्ण संकेत सामान्य'}" if language == "Hindi" else f"**Identified Risk Factors:** {', '.join(factors) if factors else 'None - Vitals Normal'}"
                st.info(factors_text)
                
                # G. Prediction Display
                st.markdown("<br>", unsafe_allow_html=True)  # Add spacing
                if future_pred:
                    if language == "Hindi":
                        pred_text = f"📉 **प्रवृत्ति विश्लेषण:** आपके इतिहास के आधार पर, यदि आप वर्तमान आदतें जारी रखते हैं, तो आपकी भविष्यवाणी की गई रक्त शर्करा अगली यात्रा पर **{future_pred.get('Sugar', 'N/A')} mg/dL** होगी।"
                    else:
                        pred_text = f"📉 **Trend Analysis:** Based on your history, if you continue current habits, your predicted Sugar next visit is **{future_pred.get('Sugar', 'N/A')} mg/dL**."
                    st.info(pred_text)
                else:
                    if language == "Hindi":
                        st.caption("ℹ️ प्रवृत्ति पूर्वानुमान के लिए कृपया फिर से आएं।")
                    else:
                        st.caption("ℹ️ Visit us again to unlock Trend Predictions.")
                
                # H. AI Advice Display
                if advice_text:
                    advice_title = "🤖 डॉ. स्वास्थ्य की देखभाल योजना" if language == "Hindi" else "🤖 Dr. Swasthya's Care Plan"
                    st.markdown("<br>", unsafe_allow_html=True)  # Add spacing
                    st.markdown("---")
                    st.subheader(advice_title)
                    st.markdown(f"""
                    <div style="background-color:#F0F8FF;padding:20px;border-radius:10px;border-left:5px solid #008080;margin-bottom:20px;">
                        {advice_text}
                    </div>
                    """, unsafe_allow_html=True)
                
                # I. Follow-up Date
                if followup_date:
                    followup_text = f"📅 **अनुशंसित अनुवर्ती तिथि:** {followup_date.strftime('%Y-%m-%d')}" if language == "Hindi" else f"📅 **Recommended Follow-up Date:** {followup_date.strftime('%Y-%m-%d')}"
                    st.warning(followup_text)
                
                # J. Save to DB
                record_data = {
                    'patient_id': patient_id,
                    'name': name, 
                    'age': age, 
                    'gender': gender, 
                    'weight': weight, 
                    'height': height, 
                    'bmi': bmi, 
                    'sugar': sugar, 
                    'sys': sys_bp, 
                    'dia': dia_bp, 
                    'score': score, 
                    'label': label,
                    'phone': phone,
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                    'followup_date': followup_date.strftime("%Y-%m-%d") if followup_date else None,
                    'advice': advice_text or ""
                }
                database.add_record(record_data)
            
                # K. Actions (Reports)
                st.markdown("<br>", unsafe_allow_html=True)  # Add spacing
                st.divider()
                export_title = "निर्यात और साझा करें" if language == "Hindi" else "Export & Share"
                st.subheader(export_title)
                c1, c2 = st.columns(2, gap="medium")
                with c1:
                    try:
                        pdf_bytes = reports.create_pdf(record_data, language=language)
                        if pdf_bytes:
                            button_text = "आधिकारिक रिपोर्ट डाउनलोड करें (PDF)" if language == "Hindi" else "Download Official Report (PDF)"
                            st.download_button(
                                button_text, 
                                data=pdf_bytes, 
                                file_name=f"Swasthya_Report_{patient_id}_{datetime.now().strftime('%Y%m%d')}.pdf", 
                                mime="application/pdf",
                                use_container_width=True
                            )
                        else:
                            st.error("PDF generation returned empty data")
                    except Exception as e:
                        st.error(f"PDF generation failed: {str(e)}")
                with c2:
                    try:
                        wa_link = reports.get_whatsapp_link(name, score, label, language)
                        button_text = "WhatsApp पर साझा करें" if language == "Hindi" else "Share via WhatsApp"
                        st.link_button(button_text, wa_link, use_container_width=True)
                    except Exception as e:
                        st.error(f"WhatsApp link generation failed: {str(e)}")
    else:
        info_text = "👈 साइडबार में रोगी विवरण दर्ज करें और 'निदान चलाएं' पर क्लिक करें" if language == "Hindi" else "👈 Enter patient details in the sidebar and click 'Run Diagnostics'"
        st.info(info_text)

with tab2:
    st.subheader("Hospital Database Records")
    df = database.get_history()
    
    if df.empty:
        st.info("No patient records found. Records will appear here after analysis.")
    else:
        st.dataframe(df, use_container_width=True)
        
        # Population Analytics
        if 'Risk_Score' in df.columns:
            st.subheader("Population Analytics")
            st.bar_chart(df['Risk_Score'])
        elif 'Label' in df.columns:
            st.subheader("Population Analytics")
            # Count risk levels if Risk_Score column is missing
            risk_counts = df['Label'].value_counts()
            st.bar_chart(risk_counts)
