"""
Banking Operations Simulator — VIEW (Scene)
============================================
Builds the full animated banking floor: cashier counter (left), loan counter
(right), bank manager office (top-right), entrance/exit (left edge), reception
sign, queue rails. Includes a top control bar, live status, simulation clock,
and live KPI dashboard.
"""
import json


def build_simulator(officer_svg, cashier_svg, manager_svg, customer_svgs, day_data_json, mode="full"):
    return (_SCENE
            .replace("/*OFFICER*/", officer_svg)
            .replace("/*CASHIER*/", cashier_svg)
            .replace("/*MANAGER*/", manager_svg)
            .replace("'__CUSTS__'", json.dumps(customer_svgs))
            .replace("'__DAYS__'", day_data_json)
            .replace("__MODE__", mode))


_SCENE = r"""
<div id="bsRoot">
<style>
  #bsRoot *{box-sizing:border-box;}
  #bsRoot{font-family:'Inter','Segoe UI',system-ui,sans-serif;color:#0f2547;}
  .bs-app{background:#eef2f9;border-radius:16px;overflow:hidden;border:1px solid #ccd6e8;box-shadow:0 8px 24px #0f254712;}

  /* ===== HEADER ===== */
  .bs-bar{display:flex;align-items:center;justify-content:space-between;
    background:linear-gradient(90deg,#003d2b,#005a3f 60%,#00805a);color:#fff;padding:12px 18px;
    border-bottom:2px solid #00b894;}
  .bs-brand{display:flex;align-items:center;gap:12px;}
  .bs-logo{width:36px;height:36px;border-radius:8px;background:linear-gradient(135deg,#00b894,#00805a);
    display:flex;align-items:center;justify-content:center;color:#fff;font-weight:900;font-size:18px;
    box-shadow:0 2px 8px #00b89440;}
  .bs-name{font-weight:800;font-size:17px;letter-spacing:.4px;}
  .bs-tag{font-size:10px;color:#a8c2f0;font-weight:500;margin-top:1px;letter-spacing:1px;}
  .bs-status{display:flex;align-items:center;gap:18px;}
  .bs-stat-pill{display:flex;align-items:center;gap:6px;background:#ffffff14;padding:5px 12px;border-radius:20px;
    font-size:12px;backdrop-filter:blur(6px);}
  .bs-dot{width:8px;height:8px;border-radius:50%;background:#27ae60;box-shadow:0 0 8px #27ae60;}
  .bs-dot.paused{background:#f39c12;box-shadow:0 0 8px #f39c12;animation:pulse 1s infinite;}
  .bs-dot.stopped{background:#e74c3c;box-shadow:0 0 8px #e74c3c;}
  @keyframes pulse{50%{opacity:0.4;}}
  .bs-clock{font-variant-numeric:tabular-nums;font-weight:700;font-size:14px;}

  /* ===== CONTROL BAR ===== */
  .bs-ctrl{display:flex;gap:10px;align-items:center;flex-wrap:wrap;padding:12px 18px;background:#fff;
    border-bottom:1px solid #e0e6f0;}
  .bs-btn{border:none;padding:9px 18px;border-radius:9px;font-weight:700;font-size:13px;cursor:pointer;
    color:#fff;transition:all .15s;display:flex;align-items:center;gap:6px;box-shadow:0 2px 6px #0002;}
  .bs-btn:hover{transform:translateY(-1px);box-shadow:0 4px 10px #0003;}
  .bs-btn:active{transform:translateY(0);}
  .bs-run{background:linear-gradient(135deg,#27ae60,#1c8e4e);}
  .bs-pause{background:linear-gradient(135deg,#f39c12,#d68910);}
  .bs-stop{background:linear-gradient(135deg,#e74c3c,#c0392b);}
  .bs-reset{background:linear-gradient(135deg,#7f8c8d,#5d6d6e);}
  .bs-btn:disabled{opacity:0.4;cursor:not-allowed;transform:none;}
  .bs-spd{display:flex;gap:4px;margin-left:auto;align-items:center;background:#f4f7fc;padding:4px;border-radius:8px;}
  .bs-spd .lbl{font-size:11px;color:#6b7c99;margin:0 6px;font-weight:600;}
  .bs-sp{background:transparent;color:#1c4a96;border:none;padding:5px 10px;border-radius:5px;cursor:pointer;
    font-size:12px;font-weight:700;}
  .bs-sp.on{background:#1c4a96;color:#fff;}
  .bs-audio{margin-left:10px;background:#e8eef9;color:#1c4a96;border:none;padding:7px 12px;border-radius:8px;
    cursor:pointer;font-weight:700;font-size:13px;}

  /* ===== STAGE: BANK FLOOR ===== */
  .bs-stage{position:relative;height:440px;
    background:
      linear-gradient(180deg,#d8e2f4 0%,#d8e2f4 28%,#e8ecf2 28%,#dde2ed 100%);
    overflow:hidden;border-bottom:1px solid #ccd6e8;}
  /* back wall sign */
  .bs-sign{position:absolute;top:10px;left:50%;transform:translateX(-50%);
    background:linear-gradient(180deg,#003d2b,#005a3f);color:#fff;padding:7px 26px;border-radius:6px;
    font-weight:900;letter-spacing:3px;font-size:13px;box-shadow:0 4px 12px #0003;border:2px solid #00b894;}
  .bs-sign small{display:block;color:#fff;font-size:8px;letter-spacing:3px;font-weight:600;text-align:center;}
  /* marble floor lines */
  .bs-floor{position:absolute;bottom:0;left:0;right:0;height:72%;
    background-image:linear-gradient(#ffffff60 1px,transparent 1px),linear-gradient(90deg,#9fb2d044 1px,transparent 1px);
    background-size:56px 32px;}
  /* entrance */
  .bs-door{position:absolute;left:10px;bottom:50px;width:62px;height:130px;border-radius:6px 6px 0 0;
    background:linear-gradient(180deg,#3a5c92,#1a3360);border:3px solid #5b86e0;
    box-shadow:inset 0 0 20px #ffffff22;}
  .bs-door:after{content:"ENTRANCE";position:absolute;bottom:-22px;left:-3px;width:68px;text-align:center;
    font-size:9px;color:#1c4a96;font-weight:800;letter-spacing:1px;}
  .bs-door-glass{position:absolute;inset:5px;background:linear-gradient(180deg,#7da3d955,#4a72b022);
    border-left:1px solid #ffffff55;}
  /* reception desk */
  .bs-recep{position:absolute;left:90px;top:60px;width:120px;height:38px;
    background:linear-gradient(180deg,#8b6b3a,#6b4e25);border-radius:6px;
    box-shadow:0 4px 10px #0003;}
  .bs-recep-sign{position:absolute;left:104px;top:42px;color:#1c4a96;font-size:9px;font-weight:800;letter-spacing:2px;}
  /* CASHIER counter (left half, lower) */
  .bs-cash-zone{position:absolute;bottom:50px;}
  .bs-cash-zone.c1{left:170px;}
  .bs-cash-zone.c2{left:368px;}
  .bs-cash-desk{width:140px;height:70px;
    background:linear-gradient(180deg,#7a5230,#5e3f23);border-radius:6px 6px 4px 4px;
    box-shadow:0 6px 14px #0003;border-top:4px solid #92633c;}
  .bs-cash-label{position:absolute;top:-58px;left:0;width:140px;text-align:center;
    font-size:11px;font-weight:800;color:#0a1f4a;letter-spacing:1.5px;}
  .bs-cash-glass{position:absolute;top:-40px;left:8px;width:124px;height:26px;
    background:linear-gradient(180deg,#a8c8e833,#7da3d922);border:1px solid #b8d2ef;border-radius:4px 4px 0 0;}
  .bs-cash-mon{position:absolute;top:-34px;left:42px;width:48px;height:28px;background:#0d2138;
    border:2px solid #2c3e5c;border-radius:3px;overflow:hidden;}
  .bs-cash-mon .scr{position:absolute;inset:2px;background:#0f3b66;color:#9fe3ff;font-size:6px;padding:2px;line-height:1.3;}
  .bs-cash-mon-2{display:none;}
  .bs-cashier{position:absolute;bottom:90px;z-index:3;}
  .bs-cashier.c1{left:240px;}
  .bs-cashier.c2{left:438px;}
  .cashier-armR{transform-origin:top center;}
  .bs-typing-c .cashier-armR{animation:type .4s ease-in-out infinite;}
  @keyframes type{0%,100%{transform:rotate(0);}50%{transform:rotate(-15deg);}}

  /* LOAN counter (right side, lower) */
  .bs-loan-zone{position:absolute;right:25px;bottom:50px;}
  .bs-loan-desk{width:180px;height:74px;
    background:linear-gradient(180deg,#7a5230,#5e3f23);border-radius:6px 6px 4px 4px;
    box-shadow:0 6px 14px #0003;border-top:4px solid #92633c;}
  .bs-loan-label{position:absolute;top:-66px;left:0;width:180px;text-align:center;
    font-size:11px;font-weight:800;color:#0a1f4a;letter-spacing:1.5px;}
  .bs-loan-glass{position:absolute;top:-46px;left:10px;width:160px;height:30px;
    background:linear-gradient(180deg,#a8c8e833,#7da3d922);border:1px solid #b8d2ef;border-radius:4px 4px 0 0;}
  .bs-loan-mon{position:absolute;top:-38px;left:60px;width:60px;height:32px;background:#0d2138;
    border:2px solid #2c3e5c;border-radius:3px;overflow:hidden;}
  .bs-loan-mon .scr{position:absolute;inset:2px;background:#0f3b66;color:#9fe3ff;font-size:6px;padding:2px;line-height:1.3;}
  .bs-officer{position:absolute;bottom:90px;right:85px;z-index:3;}
  .officer-armR{transform-origin:top center;}
  .bs-typing-l .officer-armR{animation:type .4s ease-in-out infinite;}

  /* MANAGER OFFICE (top right corner) */
  .bs-mgr-room{position:absolute;top:42px;right:30px;width:180px;height:120px;
    background:linear-gradient(180deg,#f7e8c8,#e8d4a0);
    border:3px solid #6b4e25;border-radius:6px;box-shadow:0 6px 16px #0004;overflow:hidden;}
  .bs-mgr-room:before{content:"MANAGER OFFICE";position:absolute;top:-2px;left:0;right:0;
    background:#003d2b;color:#fff;text-align:center;font-size:9px;font-weight:800;padding:3px;letter-spacing:1.5px;}
  .bs-mgr-window{position:absolute;top:20px;right:8px;width:50px;height:42px;
    background:linear-gradient(180deg,#a8c8e8,#7da3d9);border:2px solid #6b4e25;border-radius:3px;}
  .bs-mgr-window:after{content:"";position:absolute;top:50%;left:0;right:0;height:1px;background:#6b4e25;}
  .bs-mgr-desk{position:absolute;bottom:8px;left:8px;width:120px;height:24px;
    background:linear-gradient(180deg,#7a5230,#5e3f23);border-radius:3px;}
  .bs-mgr-person{position:absolute;bottom:32px;left:14px;}

  /* queue rails (red+gold ribbon) */
  .bs-rail{position:absolute;height:3px;background:repeating-linear-gradient(90deg,#9b1c1c,#9b1c1c 12px,#c0a000 12px,#c0a000 16px);border-radius:2px;}
  .bs-rail-post{position:absolute;width:5px;height:28px;background:linear-gradient(180deg,#aab4c6,#7a839a);border-radius:2px;}

  /* ===== PEOPLE / ANIMATIONS ===== */
  .bs-person{position:absolute;bottom:50px;z-index:4;transition:left .55s linear,bottom .55s linear;}
  @keyframes leg-l{0%,100%{transform:rotate(22deg);}50%{transform:rotate(-22deg);}}
  @keyframes leg-r{0%,100%{transform:rotate(-22deg);}50%{transform:rotate(22deg);}}
  @keyframes arm-l{0%,100%{transform:rotate(-18deg);}50%{transform:rotate(18deg);}}
  @keyframes arm-r{0%,100%{transform:rotate(18deg);}50%{transform:rotate(-18deg);}}
  @keyframes bob{0%,100%{transform:translateY(0);}50%{transform:translateY(-1.5px);}}
  .bs-walking .bs-fig{animation:bob .42s ease-in-out infinite;}
  .bs-walking .leg-l{animation:leg-l .42s ease-in-out infinite;transform-origin:50% 0;}
  .bs-walking .leg-r{animation:leg-r .42s ease-in-out infinite;transform-origin:50% 0;}
  .bs-walking .arm-l{animation:arm-l .42s ease-in-out infinite;transform-origin:50% 0;}
  .bs-walking .arm-r{animation:arm-r .42s ease-in-out infinite;transform-origin:50% 0;}
  .bs-person.facing-left .bs-fig{transform:scaleX(-1);}

  /* speech bubble for emotion */
  .bs-bubble{position:absolute;bottom:178px;background:#fff;border:2px solid #1c4a96;border-radius:10px;
    padding:5px 11px;font-size:12px;font-weight:700;color:#13315e;z-index:9;white-space:nowrap;
    box-shadow:0 4px 10px #0003;transition:opacity .35s;}
  .bs-bubble:after{content:"";position:absolute;bottom:-7px;left:18px;border:6px solid transparent;border-top-color:#1c4a96;}
  .bs-bubble.ok{border-color:#1c7a4a;color:#0f5a34;}.bs-bubble.ok:after{border-top-color:#1c7a4a;}
  .bs-bubble.bad{border-color:#b03a2e;color:#8a2418;}.bs-bubble.bad:after{border-top-color:#b03a2e;}

  /* result card (loan decision) */
  .bs-result{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%) scale(0.7);
    background:#fff;border-radius:14px;padding:20px 28px;text-align:center;
    box-shadow:0 20px 50px #0a1f4a55;z-index:30;opacity:0;pointer-events:none;
    transition:all .35s cubic-bezier(.34,1.56,.64,1);min-width:280px;}
  .bs-result.show{opacity:1;transform:translate(-50%,-50%) scale(1);}
  .bs-result.ok{border-top:5px solid #27ae60;}
  .bs-result.no{border-top:5px solid #e74c3c;}
  .bs-result .ico{font-size:38px;line-height:1;margin-bottom:6px;}
  .bs-result .hd{font-size:18px;font-weight:900;letter-spacing:1px;}
  .bs-result.ok .hd{color:#0f5a34;}
  .bs-result.no .hd{color:#8a2418;}
  .bs-result .nm{font-size:13px;color:#13315e;margin-top:4px;}
  .bs-result .det{font-size:11px;color:#6b7c99;margin-top:8px;line-height:1.5;}
  .bs-result .amt{font-size:15px;font-weight:800;color:#0a1f4a;margin-top:6px;}
  @keyframes confetti{0%{transform:translateY(-10px) rotate(0);opacity:1;}100%{transform:translateY(140px) rotate(360deg);opacity:0;}}
  .bs-conf{position:absolute;width:8px;height:8px;animation:confetti 1.5s ease-out forwards;}

  /* ===== KPI DASHBOARD ===== */
  .bs-kpis{display:grid;grid-template-columns:repeat(6,1fr);gap:10px;padding:14px 18px;background:#fff;}
  .bs-kpi{background:linear-gradient(180deg,#f7faff,#eef3fb);border:1px solid #dde7f5;border-radius:11px;
    padding:11px 13px;position:relative;overflow:hidden;}
  .bs-kpi .icn{position:absolute;top:8px;right:10px;font-size:18px;opacity:0.25;}
  .bs-kpi .v{font-size:22px;font-weight:800;color:#13315e;font-variant-numeric:tabular-nums;}
  .bs-kpi .l{font-size:10px;color:#6b7c99;margin-top:1px;font-weight:600;text-transform:uppercase;letter-spacing:.5px;}
  .bs-kpi.green .v{color:#1c7a4a;} .bs-kpi.red .v{color:#b03a2e;}
  .bs-kpi.blue .v{color:#1c4a96;}

  /* ===== END OF DAY REPORT ===== */
  .bs-report{padding:14px 18px;background:linear-gradient(135deg,#003d2b,#005a3f);color:#fff;display:none;}
  .bs-report.show{display:block;}
  .bs-report-hd{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;}
  .bs-report-hd h3{margin:0;font-size:15px;font-weight:800;letter-spacing:.5px;}
  .bs-report-hd .day-badge{background:#00b894;color:#fff;padding:4px 11px;border-radius:6px;font-weight:800;font-size:12px;}
  .bs-report-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;}
  .bs-rcard{background:#ffffff12;backdrop-filter:blur(8px);padding:10px;border-radius:9px;border:1px solid #ffffff20;}
  .bs-rcard .v{font-size:20px;font-weight:800;}
  .bs-rcard .l{font-size:10px;color:#a8c2f0;margin-top:2px;font-weight:600;}
  @media(max-width:900px){.bs-kpis{grid-template-columns:repeat(3,1fr);}.bs-report-grid{grid-template-columns:repeat(2,1fr);}}
</style>

<div class="bs-app">
  <!-- HEADER -->
  <div class="bs-bar">
    <div class="bs-brand">
      <div class="bs-logo">M</div>
      <div><div class="bs-name">Meezan Bank — Operations Simulator</div>
        <div class="bs-tag">LIVE QUEUE & TRANSACTION SIMULATION</div></div>
    </div>
    <div class="bs-status">
      <div class="bs-stat-pill"><span class="bs-dot stopped" id="bsDot"></span>
        <span id="bsStat">STOPPED</span></div>
      <div class="bs-stat-pill">Day <b id="bsDay" style="margin-left:5px;">0</b></div>
      <div class="bs-stat-pill bs-clock" id="bsClock">09:00 AM</div>
      <div class="bs-stat-pill">Speed <b id="bsSpdLbl" style="margin-left:5px;">2x</b></div>
    </div>
  </div>

  <!-- CONTROL BAR -->
  <div class="bs-ctrl">
    <button class="bs-btn bs-run" id="bsRun">&#9654; Run</button>
    <button class="bs-btn bs-pause" id="bsPause" disabled>&#10074;&#10074; Pause</button>
    <button class="bs-btn bs-stop" id="bsStop" disabled>&#9632; Stop</button>
    <button class="bs-btn bs-reset" id="bsReset">&#8634; Reset</button>
    <button class="bs-audio" id="bsAudio">&#128266; Audio On</button>
    <div class="bs-spd">
      <span class="lbl">SPEED</span>
      <button class="bs-sp" data-s="1">1x</button>
      <button class="bs-sp on" data-s="2">2x</button>
      <button class="bs-sp" data-s="4">4x</button>
      <button class="bs-sp" data-s="8">8x</button>
    </div>
  </div>

  <!-- STAGE -->
  <div class="bs-stage" id="bsStage">
    <div class="bs-sign">MEEZAN BANK<small>ISLAMIC BANKING</small></div>
    <div class="bs-floor"></div>
    <div class="bs-door"><div class="bs-door-glass"></div></div>

    <div class="bs-recep"></div>
    <div class="bs-recep-sign">RECEPTION</div>

    <div class="bs-cash-zone c1">
      <div class="bs-cash-glass"></div>
      <div class="bs-cash-mon"><div class="scr" id="bsCashScr1">&gt; teller 1<br>&gt; ready</div></div>
      <div class="bs-cash-label">CASHIER 1</div>
      <div class="bs-cash-desk"></div>
    </div>
    <div class="bs-cashier c1" id="bsCashier1">/*CASHIER*/</div>
    <div class="bs-cash-zone c2">
      <div class="bs-cash-glass"></div>
      <div class="bs-cash-mon"><div class="scr" id="bsCashScr2">&gt; teller 2<br>&gt; ready</div></div>
      <div class="bs-cash-label">CASHIER 2</div>
      <div class="bs-cash-desk"></div>
    </div>
    <div class="bs-cashier c2" id="bsCashier2">/*CASHIER*/</div>

    <div class="bs-loan-zone">
      <div class="bs-loan-glass"></div>
      <div class="bs-loan-mon"><div class="scr" id="bsLoanScreen">&gt; ML system<br>&gt; ready</div></div>
      <div class="bs-loan-label">LOAN COUNTER</div>
      <div class="bs-loan-desk"></div>
    </div>
    <div class="bs-officer" id="bsOfficer">/*OFFICER*/</div>

    <div class="bs-mgr-room">
      <div class="bs-mgr-window"></div>
      <div class="bs-mgr-desk"></div>
      <div class="bs-mgr-person">/*MANAGER*/</div>
    </div>

    <div class="bs-result" id="bsResult"></div>
  </div>

  <!-- KPI DASHBOARD -->
  <div class="bs-kpis">
    <div class="bs-kpi blue"><div class="icn">&#128100;</div>
      <div class="v" id="kActive">0</div><div class="l">Active in Bank</div></div>
    <div class="bs-kpi"><div class="icn">&#128241;</div>
      <div class="v" id="kCashQ">0</div><div class="l">Cashier Queue</div></div>
    <div class="bs-kpi"><div class="icn">&#128241;</div>
      <div class="v" id="kLoanQ">0</div><div class="l">Loan Queue</div></div>
    <div class="bs-kpi green"><div class="icn">&#10003;</div>
      <div class="v" id="kAppr">0</div><div class="l">Approved Today</div></div>
    <div class="bs-kpi red"><div class="icn">&#10007;</div>
      <div class="v" id="kRej">0</div><div class="l">Rejected Today</div></div>
    <div class="bs-kpi blue"><div class="icn">&#128181;</div>
      <div class="v" id="kServed">0</div><div class="l">Cashier Served</div></div>
  </div>

  <!-- END OF DAY REPORT -->
  <div class="bs-report" id="bsReport">
    <div class="bs-report-hd">
      <h3>&#128202; SIMULATION REPORT</h3>
      <div class="day-badge" id="bsRptDay">Day 1</div>
    </div>
    <div class="bs-report-grid" id="bsRptGrid"></div>
  </div>
</div>

<script>
(function(){
  const CUSTS='__CUSTS__';
  const DAYS='__DAYS__';
  const stage=document.getElementById('bsStage');
  const officer=document.getElementById('bsOfficer');
  

  // ===== STATE =====
  let speed=2, running=false, paused=false, audioOn=true; const MODE='__MODE__';
  let dayIdx=0, simMin=0, loopT=null;
  let cashQueue=[], cashIdx=0; const cashSlots=[null,null]; const cashSrvT=[0,0]; const cashEls=['bsCashier1','bsCashier2'];
  let loanQueue=[], loanIdx=0, loanServing=null, loanServeT=0, loanPhase='idle', loanPhaseT=0;
  let activeBank=0;
  // per-day metrics
  let mAppr=0, mRej=0, mCashServed=0, mWaitSum=0, mWaitN=0, mQSum=0, mQN=0;
  // cumulative (whole period)
  let totAppr=0, totRej=0, totCash=0, totLoan=0;
  const dailyLog=[];  // {day, loans, approved, rejected, cashier, avgWait}

  // ===== GEOMETRY =====
  const DOOR_X=18;
  const CASH_Q_X=170, CASH_Q_DX=42; const CASH_SERVE_X=[262,460];
  const LOAN_Q_X=380, LOAN_Q_DX=42, LOAN_SERVE_X=W()-200;
  function W(){return stage.clientWidth || 900;}
  const FLOOR_B=50;

  // place rails
  function makeRails(){
    const cR=document.createElement('div');cR.className='bs-rail';
    cR.style.left=CASH_Q_X+'px';cR.style.width=(CASH_Q_DX*3)+'px';cR.style.bottom='42px';
    stage.appendChild(cR);
    const lR=document.createElement('div');lR.className='bs-rail';
    lR.style.left=LOAN_Q_X+'px';lR.style.width=(LOAN_Q_DX*3)+'px';lR.style.bottom='42px';
    stage.appendChild(lR);
  }
  makeRails();

  // ===== CLOCK =====
  function clockStr(){
    let m=9*60+Math.floor(simMin); let hh=Math.floor(m/60),mm=m%60;
    const ap=hh>=12?'PM':'AM'; let h12=hh%12; if(h12===0)h12=12;
    return String(h12).padStart(2,'0')+':'+String(mm).padStart(2,'0')+' '+ap;
  }

  // ===== PEOPLE =====
  function makePerson(data, area){
    const el=document.createElement('div');
    el.className='bs-person bs-walking';
    el.innerHTML=CUSTS[data.variant % CUSTS.length];
    el.style.left=DOOR_X+'px';
    el.style.bottom=FLOOR_B+'px';
    stage.appendChild(el);
    activeBank++;
    return {el, data, area, arriveTime:simMin};
  }
  function moveTo(p,x){p.el.style.left=x+'px';}
  function walk(p,on){if(on)p.el.classList.add('bs-walking');else p.el.classList.remove('bs-walking');}
  function facingLeft(p,on){if(on)p.el.classList.add('facing-left');else p.el.classList.remove('facing-left');}
  function remove(p){
    if(p.el && p.el.parentNode) p.el.parentNode.removeChild(p.el);
    activeBank=Math.max(0,activeBank-1);
  }

  // ===== QUEUE LAYOUT =====
  function layoutCashQueue(){
    cashQueue.forEach((p,i)=>{moveTo(p,CASH_Q_X+i*CASH_Q_DX);walk(p,i>0);facingLeft(p,false);});
    document.getElementById('kCashQ').textContent=cashQueue.length;
    mQSum+=cashQueue.length+loanQueue.length; mQN++;
  }
  function layoutLoanQueue(){
    loanQueue.forEach((p,i)=>{moveTo(p,LOAN_Q_X+i*LOAN_Q_DX);walk(p,i>0);facingLeft(p,false);});
    document.getElementById('kLoanQ').textContent=loanQueue.length;
  }

  // ===== BUBBLES =====
  function bubble(p,txt,cls){
    const b=document.createElement('div');
    b.className='bs-bubble '+(cls||'');
    b.textContent=txt;
    b.style.left=(parseInt(p.el.style.left)-12)+'px';
    stage.appendChild(b);
    setTimeout(()=>{b.style.opacity='0';},1700);
    setTimeout(()=>{if(b.parentNode)b.parentNode.removeChild(b);},2100);
  }

  // ===== VOICE =====
  function speak(txt){
    if(!audioOn || !window.speechSynthesis)return;
    try{
      const u=new SpeechSynthesisUtterance(txt);
      u.rate=1.0; u.pitch=1.0; u.volume=0.9;
      window.speechSynthesis.cancel();
      window.speechSynthesis.speak(u);
    }catch(e){}
  }

  // ===== RESULT CARD =====
  function showResult(a){
    const r=document.getElementById('bsResult');
    const ok=a.decision==='APPROVED';
    r.className='bs-result '+(ok?'ok':'no')+' show';
    r.innerHTML=
      '<div class="ico">'+(ok?'&#127881;':'&#128577;')+'</div>'+
      '<div class="hd">'+(ok?'LOAN APPROVED':'LOAN REJECTED')+'</div>'+
      '<div class="nm">'+a.name+'</div>'+
      '<div class="amt">Rs. '+(a.loan_amount*1000).toLocaleString()+'</div>'+
      '<div class="det">Risk Score: <b>'+a.risk_score+'</b> &nbsp; • &nbsp; '+a.reason+'<br>'+
      'Model probability: '+(a.probability*100).toFixed(1)+'%</div>';
    if(ok){
      // confetti
      for(let i=0;i<14;i++){
        const c=document.createElement('div'); c.className='bs-conf';
        c.style.background=['#fcc94a','#27ae60','#1c4a96','#e74c3c'][i%4];
        c.style.left=(140+Math.random()*200)+'px'; c.style.top='30%';
        c.style.animationDelay=(i*0.05)+'s';
        r.parentNode.appendChild(c);
        setTimeout(()=>{if(c.parentNode)c.parentNode.removeChild(c);},2000);
      }
      speak('Congratulations. Your loan application has been approved.');
    } else {
      speak('We are sorry. Your loan application has not been approved.');
    }
    setTimeout(()=>{r.classList.remove('show');},2800/Math.max(speed/2,1));
  }

  // ===== STATUS UPDATE =====
  function setStatus(s){
    const d=document.getElementById('bsDot'),t=document.getElementById('bsStat');
    d.className='bs-dot '+(s==='Running'?'':s==='Paused'?'paused':'stopped');
    t.textContent=s.toUpperCase();
  }

  function updateKPIs(){
    document.getElementById('bsClock').textContent=clockStr();
    document.getElementById('bsDay').textContent=dayIdx+1;
    document.getElementById('kActive').textContent=activeBank;
    document.getElementById('kAppr').textContent=mAppr;
    document.getElementById('kRej').textContent=mRej;
    document.getElementById('kServed').textContent=mCashServed;
  }

  // ===== CASHIER SERVICE =====
  function startCashService(p,slot){
    cashSlots[slot]=p; walk(p,false); moveTo(p,CASH_SERVE_X[slot]); p.el.style.bottom=(FLOOR_B+6)+'px';
    cashSrvT[slot]=p.data.service_time;
    document.getElementById(cashEls[slot]).classList.add('bs-typing-c');
    document.getElementById('bsCashScr'+(slot+1)).innerHTML='&gt; teller '+(slot+1)+'<br>&gt; '+p.data.service.toLowerCase();
  }
  function tickCashService(dt,slot){
    cashSrvT[slot]-=dt;
    if(cashSrvT[slot]<=0){
      const p=cashSlots[slot];
      mCashServed++; totCash++;
      const wait=Math.max(0,simMin-p.arriveTime); mWaitSum+=wait; mWaitN++;
      bubble(p,'Thanks!','ok');
      walk(p,true); facingLeft(p,true); moveTo(p,DOOR_X);
      const gone=p; cashSlots[slot]=null;
      document.getElementById(cashEls[slot]).classList.remove('bs-typing-c');
      document.getElementById('bsCashScr'+(slot+1)).innerHTML='&gt; teller '+(slot+1)+'<br>&gt; ready';
      setTimeout(()=>remove(gone),1100);
    }
  }

  // ===== LOAN PROCESSING (multi-phase) =====
  const LOAN_PHASES=['walkin','analyzing','credit','risk','decision','reveal','leave'];
  function startLoanService(p){
    loanServing=p; walk(p,false); moveTo(p,LOAN_SERVE_X); p.el.style.bottom=(FLOOR_B+6)+'px';
    loanPhase='analyzing'; loanPhaseT=0;
    document.getElementById('bsLoanScreen').innerHTML='&gt; analyzing<br>&gt; application';
    officer.classList.add('bs-typing-l');
  }
  function tickLoanService(dt){
    loanPhaseT+=dt;
    const a=loanServing.data;
    if(loanPhase==='analyzing'){
      if(loanPhaseT>1.2){loanPhase='credit';loanPhaseT=0;
        document.getElementById('bsLoanScreen').innerHTML='&gt; checking<br>&gt; credit history';}
    } else if(loanPhase==='credit'){
      if(loanPhaseT>1.2){loanPhase='risk';loanPhaseT=0;
        document.getElementById('bsLoanScreen').innerHTML='&gt; risk score:<br>&gt; '+a.risk_score;}
    } else if(loanPhase==='risk'){
      if(loanPhaseT>1.2){loanPhase='decision';loanPhaseT=0;
        document.getElementById('bsLoanScreen').innerHTML='&gt; ML model<br>&gt; deciding...';}
    } else if(loanPhase==='decision'){
      if(loanPhaseT>1.0){
        if(a.decision==='APPROVED'){mAppr++;totAppr++;}else{mRej++;totRej++;}
        totLoan++;
        const wait=Math.max(0,simMin-loanServing.arriveTime); mWaitSum+=wait; mWaitN++;
        showResult(a);
        document.getElementById('bsLoanScreen').innerHTML='&gt; decision:<br>&gt; '+a.decision;
        bubble(loanServing, a.decision==='APPROVED'?'Thank you!':'Okay.', a.decision==='APPROVED'?'ok':'bad');
        loanPhase='leave'; loanPhaseT=0;
        officer.classList.remove('bs-typing-l');
      }
    } else if(loanPhase==='leave'){
      if(loanPhaseT>1.0){
        walk(loanServing,true); facingLeft(loanServing,true); moveTo(loanServing,DOOR_X);
        const gone=loanServing; loanServing=null; loanPhase='idle';
        setTimeout(()=>remove(gone),1100);
      }
    }
  }

  // ===== END OF DAY REPORT =====
  function endOfDay(){
    const dl=mAppr+mRej;
    const avgWait=mWaitN?(mWaitSum/mWaitN).toFixed(1):'0';
    dailyLog.push({day:dayIdx+1, loans:dl, approved:mAppr, rejected:mRej,
                   cashier:mCashServed, avgWait:avgWait});
  }
  function endOfPeriod(){
    const rate=totLoan?Math.round(totAppr/totLoan*100):0;
    const items=[
      ['Total Loan Apps',totLoan],['Approved',totAppr],['Rejected',totRej],
      ['Approval Rate',rate+'%'],['Cashier Served',totCash],
      ['Days Simulated',dailyLog.length],['Loan Officer Performance',(totAppr+totRej)+' processed'],
      ['Avg Loans / Day',dailyLog.length?(totLoan/dailyLog.length).toFixed(1):'0'],
      ['Avg Cashier / Day',dailyLog.length?(totCash/dailyLog.length).toFixed(1):'0'],
      ['Period Complete','&#10003;']];
    const cards=items.map(it=>'<div class="bs-rcard"><div class="v">'+it[1]+'</div><div class="l">'+it[0]+'</div></div>').join('');
    // mini daily breakdown table
    let table='<table style="width:100%;margin-top:14px;border-collapse:collapse;font-size:11px;color:#fff;">'
      +'<thead><tr style="background:#ffffff22;"><th style="padding:6px;text-align:left;">Day</th>'
      +'<th style="padding:6px;">Loans</th><th style="padding:6px;">Approved</th>'
      +'<th style="padding:6px;">Rejected</th><th style="padding:6px;">Cashier</th>'
      +'<th style="padding:6px;">Avg Wait</th></tr></thead><tbody>';
    // For long periods, show first 10 + last 5
    const showLog = dailyLog.length<=15 ? dailyLog : [...dailyLog.slice(0,10),null,...dailyLog.slice(-5)];
    showLog.forEach(r=>{
      if(r===null){table+='<tr><td colspan="6" style="text-align:center;padding:4px;color:#a8c2f0;">...</td></tr>';return;}
      table+='<tr style="border-top:1px solid #ffffff15;"><td style="padding:5px;">'+r.day+'</td>'
        +'<td style="text-align:center;">'+r.loans+'</td><td style="text-align:center;color:#27e082;">'+r.approved+'</td>'
        +'<td style="text-align:center;color:#ff7a6a;">'+r.rejected+'</td>'
        +'<td style="text-align:center;">'+r.cashier+'</td><td style="text-align:center;font-weight:600;">'+(r.loans+r.cashier)+'</td></tr>';
    });
    table+='</tbody></table>';
    document.getElementById('bsRptGrid').innerHTML=cards+table;
    document.getElementById('bsRptDay').textContent='Period: '+dailyLog.length+' Day'+(dailyLog.length>1?'s':'');
    document.getElementById('bsReport').classList.add('show');
  }

  // ===== MAIN LOOP =====
  function startNextDay(){
    if(dayIdx>=DAYS.length){running=false; setStatus('Stopped'); return;}
    cashIdx=0; loanIdx=0; simMin=0;
    mAppr=0; mRej=0; mCashServed=0; mWaitSum=0; mWaitN=0; mQSum=0; mQN=0;
  }
  startNextDay();

  function step(dt){
    simMin+=dt;
    const today=DAYS[dayIdx];
    if(!today){running=false; setStatus('Stopped'); return;}

    // spawn cashier customers
    while(cashIdx<today.cashier_custs.length && today.cashier_custs[cashIdx].arrival_min<=simMin){
      // For long sims, just count cashier customers without spawning every one visually
      if(DAYS.length>=30 && (cashQueue.length+ (cashSlots[0]?1:0)+(cashSlots[1]?1:0))>=4){
        // virtual-serve: directly bump cashier total to keep counter moving
        mCashServed++; totCash++; cashIdx++; continue;
      }
      const p=makePerson(today.cashier_custs[cashIdx],'cashier');
      cashQueue.push(p); layoutCashQueue(); cashIdx++;
    }
    // spawn loan applicants
    while(loanIdx<today.loan_apps.length && today.loan_apps[loanIdx].arrival_min<=simMin){
      // For long sims, virtual-process loan applicants in queue overflow
      if(DAYS.length>=30 && (loanQueue.length + (loanServing?1:0))>=3){
        const a=today.loan_apps[loanIdx];
        if(a.decision==='APPROVED'){mAppr++;totAppr++;}else{mRej++;totRej++;}
        totLoan++; loanIdx++; continue;
      }
      const p=makePerson(today.loan_apps[loanIdx],'loan');
      loanQueue.push(p); layoutLoanQueue(); loanIdx++;
    }

    // assign cashier (2 slots, both pull from same queue)
    for(let k=0;k<2;k++){
      if(!cashSlots[k] && cashQueue.length>0){
        const p=cashQueue.shift(); layoutCashQueue(); startCashService(p,k);
      }
    }
    for(let k=0;k<2;k++) if(cashSlots[k]) tickCashService(dt,k);

    // assign loan officer
    if(!loanServing && loanQueue.length>0 && loanPhase==='idle'){
      const p=loanQueue.shift(); layoutLoanQueue(); startLoanService(p);
    }
    if(loanServing) tickLoanService(dt);

    updateKPIs();

    // End of day check
    if(simMin>=480 && !cashSlots[0] && !cashSlots[1] && !loanServing && cashQueue.length===0 && loanQueue.length===0
       && cashIdx>=today.cashier_custs.length && loanIdx>=today.loan_apps.length){
      endOfDay();
      dayIdx++;
      if(dayIdx<DAYS.length){
        // brief pause then continue next day
        const delay = DAYS.length<=7 ? 1200 : (DAYS.length<=30 ? 200 : 20);
        setTimeout(()=>{startNextDay(); updateKPIs();}, delay/Math.max(speed/2,1));
      } else {
        running=false; setStatus('Completed');
        document.getElementById('bsRun').disabled=false;
        document.getElementById('bsPause').disabled=true;
        document.getElementById('bsStop').disabled=true;
        endOfPeriod();
      }
    }
  }

  function loop(){
    if(!running||paused)return;
    let periodMult = 1;
    let stepsPerFrame = 1;
    if(DAYS.length>=365){ periodMult = 60; stepsPerFrame = 3; }
    else if(DAYS.length>=30){ periodMult = 12; stepsPerFrame = 2; }
    else if(DAYS.length>=7){ periodMult = 2.5; }
    for(let k=0;k<stepsPerFrame;k++) step(0.20*speed*periodMult);
    loopT=setTimeout(loop, speed>=8?40:speed>=4?60:90);
  }

  // ===== CONTROL HANDLERS =====
  document.getElementById('bsRun').onclick=()=>{
    if(running&&!paused)return;
    running=true; paused=false; setStatus('Running');
    document.getElementById('bsRun').disabled=true;
    document.getElementById('bsPause').disabled=false;
    document.getElementById('bsStop').disabled=false;
    loop();
  };
  document.getElementById('bsPause').onclick=()=>{
    if(!running)return;
    paused=!paused;
    document.getElementById('bsPause').innerHTML=paused?'&#9654; Resume':'&#10074;&#10074; Pause';
    setStatus(paused?'Paused':'Running');
    if(!paused)loop();
  };
  document.getElementById('bsStop').onclick=()=>{
    running=false; paused=false; if(loopT)clearTimeout(loopT);
    setStatus('Stopped');
    document.getElementById('bsRun').disabled=false;
    document.getElementById('bsPause').disabled=true;
    document.getElementById('bsStop').disabled=true;
    document.getElementById('bsPause').innerHTML='&#10074;&#10074; Pause';
  };
  document.getElementById('bsReset').onclick=()=>{
    running=false; paused=false; if(loopT)clearTimeout(loopT);
    document.querySelectorAll('.bs-person,.bs-bubble,.bs-conf').forEach(e=>e.remove());
    cashQueue=[]; loanQueue=[]; cashSlots[0]=null; cashSlots[1]=null; loanServing=null; loanPhase='idle';
    dayIdx=0; activeBank=0; totAppr=0; totRej=0; totCash=0; totLoan=0; dailyLog.length=0; startNextDay(); updateKPIs();
    setStatus('Stopped');
    document.getElementById('bsResult').classList.remove('show');
    document.getElementById('bsReport').classList.remove('show');
    document.getElementById('bsRun').disabled=false;
    document.getElementById('bsPause').disabled=true;
    document.getElementById('bsStop').disabled=true;
    document.getElementById('bsPause').innerHTML='&#10074;&#10074; Pause';
    document.getElementById('kCashQ').textContent='0';
    document.getElementById('kLoanQ').textContent='0';
  };
  document.getElementById('bsAudio').onclick=()=>{
    audioOn=!audioOn;
    document.getElementById('bsAudio').innerHTML=audioOn?'&#128266; Audio On':'&#128263; Muted';
    if(!audioOn && window.speechSynthesis) window.speechSynthesis.cancel();
  };
  document.querySelectorAll('.bs-sp').forEach(b=>{
    b.onclick=()=>{
      document.querySelectorAll('.bs-sp').forEach(x=>x.classList.remove('on'));
      b.classList.add('on'); speed=parseFloat(b.dataset.s);
      document.getElementById('bsSpdLbl').textContent=speed+'x';
    };
  });

  updateKPIs();
})();
</script>
</div>
"""
