# 🏦 Bank Loan Approval Prediction & Bank Queue Simulation System

A complete **Simulation & Modeling** final project that combines **Machine Learning** (loan-approval prediction) with **Discrete-Event Simulation** (bank queue / M/M/c model), wrapped in an interactive **Streamlit** dashboard.

> University of Management and Technology (UMT), Lahore — Department of Software Engineering

---

## 📋 Overview

This project solves two connected banking problems:

1. **Loan Approval Prediction** — train and compare **Logistic Regression**, **Decision Tree**, and **Random Forest** classifiers to predict whether a loan application is approved.
2. **Bank Queue Simulation** — model customer arrivals at a branch using the **M/M/c queueing model** in **SimPy**, to study waiting time and teller utilization and find the optimal number of tellers.

Both components are exposed through a professional 4-page Streamlit dashboard.

---

## 📁 Project Structure

```
Banking_Simulation_Project/
│
├── data/                     # Dataset
│   └── loan_data.csv
├── notebooks/                # EDA + model training scripts
│   ├── eda_analysis.py
│   └── train_models.py
├── models/                   # Saved models & metrics
│   ├── logistic.pkl
│   ├── decisiontree.pkl
│   ├── randomforest.pkl
│   ├── scaler.pkl
│   ├── features.pkl
│   └── metrics.json
├── simulation/               # SimPy bank queue simulation
│   ├── bank_simulation.py
│   └── loan_counter_simulation.py
├── dashboard/                # Streamlit app
│   └── app.py
├── report/                   # Final Word report
│   └── Project_Report.docx
├── presentation/             # 12-slide deck
│   └── Project_Presentation.pptx
├── screenshots/              # Generated charts (EDA, ML, simulation)
├── requirements.txt
├── README.md
├── COMMITS.md                # 25 suggested commit messages
└── VIVA_QA.md                # Viva questions & answers
```

---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/Banking_Simulation_Project.git
cd Banking_Simulation_Project
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run

Run the steps **in order** the first time so the models and charts are generated.

### Step 1 — Generate EDA visualizations
```bash
python notebooks/eda_analysis.py
```
Produces histograms, boxplots, heatmap, bar charts and a pairplot in `screenshots/`.

### Step 2 — Train the ML models
```bash
python notebooks/train_models.py
```
Trains all three models, saves `*.pkl` files + `metrics.json`, and generates confusion-matrix, ROC and comparison charts.

### Step 3 — Run the simulation
```bash
python simulation/bank_simulation.py
```
Runs the M/M/c bank-queue simulation and saves queue-length, waiting-time and utilization graphs.

### Step 4 — Launch the dashboard
```bash
streamlit run dashboard/app.py
```
Opens the interactive 4-page dashboard in your browser (default: http://localhost:8501).

---

## 🖥️ Dashboard Pages

| Page | Content |
|------|---------|
| **1. Project Overview** | Goals, scope, tech stack |
| **2. Dataset Analysis** | Full EDA with visualizations & conclusions |
| **3. Loan Prediction** | Enter income, loan amount, education, credit history, property area → **Approved / Rejected** |
| **4. Simulation** | Adjust tellers / arrival / service rate → live waiting time, customers served, queue length & utilization graphs |
| **5. Loan Counter Simulation** | Loan Application Counter using the **existing trained model**. Daily/Weekly/Monthly/Yearly modes, speed controls, live event log, live stats, final report & 5 charts |

---

## 🤖 Machine Learning Results

| Model | Accuracy | Precision | Recall | F1 |
|-------|----------|-----------|--------|-----|
| Logistic Regression | **0.89** | 0.88 | 0.99 | **0.93** |
| Decision Tree | 0.86 | 0.87 | 0.96 | 0.91 |
| Random Forest | 0.85 | 0.87 | 0.95 | 0.91 |

**Logistic Regression** is recommended — it has the best accuracy/F1 and is the most interpretable, which matters for auditable lending decisions.

---

## ⏳ Simulation Model (M/M/c)

- **M** — Poisson (Markovian) arrivals, rate λ
- **M** — Exponential service times, rate μ
- **c** — number of parallel tellers (shared FIFO queue)
- Utilization: **ρ = λ / (c · μ)**, stable when **ρ < 1**
- Mean waiting time (Little's Law): **Wq = Lq / λ**

Baseline: arrival every ~4 min, ~10 min service, 3 tellers, 480-min day → ρ ≈ 0.83.

---

## 📊 Dataset

The dataset follows the standard **Kaggle Loan Prediction** schema
(`Gender, Married, Dependents, Education, Self_Employed, ApplicantIncome,
CoapplicantIncome, LoanAmount, Loan_Amount_Term, Credit_History,
Property_Area, Loan_Status`). A reproducible version is included in `data/`
so the project runs without a Kaggle account.
Original dataset: https://www.kaggle.com/datasets/altruistdelhite04/loan-prediction-problem-dataset

---

## 🛠️ Tech Stack

`Python` · `Pandas` · `NumPy` · `Matplotlib` · `Seaborn` · `Scikit-Learn` · `SimPy` · `Streamlit`

---

## 👤 Author

**Sameel** — BS Software Engineering, UMT Lahore

## 📄 License

MIT License — free to use for academic purposes.
