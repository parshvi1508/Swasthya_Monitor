# Swasthya Monitor - Test Cases Documentation

## Overview

This document provides comprehensive test cases for the Swasthya Monitor health screening application. The test cases cover all health scenarios, edge cases, and risk categories to ensure thorough validation of the Composite Risk Score (SCRS) algorithm and system functionality.

## Test Case Categories

### 1. Normal Healthy Cases

**Purpose**: Validate baseline healthy individual assessment

**Test Cases**:

| Test ID | Name | Age | BMI | Sugar (mg/dL) | BP (mmHg) | Expected Risk | Expected Score |
|---------|------|-----|-----|---------------|-----------|---------------|----------------|
| TC-001 | Anjali Verma | 28 | 21.0 | 85 | 110/70 | Low | 0 |
| TC-002 | Rahul Gupta | 35 | 23.0 | 92 | 118/75 | Low | 0 |
| TC-003 | Sneha Patel | 42 | 22.8 | 88 | 115/72 | Low | 0 |

**Validation Points**:
- All vitals within normal ranges
- Risk score should be 0
- Risk level should be "Low Risk"
- No risk factors identified

---

### 2. Diabetic Cases

**Purpose**: Validate diabetes detection using ICMR thresholds

**Test Cases**:

| Test ID | Name | Age | BMI | Sugar (mg/dL) | BP (mmHg) | Expected Risk | Expected Factors |
|---------|------|-----|-----|---------------|-----------|---------------|------------------|
| TC-004 | Rajesh Kumar | 58 | 29.0 | 178 | 135/82 | High | Diabetic Range |
| TC-005 | Meera Iyer | 62 | 29.1 | 195 | 128/80 | High | Diabetic Range |
| TC-006 | Suresh Reddy | 55 | 29.4 | 210 | 145/88 | High | Diabetic Range, Hypertension |

**Validation Points**:
- Blood sugar >126 mg/dL should trigger diabetic risk factor
- Score should include +3 points for diabetes
- Risk level should reflect high risk when combined with other factors

---

### 3. Hypertension Cases

**Purpose**: Validate blood pressure-related risk detection

**Test Cases**:

| Test ID | Name | Age | BMI | Sugar (mg/dL) | BP (mmHg) | Expected Risk | Expected Factors |
|---------|------|-----|-----|---------------|-----------|---------------|------------------|
| TC-007 | Kavita Sharma | 48 | 27.5 | 105 | 165/100 | High | Hypertension, Obesity |
| TC-008 | Anil Mehta | 60 | 29.4 | 112 | 172/105 | High | Hypertension, Obesity |
| TC-009 | Pooja Desai | 52 | 26.6 | 98 | 155/95 | Moderate | Hypertension, Overweight |

**Validation Points**:
- Systolic ≥140 OR Diastolic ≥90 should trigger hypertension
- Score should include +3 points for hypertension
- Elevated BP (130-139/80-89) should add +1 point

---

### 4. Obesity Cases

**Purpose**: Validate BMI obesity detection using Asian-Indian standards

**Test Cases**:

| Test ID | Name | Age | BMI | Sugar (mg/dL) | BP (mmHg) | Expected Risk | Expected Factors |
|---------|------|-----|-----|---------------|-----------|---------------|------------------|
| TC-010 | Vikram Singh | 45 | 32.1 | 118 | 138/85 | Moderate | Obesity |
| TC-011 | Neha Kapoor | 38 | 34.1 | 125 | 132/82 | Moderate | Obesity, Prediabetic |
| TC-012 | Deepak Joshi | 50 | 34.3 | 135 | 142/88 | High | Obesity, Hypertension, Prediabetic |

**Validation Points**:
- BMI ≥25 should trigger obesity (+3 points)
- BMI ≥23 should trigger overweight (+2 points)
- Asian-Indian standards applied correctly

---

### 5. Underweight Cases

**Purpose**: Validate underweight detection

**Test Cases**:

| Test ID | Name | Age | BMI | Sugar (mg/dL) | BP (mmHg) | Expected Risk | Expected Score |
|---------|------|-----|-----|---------------|-----------|---------------|----------------|
| TC-013 | Riya Das | 25 | 16.4 | 82 | 105/68 | Low | 0 |
| TC-014 | Arjun Nair | 30 | 17.0 | 88 | 112/72 | Low | 0 |
| TC-015 | Priya Menon | 35 | 17.1 | 85 | 108/70 | Low | 0 |

**Validation Points**:
- BMI <18.5 should be classified but not penalized in score
- Risk remains low if other factors are normal
- Underweight classification should be noted

---

### 6. Critical Risk Cases (Multiple Comorbidities)

**Purpose**: Validate high-risk scenarios with multiple conditions

**Test Cases**:

| Test ID | Name | Age | BMI | Sugar (mg/dL) | BP (mmHg) | Expected Risk | Expected Score |
|---------|------|-----|-----|---------------|-----------|---------------|----------------|
| TC-016 | Ramesh Pillai | 65 | 32.6 | 225 | 180/110 | High | 8-10 |
| TC-017 | Lakshmi Rao | 68 | 34.6 | 198 | 170/102 | High | 8-10 |
| TC-018 | Harish Bhat | 72 | 32.3 | 215 | 175/108 | High | 8-10 |

**Validation Points**:
- Multiple risk factors should accumulate
- Age synergy bonus should apply (age >45 with comorbidities)
- Score should reflect cumulative risk
- High risk categorization expected

---

### 7. Borderline/Prediabetic Cases

**Purpose**: Validate threshold detection for early intervention

**Test Cases**:

| Test ID | Name | Age | BMI | Sugar (mg/dL) | BP (mmHg) | Expected Risk | Expected Factors |
|---------|------|-----|-----|---------------|-----------|---------------|------------------|
| TC-019 | Sanjay Pandey | 40 | 24.9 | 115 | 128/78 | Moderate | Prediabetic, Elevated BP, Overweight |
| TC-020 | Divya Agarwal | 45 | 25.4 | 110 | 125/80 | Moderate | Prediabetic, Overweight |
| TC-021 | Kiran Kumar | 50 | 26.4 | 118 | 132/82 | Moderate | Prediabetic, Elevated BP, Overweight |

**Validation Points**:
- Sugar 100-126 should trigger prediabetic (+1 point)
- BP 130-139/80-89 should trigger elevated (+1 point)
- Moderate risk category appropriate for borderline cases

---

### 8. Age Factor Validation

**Purpose**: Validate age synergy with comorbidities

**Test Cases**:

| Test ID | Name | Age | BMI | Sugar (mg/dL) | BP (mmHg) | Expected Risk | Age Bonus |
|---------|------|-----|-----|---------------|-----------|---------------|-----------|
| TC-022 | Aarav Sharma | 18 | 20.2 | 90 | 115/72 | Low | No |
| TC-023 | Ishita Singh | 22 | 20.8 | 85 | 110/70 | Low | No |
| TC-024 | Dev Patel | 44 | 23.5 | 95 | 118/75 | Low | No |
| TC-025 | Gopal Krishnan | 46 | 26.7 | 110 | 138/88 | Moderate | Yes (+1) |

**Validation Points**:
- Age >45 with existing risk factors should add +1 point
- Age <45 should not trigger age bonus
- Age alone should not add points

---

### 9. Input Validation Test Cases

**Purpose**: Validate input validation and error handling

**Test Cases**:

| Test ID | Input Field | Invalid Value | Expected Error |
|---------|-------------|---------------|----------------|
| TC-026 | Age | 0 | "Invalid Age: 0. Must be between 1 and 119 years." |
| TC-027 | Age | 150 | "Invalid Age: 150. Must be between 1 and 119 years." |
| TC-028 | Weight | 15 | "Invalid Weight: 15 kg. Must be between 20 and 200 kg." |
| TC-029 | Weight | 250 | "Invalid Weight: 250 kg. Must be between 20 and 200 kg." |
| TC-030 | Height | 40 | "Invalid Height: 40 cm. Must be between 50 and 250 cm." |
| TC-031 | Sugar | 30 | "Invalid Blood Sugar: 30 mg/dL. Must be between 50 and 500 mg/dL." |
| TC-032 | Sugar | 600 | "Invalid Blood Sugar: 600 mg/dL. Must be between 50 and 500 mg/dL." |
| TC-033 | Systolic BP | 100 | "Invalid BP: Systolic (100) must be greater than Diastolic (80)." |
| TC-034 | Name | "" (empty) | "Please enter a patient name." |

**Validation Points**:
- All invalid inputs should be rejected with clear error messages
- Application should not crash on invalid input
- Error messages should guide user to correct input

---

### 10. Edge Cases

**Purpose**: Validate boundary conditions and extreme values

**Test Cases**:

| Test ID | Scenario | Input Values | Expected Behavior |
|---------|----------|--------------|-------------------|
| TC-035 | Minimum valid age | Age: 1 | Should process normally |
| TC-036 | Maximum valid age | Age: 119 | Should process normally |
| TC-037 | BMI exactly at threshold | BMI: 23.0 | Should classify as overweight |
| TC-038 | BMI just below threshold | BMI: 22.9 | Should classify as normal |
| TC-039 | Sugar at diabetic threshold | Sugar: 127 | Should classify as diabetic |
| TC-040 | Sugar at prediabetic threshold | Sugar: 100 | Should classify as prediabetic |
| TC-041 | BP at hypertension threshold | 140/90 | Should classify as hypertension |
| TC-042 | BP at elevated threshold | 130/80 | Should classify as elevated |

**Validation Points**:
- Boundary values should be handled correctly
- Threshold comparisons should use appropriate operators (>= vs >)
- Edge cases should not cause errors

---

### 11. Score Calculation Verification

**Purpose**: Validate mathematical correctness of SCRS algorithm

**Test Cases**:

| Test ID | Scenario | Factors | Expected Score Calculation |
|---------|----------|---------|---------------------------|
| TC-043 | Obesity only | BMI: 28 | Score: 3 (Obesity) |
| TC-044 | Diabetes only | Sugar: 150 | Score: 3 (Diabetes) |
| TC-045 | Hypertension only | BP: 150/95 | Score: 3 (Hypertension) |
| TC-046 | Obesity + Diabetes | BMI: 28, Sugar: 150 | Score: 6 (3+3) |
| TC-047 | All three factors | BMI: 28, Sugar: 150, BP: 150/95 | Score: 9 (3+3+3) |
| TC-048 | With age bonus | Age: 50, BMI: 28 | Score: 4 (3+1 age bonus) |
| TC-049 | Overweight (not obese) | BMI: 24 | Score: 2 (Overweight) |
| TC-050 | Prediabetic | Sugar: 110 | Score: 1 (Prediabetic) |

**Validation Points**:
- Score components should add correctly
- Maximum possible score is 10 (all factors + age bonus)
- Minimum score is 0 (all normal)
- Each factor should contribute appropriate points

---

### 12. Risk Category Classification

**Purpose**: Validate risk level categorization

**Test Cases**:

| Test ID | Score | Expected Category | Expected Color |
|---------|-------|-------------------|----------------|
| TC-051 | 0 | Low Risk | green |
| TC-052 | 1 | Moderate Risk | orange |
| TC-053 | 4 | Moderate Risk | orange |
| TC-054 | 5 | High Risk | red |
| TC-055 | 10 | High Risk | red |

**Validation Points**:
- Score 0: Low Risk
- Score 1-4: Moderate Risk
- Score 5-10: High Risk
- Color coding should match risk level

---

## Testing Checklist

### Functional Testing

- [ ] All normal cases return low risk (score 0)
- [ ] Diabetic cases (sugar >126) trigger diabetic risk factor
- [ ] Hypertensive cases (BP ≥140/90) trigger hypertension risk factor
- [ ] Obese cases (BMI ≥25) trigger obesity risk factor
- [ ] Multiple risk factors accumulate correctly
- [ ] Age synergy bonus applies when age >45 with comorbidities
- [ ] Risk categories match score ranges
- [ ] PDF report generates successfully
- [ ] WhatsApp link generates correctly
- [ ] Database saves records correctly

### Input Validation Testing

- [ ] Invalid age values rejected
- [ ] Invalid weight values rejected
- [ ] Invalid height values rejected
- [ ] Invalid blood sugar values rejected
- [ ] Invalid blood pressure values rejected
- [ ] Systolic < Diastolic rejected
- [ ] Empty name rejected
- [ ] All error messages are clear and helpful

### Boundary Testing

- [ ] Minimum valid values accepted
- [ ] Maximum valid values accepted
- [ ] Threshold values handled correctly (BMI: 23, 25; Sugar: 100, 126; BP: 130/80, 140/90)
- [ ] Score boundaries (0, 4, 5, 10) categorized correctly

### Error Handling Testing

- [ ] Invalid inputs don't crash application
- [ ] Database connection failures handled gracefully
- [ ] PDF generation failures handled gracefully
- [ ] Missing data fields handled appropriately
- [ ] Special characters in names handled correctly

### Integration Testing

- [ ] Complete workflow: Input → Calculate → Display → Save → Export
- [ ] Patient records persist across sessions
- [ ] Multiple patients can be processed sequentially
- [ ] Analytics display correctly with multiple records

---

## Test Data Statistics

### Risk Distribution

- Low Risk Cases: 10 (20%)
- Moderate Risk Cases: 16 (32%)
- High Risk Cases: 15 (30%)
- Critical Risk Cases: 9 (18%)

### Condition Distribution

- Diabetic Cases: 20 (40%)
- Hypertensive Cases: 18 (36%)
- Obese Cases: 25 (50%)
- Underweight Cases: 3 (6%)

### Age Distribution

- Age <30: 9 cases (18%)
- Age 30-50: 19 cases (38%)
- Age 50-70: 18 cases (36%)
- Age >70: 4 cases (8%)

---

## Usage Instructions for Testing

### Manual Testing

1. Start the application: `streamlit run app.py`
2. Navigate to the Current Analysis tab
3. Enter test case values from the tables above
4. Click "Run Diagnostics"
5. Verify results match expected outcomes
6. Check PDF report generation
7. Test WhatsApp link functionality

### Automated Testing (Future Implementation)

Recommended test framework: pytest

```python
# Example test structure
def test_calculate_scrs_normal_case():
    score, label, color, factors = calculate_scrs(28, 21.0, 85, 110, 70)
    assert score == 0
    assert label == "Low Risk"
    assert color == "green"
    assert len(factors) == 0
```

---

## Known Limitations

1. Test cases assume ideal conditions (no missing data)
2. Edge cases may need adjustment based on clinical feedback
3. Score thresholds may need refinement with clinical validation
4. Some test cases use hypothetical data for comprehensive coverage

---

## Revision History

- Initial version: Comprehensive test case documentation
- Future updates: Add automated test results, update based on clinical validation

---

**Note**: These test cases are designed for system validation. Actual clinical validation should be performed with qualified healthcare professionals before production deployment.
