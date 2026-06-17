"""
Banking Operations Simulator — MODEL LAYER
===========================================
Real-time loan evaluation using the EXISTING trained model.
No new model is trained here.
"""
import os
import random
import numpy as np
import pandas as pd
import joblib

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_MODELS = os.path.join(_ROOT, "models")

FIRST_NAMES = ["Ahmed", "Sara", "Bilal", "Ayesha", "Usman", "Fatima", "Hassan",
               "Zainab", "Imran", "Hira", "Omar", "Mariam", "Ali", "Noor",
               "Tariq", "Aisha", "Kamran", "Saima", "Faisal", "Nadia"]
LAST_NAMES = ["Khan", "Malik", "Sheikh", "Butt", "Raza", "Iqbal", "Chaudhry",
              "Qureshi", "Hashmi", "Siddiqui", "Aslam", "Javed", "Rashid", "Akram"]


def load_model(model_name="Logistic Regression"):
    fmap = {"Logistic Regression": "logistic.pkl",
            "Decision Tree": "decisiontree.pkl",
            "Random Forest": "randomforest.pkl"}
    fname = fmap.get(model_name, "logistic.pkl")
    return {
        "model": joblib.load(os.path.join(_MODELS, fname)),
        "features": joblib.load(os.path.join(_MODELS, "features.pkl")),
        "scaler": joblib.load(os.path.join(_MODELS, "scaler.pkl")),
        "needs_scaling": model_name == "Logistic Regression",
    }


def generate_loan_applicant():
    age = random.randint(22, 62)
    income = int(np.random.lognormal(8.45, 0.5))
    credit_score = int(min(850, max(300, np.random.normal(685, 90))))
    loan_amount = int(income / 1000 * random.uniform(2.0, 4.0)) * 10
    return {
        "name": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
        "age": age,
        "income": income,
        "employment": random.choice(["Salaried", "Self-Employed", "Business Owner"]),
        "credit_score": credit_score,
        "existing_loans": random.choice([0, 0, 1, 1, 2, 3]),
        "loan_amount": max(loan_amount, 30),
        "education": random.choice(["Graduate", "Not Graduate"]),
        "married": random.choice(["Yes", "No"]),
        "dependents": random.choice([0, 1, 2, 3]),
        "gender": random.choice(["Male", "Female"]),
        "property_area": random.choice(["Urban", "Semiurban", "Rural"]),
        "variant": random.randint(0, 5),
    }


def generate_cashier_customer():
    return {
        "name": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
        "service": random.choice(["Deposit", "Withdrawal", "Bill Payment",
                                  "Cheque Cashing", "Balance Inquiry", "Transfer"]),
        "service_time": random.uniform(2.0, 6.0),
        "variant": random.randint(0, 5),
    }


def _to_features(app, features):
    credit_history = 1.0 if app["credit_score"] >= 620 else 0.0
    row = {
        "Gender": 1 if app["gender"] == "Male" else 0,
        "Married": 1 if app["married"] == "Yes" else 0,
        "Dependents": app["dependents"],
        "Education": 1 if app["education"] == "Graduate" else 0,
        "Self_Employed": 1 if app["employment"] != "Salaried" else 0,
        "Credit_History": credit_history,
        "Property_Area": {"Urban": 2, "Semiurban": 1, "Rural": 0}[app["property_area"]],
        "Total_Income_log": np.log1p(app["income"]),
        "LoanAmount_log": np.log1p(app["loan_amount"]),
        "Income_Loan_Ratio": app["income"] / (app["loan_amount"] + 1),
    }
    return pd.DataFrame([[row[f] for f in features]], columns=features)


def evaluate_loan(bundle, app):
    """Run the existing trained model. Returns decision, probability, risk score, reason."""
    X = _to_features(app, bundle["features"])
    Xin = bundle["scaler"].transform(X) if bundle["needs_scaling"] else X
    try:
        proba = float(bundle["model"].predict_proba(Xin)[0][1])
    except Exception:
        proba = float(bundle["model"].predict(Xin)[0])
    decision = "APPROVED" if proba >= 0.5 else "REJECTED"
    risk_score = round((1 - proba) * 100, 1)
    if decision == "APPROVED":
        reason = ("Excellent credit profile" if app["credit_score"] >= 750
                  else "Acceptable creditworthiness")
    else:
        if app["credit_score"] < 620:
            reason = "Low credit score"
        elif app["existing_loans"] >= 2:
            reason = "High existing debt"
        elif app["income"] / (app["loan_amount"] + 1) < 1.5:
            reason = "Insufficient income"
        else:
            reason = "Risk threshold exceeded"
    return {
        "decision": decision,
        "probability": round(proba, 3),
        "risk_score": risk_score,
        "reason": reason,
    }


def prepare_day(bundle, day_num, loan_count, cashier_count):
    """Pre-compute all applicants & decisions for one day."""
    loan_apps = []
    for i in range(loan_count):
        a = generate_loan_applicant()
        r = evaluate_loan(bundle, a)
        a.update(r)
        a["arrival_min"] = round(10 + i * (420 / max(loan_count, 1)) + random.uniform(-5, 5), 1)
        a["service_time"] = round(random.uniform(4.0, 8.0), 1)
        a["id"] = f"L{day_num:02d}{i+1:03d}"
        loan_apps.append(a)

    cashier_custs = []
    for i in range(cashier_count):
        c = generate_cashier_customer()
        c["arrival_min"] = round(5 + i * (450 / max(cashier_count, 1)) + random.uniform(-3, 3), 1)
        c["id"] = f"C{day_num:02d}{i+1:03d}"
        cashier_custs.append(c)

    return {"day": day_num, "loan_apps": loan_apps, "cashier_custs": cashier_custs}
