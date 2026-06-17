"""
Meezan Bank — AI Loan & Operations Dashboard
=============================================
3 attractive pages: Overview, Dataset Analysis, Loan Counter Simulation.
Focus is on the AI-powered loan simulation. Uses the EXISTING trained ML model only.
Run:  streamlit run dashboard/app.py
"""
import os, json, joblib, sys
import numpy as np, pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from banking_simulator import build_banking_simulator, aggregate_stats
from banking_simulator import ml_engine

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOTS = os.path.join(ROOT, "screenshots")
sns.set_style("whitegrid")

st.set_page_config(page_title="Meezan Bank — AI Loan System",
                   page_icon="🏦", layout="wide")

# ============================================================
# GLOBAL STYLES (attractive design across pages)
# ============================================================
st.markdown("""
<style>
.stApp{background:linear-gradient(180deg,#f4f7fb 0%,#e8eef9 100%);}
.block-container{padding-top:1.4rem;padding-bottom:2rem;max-width:1380px;}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#003d2b,#005a3f);}
[data-testid="stSidebar"] *{color:#e8eef9 !important;}
[data-testid="stSidebar"] label, [data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2, [data-testid="stSidebar"] .stRadio label{color:#fff !important;}
[data-testid="stSidebar"] .stRadio>div>label{padding:9px 12px;border-radius:8px;margin:3px 0;
  background:#ffffff14;transition:.15s;}
[data-testid="stSidebar"] .stRadio>div>label:hover{background:#ffffff28;}
[data-testid="stSidebar"] .stRadio>div>label[data-checked="true"]{background:#00b894;color:#fff !important;}
.mz-hero{background:linear-gradient(135deg,#003d2b 0%,#005a3f 60%,#00805a 100%);color:#fff;
  padding:24px 28px;border-radius:16px;margin-bottom:18px;box-shadow:0 12px 30px #0a1f4a25;
  border:1px solid #1e4cb830;position:relative;overflow:hidden;}
.mz-hero:before{content:"";position:absolute;top:-30px;right:-30px;width:200px;height:200px;
  background:radial-gradient(circle,#fcc94a33,transparent 70%);}
.mz-hero h1{margin:0;font-size:26px;font-weight:800;letter-spacing:.4px;}
.mz-hero p{margin:8px 0 0;color:#a8c2f0;font-size:14px;}
.mz-badge{display:inline-block;background:#fcc94a;color:#003d2b;padding:3px 11px;border-radius:5px;
  font-weight:800;font-size:11px;letter-spacing:1.2px;margin-right:6px;}
.mz-badge.live{background:#27ae60;color:#fff;}
.mz-badge.ml{background:#e74c3c;color:#fff;}
.mz-card{background:#fff;padding:18px 20px;border-radius:13px;border:1px solid #dde7f5;
  box-shadow:0 4px 12px #0a1f4a0d;margin-bottom:14px;}
.mz-card h3{margin:0 0 10px;color:#003d2b;font-size:16px;font-weight:800;letter-spacing:.3px;}
.mz-kpi-row{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:16px;}
.mz-kpi{background:linear-gradient(180deg,#fff,#f5f8fd);border:1px solid #dde7f5;border-radius:12px;
  padding:14px 16px;position:relative;overflow:hidden;}
.mz-kpi:before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;background:#005a3f;}
.mz-kpi.green:before{background:#27ae60;} .mz-kpi.gold:before{background:#fcc94a;}
.mz-kpi.red:before{background:#e74c3c;}
.mz-kpi .v{font-size:28px;font-weight:800;color:#003d2b;}
.mz-kpi .l{font-size:11px;color:#6b7c99;text-transform:uppercase;letter-spacing:.6px;font-weight:600;margin-top:2px;}
.mz-feat-row{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;}
.mz-feat{background:#fff;border:1px solid #dde7f5;border-radius:12px;padding:18px;text-align:center;
  box-shadow:0 4px 10px #0a1f4a0a;transition:transform .18s;}
.mz-feat:hover{transform:translateY(-3px);box-shadow:0 8px 18px #0a1f4a18;}
.mz-feat .ic{font-size:34px;margin-bottom:6px;}
.mz-feat h4{margin:6px 0 4px;color:#003d2b;font-size:14px;font-weight:800;}
.mz-feat p{margin:0;color:#6b7c99;font-size:12px;line-height:1.5;}
.mz-pred-result{padding:18px 22px;border-radius:13px;text-align:center;font-weight:800;font-size:18px;
  box-shadow:0 6px 16px #0002;margin-top:10px;}
.mz-pred-result.ok{background:linear-gradient(135deg,#e3f6ec,#c3eed4);color:#0f5a34;border:2px solid #27ae60;}
.mz-pred-result.no{background:linear-gradient(135deg,#fdecea,#f8d7d3);color:#8a2418;border:2px solid #e74c3c;}
.mz-pred-result .conf{font-size:13px;font-weight:600;margin-top:4px;color:#5a6b88;}
div.stButton > button[kind="primary"]{
  background:linear-gradient(135deg,#003d2b,#00805a);color:#fff;border:none;padding:11px 20px;
  border-radius:9px;font-weight:700;letter-spacing:.3px;box-shadow:0 4px 12px #0a1f4a30;}
div.stButton > button[kind="primary"]:hover{background:linear-gradient(135deg,#005a3f,#00b894);
  transform:translateY(-1px);}
</style>
""", unsafe_allow_html=True)

# ============================================================
# CACHED LOADERS
# ============================================================
@st.cache_data
def load_data():
    return pd.read_csv(os.path.join(ROOT, "data", "loan_data.csv"))

@st.cache_resource
def load_models():
    m = {}
    for f in ["logistic.pkl", "decisiontree.pkl", "randomforest.pkl",
              "scaler.pkl", "features.pkl"]:
        p = os.path.join(ROOT, "models", f)
        if os.path.exists(p):
            m[f.split(".")[0]] = joblib.load(p)
    return m

@st.cache_data
def load_metrics():
    p = os.path.join(ROOT, "models", "metrics.json")
    return json.load(open(p)) if os.path.exists(p) else {}

@st.cache_resource
def load_eval_bundle(model_name):
    return ml_engine.load_model(model_name)

def img(name):
    p = os.path.join(SHOTS, name)
    if os.path.exists(p):
        st.image(p, use_container_width=True)
    else:
        st.info(f"Run the analysis scripts to generate {name}")

# ============================================================
# SIDEBAR — branded navigation
# ============================================================
st.sidebar.markdown("""
<div style="text-align:center;padding:18px 0 14px;border-bottom:1px solid #ffffff22;margin-bottom:14px;">
  <div style="width:54px;height:54px;border-radius:12px;background:linear-gradient(135deg,#00b894,#005a3f);
    margin:0 auto 8px;display:flex;align-items:center;justify-content:center;color:#fff;
    font-weight:900;font-size:26px;box-shadow:0 4px 14px #00b89450;">M</div>
  <div style="font-weight:800;font-size:16px;color:#fff !important;letter-spacing:.5px;">Meezan Bank</div>
  <div style="font-size:10px;color:#a8c2f0 !important;margin-top:2px;letter-spacing:1.2px;">AI LOAN SYSTEM</div>
</div>
""", unsafe_allow_html=True)
page = st.sidebar.radio("Navigation", [
    "🏠 Project Overview",
    "📊 Dataset Analysis",
    "✅ Loan Application Predictor",
    "🏛️ Loan Counter Simulation"], label_visibility="collapsed")
st.sidebar.markdown("<div style='margin-top:30px;font-size:11px;color:#a8c2f0;text-align:center;'>"
                    "Simulation &amp; Modeling Final Project</div>", unsafe_allow_html=True)


# ============================================================
# PAGE 1 — PROJECT OVERVIEW
# ============================================================
if page == "🏠 Project Overview":
    st.markdown("""
    <div class="mz-hero">
      <div style="display:flex;align-items:center;gap:14px;margin-bottom:10px;">
        <div style="width:46px;height:46px;border-radius:10px;background:linear-gradient(135deg,#00b894,#005a3f);
          display:flex;align-items:center;justify-content:center;color:#fff;font-weight:900;font-size:24px;
          box-shadow:0 4px 12px #00b89450;border:2px solid #fcc94a;">M</div>
        <div>
          <span class="mz-badge live">LIVE</span><span class="mz-badge ml">ML-DRIVEN</span><span class="mz-badge">FYP 2026</span>
        </div>
      </div>
      <h1>Meezan Bank — AI Loan Simulator</h1>
      <p>An AI-powered banking system combining a trained Machine Learning model for loan
      approval with a realistic animated Meezan Bank simulation — applicants walk in, are
      evaluated by the model, and receive Approved/Rejected decisions live.</p>
    </div>
    """, unsafe_allow_html=True)

    df = load_data(); metrics = load_metrics()
    a, b, c, d = st.columns(4)
    a.markdown(f"<div class='mz-kpi'><div class='v'>{len(df)}</div><div class='l'>Dataset Records</div></div>", unsafe_allow_html=True)
    b.markdown(f"<div class='mz-kpi green'><div class='v'>3</div><div class='l'>ML Models Trained</div></div>", unsafe_allow_html=True)
    best = max(metrics.items(), key=lambda x: x[1]["Accuracy"])[1]["Accuracy"]*100 if metrics else 89
    c.markdown(f"<div class='mz-kpi gold'><div class='v'>{best:.1f}%</div><div class='l'>Best Accuracy</div></div>", unsafe_allow_html=True)
    d.markdown(f"<div class='mz-kpi'><div class='v'>SimPy</div><div class='l'>Simulation Engine</div></div>", unsafe_allow_html=True)

    st.markdown("<div class='mz-card'><h3>🎯 What This System Does</h3>", unsafe_allow_html=True)
    st.markdown("""
    This dual-purpose banking system:

    1. **Predicts loan approval** using three trained machine-learning models (Logistic Regression,
       Decision Tree, Random Forest) on real applicant attributes.
    2. **Simulates branch operations** with an animated bank floor — customers walk in, queue at
       the cashier and loan counter, get served, and receive ML-driven loan decisions live.

    Everything is exposed through this professional dashboard so evaluators can interact with
    the prediction model and watch the bank operate in real time.
    """)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("### ✨ Core Features")
    st.markdown("""
    <div class="mz-feat-row">
      <div class="mz-feat"><div class="ic">📊</div><h4>Complete EDA</h4>
        <p>Histograms, boxplots, heatmap, bar charts and pair-plots — every chart with a conclusion.</p></div>
      <div class="mz-feat"><div class="ic">🤖</div><h4>3 ML Models</h4>
        <p>Logistic Regression, Decision Tree and Random Forest — all compared on 5 metrics.</p></div>
      <div class="mz-feat"><div class="ic">🏦</div><h4>Animated Bank</h4>
        <p>Real bank floor: cashier, loan counter, manager office. Customers walk in and out.</p></div>
      <div class="mz-feat"><div class="ic">⏱️</div><h4>Period Simulation</h4>
        <p>Choose Day / Week / Month / Year — customer counts are generated automatically.</p></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><div class='mz-card'><h3>🛠️ Technology Stack</h3>"
                "<p style='color:#5a6b88;'>"
                "<b>Python</b> · <b>Pandas</b> · <b>NumPy</b> · <b>Matplotlib</b> · <b>Seaborn</b> · "
                "<b>Scikit-Learn</b> · <b>SimPy</b> · <b>Streamlit</b> · <b>HTML/CSS/JS</b> animation</p>"
                "</div>", unsafe_allow_html=True)


# ============================================================
# PAGE 2 — DATASET ANALYSIS
# ============================================================
elif page == "📊 Dataset Analysis":
    st.markdown("""
    <div class="mz-hero">
      <div style="display:flex;align-items:center;gap:14px;margin-bottom:10px;">
        <div style="width:46px;height:46px;border-radius:10px;background:linear-gradient(135deg,#00b894,#005a3f);
          display:flex;align-items:center;justify-content:center;color:#fff;font-weight:900;font-size:24px;
          box-shadow:0 4px 12px #00b89450;border:2px solid #fcc94a;">M</div>
        <div><span class="mz-badge">EDA</span><span class="mz-badge live">614 RECORDS</span></div>
      </div>
      <h1>📊 Dataset Analysis</h1>
      <p>Complete exploratory analysis: cleaning, outliers, correlations and visual insights.</p>
    </div>
    """, unsafe_allow_html=True)

    df = load_data()
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f"<div class='mz-kpi'><div class='v'>{df.shape[0]}</div><div class='l'>Total Records</div></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='mz-kpi gold'><div class='v'>{df.shape[1]}</div><div class='l'>Attributes</div></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='mz-kpi green'><div class='v'>{(df.Loan_Status=='Y').mean()*100:.1f}%</div><div class='l'>Approval Rate</div></div>", unsafe_allow_html=True)
    c4.markdown(f"<div class='mz-kpi red'><div class='v'>{int(df.isna().sum().sum())}</div><div class='l'>Missing Cells</div></div>", unsafe_allow_html=True)

    st.markdown("<div class='mz-card'><h3>🔍 Dataset Preview</h3>", unsafe_allow_html=True)
    st.dataframe(df.head(10), use_container_width=True, height=300)
    st.markdown("</div>", unsafe_allow_html=True)

    tabs = st.tabs(["📈 Distributions", "📦 Outliers", "🔥 Correlation", "📊 Categories", "🔗 Pairplot"])
    with tabs[0]:
        img("eda_histograms.png")
        st.success("**Insight:** Income and loan amount are right-skewed — log transform applied before modelling.")
    with tabs[1]:
        img("eda_boxplots.png")
        st.success("**Insight:** Several high-income outliers exist — log scaling reduces their leverage on the models.")
    with tabs[2]:
        img("eda_heatmap.png")
        st.success("**Insight:** Credit_History is the strongest standalone predictor of approval.")
    with tabs[3]:
        img("eda_barcharts.png")
        st.success("**Insight:** Clean credit history and semi-urban properties show the highest approval rates.")
    with tabs[4]:
        img("eda_pairplot.png")
        st.success("**Insight:** Approved/rejected classes overlap — non-linear models can help capture this.")


# ============================================================
# PAGE 3 — LOAN APPLICATION PREDICTOR (manual entry, ML decision)
# ============================================================
elif page == "✅ Loan Application Predictor":
    st.markdown("""
    <div class="mz-hero">
      <div style="display:flex;align-items:center;gap:14px;margin-bottom:10px;">
        <div style="width:46px;height:46px;border-radius:10px;background:linear-gradient(135deg,#00b894,#005a3f);
          display:flex;align-items:center;justify-content:center;color:#fff;font-weight:900;font-size:24px;
          box-shadow:0 4px 12px #00b89450;border:2px solid #fcc94a;">M</div>
        <div><span class="mz-badge live">LIVE</span><span class="mz-badge ml">ML POWERED</span></div>
      </div>
      <h1>✅ Loan Application Predictor</h1>
      <p>Enter a single applicant's details and get an instant Approve / Reject decision
      straight from one of the three trained ML models — with probability and reasoning.</p>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns([1.15, 1])

    with left:
        st.markdown("<div class='mz-card'><h3>📝 Applicant Details</h3>", unsafe_allow_html=True)

        model_choice = st.selectbox("AI Model to Use", ["Logistic Regression", "Decision Tree", "Random Forest"],
                                     key="pred_model")

        r1c1, r1c2 = st.columns(2)
        gender = r1c1.selectbox("Gender", ["Male", "Female"])
        married = r1c2.selectbox("Married", ["Yes", "No"])

        r2c1, r2c2 = st.columns(2)
        dependents = r2c1.selectbox("Dependents", [0, 1, 2, 3])
        education = r2c2.selectbox("Education", ["Graduate", "Not Graduate"])

        r3c1, r3c2 = st.columns(2)
        employment = r3c1.selectbox("Employment Type", ["Salaried", "Self-Employed", "Business Owner"])
        property_area = r3c2.selectbox("Property Area", ["Urban", "Semiurban", "Rural"])

        r4c1, r4c2 = st.columns(2)
        credit_score = r4c1.slider("Credit Score", 300, 850, 685, step=5,
                                    help="Used to derive Credit History: 620+ counts as a clean history.")
        existing_loans = r4c2.slider("Existing Loans", 0, 5, 0)

        r5c1, r5c2 = st.columns(2)
        income = r5c1.number_input("Monthly Income (PKR)", min_value=1000, max_value=1_000_000,
                                    value=25000, step=500)
        loan_amount = r5c2.number_input("Loan Amount Requested (PKR thousands)", min_value=1,
                                         max_value=2000, value=150, step=5,
                                         help="In thousands, matching the dataset's LoanAmount unit.")

        predict_clicked = st.button("🔍 Predict Decision", type="primary", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown("<div class='mz-card'><h3>📊 Decision Result</h3>", unsafe_allow_html=True)

        if predict_clicked:
            applicant = {
                "name": "Applicant",
                "gender": gender,
                "married": married,
                "dependents": dependents,
                "education": education,
                "employment": employment,
                "property_area": property_area,
                "credit_score": credit_score,
                "existing_loans": existing_loans,
                "income": income,
                "loan_amount": loan_amount,
            }
            bundle = load_eval_bundle(model_choice)
            result = ml_engine.evaluate_loan(bundle, applicant)
            st.session_state["pred_result"] = result
            st.session_state["pred_applicant"] = applicant

        if "pred_result" in st.session_state:
            result = st.session_state["pred_result"]
            applicant = st.session_state["pred_applicant"]
            if result["decision"] == "APPROVED":
                st.markdown(f"""
                <div class="mz-pred-result ok">✅ LOAN APPROVED
                  <div class="conf">Approval probability: {result['probability']*100:.1f}% &nbsp;|&nbsp;
                  Risk score: {result['risk_score']}</div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="mz-pred-result no">❌ LOAN REJECTED
                  <div class="conf">Approval probability: {result['probability']*100:.1f}% &nbsp;|&nbsp;
                  Risk score: {result['risk_score']}</div>
                </div>""", unsafe_allow_html=True)

            st.markdown(f"<p style='margin-top:14px;color:#5a6b88;'><b>Reason:</b> {result['reason']}</p>",
                        unsafe_allow_html=True)

            st.progress(min(max(result["probability"], 0.0), 1.0),
                        text=f"Model confidence (probability of approval): {result['probability']*100:.1f}%")

            st.markdown("<div style='margin-top:14px;font-size:12px;color:#6b7c99;'>"
                        f"Model used: <b>{model_choice}</b> &nbsp;·&nbsp; "
                        f"Credit History derived as <b>{'Clean (≥620)' if applicant['credit_score']>=620 else 'Poor (<620)'}</b> "
                        f"&nbsp;·&nbsp; Income/Loan ratio: <b>{applicant['income']/(applicant['loan_amount']+1):.2f}</b>"
                        "</div>", unsafe_allow_html=True)
        else:
            st.info("👈 Fill in the applicant's details and click **Predict Decision** to see the "
                    "model's Approve/Reject outcome here.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.caption("💡 This uses the **same trained model files** (`logistic.pkl`, `decisiontree.pkl`, "
               "`randomforest.pkl`) and the same feature engineering as the Loan Counter Simulation — "
               "no separate model is trained for this page.")


# ============================================================
# PAGE 4 — LOAN COUNTER SIMULATION (animated + ML decisions)
# ============================================================
elif page == "🏛️ Loan Counter Simulation":
    st.markdown("""
    <div class="mz-hero">
      <div style="display:flex;align-items:center;gap:14px;margin-bottom:10px;">
        <div style="width:46px;height:46px;border-radius:10px;background:linear-gradient(135deg,#00b894,#005a3f);
          display:flex;align-items:center;justify-content:center;color:#fff;font-weight:900;font-size:24px;
          box-shadow:0 4px 12px #00b89450;border:2px solid #fcc94a;">M</div>
        <div><span class="mz-badge live">LIVE</span><span class="mz-badge ml">ML POWERED</span></div>
      </div>
      <h1>🏛️ Loan Counter Simulation</h1>
      <p>Animated Meezan Bank loan department — applicants walk in, are evaluated by the
      trained ML model in real time, and receive Approved/Rejected decisions with full reasoning.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1, 1])
    period = c1.selectbox("Simulation Period", ["Day", "Week", "Month", "Year"], index=0)
    model_name = c2.selectbox("AI Model", ["Logistic Regression", "Decision Tree", "Random Forest"])
    c3.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)
    if c3.button("🎬 Generate & Load", type="primary", use_container_width=True):
        with st.spinner(f"Pre-computing applicants and ML decisions for one {period.lower()}..."):
            html = build_banking_simulator(period=period, model_name=model_name, mode="full")
        st.session_state["loan_html"] = html

    if "loan_html" in st.session_state:
        st.markdown("<br>", unsafe_allow_html=True)
        components.html(st.session_state["loan_html"], height=900, scrolling=False)
        st.caption("💡 Inside the simulator use **Run / Pause / Stop / Reset**, the **1x–8x speed** "
                   "selector and the **Audio** toggle. Every loan decision comes from the existing trained "
                   "ML model — no random approvals. Customer counts are randomly generated within "
                   "realistic ranges (2–12 loans, 10–30 cashier per day). For Week/Month/Year, the system "
                   "processes every single day and the **final report at the end** covers the entire period.")
    else:
        st.info("👆 Configure the period and click **Generate & Load** to start.")
