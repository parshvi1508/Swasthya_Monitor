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
            advice_text = str(data.get('advice', ''))
            # Remove markdown, emojis, and special characters
            advice_clean = advice_text.replace('**', '').replace('#', '').replace('*', '')
            advice_clean = advice_clean.replace('🤖', '').replace('📋', '').replace('AI-Generated Advice', 'AI Advice')
            advice_clean = advice_clean.strip()
            
            # Encode to latin-1, removing unsupported characters
            advice_clean = advice_clean.encode('latin-1', 'ignore').decode('latin-1')
            
            # Split into lines and add
            for line in advice_clean.split('\n'):
                line_clean = line.strip()
                if line_clean and len(line_clean) > 2:
                    # Break long lines
                    if len(line_clean) > 80:
                        words = line_clean.split()
                        current_line = ''
                        for word in words:
                            if len(current_line + word) < 80:
                                current_line += word + ' '
                            else:
                                if current_line:
                                    pdf.cell(0, 6, current_line.strip(), ln=True)
                                current_line = word + ' '
                        if current_line:
                            pdf.cell(0, 6, current_line.strip(), ln=True)
                    else:
                        pdf.cell(0, 6, line_clean, ln=True)
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
        disclaimer = "Note: This is a screening tool. Consult a healthcare professional for diagnosis."
        pdf.multi_cell(0, 5, disclaimer)
        
        # Return PDF as bytes - try both methods for compatibility
        try:
            # For fpdf2 v2.7+
            pdf_output = pdf.output(dest='S')
            if isinstance(pdf_output, bytes):
                return pdf_output
            elif isinstance(pdf_output, str):
                return pdf_output.encode('latin-1')
            else:
                return bytes(pdf_output)
        except TypeError:
            # For older fpdf2 versions
            return pdf.output()
            
    except Exception as e:
        # Return a minimal error PDF if generation fails
        print(f"PDF Generation Error: {str(e)}")
        try:
            error_pdf = FPDF()
            error_pdf.add_page()
            error_pdf.set_font("Arial", size=12)
            error_pdf.cell(0, 10, "Error generating report. Please try again.", ln=True)
            error_pdf.cell(0, 10, f"Error: {str(e)[:50]}", ln=True)
            try:
                return error_pdf.output(dest='S') if hasattr(error_pdf.output, '__call__') else error_pdf.output()
            except:
                return error_pdf.output()
        except Exception:
            # If even error PDF fails, return None to trigger proper error handling
            return None

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

