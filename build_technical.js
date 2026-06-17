const fs = require('fs');
const path = require('path');
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, HeadingLevel, BorderStyle, WidthType, ShadingType,
  PageBreak, TableOfContents, PageNumber, Footer, LevelFormat } = require('docx');

const FONT = "Calibri";
const NAVY = "1F3864", BLUE = "2E5AAC", CODEBG = "F2F2F2", GREEN="1E6B3A", PURPLE="6A1B9A";
const border = { style: BorderStyle.SINGLE, size: 1, color: "BBBBBB" };
const borders = { top: border, bottom: border, left: border, right: border,
  insideHorizontal: border, insideVertical: border };

function h1(t){return new Paragraph({heading:HeadingLevel.HEADING_1,children:[new TextRun(t)]});}
function h2(t){return new Paragraph({heading:HeadingLevel.HEADING_2,children:[new TextRun(t)]});}
function h3(t){return new Paragraph({heading:HeadingLevel.HEADING_3,children:[new TextRun(t)]});}
function p(t){return new Paragraph({spacing:{after:120,line:278},children:[new TextRun(t)]});}
function pr(runs){return new Paragraph({spacing:{after:120,line:278},children:runs});}
function b(t){return new Paragraph({numbering:{reference:"bul",level:0},spacing:{after:60},children:[new TextRun(t)]});}
function num(t){return new Paragraph({numbering:{reference:"nm",level:0},spacing:{after:60},children:[new TextRun(t)]});}
function code(lines){
  return lines.map((l,i)=>new Paragraph({
    spacing:{after: i===lines.length-1?120:0, before: i===0?60:0},
    shading:{fill:CODEBG,type:ShadingType.CLEAR},
    border:{left:{style:BorderStyle.SINGLE,size:12,color:BLUE,space:6}},
    indent:{left:120},
    children:[new TextRun({text:l||" ",font:"Consolas",size:19,color:"1A1A1A"})]}));
}
function note(label,color,bg,t){return new Paragraph({spacing:{before:80,after:120},shading:{fill:bg,type:ShadingType.CLEAR},
  border:{left:{style:BorderStyle.SINGLE,size:14,color:color,space:6}},indent:{left:120},
  children:[new TextRun({text:label,bold:true,color:color}),new TextRun({text:t,color:"333333"})]});}
function tip(t){return note("💡 Yaad Rakho: ","8A6D00","FFF7E0",t);}
function key(t){return note("🔑 Asaan Lafzon Mein: ","1E6B3A","E8F5E9",t);}
function viva(t){return note("🎓 Viva Tip: ","6A1B9A","F3E5F5",t);}

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

// TITLE
C.push(new Paragraph({alignment:AlignmentType.CENTER,spacing:{before:2400,after:100},
  children:[new TextRun({text:"Project Ki Poori Technical Samajh",bold:true,size:44,color:NAVY})]}));
C.push(new Paragraph({alignment:AlignmentType.CENTER,spacing:{after:300},
  children:[new TextRun({text:"Dataset · Machine Learning Models · Simulation",size:26,color:BLUE})]}));
C.push(new Paragraph({alignment:AlignmentType.CENTER,spacing:{after:120},
  children:[new TextRun({text:"Har ek cheez detail mein — Roman Urdu",size:22,color:"444444"})]}));
C.push(new Paragraph({alignment:AlignmentType.CENTER,spacing:{before:1300},
  children:[new TextRun({text:"Banking Simulation Project — Sameel",size:20,color:"555555"})]}));
C.push(new Paragraph({alignment:AlignmentType.CENTER,spacing:{before:600},
  children:[new TextRun({text:"Yeh document evaluation/viva ke liye hai. Isme code chalane ka tareeqa nahi,",italics:true,size:19,color:"666666"})]}));
C.push(new Paragraph({alignment:AlignmentType.CENTER,
  children:[new TextRun({text:"balke yeh samjhaya gaya hai ke har cheez kaam KAISE karti hai aur KYUN.",italics:true,size:19,color:"666666"})]}));
C.push(new Paragraph({children:[new PageBreak()]}));

// TOC
C.push(h1("Fehrist"));
C.push(new TableOfContents("Contents",{hyperlink:true,headingStyleRange:"1-2"}));
C.push(new Paragraph({children:[new PageBreak()]}));

// =====================================================================
// PART 1: DATASET
// =====================================================================
C.push(h1("PART 1 — Dataset (Data Ki Poori Kahani)"));

C.push(h2("1.1 Dataset Kya Hai?"));
C.push(p("Machine learning mein 'dataset' woh purana record hota hai jis se computer seekhta hai. Hamara dataset 614 logon ka loan record hai — har banday ki info, aur yeh ke uska loan approve hua ya reject. Computer in 614 misalon ko dekh kar 'pattern' samajhta hai, phir naye banday ke liye prediction karta hai."));
C.push(tbl([
 ["Cheez","Tafseel"],
 ["Total rows (log)","614 loan applications"],
 ["Total columns","13"],
 ["Approve hue","74.3% (yani 74 mein se 100 approve hue)"],
 ["Reject hue","~25.7%"],
 ["Missing (khaali) values","145 khaane khaali the (jinhe humne bhara)"],
 ["Source","Kaggle Loan Prediction dataset schema"],
], [3200,6160]));
C.push(key("Dataset = ek bara table jisme har row ek banda hai aur har column us banday ki ek khaasiyat (jaise income, credit history)."));

C.push(h2("1.2 Saare 13 Columns Ka Matlab"));
C.push(p("Columns do tarah ke hote hain: 'Input' columns (jin se model seekhta hai) aur 'Target' column (jo model ko predict karna hai)."));
C.push(tbl([
 ["Column","Matlab","Type"],
 ["Loan_ID","Har application ka unique number","ID (ignore)"],
 ["Gender","Male / Female","Input"],
 ["Married","Shaadi-shuda hai ya nahi","Input"],
 ["Dependents","Kitne log us pe depend karte (0,1,2,3+)","Input"],
 ["Education","Graduate / Not Graduate","Input"],
 ["Self_Employed","Apna kaam karta hai ya naukri","Input"],
 ["ApplicantIncome","Khud ki income","Input"],
 ["CoapplicantIncome","Saath wale (jaise biwi) ki income","Input"],
 ["LoanAmount","Loan ki raqam (hazaron mein)","Input"],
 ["Loan_Amount_Term","Loan kitne mahinon ka hai (jaise 360)","Input"],
 ["Credit_History","Pehle qarz theek se chukaya? 1=haan, 0=nahi","Input (SABSE AHEM)"],
 ["Property_Area","Urban / Semiurban / Rural","Input"],
 ["Loan_Status","FINAL JAWAB: Y=approve, N=reject","TARGET"],
], [2500,5360,1500]));
C.push(viva("Agar poocha jaye 'sabse important feature kaunsa hai?' — jawab: Credit_History. Jiska credit record saaf hai uska loan approve hone ke chances bohat zyada hote hain."));

C.push(h2("1.3 Data Cleaning — Khaali Khaane Bharna"));
C.push(p("Asli data mein kuch khaane khaali (missing) hote hain — jaise kisi ne apni income nahi likhi. Machine learning aise khaali khaanon ke saath kaam nahi karti, to humein unhe bharna parta hai. Hum do tareeqe use karte hain:"));
C.push(tbl([
 ["Tareeqa","Kahan Use Hua","Kyun"],
 ["Mode (sabse common value) se bharna","Gender, Married, Dependents, Self_Employed, Credit_History","Yeh text/category columns hain, in mein jo value sabse zyada baar aati hai wahi bhar dete hain"],
 ["Median (darmiyani value) se bharna","LoanAmount, Loan_Amount_Term","Yeh number columns hain. Median outliers se mehfooz rehta hai (average ke muqable)"],
], [3000,3000,3360]));
C.push(key("Mode = jo cheez sabse zyada baar nazar aaye. Median = saare numbers ko line mein laga kar beech wala number. Average ki jagah median is liye ke ek bohat bara number (jaise koi crorepati) average ko kharab kar deta hai, median ko nahi."));

C.push(h2("1.4 Feature Engineering — Naye Columns Banana"));
C.push(p("'Feature engineering' ka matlab hai purane columns se naye, zyada kaam ke columns banana. Humne 4 naye banaye:"));
C.push(tbl([
 ["Naya Feature","Kaise Bana","Faida"],
 ["Total_Income","ApplicantIncome + CoapplicantIncome","Ghar ki total income ek hi number mein"],
 ["Income_Loan_Ratio","Total income / Loan amount","Banda loan ke muqable kitna kamata hai — repayment capacity"],
 ["LoanAmount_log","Loan amount ka logarithm","Bare numbers ko chhota karke model ko balance deta hai"],
 ["Total_Income_log","Total income ka logarithm","Income ki long tail ko theek karta hai"],
], [2400,3200,3760]));
C.push(key("'Log' transform ek mathematical trick hai jo bohat bare numbers (jaise 5 lakh income) ko chhote scale pe le aata hai, taake ek-do ameer log poore model ko apni taraf na kheench lein."));

C.push(h2("1.5 Encoding — Text Ko Numbers Mein Badalna"));
C.push(p("Computer 'Male', 'Female', 'Graduate' jaise lafz nahi samajhta — woh sirf numbers samajhta hai. To har text ko number mein badalte hain. Ise 'encoding' kehte hain:"));
C.push(...code([
"Gender:        Male = 1,      Female = 0",
"Married:       Yes = 1,       No = 0",
"Education:     Graduate = 1,  Not Graduate = 0",
"Property_Area: Urban = 2, Semiurban = 1, Rural = 0",
"Loan_Status:   Y = 1,        N = 0"
]));
C.push(p("Ab poora data sirf numbers ka ban gaya, jise model padh sakta hai."));

C.push(h2("1.6 EDA — Data Ko Charts Se Samajhna"));
C.push(p("EDA (Exploratory Data Analysis) ka matlab hai data ko graph bana kar dekhna taake patterns samajh aayein. Humne 5 tarah ke charts banaye:"));
C.push(tbl([
 ["Chart","Kya Dikhata Hai","Conclusion"],
 ["Histogram","Income/loan kis range mein hain","Income right-skewed hai (zyadatar log kam kamate, kuch bohat zyada)"],
 ["Boxplot","Outliers (anokhe bare numbers)","Kuch bohat ameer log hain — log transform se handle kiye"],
 ["Heatmap","Columns aapas mein kitne juray hain","Credit history ka approval se sabse strong rishta"],
 ["Bar Chart","Har category mein approval rate","Saaf credit history = zyada approval"],
 ["Pairplot","Do columns ka aapas mein milap","Approve/reject classes overlap karti hain (linear nahi)"],
], [2000,3760,3600]));
C.push(viva("Agar poocha 'income ko log kyun kiya?' — jawab: histogram aur boxplot mein income right-skewed thi aur usme outliers the, log transform ne unhe balance kar diya."));

// =====================================================================
// PART 2: ML MODELS
// =====================================================================
C.push(new Paragraph({children:[new PageBreak()]}));
C.push(h1("PART 2 — Machine Learning Models (Teen Models Ki Samajh)"));

C.push(h2("2.1 Machine Learning Kya Hai?"));
C.push(p("Machine learning mein hum computer ko rule nahi batate, balke misalein dikhate hain aur woh khud rule seekhta hai. Jaise bachay ko 100 kutton ki tasveerein dikhao to woh khud kutta pehchanna seekh jaata hai — waise hi computer 614 loan misalon se seekhta hai ke loan kab approve hota hai."));
C.push(key("Hum data ko 2 hisson mein baant'te hain: 80% se model SEEKHTA hai (training), aur 20% pe TEST karte hain ke usne sahi seekha ya nahi. Is se pata chalta hai model naye logon pe kitna sahi kaam karega."));

C.push(h2("2.2 Hamare Teen Models"));

C.push(h3("Model 1 — Logistic Regression"));
C.push(p("Yeh sabse simple model hai. Yeh har feature ko ek 'weight' (ahmiyat) deta hai aur unhe jorr kar ek probability (chance) nikaalta hai ke loan approve hoga ya nahi. Agar chance 50% se zyada to 'Approve', warna 'Reject'."));
C.push(b("Faida: Simple, tez, aur sabse important — interpretable (samajh aata hai ke kis cheez ne faisla badla)"));
C.push(b("Banks ko yeh pasand hai kyunke regulator ko bata sakte hain ke loan kyun reject hua"));
C.push(key("Soch lo ek scoring system: credit history ke 3 points, graduate ke 1 point, zyada income ke points... sab jorr kar agar score zyada to approve. Logistic regression aise hi kaam karta hai."));

C.push(h3("Model 2 — Decision Tree"));
C.push(p("Yeh ek 'agar-to' (if-else) sawalon ka darakht (tree) banata hai. Jaise: 'Credit history saaf hai? Agar haan to aage poochho income zyada hai? Agar haan to APPROVE.' Har sawal ek branch hai, aur aakhir mein patte (leaves) pe faisla hota hai."));
C.push(b("Faida: Insaan ki tarah sochta hai, samajhna asaan"));
C.push(b("Nuksaan: Akela tree thoda 'overfit' ho jaata hai (yani training data rata leta hai, naye data pe galti karta hai)"));

C.push(h3("Model 3 — Random Forest"));
C.push(p("Yeh ek nahi, balke 200 decision trees banata hai (forest = jungle of trees). Har tree thora alag hota hai. Phir saare trees vote karte hain aur jis taraf zyada vote hote hain wahi final faisla. 'Bohat saare logon ki raye ek banday se behtar hoti hai' — yahi iska usool hai."));
C.push(b("Faida: Akele tree se zyada accurate aur reliable, overfitting kam"));
C.push(b("Nuksaan: Samajhna mushkil (200 trees ka faisla explain karna mushkil), thora slow"));
C.push(viva("Agar poocha 'Random Forest aur Decision Tree mein farak?' — jawab: Decision Tree ek hi tree hai, Random Forest 200 trees ka group jo vote karke faisla karta hai, isliye zyada bharosemand."));

C.push(h2("2.3 Models Ki Performance — Numbers"));
C.push(p("Teeno models ko test karne ke baad yeh results aaye (yeh asli numbers hain aapke project se):"));
C.push(tbl([
 ["Model","Accuracy","Precision","Recall","F1 Score"],
 ["Logistic Regression","0.8943 (89%)","0.8824","0.989","0.9326"],
 ["Decision Tree","0.8618 (86%)","0.87","0.956","0.911"],
 ["Random Forest","0.8537 (85%)","0.8687","0.9451","0.9053"],
], [2600,1700,1700,1700,1660]));
C.push(pr([new TextRun({text:"Winner: ",bold:true,color:GREEN}),
  new TextRun({text:"Logistic Regression — sabse zyada accuracy (89%) aur F1 score, aur sabse aasaan samajhne wala.",bold:false})]));

C.push(h2("2.4 In 5 Numbers Ka Matlab (Bohat Zaroori)"));
C.push(p("Yeh 5 cheezein batati hain ke model kitna achha hai. Inhe samajhna viva ke liye must hai:"));
C.push(tbl([
 ["Metric","Matlab","Aasaan Misal"],
 ["Accuracy","Kitne % faisle sahi the","100 mein se 89 sahi = 89% accuracy"],
 ["Precision","Jinhe approve kaha, un mein se kitne sach much approve thay","Galat approve (risky loan) se bachata hai"],
 ["Recall","Jo sach much approve thay, un mein se kitne pakde","Achhe customer chhootne se bachata hai"],
 ["F1 Score","Precision aur Recall ka balance (average)","Dono ko ek number mein milata hai"],
 ["Confusion Matrix","Sahi/galat faislon ka 2x2 table","Kahan kahan galti hui, saaf dikhata hai"],
], [2200,3400,3760]));

C.push(h3("Confusion Matrix Ko Samajhna"));
C.push(p("Yeh ek chhota table hai jo 4 cheezein dikhata hai. Logistic Regression ka example (aapke project se):"));
C.push(tbl([
 ["","Model: Reject","Model: Approve"],
 ["Asli: Reject","20 (sahi)","12 (galti)"],
 ["Asli: Approve","1 (galti)","90 (sahi)"],
], [2800,3280,3280]));
C.push(p("Matlab: 20+90 = 110 faisle bilkul sahi, sirf 12+1 = 13 galat. Yeh achhi performance hai."));
C.push(key("Diagonal (20 aur 90) sahi faisle hain. Baqi do (12 aur 1) galtiyaan hain. Jitne zyada diagonal pe ho utna behtar model."));

C.push(h2("2.5 ROC Curve Kya Hai?"));
C.push(p("ROC curve ek graph hai jo dikhata hai model 'sahi approve' aur 'galat approve' ke darmiyan kitna achha farak karta hai. Curve jitni upar-bائیں taraf ho utna behtar. 'AUC' is curve ke neeche ka area hai — 1.0 perfect, 0.5 bilkul random (sikka uchhalne jaisa)."));
C.push(viva("ROC-AUC agar 0.8 se upar hai to model achha hai. Hamare models 0.77 se 0.83 ke darmiyan hain — solid performance."));

C.push(h2("2.6 Logistic Regression Hi Kyun Jeeta?"));
C.push(p("Aam taur pe Random Forest jeetta hai, lekin yahan Logistic Regression aage raha. Wajah:"));
C.push(num("Sabse bara factor (credit history) ka approval se rishta tقریباً seedha (linear) hai — simple model isay aasani se pakar leta hai."));
C.push(num("Hamara data chhota hai (sirf 614 rows). Chhote data pe complex models (tree) thora overfit ho jaate hain."));
C.push(num("Logistic Regression interpretable hai — banks ke liye yeh zaroori hai."));
C.push(viva("Yeh sawal viva mein zaroor aayega. Rata yaad rakho: 'Credit history ka rishta linear tha, data chhota tha, isliye simple Logistic Regression ne tree models ko maat di — aur woh interpretable bhi hai.'"));

C.push(h2("2.7 .pkl Files Kya Hain?"));
C.push(p("Jab model train ho jaata hai, hum usay file mein 'save' kar lete hain (jaise game ki progress save karte hain). In files ko .pkl (pickle) files kehte hain. Phir dashboard inhe load karke foran prediction karta hai — bina dobara train kiye. Isiliye 3 files banti hain: logistic.pkl, decisiontree.pkl, randomforest.pkl."));

// =====================================================================
// PART 3: SIMULATION
// =====================================================================
C.push(new Paragraph({children:[new PageBreak()]}));
C.push(h1("PART 3 — Bank Queue Simulation (Line Ka Nizaam)"));

C.push(h2("3.1 Simulation Kya Hai Aur Kyun?"));
C.push(p("Simulation ka matlab hai kisi asli cheez ko computer mein nakli tareeqe se chala kar dekhna — bina asli mein kiye. Yahan hum ek bank branch ko nakli chalate hain: customers aate hain, line lagti hai, tellers serve karte hain. Is se hum bina asli bank kholе yeh pata laga sakte hain ke kitne tellers honay chahiyein."));
C.push(key("Misal: agar aap janna chahte ho ke 3 tellers se log kitna wait karenge — to asli bank mein experiment karna mehenga aur risky hai. Simulation computer mein yeh free aur foran bata deti hai."));

C.push(h2("3.2 M/M/c Model — Yeh Naam Kya Hai?"));
C.push(p("Hamari simulation 'M/M/c' naam ke mashhoor queueing model pe bani hai. Is ke teen hisse hain:"));
C.push(tbl([
 ["Hissa","Matlab","Aasaan Samajh"],
 ["Pehla M","Markovian arrivals (Poisson)","Customers random time pe aate hain, fixed nahi"],
 ["Doosra M","Markovian service (Exponential)","Har customer ko serve karne ka time bhi random hai"],
 ["c","Number of servers","Kitne teller hain (jaise c=3)"],
], [1800,3400,4160]));
C.push(viva("Agar poocha 'M/M/c mein M ka kya matlab?' — jawab: pehla M = random (Poisson) arrivals, doosra M = random (exponential) service time, c = tellers ki tadaad."));

C.push(h2("3.3 Teen Zaroori Formulas"));
C.push(p("Simulation in mathematical usoolon pe chalti hai:"));
C.push(...code([
"Utilization (rho) = lambda / (c * mu)",
"",
"   lambda = customer aane ki rate",
"   mu     = ek teller ke serve karne ki rate",
"   c      = tellers ki tadaad",
"",
"System tabhi theek chalega jab rho < 1 ho",
"",
"Little's Law:  Wq = Lq / lambda",
"   (average wait time = line ki lambai / aane ki rate)"
]));
C.push(key("Rho (utilization) batata hai teller kitne busy hain. Agar rho = 1 ke kareeb to teller hamesha busy aur line bohat lambi. Agar rho chhota to teller khaali bethe. Behtareen jagah beech mein hai."));

C.push(h2("3.4 Hamari Baseline Settings"));
C.push(tbl([
 ["Setting","Value","Matlab"],
 ["Arrival (lambda)","Har ~4 min mein ek customer","Customer aane ki speed"],
 ["Service (mu)","Har customer ~10 min","Serve karne ka time"],
 ["Tellers (c)","3","Teen cashiers"],
 ["Sim time","480 min (8 ghante)","Poora bank ka din"],
 ["Result rho","0.83","Busy lekin stable (rho < 1)"],
], [2400,2800,4160]));
C.push(p("Hisaab: rho = 0.25 / (3 × 0.1) = 0.83. Yani teller 83% waqt busy rehte hain — masroof magar manageable."));

C.push(h2("3.5 SimPy — Yeh Kaam Kaise Karti Hai"));
C.push(p("SimPy ek Python library hai jo time ko aage barhati hai 'event by event' (waqia dar waqia). Yeh aise kaam karti hai:"));
C.push(num("Ek 'source' customers paida karta hai random waqfon se."));
C.push(num("Har customer ek teller maangta hai (SimPy mein teller ek 'Resource' hai jiski capacity = c)."));
C.push(num("Agar saare teller busy hon, customer khud-ba-khud line mein lag jaata hai."));
C.push(num("Serve hone ka time random (exponential) hota hai."));
C.push(num("Simulation har customer ka wait time, line ki lambai, aur teller ki busy-ness record karti hai."));

C.push(h2("3.6 Simulation Ke Natije (Outputs)"));
C.push(p("Simulation 3 graphs aur kuch numbers deti hai:"));
C.push(tbl([
 ["Output","Kya Dikhata Hai"],
 ["Average Wait Time","Customer ausatan kitni der line mein khara raha (~9-10 min)"],
 ["Customers Served","Poore din mein kitne customer serve hue (~100-110)"],
 ["Utilization","Teller kitne busy rahe (~79%)"],
 ["Queue Length Graph","Waqt ke saath line kitni lambi hoti gayi"],
 ["Waiting Time Graph","Kitne customers ne kitni der wait kiya"],
 ["Utilization Graph","Tellers barhane se utilization kaise girti hai"],
], [3000,6360]));

C.push(h2("3.7 Sabse Bara Sabaq (Conclusion)"));
C.push(p("Simulation se yeh trade-off (lain-dain) samajh aata hai:"));
C.push(b("Kam teller (1-2): teller bohat busy, lekin customers bohat der wait karte — bura experience"));
C.push(b("Zyada teller (5+): customers foran serve, lekin teller khaali bethe — paise ka zaaya"));
C.push(b("3 teller: dono ka behtareen balance — na zyada wait, na zyada khaali"));
C.push(viva("Simulation ka maqsad yahi hai: bank ko batana ke optimal kitne teller hain taake customer khush rahe aur paisa bhi na zaaya ho. Hamare case mein 3 teller best hain."));

// =====================================================================
// PART 4: SAB KUCH KAISE JURTA HAI
// =====================================================================
C.push(new Paragraph({children:[new PageBreak()]}));
C.push(h1("PART 4 — Teeno Hisse Aapas Mein Kaise Jurte Hain"));
C.push(p("Project ke teen hisse alag lagte hain lekin ek soch ke neeche aate hain — banking ko data se behtar banana:"));
C.push(num("Dataset: asli loan record jis se sab shuru hota hai."));
C.push(num("ML Models: us data se seekh kar naye loan ka faisla foran aur bharosemand tareeqe se karte hain."));
C.push(num("Simulation: branch mein customer flow ko model karke staffing optimize karti hai."));
C.push(num("Dashboard: in teeno ko ek screen pe la kar 'decision support tool' bana deta hai."));
C.push(key("Connection: agar loan faisla automatic aur tez ho jaye (ML se), to customer ka kaam jaldi nipat'ta hai, jis se simulation mein service time kam ho jaata hai — yani dono ek doosre ki madad karte hain."));

C.push(h2("Aap Ke Project Mein Konsi Technology Kahan"));
C.push(tbl([
 ["Library/Tool","Kahan Use Hui"],
 ["Pandas","Data load aur clean karne ke liye"],
 ["NumPy","Numbers aur math (jaise log transform)"],
 ["Matplotlib + Seaborn","Saare charts aur graphs"],
 ["Scikit-Learn","Teeno ML models train karne ke liye"],
 ["SimPy","Bank queue simulation"],
 ["Streamlit","Interactive dashboard"],
 ["Joblib","Models ko .pkl files mein save karne ke liye"],
], [2800,6560]));

C.push(new Paragraph({spacing:{before:400},alignment:AlignmentType.CENTER,
  children:[new TextRun({text:"— Document Khatam. Ab aapko project ki har cheez ki samajh hai. Best of luck! —",italics:true,color:BLUE,size:21})]}));

// BUILD
const doc = new Document({
  styles:{default:{document:{run:{font:FONT,size:22}}},
    paragraphStyles:[
      {id:"Heading1",name:"Heading 1",basedOn:"Normal",next:"Normal",quickFormat:true,
        run:{size:30,bold:true,font:FONT,color:NAVY},paragraph:{spacing:{before:300,after:160},outlineLevel:0}},
      {id:"Heading2",name:"Heading 2",basedOn:"Normal",next:"Normal",quickFormat:true,
        run:{size:25,bold:true,font:FONT,color:BLUE},paragraph:{spacing:{before:220,after:120},outlineLevel:1}},
      {id:"Heading3",name:"Heading 3",basedOn:"Normal",next:"Normal",quickFormat:true,
        run:{size:22,bold:true,font:FONT,color:PURPLE},paragraph:{spacing:{before:160,after:80},outlineLevel:2}},
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
      children:[new TextRun({children:["Project Ki Poori Technical Samajh   |   Page ",PageNumber.CURRENT],size:16,color:"888888"})]})]})},
    children:C
  }]
});
Packer.toBuffer(doc).then(buf=>{
  fs.writeFileSync(path.join(__dirname,'TECHNICAL_EXPLANATION_RomanUrdu.docx'),buf);
  console.log("Technical doc written");
});
