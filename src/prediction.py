"""
Prediction module using Linear Regression to forecast patient health trends.
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

def predict_trends(history_df):
    """
    Predicts next visit values based on past visits using Linear Regression.
    
    Input: DataFrame of patient history with columns: Date, Sugar, BP (or Systolic_BP, Diastolic_BP)
    Output: Dictionary of predictions {'Sugar': value, 'BP': value} or None if insufficient data
    
    Args:
        history_df: pandas.DataFrame with patient historical data
    
    Returns:
        dict: Dictionary with predicted values, or None if insufficient data
    """
    if history_df is None or len(history_df) < 2:
        return None  # Need at least 2 points to draw a line
    
    # Ensure DataFrame is sorted by date
    if 'Date' in history_df.columns:
        history_df = history_df.sort_values('Date')
    else:
        # If no Date column, assume chronological order
        history_df = history_df.reset_index(drop=True)
    
    # Prepare Data (X = Visit Number, y = Value)
    X = np.arange(len(history_df)).reshape(-1, 1)
    
    # Next Visit Index
    next_X = np.array([[len(history_df)]])
    
    predictions = {}
    
    try:
        # Predict Sugar
        if 'Sugar' in history_df.columns:
            model = LinearRegression()
            sugar_values = pd.to_numeric(history_df['Sugar'], errors='coerce').dropna()
            if len(sugar_values) >= 2:
                X_sugar = np.arange(len(sugar_values)).reshape(-1, 1)
                model.fit(X_sugar, sugar_values.values)
                pred_sugar = model.predict(next_X)[0]
                predictions['Sugar'] = max(50, min(500, int(pred_sugar)))  # Clamp to valid range
        
        # Predict Blood Pressure
        # Try different column name formats
        bp_columns = ['Systolic_BP', 'sys_bp', 'BP']
        sys_bp_col = None
        dia_bp_col = None
        
        for col in history_df.columns:
            if 'sys' in col.lower() or 'systolic' in col.lower():
                sys_bp_col = col
            if 'dia' in col.lower() or 'diastolic' in col.lower():
                dia_bp_col = col
        
        # If BP is stored as "140/90" format
        if 'BP' in history_df.columns and sys_bp_col is None:
            # Extract systolic values
            bp_values = history_df['BP'].apply(lambda x: int(str(x).split('/')[0]) if '/' in str(x) else None)
            bp_values = bp_values.dropna()
            if len(bp_values) >= 2:
                X_bp = np.arange(len(bp_values)).reshape(-1, 1)
                model = LinearRegression()
                model.fit(X_bp, bp_values.values)
                pred_sys = model.predict(next_X)[0]
                predictions['Systolic_BP'] = max(90, min(250, int(pred_sys)))
        
        elif sys_bp_col:
            sys_bp_values = pd.to_numeric(history_df[sys_bp_col], errors='coerce').dropna()
            if len(sys_bp_values) >= 2:
                X_bp = np.arange(len(sys_bp_values)).reshape(-1, 1)
                model = LinearRegression()
                model.fit(X_bp, sys_bp_values.values)
                pred_sys = model.predict(next_X)[0]
                predictions['Systolic_BP'] = max(90, min(250, int(pred_sys)))
        
    except Exception as e:
        # If prediction fails, return None
        return None
    
    return predictions if predictions else None

def calculate_followup_date(risk_score, days_offset=30):
    """
    Calculate recommended follow-up date based on risk score.
    
    Args:
        risk_score: Patient's composite risk score (0-10)
        days_offset: Default days until follow-up (default: 30)
    
    Returns:
        datetime: Recommended follow-up date, or None if not needed
    """
    if risk_score > 6:
        return datetime.now() + timedelta(days=days_offset)
    return None

