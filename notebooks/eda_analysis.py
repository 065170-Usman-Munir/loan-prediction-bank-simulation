"""Complete EDA: cleaning, outliers, correlation, professional visualizations."""
import numpy as np, pandas as pd, os
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, seaborn as sns
sns.set_style('whitegrid'); plt.rcParams['figure.dpi']=110
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.join(ROOT,'screenshots')
df = pd.read_csv(os.path.join(ROOT,'data','loan_data.csv'))

# Clean for plotting
for c in ['Gender','Married','Dependents','Self_Employed']: df[c]=df[c].fillna(df[c].mode()[0])
df['LoanAmount']=df['LoanAmount'].fillna(df['LoanAmount'].median())
df['Credit_History']=df['Credit_History'].fillna(df['Credit_History'].mode()[0])
df['Total_Income']=df['ApplicantIncome']+df['CoapplicantIncome']

# 1. Histograms
fig,ax=plt.subplots(2,2,figsize=(12,8))
for a,col in zip(ax.ravel(),['ApplicantIncome','LoanAmount','Total_Income','Loan_Amount_Term']):
    sns.histplot(df[col].dropna(),kde=True,ax=a,color='steelblue'); a.set_title(f'Distribution of {col}')
plt.tight_layout(); plt.savefig(f'{S}/eda_histograms.png'); plt.close()

# 2. Boxplots (outlier detection)
fig,ax=plt.subplots(1,3,figsize=(13,4))
for a,col in zip(ax,['ApplicantIncome','CoapplicantIncome','LoanAmount']):
    sns.boxplot(y=df[col],ax=a,color='salmon'); a.set_title(f'Boxplot: {col}')
plt.tight_layout(); plt.savefig(f'{S}/eda_boxplots.png'); plt.close()

# 3. Correlation heatmap
num=['ApplicantIncome','CoapplicantIncome','LoanAmount','Loan_Amount_Term','Credit_History','Total_Income']
plt.figure(figsize=(8,6))
sns.heatmap(df[num].corr(),annot=True,cmap='coolwarm',fmt='.2f',square=True,linewidths=.5)
plt.title('Correlation Heatmap'); plt.tight_layout(); plt.savefig(f'{S}/eda_heatmap.png'); plt.close()

# 4. Bar charts (categorical vs approval)
fig,ax=plt.subplots(2,2,figsize=(12,8))
for a,col in zip(ax.ravel(),['Education','Credit_History','Property_Area','Married']):
    ct=pd.crosstab(df[col],df['Loan_Status'],normalize='index')
    ct.plot(kind='bar',stacked=True,ax=a,colormap='Set2'); a.set_title(f'Approval rate by {col}')
    a.set_ylabel('Proportion'); a.legend(['Rejected','Approved'],fontsize=8)
plt.tight_layout(); plt.savefig(f'{S}/eda_barcharts.png'); plt.close()

# 5. Pairplot
sub=df[['ApplicantIncome','LoanAmount','Total_Income','Loan_Status']].dropna()
g=sns.pairplot(sub,hue='Loan_Status',palette='husl',diag_kind='kde'); g.fig.suptitle('Pairplot',y=1.02)
g.savefig(f'{S}/eda_pairplot.png'); plt.close()
print("EDA visualizations saved:", os.listdir(S))
