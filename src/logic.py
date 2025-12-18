def calculate_scrs(age, bmi, sugar, sys_bp, dia_bp):
    """
    Swasthya Composite Risk Score (SCRS)
    Input: Vitals
    Output: Risk Score (0-10), Risk Level, Color
    Logic: Asian-Indian Standards
    """
    score = 0
    risk_factors = []
    
    # 1. BMI (Indian Standard: >23 is Overweight, >25 is Obese)
    if bmi >= 25:
        score += 3
        risk_factors.append("Obesity (Indian Std)")
    elif bmi >= 23:
        score += 2
        risk_factors.append("Overweight")
    
    # 2. Diabetes (ICMR Standard)
    if sugar > 126:
        score += 3
        risk_factors.append("Diabetic Range")
    elif sugar > 100:
        score += 1
        risk_factors.append("Prediabetic")
    
    # 3. Hypertension (AHA Standard)
    if sys_bp >= 140 or dia_bp >= 90:
        score += 3
        risk_factors.append("Hypertension")
    elif sys_bp >= 130 or dia_bp >= 80:
        score += 1
        risk_factors.append("Elevated BP")
    
    # 4. Age Synergy (Risk increases with age)
    if age > 45 and len(risk_factors) > 0:
        score += 1  # Bonus risk point for age + comorbidity
    
    # Result Interpretation
    if score == 0:
        return score, "Low Risk", "green", risk_factors
    elif score <= 4:
        return score, "Moderate Risk", "orange", risk_factors
    else:
        return score, "High Risk", "red", risk_factors


def detect_chronotype(bedtime, waketime):
    """
    Detects patient chronotype (sleep pattern) based on mid-sleep point.
    
    Args:
        bedtime: Bedtime hour (24-hour format, e.g., 22 for 10 PM)
        waketime: Wake time hour (24-hour format, e.g., 6 for 6 AM)
    
    Returns:
        str: Chronotype classification ("Early Bird", "Night Owl", or "Intermediate")
    """
    # Calculate mid-sleep point
    # Handle overnight sleep (e.g., 22:00 to 06:00)
    if bedtime > waketime:
        # Sleep spans midnight
        total_sleep_hours = (24 - bedtime) + waketime
        mid_sleep_hour = (bedtime + total_sleep_hours / 2) % 24
    else:
        # Normal same-day sleep
        total_sleep_hours = waketime - bedtime
        mid_sleep_hour = bedtime + total_sleep_hours / 2
    
    # Classify chronotype
    if mid_sleep_hour < 3.0:
        return "Early Bird (Lark)"
    elif mid_sleep_hour > 5.5:
        return "Night Owl"
    else:
        return "Intermediate"

def validate_inputs(age, weight, height, sugar, sys_bp, dia_bp):
    """
    Validates patient input parameters against clinical ranges.
    
    Args:
        age: Patient age in years
        weight: Patient weight in kilograms
        height: Patient height in centimeters
        sugar: Fasting blood sugar in mg/dL
        sys_bp: Systolic blood pressure in mmHg
        dia_bp: Diastolic blood pressure in mmHg
    
    Returns:
        List of error messages. Empty list if all inputs are valid.
    """
    errors = []
    
    # Age validation
    if not (0 < age < 120):
        errors.append(f"Invalid Age: {age}. Must be between 1 and 119 years.")
    
    # Weight validation
    if not (20 < weight < 200):
        errors.append(f"Invalid Weight: {weight} kg. Must be between 20 and 200 kg.")
    
    # Height validation
    if not (50 < height < 250):
        errors.append(f"Invalid Height: {height} cm. Must be between 50 and 250 cm.")
    
    # Blood sugar validation
    if not (50 < sugar < 500):
        errors.append(f"Invalid Blood Sugar: {sugar} mg/dL. Must be between 50 and 500 mg/dL.")
    
    # Blood pressure validation
    if not (50 <= sys_bp <= 250):
        errors.append(f"Invalid Systolic BP: {sys_bp} mmHg. Must be between 50 and 250 mmHg.")
    
    if not (30 <= dia_bp <= 150):
        errors.append(f"Invalid Diastolic BP: {dia_bp} mmHg. Must be between 30 and 150 mmHg.")
    
    # Logical validation: Systolic must be greater than Diastolic
    if sys_bp <= dia_bp:
        errors.append(f"Invalid BP: Systolic ({sys_bp}) must be greater than Diastolic ({dia_bp}).")
    
    return errors

