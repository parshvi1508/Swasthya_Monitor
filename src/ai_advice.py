"""
AI-powered health advice generation using Groq API (Llama-3).
"""

import os

def get_holistic_advice(name, age, condition, history_trend, medications="", language="English"):
    """
    Generates personalized health advice using Llama-3 via Groq API.
    
    Args:
        name: Patient name
        age: Patient age
        condition: Current health condition/risk level
        history_trend: "positive", "negative", or "stable"
        medications: Current medications (comma-separated)
        language: Language for response ("English" or "Hindi")
    
    Returns:
        str: AI-generated health advice in markdown format
    """
    try:
        import streamlit as st
        from groq import Groq
        
        # Get API key from secrets
        api_key = st.secrets.get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY"))
        
        if not api_key:
            return get_fallback_advice(condition, language)
        
        client = Groq(api_key=api_key)
        
        # Context building
        trend_msg = "Improving" if history_trend == "positive" else "Worsening" if history_trend == "negative" else "Stable"
        
        # Language-specific prompt
        if language == "Hindi":
            prompt = f"""
            आप एक वरिष्ठ भारतीय डॉक्टर के रूप में कार्य करें।
            
            रोगी: {name} ({age} वर्ष)
            वर्तमान स्थिति: {condition}
            प्रवृत्ति: {trend_msg}
            वर्तमान दवाएं: {medications if medications else 'कोई नहीं'}
            
            एक "संपूर्ण देखभाल योजना" मार्कडाउन में प्रदान करें:
            
            1. **आहार समायोजन**: खाने/बचने के लिए विशिष्ट भारतीय खाद्य पदार्थ
            2. **जीवनशैली सूक्ष्म आदत**: एक छोटा बदलाव (जैसे, 'रात के खाने के बाद 15 मिनट टहलें')
            3. **दवा नोट**: यदि दवाएं प्रदान की गई हैं, तो अनुपालन पर सलाह; अन्यथा, प्राकृतिक प्रबंधन
            
            इसे सख्त, छोटा (अधिकतम 150 शब्द), और सहानुभूतिपूर्ण रखें।
            """
        else:
            prompt = f"""
            Act as a senior Indian Doctor.
            
            Patient: {name} ({age} yrs).
            Current Condition: {condition}.
            Trend: {trend_msg}.
            Current Meds: {medications if medications else 'None'}.
            
            Provide a "Hybrid Care Plan" in markdown:
            
            1. **Dietary Adjustment**: Specific Indian foods to eat/avoid.
            2. **Lifestyle Micro-Habit**: One small change (e.g., 'Walk 15 mins after dinner').
            3. **Medication Note**: If meds provided, advice on compliance; else, natural management.
            
            Keep it strict, short (max 150 words), and empathetic.
            """
        
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
            temperature=0.7,
            max_tokens=300
        )
        
        return chat_completion.choices[0].message.content
    
    except Exception as e:
        # Fallback to standard advice if AI service fails
        return get_fallback_advice(condition, language)

def get_fallback_advice(condition, language="English"):
    """
    Provides fallback advice when AI service is unavailable.
    
    Args:
        condition: Patient's risk condition
        language: Language for response
    
    Returns:
        str: Standard health advice
    """
    if language == "Hindi":
        advice = """
        **मानक चिकित्सा सलाह:**
        
        1. **आहार**: कम नमक, कम शक्कर, संतुलित भोजन
        2. **व्यायाम**: प्रतिदिन 30 मिनट पैदल चलना
        3. **दवा**: निर्धारित दवाओं का नियमित सेवन करें
        4. **नियमित जांच**: स्वास्थ्य संबंधी नियमित जांच करवाते रहें
        
        कृपया एक योग्य स्वास्थ्य पेशेवर से परामर्श करें।
        """
    else:
        advice = """
        **Standard Medical Advice:**
        
        1. **Diet**: Low salt, low sugar, balanced meals
        2. **Exercise**: 30 minutes walk daily
        3. **Medication**: Take prescribed medications regularly
        4. **Regular Check-ups**: Maintain regular health screenings
        
        Please consult a qualified healthcare professional.
        """
    
    if "High" in condition or "Critical" in condition:
        if language == "Hindi":
            advice += "\n\n⚠️ **तत्काल चिकित्सक परामर्श की सलाह दी जाती है।**"
        else:
            advice += "\n\n⚠️ **Immediate doctor consultation is advised.**"
    
    return advice

