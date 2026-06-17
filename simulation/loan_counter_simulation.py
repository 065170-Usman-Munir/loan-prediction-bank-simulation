"""
Loan Application Counter Simulation (SimPy)
============================================
Simulates customers arriving at a dedicated Loan Application Counter inside an
AI-powered banking system. Each customer's data is passed to the EXISTING trained
loan-approval model (logistic.pkl / decisiontree.pkl / randomforest.pkl) — no new
model is created or trained here.

Modes : Daily / Weekly / Monthly / Yearly
Speed  : handled by the dashboard (this module fast-forwards instantly and returns
         full logs; the Streamlit page replays the event_log at the chosen speed).

File: simulation/loan_counter_simulation.py
"""
import os
import random
import numpy as np
import pandas as pd
import joblib
import simpy

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(ROOT, "models")

# ----------------------------------------------------------------------
# Load the EXISTING trained model (do NOT train anything new)
# ----------------------------------------------------------------------
def load_existing_model(model_name="Logistic Regression"):
    fname = {"Logistic Regression": "logistic.pkl",
             "Decision Tree": "decisiontree.pkl",
             "Random Forest": "randomforest.pkl"}.get(model_name, "logistic.pkl")
    model = joblib.load(os.path.join(MODELS_DIR, fname))
    features = joblib.load(os.path.join(MODELS_DIR, "features.pkl"))
    scaler = joblib.load(os.path.join(MODELS_DIR, "scaler.pkl"))
    needs_scaling = (model_name == "Logistic Regression")
    return model, features, scaler, needs_scaling


# ----------------------------------------------------------------------
# Generate ONE realistic customer (raw, human-readable values)
# ----------------------------------------------------------------------
def generate_customer():
    age = random.randint(21, 65)
    income = int(np.random.lognormal(8.45, 0.55))            # monthly applicant income
    coapplicant = random.choice([0, int(np.random.lognormal(7.0, 1.2))])
    employment = random.choice(["Salaried", "Self-Employed"])
    # FICO-style score: most applicants have fair-to-good credit (skewed high)
    credit_score = int(min(850, max(300, np.random.normal(690, 85))))
    existing_debt = int(income * random.uniform(0, 3))
    loan_amount = int((income + coapplicant) / 1000 * random.uniform(1.8, 3.2))
    return {
        "age": age,
        "income": income,
        "coapplicant_income": coapplicant,
        "employment": employment,
        "credit_score": credit_score,
        "existing_debt": existing_debt,
        "loan_amount": max(loan_amount, 10),
        "education": random.choice(["Graduate", "Not Graduate"]),
        "married": random.choice(["Yes", "No"]),
        "dependents": random.choice([0, 1, 2, 3]),
        "gender": random.choice(["Male", "Female"]),
        "property_area": random.choice(["Urban", "Semiurban", "Rural"]),
    }


# ----------------------------------------------------------------------
# Convert a generated customer into the EXACT feature vector the model needs
# ----------------------------------------------------------------------
def customer_to_features(cust, features):
    # credit_score (300-850) -> Credit_History (1 good / 0 bad); >=620 considered good
    credit_history = 1.0 if cust["credit_score"] >= 620 else 0.0
    total_income = cust["income"] + cust["coapplicant_income"]
    row = {
        "Gender": 1 if cust["gender"] == "Male" else 0,
        "Married": 1 if cust["married"] == "Yes" else 0,
        "Dependents": cust["dependents"],
        "Education": 1 if cust["education"] == "Graduate" else 0,
        "Self_Employed": 1 if cust["employment"] == "Self-Employed" else 0,
        "Credit_History": credit_history,
        "Property_Area": {"Urban": 2, "Semiurban": 1, "Rural": 0}[cust["property_area"]],
        "Total_Income_log": np.log1p(total_income),
        "LoanAmount_log": np.log1p(cust["loan_amount"]),
        "Income_Loan_Ratio": total_income / (cust["loan_amount"] + 1),
    }
    return pd.DataFrame([[row[f] for f in features]], columns=features)


def predict_existing(model, features, scaler, needs_scaling, cust):
    X = customer_to_features(cust, features)
    if needs_scaling:
        X = scaler.transform(X)
    pred = model.predict(X)[0]
    return "APPROVED" if int(pred) == 1 else "REJECTED"


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------
def _fmt_clock(day, minutes_from_open):
    """Bank opens 09:00. Convert minutes-from-open into a Day N HH:MM string."""
    total = 9 * 60 + int(minutes_from_open)
    hh, mm = divmod(total, 60)
    hh = min(hh, 23)
    return f"Day {day} {hh:02d}:{mm:02d}"


MODE_DAYS = {"Daily": 1, "Weekly": 7, "Monthly": 30, "Yearly": 365}


# ----------------------------------------------------------------------
# Core SimPy simulation for a SINGLE day
# ----------------------------------------------------------------------
def _simulate_one_day(day, n_officers, processing_time, model_bundle,
                      event_log, queue_log, stats, day_open_minutes=480):
    """Runs one bank-day. 1-10 customers arrive. Appends to shared logs/stats."""
    model, features, scaler, needs_scaling = model_bundle
    env = simpy.Environment()
    officers = simpy.Resource(env, capacity=n_officers)
    n_customers = random.randint(1, 10)        # realistic: 1-10 per day

    # spread arrivals across the working day
    arrival_offsets = sorted(random.uniform(0, day_open_minutes - 30)
                             for _ in range(n_customers))

    def customer_proc(cid, arrive_at):
        yield env.timeout(arrive_at)
        cust = generate_customer()
        stats["arrived"] += 1
        event_log.append((_fmt_clock(day, env.now),
                          f"Customer {cid:03d} entered bank"))
        # join queue
        queue_log.append((day, env.now, len(officers.queue)))
        event_log.append((_fmt_clock(day, env.now),
                          f"Customer {cid:03d} joined loan queue"))
        t_join = env.now
        with officers.request() as req:
            yield req
            wait = env.now - t_join
            stats["wait_times"].append(wait)
            officer_id = random.randint(1, n_officers)
            event_log.append((_fmt_clock(day, env.now),
                              f"Customer {cid:03d} assigned to Loan Officer {officer_id}"))
            # processing time (exponential around the mean)
            yield env.timeout(random.expovariate(1.0 / processing_time))
            # === call the EXISTING model ===
            result = predict_existing(model, features, scaler, needs_scaling, cust)
            if result == "APPROVED":
                stats["approved"] += 1
            else:
                stats["rejected"] += 1
            stats["processed"] += 1
            event_log.append((_fmt_clock(day, env.now),
                              f"AI Prediction: {result}"))
            event_log.append((_fmt_clock(day, env.now),
                              f"Customer {cid:03d} exited bank"))
            stats["requests_per_day"].setdefault(day, 0)
            stats["requests_per_day"][day] += 1

    base = stats["customer_counter"]
    for i, off in enumerate(arrival_offsets):
        env.process(customer_proc(base + i + 1, off))
    stats["customer_counter"] += n_customers
    env.run()


# ----------------------------------------------------------------------
# Public entry point
# ----------------------------------------------------------------------
def run_loan_counter(mode="Daily", n_officers=2, processing_time=8.0,
                     model_name="Logistic Regression", seed=42):
    """
    Simulate the Loan Application Counter over the chosen period.
    Returns a dictionary of full results + logs (the dashboard handles speed/replay).
    """
    random.seed(seed)
    np.random.seed(seed)
    model_bundle = load_existing_model(model_name)

    days = MODE_DAYS.get(mode, 1)
    event_log, queue_log = [], []
    stats = {"arrived": 0, "processed": 0, "approved": 0, "rejected": 0,
             "wait_times": [], "requests_per_day": {}, "customer_counter": 0}

    for day in range(1, days + 1):
        _simulate_one_day(day, n_officers, processing_time, model_bundle,
                          event_log, queue_log, stats)

    total = stats["processed"]
    approval_rate = round(stats["approved"] / total * 100, 1) if total else 0.0
    rejection_rate = round(stats["rejected"] / total * 100, 1) if total else 0.0
    waits = stats["wait_times"]
    avg_q = round(np.mean([q for _, _, q in queue_log]), 2) if queue_log else 0.0

    return {
        "simulation_period": mode,
        "total_customers": stats["arrived"],
        "total_requests": total,
        "approved_loans": stats["approved"],
        "rejected_loans": stats["rejected"],
        "approval_rate": approval_rate,
        "rejection_rate": rejection_rate,
        "average_waiting_time": round(np.mean(waits), 2) if waits else 0.0,
        "max_waiting_time": round(np.max(waits), 2) if waits else 0.0,
        "average_queue_length": avg_q,
        "queue_log": queue_log,            # list of (day, minute, queue_len)
        "event_log": event_log,            # list of (clock_str, message)
        "requests_per_day": stats["requests_per_day"],
        "wait_times": waits,
        "n_officers": n_officers,
    }


# ----------------------------------------------------------------------
# CLI test
# ----------------------------------------------------------------------
if __name__ == "__main__":
    for m in ["Daily", "Weekly", "Monthly", "Yearly"]:
        r = run_loan_counter(mode=m, n_officers=2, processing_time=8.0)
        print(f"\n=== {m} ===")
        print(f"Customers: {r['total_customers']} | Processed: {r['total_requests']} | "
              f"Approved: {r['approved_loans']} ({r['approval_rate']}%) | "
              f"Rejected: {r['rejected_loans']} ({r['rejection_rate']}%)")
        print(f"Avg wait: {r['average_waiting_time']} min | Max wait: {r['max_waiting_time']} min | "
              f"Avg queue: {r['average_queue_length']}")
        print(f"Event log entries: {len(r['event_log'])}")
