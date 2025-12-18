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

# 🔹 App Main Title
st.markdown("""
<h1 style='text-align:center; color:#008080; margin-bottom:0;'>
    🏥 Swasthya Monitor
</h1>
<p style='text-align:center; color:#555; margin-top:0;'>
    AI-powered Preventive Health Screening System
</p>
<hr>
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
    
    st.subheader("महत्वपूर्ण संकेत" if language == "Hindi" else "Vitals")
    weight = st.number_input("वजन (किलो)" if language == "Hindi" else "Weight (kg)", 30, 150, 70)
    height = st.number_input("ऊंचाई (सेंटीमीटर)" if language == "Hindi" else "Height (cm)", 100, 250, 170)
    sugar = st.number_input("उपवास शर्करा (mg/dL)" if language == "Hindi" else "Fasting Sugar (mg/dL)", 50, 500, 90)
    sys_bp = st.number_input("सिस्टोलिक बीपी" if language == "Hindi" else "Systolic BP", 90, 250, 120)
    dia_bp = st.number_input("डायस्टोलिक बीपी" if language == "Hindi" else "Diastolic BP", 50, 150, 80)
    
    # Optional: Medications
    meds = st.text_input("वर्तमान दवाएं (वैकल्पिक)" if language == "Hindi" else "Current Medications (Optional)", 
                         placeholder="जैसे, Metformin, Amlodipine" if language == "Hindi" else "e.g., Metformin, Amlodipine")
    
    # Optional: Chronotype Detection
    bedtime = None
    waketime = None
    with st.expander("नींद का पैटर्न (वैकल्पिक)" if language == "Hindi" else "Sleep Pattern (Optional)"):
        bedtime = st.number_input("सोने का समय (24 घंटे)" if language == "Hindi" else "Bedtime Hour (24hr)", 0, 23, 22, 
                                   help="जैसे, 22 का मतलब 10 बजे रात" if language == "Hindi" else "e.g., 22 for 10 PM", key="bedtime")
        waketime = st.number_input("जागने का समय (24 घंटे)" if language == "Hindi" else "Wake Time Hour (24hr)", 0, 23, 6,
                                    help="जैसे, 6 का मतलब सुबह 6 बजे" if language == "Hindi" else "e.g., 6 for 6 AM", key="waketime")
    
    analyze_btn = st.button("Run Diagnostics / निदान चलाएं" if language == "Hindi" else "Run Diagnostics", 
                            type="primary")

# 4. Main Area (Tabs)
tab1, tab2 = st.tabs(["🏥 वर्तमान विश्लेषण" if language == "Hindi" else "🏥 Current Analysis", "📂 रोगी रिकॉर्ड" if language == "Hindi" else "📂 Patient Records"])

with tab1:
    if analyze_btn:
        # A. Validation
        if not name or not name.strip():
            st.error("कृपया रोगी का नाम दर्ज करें।" if language == "Hindi" else "Please enter a patient name.")
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
                
                # Chronotype Detection (if provided)
                chronotype = None
                sleep_hours = None
                if bedtime is not None and waketime is not None:
                    try:
                        chronotype = logic.detect_chronotype(bedtime, waketime)
                        # Calculate sleep duration
                        if bedtime > waketime:
                            sleep_hours = (24 - bedtime) + waketime
                        else:
                            sleep_hours = waketime - bedtime
                    except Exception:
                        chronotype = None
                        sleep_hours = None
                
                # Calculate risk score with sleep data
                score, label, color, factors = logic.calculate_scrs(age, bmi, sugar, sys_bp, dia_bp, sleep_hours)
                
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
                        advice_text = ai_advice.get_holistic_advice(name, age, label, trend, meds, language, chronotype, sleep_hours)
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
                    # BMI Category
                    bmi_category = "Underweight" if bmi < 18.5 else "Normal" if bmi < 25 else "Overweight" if bmi < 30 else "Obese"
                    st.metric("BMI", f"{bmi}", delta=bmi_category, delta_color="off")
                with col3:
                    sugar_status = "Normal" if sugar < 100 else "Prediabetic" if sugar < 126 else "Diabetic"
                    st.metric("Sugar", f"{sugar} mg/dL", delta=sugar_status, delta_color="inverse" if sugar >= 100 else "normal")
                with col4:
                    bp_status = "Normal" if sys_bp < 120 and dia_bp < 80 else "Elevated" if sys_bp < 130 else "High"
                    st.metric("BP", f"{sys_bp}/{dia_bp}", delta=bp_status, delta_color="inverse" if sys_bp >= 130 else "normal")
                
                # Additional Health Indicators Row
                st.markdown("<br>", unsafe_allow_html=True)
                col_a, col_b, col_c = st.columns(3, gap="medium")
                with col_a:
                    ideal_weight = round(22 * ((height/100)**2), 1)  # BMI 22 is ideal
                    weight_diff = weight - ideal_weight
                    st.metric("Ideal Weight", f"{ideal_weight} kg", 
                             delta=f"{weight_diff:+.1f} kg" if abs(weight_diff) > 2 else "Optimal",
                             delta_color="inverse" if abs(weight_diff) > 2 else "normal")
                with col_b:
                    # Heart Rate Zone (estimated from age)
                    max_hr = 220 - age
                    target_hr = round(max_hr * 0.7)  # 70% of max
                    st.metric("Target Heart Rate", f"{target_hr} bpm", delta=f"Max: {max_hr}")
                with col_c:
                    # Risk Level Color Indicator
                    risk_emoji = "🟢" if score <= 3 else "🟡" if score <= 6 else "🟠" if score <= 8 else "🔴"
                    st.metric("Status", f"{risk_emoji} {label}", delta="")
                
                # Chronotype & Sleep Display (if available)
                if chronotype:
                    sleep_quality = "Adequate" if sleep_hours and 7 <= sleep_hours <= 9 else "Poor" if sleep_hours and sleep_hours < 6 else "Excessive" if sleep_hours and sleep_hours > 9 else "Unknown"
                    if language == "Hindi":
                        st.info(f"**😴 नींद विश्लेषण:** {chronotype} | {sleep_hours:.1f} घंटे/रात | गुणवत्ता: {sleep_quality}")
                    else:
                        st.info(f"**😴 Sleep Analysis:** {chronotype} | {sleep_hours:.1f} hrs/night | Quality: {sleep_quality}")
                
                # Row 2: Detailed Risk Factors with Explanations
                st.markdown("---")
                st.subheader("📊 Risk Factor Analysis" if language == "English" else "📊 जोखिम कारक विश्लेषण")
                
                if factors:
                    # Create expandable sections for each risk factor
                    for factor in factors:
                        with st.expander(f"⚠️ {factor}", expanded=False):
                            # Check for BMI-related factors
                            if "Obesity" in factor or "Overweight" in factor or "BMI" in factor:
                                if bmi < 18.5:
                                    st.write("**Concern:** Underweight increases infection risk and weakens immune system.")
                                    st.write("**Action:** Increase protein intake, eat nutrient-dense foods like nuts, dairy, eggs.")
                                elif bmi >= 25:
                                    st.write("**Concern:** Excess weight increases risk of diabetes, heart disease, and joint problems.")
                                    st.write("**Action:** Reduce portion sizes, increase physical activity to 150 min/week, avoid sugary drinks.")
                                else:
                                    st.write("**Status:** Borderline weight. Monitor closely.")
                                    st.write("**Action:** Maintain balanced diet and regular exercise routine.")
                            
                            # Check for Sugar/Diabetes factors
                            elif "Diabetic" in factor or "Prediabetic" in factor or "Sugar" in factor:
                                if sugar > 126:
                                    st.write("**Concern:** Diabetic range - High blood sugar damages blood vessels, nerves, kidneys, and eyes over time.")
                                    st.write("**Action:** Consult doctor immediately, limit refined carbs, monitor blood sugar daily, take prescribed medications.")
                                elif sugar > 100:
                                    st.write("**Concern:** Prediabetic range - High risk of developing diabetes if not controlled.")
                                    st.write("**Action:** Reduce sugar intake, choose whole grains over white rice/bread, exercise 30 min daily, recheck in 3 months.")
                            
                            # Check for Blood Pressure factors
                            elif "Hypertension" in factor or "Elevated BP" in factor or "BP" in factor or "Blood Pressure" in factor:
                                if sys_bp >= 140 or dia_bp >= 90:
                                    st.write("**Concern:** Hypertension - High BP strains heart and arteries, increasing stroke and heart attack risk.")
                                    st.write("**Action:** Reduce salt to <5g/day, manage stress with yoga/meditation, avoid smoking, take BP medications as prescribed.")
                                elif sys_bp >= 130 or dia_bp >= 80:
                                    st.write("**Concern:** Elevated BP - Borderline high blood pressure, needs lifestyle intervention.")
                                    st.write("**Action:** Limit salt, reduce caffeine, increase potassium-rich foods (banana, spinach), exercise regularly.")
                            
                            # Age-related risk
                            elif "Age" in factor:
                                st.write("**Concern:** Age-related risk increases for chronic conditions like diabetes, heart disease.")
                                st.write("**Action:** Annual comprehensive health screenings, maintain active lifestyle, calcium & vitamin D supplementation.")
                            
                            # Generic fallback
                            elif "Sleep Deprivation" in factor:
                                st.write("**Concern:** Less than 6 hours of sleep increases risk of heart disease, diabetes, and weakened immunity.")
                                st.write("**Action:** Establish consistent sleep schedule, avoid screens 1hr before bed, create dark cool room.")
                            elif "Excessive Sleep" in factor:
                                st.write("**Concern:** More than 9 hours of sleep may indicate underlying health issues or depression.")
                                st.write("**Action:** Consult doctor to rule out sleep disorders, maintain regular sleep-wake schedule.")
                            else:
                                st.write(f"**Risk Factor:** {factor}")
                                st.write("**Action:** Consult healthcare provider for personalized advice.")
                else:
                    st.success("✅ All vitals within normal range! Keep up the healthy lifestyle." if language == "English" else "✅ सभी महत्वपूर्ण संकेत सामान्य सीमा में हैं! स्वस्थ जीवनशैली बनाए रखें।")
                
                # G. Historical Trend & Prediction Display
                st.markdown("---")
                st.subheader("📈 Health Trends & Predictions" if language == "English" else "📈 स्वास्थ्य प्रवृत्तियाँ और भविष्यवाणियाँ")
                
                if not history_df.empty and len(history_df) >= 2:
                    # Show historical trend chart
                    col_chart1, col_chart2 = st.columns(2, gap="medium")
                    
                    with col_chart1:
                        if 'Sugar' in history_df.columns:
                            st.line_chart(history_df[['Sugar']].tail(10), height=200)
                            st.caption("Blood Sugar Trend (Last 10 visits)" if language == "English" else "रक्त शर्करा प्रवृत्ति (पिछली 10 यात्राएं)")
                    
                    with col_chart2:
                        if 'Risk_Score' in history_df.columns:
                            st.line_chart(history_df[['Risk_Score']].tail(10), height=200)
                            st.caption("Risk Score Trend (Last 10 visits)" if language == "English" else "जोखिम स्कोर प्रवृत्ति (पिछली 10 यात्राएं)")
                    
                    # Prediction
                    if future_pred:
                        trend_emoji = "📈" if trend == "negative" else "📉" if trend == "positive" else "➡️"
                        if language == "Hindi":
                            pred_text = f"{trend_emoji} **भविष्यवाणी विश्लेषण:** यदि आप वर्तमान आदतें जारी रखते हैं, तो आपकी अगली यात्रा पर अनुमानित रक्त शर्करा **{future_pred.get('Sugar', 'N/A')} mg/dL** होगी।"
                        else:
                            pred_text = f"{trend_emoji} **Prediction Analysis:** If you continue current habits, your predicted Sugar at next visit: **{future_pred.get('Sugar', 'N/A')} mg/dL**."
                        
                        if trend == "positive":
                            st.success(pred_text + " ✅ Improving!" if language == "English" else pred_text + " ✅ सुधार हो रहा है!")
                        elif trend == "negative":
                            st.warning(pred_text + " ⚠️ Needs attention!" if language == "English" else pred_text + " ⚠️ ध्यान देने की आवश्यकता!")
                        else:
                            st.info(pred_text)
                else:
                    st.info("📊 Historical data unavailable. Visit us again to unlock trend predictions and charts!" if language == "English" else "📊 ऐतिहासिक डेटा अनुपलब्ध। प्रवृत्ति भविष्यवाणियों और चार्ट को अनलॉक करने के लिए फिर से आएं!")
                
                # H. AI Advice Display
                if advice_text:
                    advice_title = "🤖 डॉ. स्वास्थ्य की देखभाल योजना" if language == "Hindi" else "🤖 Dr. Swasthya's Care Plan"
                    st.markdown("---")
                    st.subheader(advice_title)
                    # Use Streamlit container for proper markdown rendering
                    with st.container():
                        st.markdown(advice_text)  # Direct markdown rendering - no HTML wrapper
                
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
                    'advice': advice_text or "",
                    'chronotype': chronotype,
                    'sleep_hours': sleep_hours,
                    'factors': factors
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
    st.subheader("अस्पताल डेटाबेस रिकॉर्ड" if language == "Hindi" else "Hospital Database Records")
    df = database.get_history()
    
    if df.empty:
        st.info("कोई रोगी रिकॉर्ड नहीं मिला। विश्लेषण के बाद रिकॉर्ड यहां दिखाई देंगे।" if language == "Hindi" else "No patient records found. Records will appear here after analysis.")
    else:
        st.dataframe(df, use_container_width=True)
        
        # Population Analytics
        if 'Risk_Score' in df.columns:
            st.subheader("जनसंख्या विश्लेषण" if language == "Hindi" else "Population Analytics")
            st.bar_chart(df['Risk_Score'])
        elif 'Label' in df.columns:
            st.subheader("जनसंख्या विश्लेषण" if language == "Hindi" else "Population Analytics")
            # Count risk levels if Risk_Score column is missing
            risk_counts = df['Label'].value_counts()
            st.bar_chart(risk_counts)
