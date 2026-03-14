import streamlit as st
import numpy as np
import json
import datetime
import requests
import time
import threading   # ← ADDED

# ─────────────────────────────────────────────
#  YOUR WEATHERAPI KEY
# ─────────────────────────────────────────────
WEATHER_API_KEY = "ec0aaf3d97ea407cbd7130905261403"
WEATHER_API_URL = "http://api.weatherapi.com/v1/current.json"

st.set_page_config(
    page_title="HOTTYCOLDIII DUNIYA",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Rajdhani:wght@400;500;600;700&display=swap');
:root {
    --bg:#080c14;--surface:#0d1520;--card:#101c2e;--border:#162540;
    --accent:#00d4ff;--accent2:#ff6b35;--text:#c8ddf5;--muted:#3d5470;--green:#00ff88;
}
*{box-sizing:border-box;margin:0;padding:0}
html,body,[data-testid="stAppViewContainer"],[data-testid="stMain"]{
    background:var(--bg)!important;color:var(--text)!important;font-family:'Rajdhani',sans-serif}
[data-testid="stHeader"]{display:none!important}
[data-testid="stSidebar"]{display:none!important}
[data-testid="stToolbar"]{display:none!important}
#MainMenu,footer{display:none!important}
[data-testid="stMainBlockContainer"]{padding:0!important;max-width:100%!important}
section.main>div{padding:0!important}

.navbar{display:flex;align-items:center;justify-content:space-between;
    background:var(--surface);padding:0 2rem;height:52px;position:sticky;top:0;z-index:100;
    border-bottom:1px solid var(--border)}
.nav-logo{display:flex;align-items:center;gap:.6rem;font-size:1.1rem;
    font-weight:700;color:var(--accent);letter-spacing:.03em}
.nav-logo span{color:var(--text)}
.nav-links{display:flex;gap:2rem;font-size:.85rem;font-weight:600;letter-spacing:.05em}
.nav-link{color:var(--muted);cursor:pointer}
.nav-link.active{color:var(--accent)}
.nav-right{display:flex;align-items:center;gap:1rem}
.nav-badge{background:var(--card);border:1px solid var(--border);border-radius:6px;
    padding:.25rem .9rem;font-size:.78rem;color:var(--text);cursor:pointer}
.nav-badge:hover{border-color:var(--accent);color:var(--accent)}

.search-section{background:var(--surface);border-bottom:1px solid var(--border);
    padding:0 2rem;height:44px;display:flex;align-items:center;
    position:sticky;top:52px;z-index:99}
.search-inner{display:flex;gap:.6rem;align-items:center;width:100%}
.search-box{flex:1;max-width:520px;display:flex;align-items:center;gap:.6rem;
    background:rgba(0,212,255,0.07);border:1.5px solid var(--accent);border-radius:6px;
    padding:.28rem .85rem;height:32px;transition:box-shadow .2s;
    box-shadow:0 0 10px rgba(0,212,255,0.18)}
.search-box:focus-within{box-shadow:0 0 20px rgba(0,212,255,0.35)}

.lhs-panel{background:var(--surface);border-right:1px solid var(--border);
    padding:1.2rem 1rem;overflow-y:auto}
.panel-title{font-size:.68rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;
    color:var(--muted);margin-bottom:.8rem;display:flex;align-items:center;gap:.5rem}
.panel-title::after{content:'';flex:1;height:1px;background:var(--border)}
.recent-item{display:flex;align-items:center;justify-content:space-between;
    padding:.65rem .8rem;background:var(--card);border:1px solid var(--border);
    border-radius:8px;margin-bottom:.5rem;cursor:pointer;transition:border-color .2s}
.recent-item:hover{border-color:var(--accent)}
.ri-left{display:flex;align-items:center;gap:.6rem}
.ri-dot{color:var(--accent);font-size:.75rem}
.ri-name{font-size:.88rem;font-weight:600;color:var(--text)}
.ri-time{font-size:.62rem;color:var(--muted);letter-spacing:.05em;font-family:'Space Mono',monospace}
.ri-temp{font-size:1.05rem;font-weight:700}

.radar-header{display:flex;align-items:center;justify-content:space-between;padding:.8rem 1.2rem 0}
.radar-title{font-size:.7rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;
    color:var(--muted);display:flex;align-items:center;gap:.5rem}
.radar-dot{width:8px;height:8px;border-radius:50%;background:var(--green);box-shadow:0 0 6px var(--green)}

.rhs-panel{background:var(--surface);border-left:1px solid var(--border);padding:1.2rem 1rem;
    overflow-y:auto;display:flex;flex-direction:column;gap:.6rem}
.weather-card{background:var(--card);border:1px solid var(--border);border-radius:8px;
    padding:.9rem 1rem;position:relative;overflow:hidden}
.weather-card::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;
    background:linear-gradient(90deg,var(--accent),transparent);opacity:.5}
.wc-label{font-size:.6rem;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);
    font-family:'Space Mono',monospace;display:flex;justify-content:space-between;
    align-items:center;margin-bottom:.4rem}
.wc-value{font-size:1.7rem;font-weight:700;color:var(--text);line-height:1;letter-spacing:-.02em}
.wc-unit{font-size:.9rem;color:var(--muted)}
.wc-sub{font-size:.7rem;color:var(--muted);margin-top:.25rem;font-family:'Space Mono',monospace}
.wc-icon{font-size:1rem;color:var(--accent)}
.wc-live{display:inline-flex;align-items:center;gap:4px;font-size:.58rem;font-family:'Space Mono',monospace;
    color:var(--green);letter-spacing:.08em;margin-top:.3rem}
.wc-live-dot{width:5px;height:5px;border-radius:50%;background:var(--green);animation:lp 1.5s infinite}
@keyframes lp{0%,100%{opacity:1}50%{opacity:.2}}

/* ══════════════════════════════════════
   LOADING SCREEN  ← ADDED
   ══════════════════════════════════════ */
.ld-full{display:flex;align-items:center;justify-content:center;
    width:100%;min-height:80vh;background:var(--bg)}
.ld-card{background:var(--surface);border:1px solid var(--border);border-radius:12px;
    padding:2.8rem 3.4rem;display:flex;flex-direction:column;align-items:center;
    gap:1.3rem;min-width:420px;position:relative;overflow:hidden}
.ld-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;
    background:linear-gradient(90deg,var(--accent),var(--accent2),transparent)}
.ld-live{display:inline-flex;align-items:center;gap:5px;font-size:.58rem;
    font-family:'Space Mono',monospace;color:var(--green);letter-spacing:.08em;
    background:rgba(0,229,160,.06);border:1px solid rgba(0,229,160,.2);
    border-radius:3px;padding:1px 7px}
.ld-live-dot{width:5px;height:5px;border-radius:50%;background:var(--green);animation:lp 1.5s infinite}
.ld-title{font-size:.85rem;font-weight:700;color:var(--accent);
    letter-spacing:.12em;font-family:'Space Mono',monospace;text-align:center}
.ld-timer{font-size:2.4rem;font-weight:700;color:var(--text);
    font-family:'Space Mono',monospace;letter-spacing:.04em;line-height:1;text-align:center}
.ld-timer-label{font-size:.58rem;letter-spacing:.12em;text-transform:uppercase;
    color:var(--muted);font-family:'Space Mono',monospace;text-align:center;margin-top:-.4rem}
.ld-pill{width:100%;background:var(--card);border:1px solid var(--border);
    border-radius:7px;padding:.65rem .9rem;position:relative;overflow:hidden}
.ld-pill::after{content:'';position:absolute;top:0;left:0;right:0;height:2px;
    background:linear-gradient(90deg,var(--accent),transparent);opacity:.5}
.ld-pill-label{font-size:.57rem;letter-spacing:.1em;text-transform:uppercase;
    color:var(--muted);font-family:'Space Mono',monospace;margin-bottom:.45rem;
    display:flex;justify-content:space-between;align-items:center}
.ld-track{width:100%;height:4px;background:rgba(0,212,255,0.10);border-radius:2px;overflow:hidden}
.ld-fill{height:4px;background:linear-gradient(90deg,var(--accent),var(--accent2));
    border-radius:2px;transition:width .3s ease}
.ld-shimmer{width:100%;height:3px;background:rgba(0,212,255,0.06);
    border-radius:2px;overflow:hidden;margin-top:.3rem}
.ld-shimmer-inner{height:3px;
    background:linear-gradient(90deg,transparent,rgba(0,212,255,.55),transparent);
    animation:ldshim 1.5s ease-in-out infinite}
@keyframes ldshim{0%{width:40%;margin-left:-40%}100%{width:40%;margin-left:100%}}
.ld-sub{font-size:.7rem;color:var(--muted);font-family:'Space Mono',monospace;
    letter-spacing:.05em;text-align:center;line-height:1.75}
.ld-hint{font-size:.58rem;color:rgba(61,84,112,.65);
    font-family:'Space Mono',monospace;letter-spacing:.08em;text-align:center}

.api-badge{background:rgba(0,255,136,0.08);border:1px solid rgba(0,255,136,0.25);
    border-radius:6px;padding:.3rem .8rem;font-size:.65rem;color:var(--green);
    font-family:'Space Mono',monospace;letter-spacing:.08em;display:inline-flex;align-items:center;gap:.4rem}

.error-card{background:rgba(255,68,68,.08);border:1px solid rgba(255,68,68,.3);
    border-radius:8px;padding:.8rem 1rem;font-size:.78rem;color:#ff6b6b;
    font-family:'Space Mono',monospace}

.premium-card{background:linear-gradient(135deg,rgba(0,212,255,.06),rgba(0,212,255,.02));
    border:1px solid rgba(0,212,255,.25);border-radius:8px;padding:.9rem 1rem;
    display:flex;align-items:center;gap:.8rem}
.pc-icon{font-size:1.2rem;color:var(--accent)}
.pc-title{font-size:.85rem;font-weight:700;color:var(--accent)}
.pc-sub{font-size:.68rem;color:var(--muted)}

[data-testid="stForm"]{border:none!important;padding:0!important;background:transparent!important}
[data-testid="stForm"]>div{padding:0!important;background:transparent!important}
[data-testid="stTextInput"] input{background:transparent!important;border:none!important;
    color:var(--text)!important;font-family:'Rajdhani',sans-serif!important;
    font-size:.88rem!important;padding:0!important;box-shadow:none!important}
[data-testid="stTextInput"] input:focus{outline:none!important;box-shadow:none!important}
[data-testid="stTextInput"]>div{background:transparent!important;border:none!important;padding:0!important}
[data-testid="stTextInput"]>div>div{background:transparent!important}
[data-testid="stTextInput"] label{display:none!important}
[data-testid="stButton"] button{background:var(--accent)!important;border:none!important;
    color:#080c14!important;font-family:'Rajdhani',sans-serif!important;font-size:.85rem!important;
    font-weight:700!important;letter-spacing:.06em!important;padding:.45rem 1.4rem!important;
    border-radius:5px!important;transition:opacity .2s!important}
[data-testid="stButton"] button:hover{opacity:.85!important}
[data-testid="stAlert"]{background:rgba(255,68,68,.08)!important;
    border:1px solid rgba(255,68,68,.3)!important;border-radius:6px!important;
    color:var(--text)!important;font-size:.82rem!important;margin:.3rem 1.2rem!important}
[data-testid="column"]{padding:0!important}
.stColumns{gap:0!important}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  COUNTRY DATA
# ─────────────────────────────────────────────
COUNTRY_DATA = {
    "Afghanistan":    {"lat": 33.9,  "lon":  67.7, "query": "Kabul"},
    "Argentina":      {"lat":-38.4,  "lon": -63.6, "query": "Buenos Aires"},
    "Australia":      {"lat":-25.3,  "lon": 133.8, "query": "Sydney"},
    "Brazil":         {"lat":-14.2,  "lon": -51.9, "query": "Brasilia"},
    "Canada":         {"lat": 56.1,  "lon":-106.3, "query": "Ottawa"},
    "China":          {"lat": 35.9,  "lon": 104.2, "query": "Beijing"},
    "Denmark":        {"lat": 56.3,  "lon":   9.5, "query": "Copenhagen"},
    "Egypt":          {"lat": 26.8,  "lon":  30.8, "query": "Cairo"},
    "Ethiopia":       {"lat":  9.1,  "lon":  40.5, "query": "Addis Ababa"},
    "France":         {"lat": 46.2,  "lon":   2.2, "query": "Paris"},
    "Germany":        {"lat": 51.2,  "lon":  10.5, "query": "Berlin"},
    "Greenland":      {"lat": 71.7,  "lon": -42.6, "query": "Nuuk"},
    "India":          {"lat": 20.6,  "lon":  78.9, "query": "New Delhi"},
    "Indonesia":      {"lat": -0.8,  "lon": 113.9, "query": "Jakarta"},
    "Iran":           {"lat": 32.4,  "lon":  53.7, "query": "Tehran"},
    "Japan":          {"lat": 36.2,  "lon": 138.2, "query": "Tokyo"},
    "Kenya":          {"lat": -0.0,  "lon":  37.9, "query": "Nairobi"},
    "Mexico":         {"lat": 23.6,  "lon":-102.6, "query": "Mexico City"},
    "Morocco":        {"lat": 31.8,  "lon":  -7.1, "query": "Rabat"},
    "Netherlands":    {"lat": 52.1,  "lon":   5.3, "query": "Amsterdam"},
    "New Zealand":    {"lat":-40.9,  "lon": 174.9, "query": "Wellington"},
    "Nigeria":        {"lat":  9.1,  "lon":   8.7, "query": "Abuja"},
    "Norway":         {"lat": 60.5,  "lon":   8.5, "query": "Oslo"},
    "Pakistan":       {"lat": 30.4,  "lon":  69.3, "query": "Islamabad"},
    "Peru":           {"lat": -9.2,  "lon": -75.0, "query": "Lima"},
    "Poland":         {"lat": 51.9,  "lon":  19.1, "query": "Warsaw"},
    "Russia":         {"lat": 61.5,  "lon": 105.3, "query": "Moscow"},
    "Saudi Arabia":   {"lat": 23.9,  "lon":  45.1, "query": "Riyadh"},
    "South Africa":   {"lat":-30.6,  "lon":  22.9, "query": "Cape Town"},
    "South Korea":    {"lat": 35.9,  "lon": 127.8, "query": "Seoul"},
    "Spain":          {"lat": 40.5,  "lon":  -3.7, "query": "Madrid"},
    "Sweden":         {"lat": 60.1,  "lon":  18.6, "query": "Stockholm"},
    "Switzerland":    {"lat": 46.8,  "lon":   8.2, "query": "Bern"},
    "Turkey":         {"lat": 38.9,  "lon":  35.2, "query": "Ankara"},
    "Ukraine":        {"lat": 48.4,  "lon":  31.2, "query": "Kyiv"},
    "United Kingdom": {"lat": 55.4,  "lon":  -3.4, "query": "London"},
    "United States":  {"lat": 37.1,  "lon": -95.7, "query": "Washington"},
    "Venezuela":      {"lat":  6.4,  "lon": -66.6, "query": "Caracas"},
    "Vietnam":        {"lat": 14.1,  "lon": 108.3, "query": "Hanoi"},
}

RECENT_COUNTRIES = [
    ("London, UK",    "United Kingdom", "2M AGO"),
    ("New York, USA", "United States",  "15M AGO"),
    ("Tokyo, JP",     "Japan",          "1H AGO"),
    ("Sydney, AU",    "Australia",      "4H AGO"),
    ("Mumbai, IN",    "India",          "5M AGO"),
]

# ─────────────────────────────────────────────
#  REAL WEATHER FETCHER  (unchanged from doc 5)
# ─────────────────────────────────────────────
@st.cache_data(ttl=1800, show_spinner=False)
def fetch_weather(query: str) -> dict | None:
    try:
        resp = requests.get(
            WEATHER_API_URL,
            params={"key": WEATHER_API_KEY, "q": query, "aqi": "no"},
            timeout=8,
        )
        if resp.status_code != 200:
            return None
        d = resp.json()
        cur = d["current"]
        return {
            "temp":       round(cur["temp_c"], 1),
            "feels_like": round(cur["feelslike_c"], 1),
            "wind":       round(cur["wind_kph"], 1),
            "humidity":   cur["humidity"],
            "precip":     round(cur["precip_mm"], 1),
            "condition":  cur["condition"]["text"],
            "uv":         cur.get("uv", 0),
        }
    except Exception:
        return None


# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────
if "selected_country" not in st.session_state:
    st.session_state.selected_country = None
if "error_msg" not in st.session_state:
    st.session_state.error_msg = ""
if "weather_loaded" not in st.session_state:   # ← ADDED
    st.session_state.weather_loaded = False     # ← ADDED

today     = datetime.date.today()
today_str = today.strftime("%d %b %Y")
now_str   = datetime.datetime.now().strftime("%H:%M")

# ─────────────────────────────────────────────
#  NAVBAR
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="navbar">
  <div class="nav-logo">
    🌐 <span>HOTTYCOLDII<b style="color:var(--accent)">DUNIYA</b></span>
  </div>
  <div class="nav-links">
    <span class="nav-link active">NIYANTRAN-DWAR</span>
  </div>
  <div class="nav-right">
    <span class="api-badge">⚡ LIVE · WeatherAPI.com</span>
    <span style="font-size:.72rem;color:var(--muted);font-family:'Space Mono',monospace">
      📅 {today_str} &nbsp;⏱ {now_str}
    </span>
    <span style="color:var(--muted);font-size:1rem;">🔔</span>
    <span class="nav-badge">Sign in</span>
    <div style="width:28px;height:28px;border-radius:50%;background:var(--card);
                border:1px solid var(--border);display:flex;align-items:center;
                justify-content:center;font-size:.75rem;">👤</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SEARCH BAR
# ─────────────────────────────────────────────
st.markdown('<div class="search-section"><div class="search-inner">', unsafe_allow_html=True)
with st.form(key="search_form", clear_on_submit=False):
    s_col, b_col = st.columns([9, 1])
    with s_col:
        st.markdown('<div class="search-box"><span style="color:var(--muted);font-size:.85rem">🔍</span>', unsafe_allow_html=True)
        query = st.text_input("q", placeholder="Search country… e.g. India, Brazil, Norway",
                              label_visibility="collapsed", key="search_q")
        st.markdown('</div>', unsafe_allow_html=True)
    with b_col:
        search_btn = st.form_submit_button("Search", use_container_width=True)
st.markdown('</div></div>', unsafe_allow_html=True)

if search_btn and query:
    match = None
    ql = query.strip().lower()
    for c in COUNTRY_DATA:
        if ql in c.lower():
            match = c
            break
    if match:
        st.session_state.selected_country = match
        st.session_state.error_msg = ""
        st.switch_page("pages/country_analysis.py")
    else:
        st.session_state.error_msg = f'Country "{query}" not found. Try: India, Brazil, Japan…'

if st.session_state.error_msg:
    st.error(st.session_state.error_msg)

# ─────────────────────────────────────────────
#  FETCH ALL REAL WEATHER  ← REPLACED BLOCK
#  Old code: fetch_all_countries_with_spinner()
#    — no elapsed time, blocks UI fully
#  New code: background thread + live timer
#    — shows MM:SS elapsed + per-country progress
#    — first load only; reruns use session cache
# ─────────────────────────────────────────────
_total = len(COUNTRY_DATA)
_fallback = {
    "Afghanistan":12.1,"Argentina":14.2,"Australia":21.8,"Brazil":25.0,
    "Canada":-5.3,"China":7.8,"Denmark":7.8,"Egypt":20.8,"Ethiopia":16.2,
    "France":11.3,"Germany":8.5,"Greenland":-18.7,"India":25.0,
    "Indonesia":26.5,"Iran":17.2,"Japan":14.5,"Kenya":19.5,"Mexico":21.0,
    "Morocco":17.5,"Netherlands":10.0,"New Zealand":12.5,"Nigeria":26.8,
    "Norway":1.5,"Pakistan":20.0,"Peru":18.5,"Poland":7.5,"Russia":-5.1,
    "Saudi Arabia":25.5,"South Africa":17.2,"South Korea":12.5,"Spain":14.0,
    "Sweden":2.1,"Switzerland":5.6,"Turkey":11.5,"Ukraine":7.3,
    "United Kingdom":8.5,"United States":12.0,"Venezuela":25.8,"Vietnam":23.5,
}

if not st.session_state.weather_loaded:

    _done    = [False]
    _fetched = [0]
    _result  = [{}]

    def _bg_fetch():
        out = {}
        for i, (country, info) in enumerate(COUNTRY_DATA.items()):
            data = fetch_weather(info["query"])
            if data:
                out[country] = data
            else:
                fb = _fallback.get(country, 15.0)
                out[country] = {"temp": fb, "feels_like": fb,
                                "wind": 10.0, "humidity": 60,
                                "precip": 0.0, "condition": "Data unavailable", "uv": 0}
            _fetched[0] = i + 1
        _result[0] = out
        _done[0]   = True

    _thread = threading.Thread(target=_bg_fetch, daemon=True)
    _thread.start()

    _slot = st.empty()
    _t0   = time.time()

    while not _done[0]:
        _elapsed = int(time.time() - _t0)
        _mm      = _elapsed // 60
        _ss      = _elapsed % 60
        _pct     = int(_fetched[0] / _total * 100)

        _slot.markdown(f"""
        <div class="ld-full">
          <div class="ld-card">
            <span class="ld-live">
              <span class="ld-live-dot"></span>LIVE · WeatherAPI.com
            </span>
            <div class="ld-title">⚡ FETCHING LIVE WEATHER DATA</div>
            <div class="ld-timer">{_mm:02d}:{_ss:02d}</div>
            <div class="ld-timer-label">ELAPSED · FIRST LOAD ONLY</div>
            <div class="ld-pill">
              <div class="ld-pill-label">
                <span>COUNTRIES FETCHED</span>
                <span style="color:var(--accent)">{_fetched[0]} / {_total} &nbsp; {_pct}%</span>
              </div>
              <div class="ld-track">
                <div class="ld-fill" style="width:{_pct}%"></div>
              </div>
              <div class="ld-shimmer"><div class="ld-shimmer-inner"></div></div>
            </div>
            <div class="ld-sub">
              Contacting WeatherAPI.com<br>
              Pulling real-time conditions for {_total} countries…
            </div>
            <div class="ld-hint">⏱ CACHED 30 MIN AFTER THIS · NO LOADER ON RERUNS</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.5)

    _thread.join()
    _slot.empty()

    CURRENT = _result[0]
    st.session_state["CURRENT"]      = CURRENT
    st.session_state["fetch_time"]   = time.time()
    st.session_state.weather_loaded  = True

else:
    # Re-use session cache — instant, no loader
    CURRENT = st.session_state.get("CURRENT", {})
    # Refresh if 30 min TTL expired
    if time.time() - st.session_state.get("fetch_time", 0) > 1800:
        st.session_state.weather_loaded = False
        st.rerun()

countries = list(COUNTRY_DATA.keys())

# ─────────────────────────────────────────────
#  THREE COLUMN LAYOUT  (unchanged from doc 5)
# ─────────────────────────────────────────────
lhs_col, center_col, rhs_col = st.columns([2.2, 5.5, 2.3])

# ── LEFT PANEL ──────────────────────────────
with lhs_col:
    st.markdown('<div class="lhs-panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">🕐 Recent Locations</div>', unsafe_allow_html=True)

    for label, ckey, ago in RECENT_COUNTRIES:
        cur = CURRENT[ckey]["temp"]
        color = "#ff6b35" if cur > 28 else "#00d4ff" if cur < 5 else "#ffcc02"
        st.markdown(f"""
        <div class="recent-item">
          <div class="ri-left">
            <span class="ri-dot">📍</span>
            <div>
              <div class="ri-name">{label}</div>
              <div class="ri-time">UPDATED {ago}</div>
            </div>
          </div>
          <div class="ri-temp" style="color:{color}">{cur:.1f}°C</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<br><div class="panel-title" style="margin-top:.5rem">⚡ Quick Access</div>', unsafe_allow_html=True)
    quick = [("🇮🇳","India"),("🇺🇸","United States"),("🇧🇷","Brazil"),
             ("🇯🇵","Japan"),("🇷🇺","Russia"),("🇦🇺","Australia")]
    for flag, cname in quick:
        if st.button(f"{flag} {cname}", key=f"qa_{cname}", use_container_width=True):
            st.session_state.selected_country = cname
            st.switch_page("pages/country_analysis.py")

    st.markdown('</div>', unsafe_allow_html=True)

# ── CENTER PANEL — GLOBE ─────────────────────
with center_col:
    import streamlit.components.v1 as components

    st.markdown("""
    <div class="radar-header">
      <div class="radar-title"><span class="radar-dot"></span> WORLD WEATHER RADAR — LIVE · WeatherAPI.com</div>
    </div>
    """, unsafe_allow_html=True)

    avg_t = float(np.mean([CURRENT[c]["temp"] for c in countries]))

    markers_json = json.dumps([
        {"n": c,
         "la": COUNTRY_DATA[c]["lat"],
         "lo": COUNTRY_DATA[c]["lon"],
         "t":  CURRENT[c]["temp"],
         "cond": CURRENT[c]["condition"]}
        for c in countries
    ])

    globe_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
  html,body{{margin:0;padding:0;background:#080c14;overflow:hidden;width:100%;height:100%;contain:strict}}
  canvas{{position:absolute;top:0;left:0;display:block;width:100%!important;height:100%!important}}
  #tip{{position:fixed;display:none;pointer-events:none;
    background:rgba(6,12,22,.97);border:1px solid rgba(0,180,255,0.45);border-radius:7px;
    padding:8px 13px;color:#c8ddf5;font-family:'Rajdhani',sans-serif;font-size:13px;
    line-height:1.7;white-space:nowrap;z-index:99;box-shadow:0 4px 20px rgba(0,0,0,0.6)}}
  #tip b{{color:#00d4ff;display:block;font-size:14px;font-weight:700}}
  #tip .cond{{font-size:11px;color:#7aafcf}}
  #tip .ts{{font-size:10px;color:#3d5470;letter-spacing:.06em;margin-top:2px}}
</style></head><body>
<canvas id="cv"></canvas>
<div id="tip"></div>
<script>
const MK={markers_json};
const TODAY="{today_str}";
const cv=document.getElementById('cv');
const ctx=cv.getContext('2d');
let W,H,R,cx,cy;
function resize(){{
  W=window.innerWidth;H=window.innerHeight;
  const dpr=window.devicePixelRatio||1;
  cv.width=W*dpr;cv.height=H*dpr;
  cv.style.width=W+'px';cv.style.height=H+'px';
  ctx.setTransform(dpr,0,0,dpr,0,0);
  const PAD=80;
  R=Math.floor(Math.min(W,H)*0.30);
  R=Math.min(R,Math.floor(W/2)-PAD,Math.floor(H/2)-PAD);
  cx=Math.floor(W/2);cy=Math.floor(H/2)-12;
}}
resize();window.addEventListener('resize',resize);
function tc(t){{
  const lo=-20,hi=35;
  const frac=Math.max(0,Math.min(1,(t-lo)/(hi-lo)));
  const stops=[[0.00,[49,54,149]],[0.18,[69,117,180]],[0.36,[171,217,233]],
    [0.50,[224,243,248]],[0.60,[145,207,96]],[0.72,[254,224,139]],
    [0.84,[252,141,89]],[1.00,[215,48,39]]];
  let r=255,g=255,b=255;
  for(let i=1;i<stops.length;i++){{
    const[f0,c0]=stops[i-1],[f1,c1]=stops[i];
    if(frac<=f1){{const u=(frac-f0)/(f1-f0);
      r=Math.round(c0[0]+(c1[0]-c0[0])*u);
      g=Math.round(c0[1]+(c1[1]-c0[1])*u);
      b=Math.round(c0[2]+(c1[2]-c0[2])*u);break;}}
  }}
  return[r,g,b];
}}
function project(lat,lon,rl){{
  const phi=(90-lat)*Math.PI/180,th=(lon-rl)*Math.PI/180;
  const x=Math.sin(phi)*Math.sin(th),y=Math.cos(phi),z=Math.sin(phi)*Math.cos(th);
  return{{px:cx+R*x,py:cy-R*y,z,vis:z>0}};
}}
const CONTINENTS=[
  [[-168,72],[-140,70],[-125,50],[-118,32],[-110,23],[-87,16],[-83,10],[-77,8],
   [-80,25],[-90,30],[-97,26],[-105,20],[-117,32],[-120,35],[-124,46],[-130,54],[-140,60],[-158,60],[-168,72]],
  [[-45,60],[-20,63],[-18,70],[-20,76],[-30,83],[-50,83],[-65,80],[-72,75],[-68,65],[-55,60],[-45,60]],
  [[-80,12],[-75,11],[-62,11],[-50,5],[-35,-5],[-35,-9],[-38,-15],[-40,-22],
   [-48,-28],[-52,-33],[-58,-38],[-63,-42],[-65,-55],[-68,-54],[-72,-48],
   [-75,-40],[-78,-32],[-78,-15],[-76,-1],[-80,2],[-80,12]],
  [[-10,36],[5,36],[15,37],[28,37],[30,42],[37,42],[30,47],[25,45],[18,42],
   [14,45],[13,47],[6,44],[0,44],[-2,43],[-8,44],[-10,44],[-8,48],[-4,48],
   [-2,52],[2,52],[5,54],[10,56],[14,57],[18,60],[20,58],[28,60],[30,65],
   [24,68],[18,70],[14,70],[8,62],[5,59],[2,57],[0,51],[-6,50],[-8,48],[-10,44],[-10,36]],
  [[-18,16],[-15,11],[-15,5],[-10,5],[0,5],[10,5],[15,0],[15,-5],[20,-15],
   [25,-20],[30,-30],[32,-34],[27,-34],[20,-35],[18,-34],[16,-29],[14,-22],
   [12,-18],[10,-10],[8,-4],[2,3],[-2,5],[-5,5],[-8,5],[-15,5],[-18,10],[-18,16]],
  [[30,42],[37,42],[45,42],[55,38],[60,35],[67,25],[70,23],[80,14],[82,8],
   [85,12],[90,22],[95,22],[100,13],[103,1],[108,-5],[115,-8],[120,-10],
   [125,-8],[130,0],[135,2],[140,5],[145,10],[145,15],[140,20],[140,35],
   [135,35],[132,40],[130,45],[128,50],[130,58],[132,62],[142,47],[143,40],
   [140,36],[140,38],[135,35],[128,42],[120,53],[110,53],[100,55],[90,55],
   [80,60],[70,68],[60,68],[55,60],[50,52],[45,48],[40,45],[35,42],[30,42]],
  [[130,31],[131,33],[132,34],[134,35],[137,35],[141,40],[141,44],[143,44],
   [145,43],[144,42],[142,40],[141,38],[141,35],[138,34],[135,34],[133,34],[132,33],[130,32],[130,31]],
  [[114,-22],[118,-20],[122,-18],[128,-15],[132,-12],[136,-12],[140,-17],
   [142,-18],[145,-15],[148,-20],[152,-25],[154,-28],[152,-35],[148,-38],
   [145,-38],[140,-38],[136,-35],[130,-32],[124,-32],[116,-32],[114,-28],[114,-22]],
];
const ICECAPS=[
  [[-180,75],[-150,74],[-120,74],[-90,75],[-60,74],[-30,74],[0,74],[30,74],
   [60,74],[90,75],[120,74],[150,74],[180,75],[180,90],[0,90],[-180,90],[-180,75]],
  [[-180,-65],[-150,-64],[-120,-64],[-90,-65],[-60,-64],[-30,-64],[0,-64],
   [30,-64],[60,-64],[90,-65],[120,-64],[150,-64],[180,-65],[180,-90],[0,-90],
   [-180,-90],[-180,-65]],
];
const oc=document.createElement('canvas');
const octx=oc.getContext('2d');
let rotLon=282,drag=false,dragX=0,velX=0;
cv.style.cursor='grab';
cv.addEventListener('mousedown',e=>{{drag=true;dragX=e.clientX;velX=0;cv.style.cursor='grabbing';}});
window.addEventListener('mouseup',()=>{{drag=false;cv.style.cursor='grab';}});
window.addEventListener('mousemove',e=>{{
  if(drag){{const dx=e.clientX-dragX;velX=dx*.55;rotLon=(rotLon-dx*.45+360)%360;dragX=e.clientX;}}
}});
cv.addEventListener('touchstart',e=>{{drag=true;dragX=e.touches[0].clientX;velX=0;}},{{passive:true}});
window.addEventListener('touchend',()=>{{drag=false;}});
window.addEventListener('touchmove',e=>{{
  if(drag){{const dx=e.touches[0].clientX-dragX;velX=dx*.55;rotLon=(rotLon-dx*.45+360)%360;dragX=e.touches[0].clientX;}}
}},{{passive:true}});
const tip=document.getElementById('tip');
cv.addEventListener('mousemove',e=>{{
  const r=cv.getBoundingClientRect(),mx=e.clientX-r.left,my=e.clientY-r.top;
  let found=false;
  for(const m of MK){{
    const p=project(m.la,m.lo,rotLon);
    if(!p.vis)continue;
    const dx=mx-p.px,dy=my-p.py;
    if(dx*dx+dy*dy<140){{
      tip.innerHTML='<b>'+m.n+'</b>🌡 '+m.t.toFixed(1)+'°C<div class="cond">'+m.cond+'</div><div class="ts">📅 LIVE · '+TODAY+'</div>';
      tip.style.display='block';tip.style.left=(e.clientX+18)+'px';tip.style.top=(e.clientY-14)+'px';
      cv.style.cursor='pointer';found=true;break;
    }}
  }}
  if(!found){{tip.style.display='none';if(!drag)cv.style.cursor='grab';}}
}});
cv.addEventListener('mouseleave',()=>tip.style.display='none');
function drawPoly(c,pts,fill,stroke,sw){{
  const dense=[];
  for(let i=0;i<pts.length;i++){{
    const[lon0,lat0]=pts[i],[lon1,lat1]=pts[(i+1)%pts.length];
    dense.push(pts[i]);
    const steps=Math.max(1,Math.round(Math.abs(lon1-lon0)/4));
    for(let s=1;s<steps;s++)dense.push([lon0+(lon1-lon0)*s/steps,lat0+(lat1-lat0)*s/steps]);
  }}
  c.beginPath();let first=true;
  for(const[lon,lat]of dense){{
    const p=project(lat,lon,rotLon);
    if(first){{c.moveTo(p.px,p.py);first=false;}}else c.lineTo(p.px,p.py);
  }}
  c.closePath();
  if(fill){{c.fillStyle=fill;c.fill();}}
  if(stroke){{c.strokeStyle=stroke;c.lineWidth=sw||0.5;c.stroke();}}
}}
function draw(){{
  const dpr=window.devicePixelRatio||1;
  if(oc.width!==cv.width||oc.height!==cv.height){{
    oc.width=cv.width;oc.height=cv.height;octx.setTransform(dpr,0,0,dpr,0,0);
  }}
  octx.fillStyle='#080c14';octx.fillRect(0,0,W,H);
  octx.save();
  octx.beginPath();octx.arc(cx,cy,R,0,Math.PI*2);octx.clip();
  const og=octx.createRadialGradient(cx-R*.18,cy-R*.18,R*.03,cx,cy,R*1.01);
  og.addColorStop(0,'#18344f');og.addColorStop(0.3,'#102540');
  og.addColorStop(0.6,'#091a30');og.addColorStop(1,'#050f1e');
  octx.fillStyle=og;octx.fillRect(cx-R,cy-R,R*2,R*2);
  octx.strokeStyle='rgba(40,120,180,0.12)';octx.lineWidth=0.5;
  for(let la=-60;la<=60;la+=30){{
    octx.beginPath();let st=false;
    for(let lo=-180;lo<=180;lo+=2){{
      const p=project(la,lo,rotLon);
      if(p.vis){{if(!st){{octx.moveTo(p.px,p.py);st=true;}}else octx.lineTo(p.px,p.py);}}else st=false;
    }}octx.stroke();
  }}
  for(let lo=0;lo<360;lo+=30){{
    octx.beginPath();let st=false;
    for(let la=-88;la<=88;la+=3){{
      const p=project(la,lo,rotLon);
      if(p.vis){{if(!st){{octx.moveTo(p.px,p.py);st=true;}}else octx.lineTo(p.px,p.py);}}else st=false;
    }}octx.stroke();
  }}
  octx.strokeStyle='rgba(40,130,200,0.20)';octx.lineWidth=0.8;
  octx.beginPath();let eq=false;
  for(let lo=-180;lo<=180;lo+=1.5){{
    const p=project(0,lo,rotLon);
    if(p.vis){{if(!eq){{octx.moveTo(p.px,p.py);eq=true;}}else octx.lineTo(p.px,p.py);}}else eq=false;
  }}octx.stroke();
  for(const poly of CONTINENTS)drawPoly(octx,poly,'#152a40','rgba(35,100,155,0.65)',0.7);
  for(const poly of ICECAPS)drawPoly(octx,poly,'rgba(185,215,235,0.55)','rgba(140,200,225,0.35)',0.5);
  const shad=octx.createRadialGradient(cx+R*.25,cy+R*.05,R*.3,cx,cy,R);
  shad.addColorStop(0,'rgba(0,0,0,0)');shad.addColorStop(0.5,'rgba(0,0,0,0)');
  shad.addColorStop(1,'rgba(0,0,12,0.82)');
  octx.fillStyle=shad;octx.fillRect(cx-R,cy-R,R*2,R*2);
  const hl=octx.createRadialGradient(cx-R*.28,cy-R*.28,0,cx-R*.08,cy-R*.08,R*.5);
  hl.addColorStop(0,'rgba(160,210,255,0.08)');hl.addColorStop(1,'rgba(0,0,0,0)');
  octx.fillStyle=hl;octx.fillRect(cx-R,cy-R,R*2,R*2);
  const front=[];
  for(const m of MK){{
    const p=project(m.la,m.lo,rotLon);
    if(p.vis&&p.z>0)front.push({{m,p}});
  }}
  front.sort((a,b)=>a.p.z-b.p.z);
  for(const{{m,p}}of front){{
    const[r,g,b]=tc(m.t);
    const col=`rgb(${{r}},${{g}},${{b}})`;
    const sz=5+Math.min(Math.abs(m.t),35)*0.07;
    const alpha=0.55+p.z*0.45;
    octx.globalAlpha=0.16*alpha;octx.fillStyle=col;
    octx.beginPath();octx.arc(p.px,p.py,sz*3.0,0,Math.PI*2);octx.fill();
    octx.globalAlpha=0.30*alpha;
    octx.beginPath();octx.arc(p.px,p.py,sz*1.8,0,Math.PI*2);octx.fill();
    octx.globalAlpha=0.95*alpha;octx.fillStyle=col;
    octx.beginPath();octx.arc(p.px,p.py,sz,0,Math.PI*2);octx.fill();
    octx.globalAlpha=0.50*alpha;octx.fillStyle='rgba(255,255,255,0.9)';
    octx.beginPath();octx.arc(p.px-sz*.30,p.py-sz*.30,sz*.30,0,Math.PI*2);octx.fill();
    octx.globalAlpha=0.22*alpha;octx.strokeStyle='rgba(0,0,0,0.8)';octx.lineWidth=0.9;
    octx.beginPath();octx.arc(p.px,p.py,sz,0,Math.PI*2);octx.stroke();
  }}
  octx.globalAlpha=1;octx.restore();
  const atmo=octx.createRadialGradient(cx,cy,R*.88,cx,cy,R*1.10);
  atmo.addColorStop(0,'rgba(0,80,200,0)');atmo.addColorStop(0.35,'rgba(20,100,220,0.17)');
  atmo.addColorStop(0.7,'rgba(40,120,230,0.07)');atmo.addColorStop(1,'rgba(0,50,160,0)');
  octx.beginPath();octx.arc(cx,cy,R*1.10,0,Math.PI*2);octx.fillStyle=atmo;octx.fill();
  octx.beginPath();octx.arc(cx,cy,R+1,0,Math.PI*2);
  octx.strokeStyle='rgba(50,130,220,0.28)';octx.lineWidth=2;octx.stroke();
  const cbW=10,cbH=Math.min(120,R*0.80);
  const cbX=cx+R+14,cbY=cy-cbH/2;
  if(cbX+40<W){{
    const cg=octx.createLinearGradient(0,cbY,0,cbY+cbH);
    cg.addColorStop(0.00,'#d73027');cg.addColorStop(0.15,'#f46d43');
    cg.addColorStop(0.30,'#fdae61');cg.addColorStop(0.44,'#fee090');
    cg.addColorStop(0.52,'#e0f3f8');cg.addColorStop(0.62,'#abd9e9');
    cg.addColorStop(0.74,'#74add1');cg.addColorStop(0.88,'#4575b4');
    cg.addColorStop(1.00,'#313695');
    octx.fillStyle=cg;octx.beginPath();octx.roundRect(cbX,cbY,cbW,cbH,3);octx.fill();
    octx.strokeStyle='rgba(255,255,255,0.12)';octx.lineWidth=0.5;
    octx.beginPath();octx.roundRect(cbX,cbY,cbW,cbH,3);octx.stroke();
    const ticks=[['30°',0],['10°',0.38],['-10°',0.76]];
    octx.font='9px monospace';octx.fillStyle='rgba(160,200,230,0.75)';octx.textAlign='left';
    octx.fillText('°C',cbX,cbY-6);
    for(const[lbl,f]of ticks){{
      const ty=cbY+f*cbH+3;
      octx.strokeStyle='rgba(160,200,230,0.35)';octx.lineWidth=0.5;
      octx.beginPath();octx.moveTo(cbX-3,ty);octx.lineTo(cbX+cbW+3,ty);octx.stroke();
      octx.fillStyle='rgba(160,200,230,0.75)';octx.fillText(lbl,cbX+cbW+5,ty+3);
    }}
  }}
  const AVG={avg_t:.1f};
  const badgeTxt=`LIVE · WeatherAPI.com  ·  Avg: ${{AVG.toFixed(1)}}°C  ·  {today_str}`;
  octx.font='10px monospace';
  const btw=octx.measureText(badgeTxt).width;
  const bpx=cx-btw/2-10,bpy=cy+R+14,bpw=btw+20,bph=18;
  if(bpy+bph<H-4){{
    octx.fillStyle='rgba(8,14,24,0.82)';
    octx.beginPath();octx.roundRect(bpx,bpy,bpw,bph,4);octx.fill();
    octx.strokeStyle='rgba(80,140,200,0.22)';octx.lineWidth=0.5;
    octx.beginPath();octx.roundRect(bpx,bpy,bpw,bph,4);octx.stroke();
    octx.fillStyle='#00e876';octx.beginPath();octx.arc(bpx+10,bpy+9,3,0,Math.PI*2);octx.fill();
    octx.fillStyle='rgba(160,200,230,0.80)';octx.textAlign='left';
    octx.fillText(badgeTxt,bpx+18,bpy+13);
  }}
  ctx.clearRect(0,0,W,H);ctx.drawImage(oc,0,0);
}}
const SPEED=0.10;
function loop(){{requestAnimationFrame(loop);
  if(!drag){{rotLon=(rotLon+SPEED)%360;velX*=.90;rotLon=(rotLon-velX*.18+360)%360;}}
  draw();}}
loop();
</script></body></html>"""

    components.html(globe_html, height=420, scrolling=False)

    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:1rem;padding:0 .5rem;margin-top:-.5rem">
      <div style="background:var(--card);border:1px solid var(--border);border-radius:4px;
                  padding:.3rem .8rem;font-size:.65rem;font-family:'Space Mono',monospace;
                  color:var(--green);letter-spacing:.1em">&#9679; LIVE · WeatherAPI.com</div>
      <div style="flex:1;height:3px;background:linear-gradient(90deg,var(--accent),var(--accent2));
                  border-radius:2px;opacity:.6"></div>
      <div style="font-size:.65rem;font-family:'Space Mono',monospace;color:var(--muted)">
        📅 {today_str} &nbsp;|&nbsp; Live Global Avg: {avg_t:.1f}°C
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── RIGHT PANEL ──────────────────────────────
with rhs_col:
    st.markdown('<div class="rhs-panel">', unsafe_allow_html=True)
    st.markdown(f'<div class="panel-title">🌐 Live Weather — {today_str}</div>', unsafe_allow_html=True)

    all_temps = [CURRENT[c]["temp"]     for c in countries]
    all_wind  = [CURRENT[c]["wind"]     for c in countries]
    all_hum   = [CURRENT[c]["humidity"] for c in countries]
    all_prec  = [CURRENT[c]["precip"]   for c in countries]

    g_temp = round(float(np.mean(all_temps)), 1)
    g_wind = round(float(np.mean(all_wind)),  1)
    g_hum  = round(float(np.mean(all_hum)),   1)
    g_prec = round(float(np.mean(all_prec)),  1)

    hottest_c = max(countries, key=lambda c: CURRENT[c]["temp"])
    coldest_c = min(countries, key=lambda c: CURRENT[c]["temp"])

    st.markdown(f"""
    <div class="weather-card">
      <div class="wc-label">GLOBAL TEMPERATURE <span class="wc-icon">🌡</span></div>
      <div class="wc-value">{g_temp}<span class="wc-unit"> °C</span></div>
      <div class="wc-sub">Live global mean · WeatherAPI.com</div>
      <div class="wc-live"><span class="wc-live-dot"></span> LIVE · {now_str}</div>
    </div>
    <div class="weather-card">
      <div class="wc-label">WIND SPEED <span class="wc-icon">💨</span></div>
      <div class="wc-value">{g_wind}<span class="wc-unit"> km/h</span></div>
      <div class="wc-sub">Live global average</div>
      <div class="wc-live"><span class="wc-live-dot"></span> LIVE · {now_str}</div>
    </div>
    <div class="weather-card">
      <div class="wc-label">HUMIDITY <span class="wc-icon">💧</span></div>
      <div class="wc-value">{g_hum}<span class="wc-unit"> %</span></div>
      <div class="wc-sub">Live relative humidity</div>
      <div class="wc-live"><span class="wc-live-dot"></span> LIVE · {now_str}</div>
    </div>
    <div class="weather-card">
      <div class="wc-label">PRECIPITATION <span class="wc-icon">🌧</span></div>
      <div class="wc-value">{g_prec}<span class="wc-unit"> mm</span></div>
      <div class="wc-sub">Live average rainfall</div>
      <div class="wc-live"><span class="wc-live-dot"></span> LIVE · {now_str}</div>
    </div>
    <div class="weather-card" style="padding:.7rem 1rem">
      <div class="wc-label" style="margin-bottom:.5rem">TODAY'S EXTREMES 🔥❄️</div>
      <div style="font-size:.8rem;color:var(--muted);font-family:'Space Mono',monospace;line-height:2">
        🔥 <b style="color:#ff6b35">{hottest_c}</b> — {CURRENT[hottest_c]['temp']:.1f}°C<br>
        &nbsp;&nbsp;&nbsp;&nbsp;<span style="font-size:.65rem">{CURRENT[hottest_c]['condition']}</span><br>
        ❄️ <b style="color:#4fc3f7">{coldest_c}</b> — {CURRENT[coldest_c]['temp']:.1f}°C<br>
        &nbsp;&nbsp;&nbsp;&nbsp;<span style="font-size:.65rem">{CURRENT[coldest_c]['condition']}</span>
      </div>
    </div>
    <div class="premium-card">
      <span class="pc-icon">⚡</span>
      <div>
        <div class="pc-title">Real-Time Data</div>
        <div class="pc-sub">Powered by WeatherAPI.com · Updates every 30 min</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)