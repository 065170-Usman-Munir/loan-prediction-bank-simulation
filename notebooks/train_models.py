"""
ML pipeline: cleaning, feature engineering, training & evaluating
Logistic Regression, Decision Tree, Random Forest. Saves .pkl models + metrics.
"""
import numpy as np, pandas as pd, joblib, json, os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, roc_curve, auc)
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, seaborn as sns
sns.set_style('whitegrid'); plt.rcParams['figure.dpi']=110

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
df = pd.read_csv(os.path.join(ROOT,'data','loan_data.csv'))

# ---------- Cleaning & missing values ----------
for c in ['Gender','Married','Dependents','Self_Employed']:
    df[c] = df[c].fillna(df[c].mode()[0])
df['Credit_History'] = df['Credit_History'].fillna(df['Credit_History'].mode()[0])
df['LoanAmount'] = df['LoanAmount'].fillna(df['LoanAmount'].median())
df['Loan_Amount_Term'] = df['Loan_Amount_Term'].fillna(df['Loan_Amount_Term'].mode()[0])

# ---------- Feature engineering ----------
df['Total_Income'] = df['ApplicantIncome'] + df['CoapplicantIncome']
df['Income_Loan_Ratio'] = df['Total_Income'] / (df['LoanAmount']+1)
df['LoanAmount_log'] = np.log1p(df['LoanAmount'])
df['Total_Income_log'] = np.log1p(df['Total_Income'])
df['Dependents'] = df['Dependents'].replace('3+','3').astype(int)

# ---------- Encoding ----------
enc = {'Gender':{'Male':1,'Female':0},'Married':{'Yes':1,'No':0},
       'Education':{'Graduate':1,'Not Graduate':0},'Self_Employed':{'Yes':1,'No':0},
       'Property_Area':{'Urban':2,'Semiurban':1,'Rural':0},'Loan_Status':{'Y':1,'N':0}}
for col,m in enc.items(): df[col]=df[col].map(m)

features = ['Gender','Married','Dependents','Education','Self_Employed',
    'Credit_History','Property_Area','Total_Income_log','LoanAmount_log','Income_Loan_Ratio']
X = df[features]; y = df['Loan_Status']
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=42,stratify=y)

scaler = StandardScaler().fit(X_train)
X_train_s = scaler.transform(X_train); X_test_s = scaler.transform(X_test)
joblib.dump(scaler, os.path.join(ROOT,'models','scaler.pkl'))
joblib.dump(features, os.path.join(ROOT,'models','features.pkl'))

models = {
 'Logistic Regression': (LogisticRegression(max_iter=1000,random_state=42), True,'logistic.pkl'),
 'Decision Tree': (DecisionTreeClassifier(max_depth=5,random_state=42), False,'decisiontree.pkl'),
 'Random Forest': (RandomForestClassifier(n_estimators=200,max_depth=8,random_state=42), False,'randomforest.pkl'),
}
results = {}; roc_data = {}
for name,(model,scale,fname) in models.items():
    Xtr,Xte = (X_train_s,X_test_s) if scale else (X_train,X_test)
    model.fit(Xtr,y_train)
    pred = model.predict(Xte); proba = model.predict_proba(Xte)[:,1]
    results[name] = {
      'Accuracy':round(accuracy_score(y_test,pred),4),
      'Precision':round(precision_score(y_test,pred),4),
      'Recall':round(recall_score(y_test,pred),4),
      'F1':round(f1_score(y_test,pred),4),
      'cm':confusion_matrix(y_test,pred).tolist()}
    fpr,tpr,_ = roc_curve(y_test,proba); roc_data[name]=(fpr,tpr,auc(fpr,tpr))
    joblib.dump(model, os.path.join(ROOT,'models',fname))
    print(f"{name}: {results[name]['Accuracy']} acc, F1 {results[name]['F1']}")

json.dump(results, open(os.path.join(ROOT,'models','metrics.json'),'w'), indent=2)

# ---------- Confusion matrices ----------
fig,axes = plt.subplots(1,3,figsize=(15,4))
for ax,(name,r) in zip(axes,results.items()):
    sns.heatmap(r['cm'],annot=True,fmt='d',cmap='Blues',ax=ax,cbar=False,
        xticklabels=['Reject','Approve'],yticklabels=['Reject','Approve'])
    ax.set_title(f"{name}\nAcc={r['Accuracy']}"); ax.set_ylabel('Actual'); ax.set_xlabel('Predicted')
plt.tight_layout(); plt.savefig(os.path.join(ROOT,'screenshots','confusion_matrices.png')); plt.close()

# ---------- ROC curves ----------
plt.figure(figsize=(7,6))
for name,(fpr,tpr,a) in roc_data.items():
    plt.plot(fpr,tpr,lw=2,label=f'{name} (AUC={a:.3f})')
plt.plot([0,1],[0,1],'k--',alpha=0.5)
plt.xlabel('False Positive Rate'); plt.ylabel('True Positive Rate')
plt.title('ROC Curve Comparison'); plt.legend(loc='lower right')
plt.tight_layout(); plt.savefig(os.path.join(ROOT,'screenshots','roc_curves.png')); plt.close()

# ---------- Model comparison bar ----------
comp = pd.DataFrame(results).T[['Accuracy','Precision','Recall','F1']]
comp.plot(kind='bar',figsize=(9,5),colormap='viridis')
plt.title('Model Performance Comparison'); plt.ylabel('Score'); plt.ylim(0,1)
plt.xticks(rotation=15); plt.legend(loc='lower right'); plt.tight_layout()
plt.savefig(os.path.join(ROOT,'screenshots','model_comparison.png')); plt.close()
print("Models + metric plots saved.")
