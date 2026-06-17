"""
Banking Operations Simulator — CHARACTER LIBRARY
=================================================
Realistic SVG human figures: businessmen, businesswomen, casual customers,
a seated cashier, a seated loan officer, and a bank manager. Each has head,
face, hair, neck, torso (with shading), arms, legs and shoes. Arms and legs
have animation hooks (.arm-l, .arm-r, .leg-l, .leg-r) for walking.
"""

# Walking customer variants. variant 0..5 picks different looks.
def customer_svg(variant=0):
    looks = [
        # 0: businessman navy suit red tie
        {"skin": "#e8b88a", "skin_dark": "#d9a878", "hair": "#2a1810",
         "top": "#2c3e6b", "top_hi": "#374f88", "tie": "#a02828", "tie_show": True,
         "pant": "#1a2540", "shoe": "#0c0c0c", "long_hair": False, "beard": False},
        # 1: lady purple business
        {"skin": "#f0c9a0", "skin_dark": "#e0b88a", "hair": "#5a3825",
         "top": "#7d3c98", "top_hi": "#9b5cb8", "tie": None, "tie_show": False,
         "pant": "#3a2545", "shoe": "#1a1a1a", "long_hair": True, "beard": False},
        # 2: dark-skin man green casual with beard
        {"skin": "#c68642", "skin_dark": "#a06832", "hair": "#1a0e08",
         "top": "#1c7a4a", "top_hi": "#26a060", "tie": None, "tie_show": False,
         "pant": "#2a3540", "shoe": "#3a2810", "long_hair": False, "beard": True},
        # 3: lady orange/coral business
        {"skin": "#f2d2b6", "skin_dark": "#e0c0a4", "hair": "#7a4a1e",
         "top": "#c0563b", "top_hi": "#d97050", "tie": None, "tie_show": False,
         "pant": "#4a3b5c", "shoe": "#1a1a1a", "long_hair": True, "beard": False},
        # 4: man brown skin blue shirt
        {"skin": "#a87142", "skin_dark": "#8a5a32", "hair": "#0d0d0d",
         "top": "#2c5f9e", "top_hi": "#3a7bc8", "tie": None, "tie_show": False,
         "pant": "#33405c", "shoe": "#2a1810", "long_hair": False, "beard": False},
        # 5: businessman grey suit
        {"skin": "#d9a878", "skin_dark": "#c89868", "hair": "#3a2c1e",
         "top": "#4a5566", "top_hi": "#5f6b7e", "tie": "#1c4a96", "tie_show": True,
         "pant": "#2a3038", "shoe": "#0c0c0c", "long_hair": False, "beard": False},
    ]
    L = looks[variant % 6]

    # Hair shape
    if L["long_hair"]:
        hair = (f'<path d="M26 30 Q24 14 40 11 Q56 14 54 30 L55 48 Q48 42 40 42 '
                f'Q32 42 25 48 Z" fill="{L["hair"]}"/>'
                f'<path d="M28 38 L24 56 L29 56 Z" fill="{L["hair"]}"/>'
                f'<path d="M52 38 L56 56 L51 56 Z" fill="{L["hair"]}"/>')
    else:
        hair = (f'<path d="M27 28 Q28 12 40 10 Q52 12 53 28 Q53 18 40 16 '
                f'Q31 18 27 30 Z" fill="{L["hair"]}"/>')

    beard = (f'<path d="M30 38 Q40 50 50 38 Q50 44 40 46 Q30 44 30 38 Z" '
             f'fill="{L["hair"]}"/>') if L["beard"] else ""

    tie = (f'<path d="M38.5 56 L41.5 56 L42.5 80 L40 82 L37.5 80 Z" '
           f'fill="{L["tie"]}"/>') if L["tie_show"] else ""

    return f"""
<svg viewBox="0 0 80 160" width="44" height="88" class="bs-fig">
  <ellipse cx="40" cy="158" rx="20" ry="3" fill="#000" opacity="0.25"/>
  <g class="leg-r"><rect x="42" y="98" width="11" height="48" rx="3" fill="{L['pant']}"/>
    <rect x="40" y="142" width="15" height="8" rx="2" fill="{L['shoe']}"/></g>
  <g class="leg-l"><rect x="27" y="98" width="11" height="48" rx="3" fill="{L['pant']}"/>
    <rect x="25" y="142" width="15" height="8" rx="2" fill="{L['shoe']}"/></g>
  <path d="M22 56 Q40 52 58 56 L60 100 L20 100 Z" fill="{L['top']}"/>
  <path d="M22 56 Q40 52 58 56 L58 73 Q40 68 22 73 Z" fill="{L['top_hi']}" opacity="0.5"/>
  <path d="M36 56 L40 72 L44 56 Z" fill="#ffffff"/>
  {tie}
  <g class="arm-r"><rect x="56" y="58" width="10" height="36" rx="4" fill="{L['top']}"/>
    <circle cx="61" cy="95" r="5" fill="{L['skin']}"/></g>
  <g class="arm-l"><rect x="14" y="58" width="10" height="36" rx="4" fill="{L['top']}"/>
    <circle cx="19" cy="95" r="5" fill="{L['skin']}"/></g>
  <rect x="35" y="46" width="10" height="8" fill="{L['skin_dark']}"/>
  <ellipse cx="40" cy="32" rx="13" ry="15" fill="{L['skin']}"/>
  {hair}
  {beard}
  <circle cx="36" cy="32" r="1.3" fill="#1a1a1a"/>
  <circle cx="45" cy="32" r="1.3" fill="#1a1a1a"/>
  <path d="M37 39 Q40 41 43 39" stroke="#7a4a1e" stroke-width="1" fill="none" stroke-linecap="round"/>
</svg>"""


# Seated cashier (female, professional)
CASHIER_SVG = """
<svg viewBox="0 0 90 110" width="62" height="76" class="bs-seated">
  <rect x="30" y="40" width="32" height="44" rx="6" fill="#34456b"/>
  <ellipse cx="46" cy="28" rx="13" ry="15" fill="#f0c9a0"/>
  <path d="M32 25 Q30 8 46 6 Q62 8 60 25 L61 42 Q54 36 46 36 Q38 36 31 42 Z" fill="#5a3825"/>
  <path d="M28 50 Q46 42 64 50 L66 90 L26 90 Z" fill="#9b1c8c"/>
  <path d="M40 48 L46 60 L52 48 Z" fill="#ffffff"/>
  <rect class="cashier-armL" x="22" y="60" width="10" height="26" rx="5" fill="#9b1c8c"/>
  <rect class="cashier-armR" x="60" y="60" width="10" height="26" rx="5" fill="#9b1c8c"/>
  <circle cx="27" cy="88" r="5" fill="#f0c9a0"/>
  <circle cx="65" cy="88" r="5" fill="#f0c9a0"/>
  <circle cx="42" cy="32" r="1.3" fill="#1a1a1a"/>
  <circle cx="51" cy="32" r="1.3" fill="#1a1a1a"/>
  <ellipse cx="46" cy="40" rx="2.5" ry="0.8" fill="#c0392b" opacity="0.6"/>
</svg>"""


# Seated loan officer (male, suit + tie)
LOAN_OFFICER_SVG = """
<svg viewBox="0 0 90 110" width="62" height="76" class="bs-seated">
  <rect x="30" y="40" width="32" height="44" rx="6" fill="#2a3a55"/>
  <ellipse cx="46" cy="28" rx="13" ry="15" fill="#e8b88a"/>
  <path d="M33 26 Q34 10 46 8 Q58 10 59 26 Q59 16 46 14 Q34 16 33 28 Z" fill="#2a1810"/>
  <path d="M28 48 Q46 42 64 48 L66 90 L26 90 Z" fill="#1f3a66"/>
  <path d="M40 48 L46 60 L52 48 Z" fill="#ffffff"/>
  <path d="M44 48 L48 48 L49 80 L46 82 L43 80 Z" fill="#a02828"/>
  <rect class="officer-armL" x="22" y="60" width="10" height="26" rx="5" fill="#1f3a66"/>
  <rect class="officer-armR" x="60" y="60" width="10" height="26" rx="5" fill="#1f3a66"/>
  <circle cx="27" cy="88" r="5" fill="#e8b88a"/>
  <circle cx="65" cy="88" r="5" fill="#e8b88a"/>
  <circle cx="42" cy="32" r="1.3" fill="#1a1a1a"/>
  <circle cx="51" cy="32" r="1.3" fill="#1a1a1a"/>
</svg>"""


# Standing bank manager visible in his office
MANAGER_SVG = """
<svg viewBox="0 0 80 160" width="48" height="96" class="bs-fig">
  <ellipse cx="40" cy="158" rx="20" ry="3" fill="#000" opacity="0.25"/>
  <rect x="42" y="98" width="11" height="48" rx="3" fill="#1a1a1a"/>
  <rect x="40" y="142" width="15" height="8" rx="2" fill="#0c0c0c"/>
  <rect x="27" y="98" width="11" height="48" rx="3" fill="#1a1a1a"/>
  <rect x="25" y="142" width="15" height="8" rx="2" fill="#0c0c0c"/>
  <path d="M22 56 Q40 52 58 56 L60 100 L20 100 Z" fill="#3a3030"/>
  <path d="M22 56 Q40 52 58 56 L58 73 Q40 68 22 73 Z" fill="#4a3a3a" opacity="0.6"/>
  <path d="M36 56 L40 72 L44 56 Z" fill="#ffffff"/>
  <path d="M38.5 56 L41.5 56 L42.5 80 L40 82 L37.5 80 Z" fill="#1c4a96"/>
  <rect class="mgr-armL" x="14" y="58" width="10" height="36" rx="4" fill="#3a3030"/>
  <rect class="mgr-armR" x="56" y="58" width="10" height="36" rx="4" fill="#3a3030"/>
  <circle cx="19" cy="95" r="5" fill="#d9a878"/>
  <circle cx="61" cy="95" r="5" fill="#d9a878"/>
  <rect x="35" y="46" width="10" height="8" fill="#c89868"/>
  <ellipse cx="40" cy="32" rx="13" ry="15" fill="#d9a878"/>
  <path d="M27 28 Q28 12 40 10 Q52 12 53 28 Q53 18 40 16 Q31 18 27 30 Z" fill="#8a7060"/>
  <path d="M30 38 Q40 48 50 38 Q50 42 40 44 Q30 42 30 38 Z" fill="#8a7060"/>
  <circle cx="36" cy="32" r="1.3" fill="#1a1a1a"/>
  <circle cx="45" cy="32" r="1.3" fill="#1a1a1a"/>
</svg>"""
