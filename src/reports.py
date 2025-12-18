from fpdf import FPDF
import urllib.parse

def create_pdf(data, language="English"):
    """
    Generates a professional PDF health report for the patient.
    
    Args:
        data: Dictionary containing patient information and health metrics
        language: Language for report ("English" or "Hindi")
    
    Returns:
        bytes: PDF file content encoded in latin-1
    """
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        
        # Language-specific title
        if language == "Hindi":
            pdf.cell(0, 10, "Swasthya Monitor - स्वास्थ्य रिपोर्ट", ln=True, align='C')
        else:
            pdf.cell(0, 10, "Swasthya Monitor - Health Report", ln=True, align='C')
        
        pdf.set_font("Arial", size=12)
        pdf.ln(10)
        
        # Safely encode patient name (handle special characters)
        patient_name = str(data.get('name', 'Unknown')).encode('latin-1', 'ignore').decode('latin-1')
        patient_id = data.get('patient_id', 'N/A')
        patient_line = f"Patient ID: {patient_id} | Patient: {patient_name} | Age: {data.get('age', 'N/A')} | Date: {data.get('date', 'N/A')}"
        pdf.cell(0, 10, patient_line, ln=True)
        pdf.line(10, 35, 200, 35)
        
        pdf.ln(10)
        pdf.cell(0, 10, f"Composite Risk Score: {data.get('score', 0)}/10 ({data.get('label', 'Unknown')})", ln=True)
        pdf.cell(0, 10, f"BMI: {data.get('bmi', 0)} | Sugar: {data.get('sugar', 0)} mg/dL | BP: {data.get('sys', 0)}/{data.get('dia', 0)}", ln=True)
        
        # Follow-up date if available
        if data.get('followup_date'):
            followup_text = f"Recommended Follow-up Date: {data.get('followup_date')}" if language == "English" else f"अनुशंसित अनुवर्ती तिथि: {data.get('followup_date')}"
            pdf.cell(0, 10, followup_text, ln=True)
        
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 12)
        if language == "Hindi":
            pdf.cell(0, 10, "चिकित्सकीय सिफारिशें:", ln=True)
        else:
            pdf.cell(0, 10, "Clinical Recommendations:", ln=True)
        pdf.set_font("Arial", size=12)
        
        # AI Advice if available
        if data.get('advice'):
            advice_text = data.get('advice', '')
            # Simple text extraction (remove markdown)
            advice_clean = advice_text.replace('**', '').replace('#', '').strip()
            # Split into lines and add
            for line in advice_clean.split('\n'):
                if line.strip():
                    pdf.cell(0, 8, line[:80], ln=True)  # Limit line length
        else:
            # Fallback recommendations
            score = data.get('score', 0)
            sugar = data.get('sugar', 0)
            
            if score > 4:
                if language == "Hindi":
                    pdf.cell(0, 10, "- तत्काल डॉक्टर परामर्श की सलाह दी जाती है", ln=True)
                else:
                    pdf.cell(0, 10, "- Immediate Doctor Consultation Advised", ln=True)
            if sugar > 100:
                if language == "Hindi":
                    pdf.cell(0, 10, "- कार्बोहाइड्रेट/चीनी का सेवन कम करें", ln=True)
                else:
                    pdf.cell(0, 10, "- Reduce Carbohydrate/Sugar Intake", ln=True)
            if score <= 4:
                if language == "Hindi":
                    pdf.cell(0, 10, "- नियमित स्वास्थ्य जांच जारी रखें", ln=True)
                else:
                    pdf.cell(0, 10, "- Continue regular health checkups", ln=True)
        
        pdf.ln(5)
        pdf.set_font("Arial", 'I', 8)
        if language == "Hindi":
            pdf.cell(0, 10, "नोट: यह एक स्क्रीनिंग उपकरण है। निदान के लिए एक स्वास्थ्य पेशेवर से परामर्श करें।", ln=True)
        else:
            pdf.cell(0, 10, "Note: This is a screening tool. Consult a healthcare professional for diagnosis.", ln=True)
        
        # fpdf2 returns bytes directly when using output()
        return pdf.output()
    except Exception as e:
        # Return a minimal error PDF if generation fails
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(0, 10, f"Error generating report: {str(e)}", ln=True)
            return pdf.output()
        except Exception:
            # If even error PDF fails, return empty bytes
            return b''

def get_whatsapp_link(name, score, label, language="English"):
    """
    Encodes message for WhatsApp API with language support.
    
    Args:
        name: Patient name
        score: Risk score
        label: Risk label
        language: Language for message ("English" or "Hindi")
    
    Returns:
        str: WhatsApp share link
    """
    if language == "Hindi":
        msg = f"नमस्ते {name},\nआपकी स्वास्थ्य जांच रिपोर्ट:\nजोखिम स्कोर: {score}/10\nस्थिति: {label}\nकृपया यदि जोखिम अधिक है तो डॉक्टर से परामर्श करें।"
    else:
        msg = f"Hello {name},\nYour Swasthya Health Checkup Report:\nRisk Score: {score}/10\nStatus: {label}\nPlease consult a doctor if Risk is High."
    return f"https://wa.me/?text={urllib.parse.quote(msg)}"

