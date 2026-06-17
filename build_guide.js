const fs = require('fs');
const path = require('path');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, HeadingLevel, BorderStyle, WidthType, ShadingType,
  PageBreak, TableOfContents, PageNumber, Footer, LevelFormat } = require('docx');

const FONT = "Calibri";
const NAVY = "1F3864", BLUE = "2E5AAC", CODEBG = "F2F2F2", GREEN="1E6B3A";
const border = { style: BorderStyle.SINGLE, size: 1, color: "BBBBBB" };
const borders = { top: border, bottom: border, left: border, right: border,
  insideHorizontal: border, insideVertical: border };

function h1(t){return new Paragraph({heading:HeadingLevel.HEADING_1,children:[new TextRun(t)]});}
function h2(t){return new Paragraph({heading:HeadingLevel.HEADING_2,children:[new TextRun(t)]});}
function h3(t){return new Paragraph({heading:HeadingLevel.HEADING_3,children:[new TextRun(t)]});}
function p(t){return new Paragraph({spacing:{after:120,line:276},children:[new TextRun(t)]});}
function pr(runs){return new Paragraph({spacing:{after:120,line:276},children:runs});}
function b(t){return new Paragraph({numbering:{reference:"bul",level:0},spacing:{after:60},children:[new TextRun(t)]});}
function num(t){return new Paragraph({numbering:{reference:"nm",level:0},spacing:{after:60},children:[new TextRun(t)]});}
function code(lines){
  // each line as monospace paragraph on a light background
  return lines.map((l,i)=>new Paragraph({
    spacing:{after: i===lines.length-1?120:0, before: i===0?60:0},
    shading:{fill:CODEBG,type:ShadingType.CLEAR},
    border:{left:{style:BorderStyle.SINGLE,size:12,color:BLUE,space:6}},
    indent:{left:120},
    children:[new TextRun({text:l||" ",font:"Consolas",size:19,color:"1A1A1A"})]}));
}
function tip(t){return new Paragraph({spacing:{before:80,after:120},shading:{fill:"FFF7E0",type:ShadingType.CLEAR},
  border:{left:{style:BorderStyle.SINGLE,size:14,color:"E0A800",space:6}},indent:{left:120},
  children:[new TextRun({text:"💡 ZAROORI: ",bold:true,color:"8A6D00"}),new TextRun({text:t,color:"5A4A00"})]});}
function warn(t){return new Paragraph({spacing:{before:80,after:120},shading:{fill:"FDECEA",type:ShadingType.CLEAR},
  border:{left:{style:BorderStyle.SINGLE,size:14,color:"C0392B",space:6}},indent:{left:120},
  children:[new TextRun({text:"⚠️ KHABARDAR: ",bold:true,color:"922B21"}),new TextRun({text:t,color:"6E1F18"})]});}

function tbl(rows, widths){
  const total = widths.reduce((a,c)=>a+c,0);
  const trs = rows.map((r,ri)=>new TableRow({children:r.map((c,ci)=>new TableCell({
    width:{size:widths[ci],type:WidthType.DXA},borders,
    shading:{fill: ri===0?NAVY:(ri%2?"F4F6FB":"FFFFFF"),type:ShadingType.CLEAR},
    margins:{top:70,bottom:70,left:110,right:110},
    children:[new Paragraph({children:[new TextRun({text:String(c),bold:ri===0,
      color:ri===0?"FFFFFF":"222222",size:19})]})]}))}));
  return new Table({width:{size:total,type:WidthType.DXA},columnWidths:widths,rows:trs});
}

const C = [];

// ---------- TITLE ----------
C.push(new Paragraph({alignment:AlignmentType.CENTER,spacing:{before:2600,after:100},
  children:[new TextRun({text:"Banking Simulation Project",bold:true,size:48,color:NAVY})]}));
C.push(new Paragraph({alignment:AlignmentType.CENTER,spacing:{after:300},
  children:[new TextRun({text:"Complete A-to-Z Guide (Roman Urdu)",size:30,color:BLUE})]}));
C.push(new Paragraph({alignment:AlignmentType.CENTER,spacing:{after:120},
  children:[new TextRun({text:"Bank Loan Approval Prediction + Bank Queue Simulation",size:22,color:"444444"})]}));
C.push(new Paragraph({alignment:AlignmentType.CENTER,spacing:{before:1400},
  children:[new TextRun({text:"Is document mein project ki HAR cheez detail mein hai:",italics:true,size:20,color:"555555"})]}));
C.push(new Paragraph({alignment:AlignmentType.CENTER,
  children:[new TextRun({text:"saari files, unka kaam, run karne ka tareeqa, aur changes kaise karein.",italics:true,size:20,color:"555555"})]}));
C.push(new Paragraph({alignment:AlignmentType.CENTER,spacing:{before:1200},
  children:[new TextRun({text:"Banaya gaya: Sameel ke liye",size:20})]}));
C.push(new Paragraph({children:[new PageBreak()]}));

// ---------- TOC ----------
C.push(h1("Fehrist (Table of Contents)"));
C.push(new TableOfContents("Contents",{hyperlink:true,headingStyleRange:"1-2"}));
C.push(new Paragraph({children:[new PageBreak()]}));

// ===================================================================
// 0. SABSE PEHLE
// ===================================================================
C.push(h1("0. Sabse Pehle Yeh Parho (Bohat Zaroori)"));
C.push(p("Is project mein DO Python versions ka masla aaya tha. Aapke laptop pe Python 3.14 install tha, lekin woh bohat naya hai aur usme libraries (pandas waghaira) install nahi hoti theen. Is liye humne Python 3.12 install kiya."));
C.push(tip("Is project ki HAR command 'py -3.12' se shuru hogi, sirf 'python' se NAHI. Kyunke 'python' aapke laptop pe 3.14 ko chalata hai (jisme kuch install nahi), jabke 'py -3.12' 3.12 ko chalata hai (jisme sab kuch install hai)."));
C.push(pr([new TextRun({text:"Galat: ",bold:true,color:"C0392B"}),new TextRun({text:"python notebooks/eda_analysis.py",font:"Consolas"})]));
C.push(pr([new TextRun({text:"Sahi: ",bold:true,color:GREEN}),new TextRun({text:"py -3.12 notebooks/eda_analysis.py",font:"Consolas"})]));

// ===================================================================
// 1. PROJECT KYA HAI
// ===================================================================
C.push(h1("1. Project Kya Hai? (Aasaan Lafzon Mein)"));
C.push(p("Yeh project DO alag kaam karta hai, dono banking se related hain:"));
C.push(h2("Hissa 1 — Loan Approval Prediction (Machine Learning)"));
C.push(p("Computer ko purane loan applications ka data dikhaya jaata hai (kis ki income kitni thi, credit history kaisi thi, loan approve hua ya nahi). Computer is data se 'seekhta' hai. Phir jab koi naya banda apni details daalta hai, to computer predict karta hai ke uska loan APPROVE hoga ya REJECT. Yeh kaam teen alag tareeqon (models) se hota hai aur dekha jaata hai kaunsa behtar hai."));
C.push(h2("Hissa 2 — Bank Queue Simulation (SimPy)"));
C.push(p("Yeh ek bank ki branch ko nakli (simulate) tareeqe se chala kar dikhata hai. Customers aate hain, tellers (cashiers) unhe serve karte hain, log line (queue) mein lagte hain. Is se pata chalta hai ke agar bank mein 3 teller hon to log kitni der wait karte hain, aur kitne tellers honay chahiye taake na zyada line lage na teller khali bethe rahein."));
C.push(p("Dono cheezein ek 'Dashboard' (website jaisi screen) mein dikhayi jaati hain jise Streamlit banata hai."));

// ===================================================================
// 2. FILES KI CATEGORIES
// ===================================================================
C.push(h1("2. Project Ki Saari Files (Categories Mein)"));
C.push(p("Niche saari files unki ahmiyat ke hisaab se 3 categories mein bati hain: BOHAT ZAROORI, NORMAL, aur KAM ZAROORI."));

C.push(h2("2.1 Folder Ka Pura Naqsha (Structure)"));
C.push(...code([
"Banking_Simulation_Project/",
"|",
"|-- data/                    <- Dataset (loan ka data)",
"|   |-- loan_data.csv",
"|-- notebooks/               <- EDA aur model training scripts",
"|   |-- eda_analysis.py",
"|   |-- train_models.py",
"|   |-- Loan_Analysis.ipynb",
"|-- models/                  <- Trained (seekhe hue) models yahan save hote hain",
"|   |-- logistic.pkl",
"|   |-- decisiontree.pkl",
"|   |-- randomforest.pkl",
"|   |-- scaler.pkl",
"|   |-- features.pkl",
"|   |-- metrics.json",
"|-- simulation/              <- Bank queue simulation",
"|   |-- bank_simulation.py",
"|-- dashboard/               <- Streamlit dashboard (main screen)",
"|   |-- app.py",
"|-- screenshots/             <- Saare charts/graphs yahan bante hain",
"|-- report/                  <- Word report",
"|-- presentation/            <- 12 slides ki PPT",
"|-- requirements.txt         <- Libraries ki list",
"|-- README.md",
"|-- COMMITS.md, VIVA_QA.md"
]));

C.push(h2("2.2 Category A — BOHAT ZAROORI Files (Inke Bina Project Nahi Chalega)"));
C.push(tbl([
 ["File","Kaam"],
 ["data/loan_data.csv","Saara loan data. Project ka 'fuel'. Is ke bina kuch nahi chalega."],
 ["notebooks/train_models.py","3 ML models train karke save karta hai. Pehle ise chalana zaroori."],
 ["simulation/bank_simulation.py","Poora bank queue simulation ka logic."],
 ["dashboard/app.py","Main dashboard. Sab kuch isi screen pe dikhta hai."],
 ["requirements.txt","Konsi libraries chahiye, unki list."],
], [2600,6760]));

C.push(h2("2.3 Category B — NORMAL Files (Charts aur Analysis Ke Liye)"));
C.push(tbl([
 ["File","Kaam"],
 ["notebooks/eda_analysis.py","Data ke charts (histogram, heatmap waghaira) banata hai."],
 ["models/*.pkl","Train hone ke baad models yahan automatically save hote hain."],
 ["models/metrics.json","Models ki performance (accuracy waghaira) ke numbers."],
 ["screenshots/*.png","Saare graphs jo scripts banati hain."],
], [2600,6760]));

C.push(h2("2.4 Category C — KAM ZAROORI Files (Sirf Submission/Documents Ke Liye)"));
C.push(p("Yeh files project chalane ke liye zaroori NAHI. Yeh sirf university submission ke liye hain — inhe aap seedha kholo aur use karo."));
C.push(tbl([
 ["File","Kaam"],
 ["report/Project_Report.docx","Poori report (Abstract se References tak). Seedha submit karo."],
 ["presentation/Project_Presentation.pptx","12 slides ki presentation with speaker notes."],
 ["README.md","Project ka intro (GitHub ke liye)."],
 ["COMMITS.md","25 git commit messages."],
 ["VIVA_QA.md","Viva ke 30 sawal aur jawab. Exam se pehle parho."],
 ["notebooks/Loan_Analysis.ipynb","Jupyter notebook version (optional)."],
], [3000,6360]));

// ===================================================================
// 3. HAR FILE KA LOGIC
// ===================================================================
C.push(new Paragraph({children:[new PageBreak()]}));
C.push(h1("3. Har Zaroori File Ke Andar Kya Logic Hai"));

C.push(h2("3.1 data/loan_data.csv — Dataset"));
C.push(p("Yeh ek Excel jaisi file hai jisme 614 loan applications ka data hai. Har row ek banda hai. Columns yeh hain:"));
C.push(b("Gender, Married, Dependents — banday ki demographic info"));
C.push(b("Education — Graduate hai ya nahi"));
C.push(b("ApplicantIncome, CoapplicantIncome — income"));
C.push(b("LoanAmount, Loan_Amount_Term — loan ki raqam aur muddat"));
C.push(b("Credit_History — credit record saaf hai (1) ya nahi (0). YEH SABSE AHEM column hai."));
C.push(b("Property_Area — Urban / Semiurban / Rural"));
C.push(b("Loan_Status — FINAL jawab: Y (approve) ya N (reject). Yeh woh cheez hai jo model seekhta hai."));

C.push(h2("3.2 notebooks/train_models.py — Models Training"));
C.push(p("Is file ka kaam step by step:"));
C.push(num("Data ko load karta hai aur saaf karta hai (missing values bhar deta hai)."));
C.push(num("Naye 'features' banata hai: total income, log loan amount, income-to-loan ratio."));
C.push(num("Text ko numbers mein badalta hai (Male=1, Female=0 waghaira) kyunke computer sirf numbers samajhta hai."));
C.push(num("Data ko 2 hisson mein baant'ta hai: 80% se seekhta hai (training), 20% pe test karta hai."));
C.push(num("3 models train karta hai: Logistic Regression, Decision Tree, Random Forest."));
C.push(num("Har model ki performance check karta hai (accuracy, precision, recall, F1)."));
C.push(num("Models ko .pkl files mein save kar deta hai taake dashboard unhe baad mein use kar sake."));
C.push(num("Confusion matrix aur ROC curve ke graphs banata hai."));
C.push(tip("Is file ko HAMESHA dashboard se PEHLE chalana hai, warna models hi nahi banenge aur prediction page kaam nahi karega."));

C.push(h2("3.3 simulation/bank_simulation.py — Bank Queue Simulation"));
C.push(p("Yeh 'M/M/c' naam ka mashhoor mathematical model use karta hai. Aasaan lafzon mein:"));
C.push(b("Customers random time pe aate hain (jaise asli bank mein)."));
C.push(b("Kuch tellers (cashiers) hote hain jo customers ko serve karte hain."));
C.push(b("Agar saare teller busy hon to customer line (queue) mein lag jaata hai."));
C.push(b("File hisaab lagati hai: average wait time, kitne customers serve hue, teller kitna busy raha (utilization)."));
C.push(p("Yeh teen settings important hain (inhe aap change kar sakte ho — Section 6 dekho):"));
C.push(tbl([
 ["Setting","Matlab","Default"],
 ["n_tellers","Kitne tellers/cashiers hain","3"],
 ["arrival_mean","Har customer kitni der baad aata hai (minute)","4.0"],
 ["service_mean","Ek customer ko serve karne mein kitna time (minute)","10.0"],
 ["sim_time","Simulation kitni der chale (minute)","480 (8 ghante)"],
], [2200,5160,2000]));

C.push(h2("3.4 dashboard/app.py — Main Dashboard"));
C.push(p("Yeh Streamlit se bani website jaisi screen hai. Iske 4 pages hain (left side menu se switch karo):"));
C.push(tbl([
 ["Page","Kya Dikhata Hai"],
 ["Page 1: Project Overview","Project ka intro, goals, tools."],
 ["Page 2: Dataset Analysis","Saare EDA charts apni explanation ke saath."],
 ["Page 3: Loan Prediction","Aap income/credit history daalo -> Approved ya Rejected jawab."],
 ["Page 4: Simulation","Tellers ki tadaad badlo -> live wait time aur graphs."],
], [3000,6360]));

// ===================================================================
// 4. INSTALL (EK BAAR)
// ===================================================================
C.push(new Paragraph({children:[new PageBreak()]}));
C.push(h1("4. Setup — Ek Dafa Karna Hai (Already Ho Chuka)"));
C.push(p("Yeh kaam aap pehle hi kar chuke ho. Lekin agar kabhi naye laptop pe chalana ho to yeh steps hain:"));
C.push(h2("Step 1 — Python 3.12 Install"));
C.push(p("Agar 3.12 install nahi to yeh command chalao (Windows ka launcher khud install kar dega):"));
C.push(...code(["py install 3.12"]));
C.push(p("Confirm karne ke liye:"));
C.push(...code(["py -3.12 --version"]));
C.push(p("Output mein 'Python 3.12.x' aana chahiye."));
C.push(h2("Step 2 — Libraries Install"));
C.push(p("Project folder mein VS Code terminal khol ke yeh ek command chalao:"));
C.push(...code(["py -3.12 -m pip install pandas numpy matplotlib seaborn scikit-learn simpy streamlit joblib"]));
C.push(p("End mein 'Successfully installed ...' aaye to sab theek hai."));

// ===================================================================
// 5. RUN
// ===================================================================
C.push(h1("5. Project Run Karne Ka Tareeqa (Har Dafa)"));
C.push(h2("Step 1 — VS Code Mein Folder Kholo"));
C.push(num("VS Code kholo -> File -> Open Folder -> 'Banking_Simulation_Project' folder select karo."));
C.push(num("Terminal -> New Terminal (ya Ctrl + ` shortcut)."));
C.push(warn("Confirm karo ke terminal SAHI folder mein hai. Path ke end mein 'Banking_Simulation_Project' likha hona chahiye. Agar zip ne folder ke andar folder bana diya hai to 'cd Banking_Simulation_Project' likh kar andar jao."));

C.push(h2("Step 2 — Yeh 4 Commands Isi Order Mein Chalao"));
C.push(p("Ek command Enter karo, woh khatam ho jaye, phir agli. Har command 'py -3.12' se shuru hai:"));
C.push(pr([new TextRun({text:"1) ",bold:true}),new TextRun({text:"Charts banao:",color:BLUE})]));
C.push(...code(["py -3.12 notebooks/eda_analysis.py"]));
C.push(pr([new TextRun({text:"2) ",bold:true}),new TextRun({text:"Models train karo:",color:BLUE})]));
C.push(...code(["py -3.12 notebooks/train_models.py"]));
C.push(pr([new TextRun({text:"3) ",bold:true}),new TextRun({text:"Simulation chalao:",color:BLUE})]));
C.push(...code(["py -3.12 simulation/bank_simulation.py"]));
C.push(pr([new TextRun({text:"4) ",bold:true}),new TextRun({text:"Dashboard kholo:",color:BLUE})]));
C.push(...code(["py -3.12 -m streamlit run dashboard/app.py"]));
C.push(p("Aakhri command chalate hi browser khud khul jayega. Agar na khule to terminal mein jo link (http://localhost:8501) aaye us pe Ctrl+Click karo."));
C.push(tip("Pehli dafa charon command chalana zaroori hai. Baad mein agar sirf dashboard dekhna ho to seedha 4th command (streamlit) bhi chala sakte ho, kyunke models aur charts pehle se bane hue hain."));

C.push(h2("Step 3 — Dashboard Band Karna"));
C.push(p("Terminal pe keyboard se Ctrl + C dabao. Dashboard band ho jayega."));

// ===================================================================
// 6. CHANGES
// ===================================================================
C.push(new Paragraph({children:[new PageBreak()]}));
C.push(h1("6. Agar Koi Cheez Change Karni Ho"));
C.push(p("Niche aam changes aur unka tareeqa. Har change ke baad woh wali script dobara chalani parti hai."));

C.push(h2("6.1 Simulation Mein Tellers Ya Timing Badalna"));
C.push(p("File kholo: simulation/bank_simulation.py. Sabse niche yeh line dhoondo:"));
C.push(...code(['def run(n_tellers=3, arrival_mean=4.0, service_mean=10.0, sim_time=480):']));
C.push(p("Yahan numbers badal sakte ho. Misal ke taur pe 5 tellers chahiye to n_tellers=5 kar do. Save karo, phir dobara chalao:"));
C.push(...code(["py -3.12 simulation/bank_simulation.py"]));
C.push(tip("Lekin sabse aasaan tareeqa: Dashboard ke Page 4 pe sliders hain. Wahan se bina file chhede tellers/timing live badal sakte ho. File edit ki zaroorat hi nahi."));

C.push(h2("6.2 Naya Dataset Use Karna (Asli Kaggle Wala)"));
C.push(p("Agar teacher kahe ke asli Kaggle CSV use karo:"));
C.push(num("Kaggle se loan dataset download karo."));
C.push(num("Us file ka naam 'loan_data.csv' rakho."));
C.push(num("Use 'data' folder mein purani file ke upar paste kar do (replace)."));
C.push(num("Phir dobara chalao: train_models.py aur eda_analysis.py."));
C.push(warn("Naye dataset ke columns ke naam bilkul wahi hone chahiyein jo purani file mein hain (Gender, ApplicantIncome, Credit_History, Loan_Status waghaira), warna script error degi."));

C.push(h2("6.3 Model Ki Settings Badalna"));
C.push(p("File: notebooks/train_models.py. Yeh hissa dhoondo:"));
C.push(...code([
"'Random Forest': (RandomForestClassifier(n_estimators=200,",
"                  max_depth=8, random_state=42), False, ...)"
]));
C.push(p("Misal: n_estimators=200 ko 300 kar sakte ho (zyada trees). max_depth=8 ko badal sakte ho. Save karke dobara train_models.py chalao."));

C.push(h2("6.4 Dashboard Ka Text/Title Badalna"));
C.push(p("File: dashboard/app.py. Jo text quotes (\" \") ke andar likha hai usay badal sakte ho. Misal title:"));
C.push(...code(['st.title("Bank Loan Approval Prediction ...")']));
C.push(p("Save karne ke baad dashboard ke browser tab mein upar 'Rerun' dabao, ya dashboard band karke dobara chalao."));

C.push(h2("6.5 Charts Ke Rang Badalna"));
C.push(p("File: notebooks/eda_analysis.py. Charts mein color='steelblue' jaisi cheezein hain. Inhe color='green' waghaira kar sakte ho. Save karke eda_analysis.py dobara chalao — naye charts ban jayenge."));

// ===================================================================
// 7. EXPECTED OUTPUT
// ===================================================================
C.push(h1("7. Har Command Ka Expected Output (Confirm Karne Ke Liye)"));
C.push(tbl([
 ["Command","Sahi Output (Aisa Aaye To Theek Hai)"],
 ["eda_analysis.py","'EDA visualizations saved: [...]' — yani charts ban gaye."],
 ["train_models.py","Teen models ki accuracy + 'Models + metric plots saved.'"],
 ["bank_simulation.py","'Served=... Avg wait=... Utilization=...' + 'Simulation plots saved.'"],
 ["streamlit run","'You can now view your Streamlit app...' + browser khul jaye."],
], [3200,6160]));

// ===================================================================
// 8. COMMON ERRORS
// ===================================================================
C.push(new Paragraph({children:[new PageBreak()]}));
C.push(h1("8. Aam Errors Aur Unka Hal"));

C.push(h3("Error: ModuleNotFoundError: No module named 'pandas'"));
C.push(p("Matlab: aapne 'python' se chalaya (jo 3.14 hai, khali). Hal: 'py -3.12' se chalao. Ya libraries install karo (Section 4 Step 2)."));

C.push(h3("Error: No such file or directory: 'requirements.txt'"));
C.push(p("Matlab: aap galat folder mein ho. Hal: terminal mein 'dir' chala kar dekho files dikh rahi hain ya nahi. Agar andar ek aur folder hai to 'cd Banking_Simulation_Project' likho."));

C.push(h3("Error: pandas install karte waqt lambi red error (meson / WinError 5)"));
C.push(p("Matlab: aap Python 3.14 use kar rahe ho jisme libraries build nahi hotin. Hal: Python 3.12 use karo (jo aap kar chuke ho)."));

C.push(h3("Error: 'py' is not recognized / No runtime matches 3.12"));
C.push(p("Matlab: Python 3.12 install nahi. Hal: 'py install 3.12' chalao."));

C.push(h3("Dashboard khula lekin Page 3 (prediction) pe error 'Models not found'"));
C.push(p("Matlab: aapne train_models.py nahi chalaya. Hal: pehle 'py -3.12 notebooks/train_models.py' chalao, phir dashboard."));

C.push(h3("Browser khud nahi khula"));
C.push(p("Hal: terminal mein jo link 'http://localhost:8501' dikhe, use copy karke browser mein khud paste karo."));

// ===================================================================
// 9. QUICK CHEAT SHEET
// ===================================================================
C.push(h1("9. Quick Cheat Sheet (Sab Kuch Ek Jagah)"));
C.push(p("Roz project chalane ke liye sirf yeh yaad rakho:"));
C.push(...code([
"# 1. VS Code mein project folder kholo, terminal kholo",
"",
"# 2. Yeh 4 commands chalao (pehli dafa saari, baad mein sirf aakhri):",
"py -3.12 notebooks/eda_analysis.py",
"py -3.12 notebooks/train_models.py",
"py -3.12 simulation/bank_simulation.py",
"py -3.12 -m streamlit run dashboard/app.py",
"",
"# 3. Band karne ke liye terminal pe: Ctrl + C"
]));
C.push(tip("Sone se pehle ek baat yaad rakho: is project mein 'python' kabhi mat likhna, hamesha 'py -3.12' likhna. Bas yahi ek cheez sab masail se bacha legi."));

C.push(new Paragraph({spacing:{before:400},alignment:AlignmentType.CENTER,
  children:[new TextRun({text:"— Guide Khatam. Best of luck, Sameel! —",italics:true,color:BLUE,size:22})]}));

// ---------- BUILD ----------
const doc = new Document({
  styles:{default:{document:{run:{font:FONT,size:22}}},
    paragraphStyles:[
      {id:"Heading1",name:"Heading 1",basedOn:"Normal",next:"Normal",quickFormat:true,
        run:{size:30,bold:true,font:FONT,color:NAVY},paragraph:{spacing:{before:300,after:160},outlineLevel:0}},
      {id:"Heading2",name:"Heading 2",basedOn:"Normal",next:"Normal",quickFormat:true,
        run:{size:25,bold:true,font:FONT,color:BLUE},paragraph:{spacing:{before:220,after:120},outlineLevel:1}},
      {id:"Heading3",name:"Heading 3",basedOn:"Normal",next:"Normal",quickFormat:true,
        run:{size:22,bold:true,font:FONT,color:"C0392B"},paragraph:{spacing:{before:160,after:80},outlineLevel:2}},
    ]},
  numbering:{config:[
    {reference:"bul",levels:[{level:0,format:LevelFormat.BULLET,text:"\u2022",alignment:AlignmentType.LEFT,
      style:{paragraph:{indent:{left:720,hanging:360}}}}]},
    {reference:"nm",levels:[{level:0,format:LevelFormat.DECIMAL,text:"%1.",alignment:AlignmentType.LEFT,
      style:{paragraph:{indent:{left:720,hanging:360}}}}]},
  ]},
  sections:[{
    properties:{page:{size:{width:12240,height:15840},margin:{top:1440,right:1440,bottom:1440,left:1440}}},
    footers:{default:new Footer({children:[new Paragraph({alignment:AlignmentType.CENTER,
      children:[new TextRun({children:["Banking Simulation Project — Guide   |   Page ",PageNumber.CURRENT],size:16,color:"888888"})]})]})},
    children:C
  }]
});
Packer.toBuffer(doc).then(buf=>{
  fs.writeFileSync(path.join(__dirname,'COMPLETE_GUIDE_RomanUrdu.docx'),buf);
  console.log("Guide written");
});
