import streamlit as st
import numpy as np
import json
import datetime
import requests
import time
import threading

WEATHER_API_KEY = "ec0aaf3d97ea407cbd7130905261403"
WEATHER_API_URL = "http://api.weatherapi.com/v1/current.json"

st.set_page_config(
    page_title="DUNIYA · Global Weather",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=Syne:wght@400;600;700;800&display=swap');
:root{
  --bg:#04080f;--surface:#080e1a;--card:#0c1525;--border:#13213a;
  --accent:#00c8ff;--accent2:#ff4d6d;--accent3:#00ff9d;
  --text:#b8d4f0;--muted:#2d4a6e;--dim:#1a3050;
  --warn:#ffb700;--purple:#9d7dff;
}
*{box-sizing:border-box;margin:0;padding:0}
html,body,[data-testid="stAppViewContainer"],[data-testid="stMain"]{
  background:var(--bg)!important;color:var(--text)!important;
  font-family:'Syne',sans-serif}
[data-testid="stHeader"],[data-testid="stSidebar"],[data-testid="stToolbar"],#MainMenu,footer{display:none!important}
[data-testid="stMainBlockContainer"]{padding:0!important;max-width:100%!important}
section.main>div{padding:0!important}

/* ── NAVBAR ── */
.nav{display:flex;align-items:center;justify-content:space-between;
  background:rgba(8,14,26,.95);backdrop-filter:blur(12px);
  padding:0 1.8rem;height:56px;position:sticky;top:0;z-index:200;
  border-bottom:1px solid var(--border)}
.nav::after{content:'';position:absolute;bottom:-1px;left:0;width:60px;
  height:2px;background:linear-gradient(90deg,var(--accent),transparent)}
.nav-logo{display:flex;align-items:center;gap:.5rem;font-size:1rem;
  font-weight:800;letter-spacing:.06em;color:var(--accent)}
.nav-logo em{color:var(--text);font-style:normal;font-weight:600}
.nav-center{display:flex;gap:2.4rem;font-size:.72rem;font-weight:600;
  letter-spacing:.1em;text-transform:uppercase}
.nav-link{color:var(--muted);cursor:pointer;padding:.3rem 0;
  border-bottom:2px solid transparent;transition:all .2s}
.nav-link.on{color:var(--accent);border-color:var(--accent)}
.nav-right{display:flex;align-items:center;gap:.8rem}
.live-chip{display:inline-flex;align-items:center;gap:5px;font-size:.6rem;
  font-family:'JetBrains Mono',monospace;color:var(--accent3);letter-spacing:.08em;
  background:rgba(0,255,157,.07);border:1px solid rgba(0,255,157,.2);
  border-radius:3px;padding:2px 8px}
.ld{width:5px;height:5px;border-radius:50%;background:var(--accent3);animation:pulse 1.5s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.2}}
.time-chip{font-size:.62rem;font-family:'JetBrains Mono',monospace;color:var(--muted);
  background:var(--card);border:1px solid var(--border);border-radius:4px;padding:3px 9px}

/* ── SEARCH BAR ── */
.search-bar{background:rgba(8,14,26,.9);border-bottom:1px solid var(--border);
  padding:0 1.8rem;height:48px;display:flex;align-items:center;gap:1rem;
  position:sticky;top:56px;z-index:199}
.s-box{flex:1;max-width:580px;display:flex;align-items:center;gap:.6rem;
  background:rgba(0,200,255,.05);border:1.5px solid rgba(0,200,255,.3);
  border-radius:8px;padding:.3rem 1rem;height:34px;
  box-shadow:0 0 16px rgba(0,200,255,.12);transition:box-shadow .2s}
.s-box:focus-within{box-shadow:0 0 28px rgba(0,200,255,.28);border-color:var(--accent)}
.s-icon{color:var(--muted);font-size:.8rem;flex-shrink:0}
.s-pills{display:flex;gap:.5rem;align-items:center}
.s-pill{font-size:.6rem;font-family:'JetBrains Mono',monospace;
  background:rgba(0,200,255,.08);border:1px solid rgba(0,200,255,.2);
  border-radius:3px;padding:2px 7px;color:var(--muted);cursor:pointer;
  transition:all .15s}
.s-pill:hover{color:var(--accent);border-color:var(--accent)}

/* ── LOADING SCREEN ── */
.ld-wrap{display:flex;align-items:center;justify-content:center;
  min-height:82vh;background:var(--bg)}
.ld-card{background:var(--surface);border:1px solid var(--border);
  border-radius:16px;padding:3rem 3.5rem;width:440px;
  display:flex;flex-direction:column;align-items:center;gap:1.2rem;
  position:relative;overflow:hidden}
.ld-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,var(--accent),var(--accent2),transparent)}
.ld-title{font-size:.85rem;font-weight:700;color:var(--accent);
  font-family:'JetBrains Mono',monospace;letter-spacing:.1em;text-align:center}
.ld-timer{font-size:3rem;font-weight:700;font-family:'JetBrains Mono',monospace;
  color:var(--text);letter-spacing:.04em;line-height:1}
.ld-sub{font-size:.62rem;color:var(--muted);font-family:'JetBrains Mono',monospace;
  text-align:center;line-height:1.8}
.ld-prog{width:100%;background:var(--card);border:1px solid var(--border);
  border-radius:8px;padding:.65rem .9rem}
.ld-prog-top{display:flex;justify-content:space-between;font-size:.58rem;
  font-family:'JetBrains Mono',monospace;color:var(--muted);margin-bottom:.45rem}
.ld-prog-top span:last-child{color:var(--accent)}
.ld-track{height:4px;background:rgba(0,200,255,.1);border-radius:2px;overflow:hidden}
.ld-fill{height:4px;background:linear-gradient(90deg,var(--accent),var(--accent2));
  border-radius:2px;transition:width .35s ease}
.ld-hint{font-size:.56rem;color:rgba(45,74,110,.7);
  font-family:'JetBrains Mono',monospace;text-align:center}

/* ── MAIN LAYOUT ── */
.outer{display:grid;grid-template-columns:220px 1fr 260px;gap:0;min-height:calc(100vh - 104px)}
.panel-l{background:var(--surface);border-right:1px solid var(--border);
  padding:1rem .8rem;overflow-y:auto;display:flex;flex-direction:column;gap:1rem}
.panel-c{background:var(--bg);padding:0;overflow:hidden}
.panel-r{background:var(--surface);border-left:1px solid var(--border);
  padding:1rem .8rem;overflow-y:auto;display:flex;flex-direction:column;gap:.55rem}

.sect-title{font-size:.58rem;font-weight:700;letter-spacing:.15em;
  text-transform:uppercase;color:var(--muted);margin-bottom:.6rem;
  display:flex;align-items:center;gap:.5rem}
.sect-title::after{content:'';flex:1;height:1px;background:var(--border)}

/* ── RECENT ITEMS ── */
.ri{display:flex;align-items:center;justify-content:space-between;
  padding:.55rem .7rem;background:var(--card);border:1px solid var(--border);
  border-radius:7px;margin-bottom:.4rem;cursor:pointer;transition:all .2s}
.ri:hover{border-color:var(--accent);transform:translateX(2px)}
.ri-l{display:flex;align-items:center;gap:.55rem}
.ri-name{font-size:.82rem;font-weight:700}
.ri-meta{font-size:.56rem;color:var(--muted);font-family:'JetBrains Mono',monospace}
.ri-temp{font-size:1rem;font-weight:800;font-family:'JetBrains Mono',monospace}

/* ── QUICK ACCESS BUTTONS ── */
.qa-grid{display:grid;grid-template-columns:1fr 1fr;gap:.35rem}
.qa-btn{background:var(--card);border:1px solid var(--border);border-radius:6px;
  padding:.4rem .5rem;font-size:.72rem;font-weight:600;cursor:pointer;
  text-align:center;transition:all .2s;color:var(--text)}
.qa-btn:hover{border-color:var(--accent);color:var(--accent);
  background:rgba(0,200,255,.06)}

/* ── STATS CARDS (right panel) ── */
.stat-card{background:var(--card);border:1px solid var(--border);
  border-radius:8px;padding:.8rem .9rem;position:relative;overflow:hidden;
  flex-shrink:0}
.stat-card::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;
  background:linear-gradient(90deg,var(--accent),transparent);opacity:.6}
.sc-label{font-size:.56rem;letter-spacing:.12em;text-transform:uppercase;
  color:var(--muted);font-family:'JetBrains Mono',monospace;
  display:flex;justify-content:space-between;margin-bottom:.35rem}
.sc-val{font-size:1.6rem;font-weight:800;color:var(--text);
  font-family:'JetBrains Mono',monospace;letter-spacing:-.02em;line-height:1}
.sc-unit{font-size:.8rem;font-weight:400;color:var(--muted)}
.sc-sub{font-size:.6rem;color:var(--muted);margin-top:.2rem;
  font-family:'JetBrains Mono',monospace}
.sc-live{display:inline-flex;align-items:center;gap:4px;font-size:.56rem;
  font-family:'JetBrains Mono',monospace;color:var(--accent3);margin-top:.25rem}
.sc-live-dot{width:4px;height:4px;border-radius:50%;background:var(--accent3);
  animation:pulse 1.5s infinite}

/* ── EXTREMES CARD ── */
.ext-card{background:var(--card);border:1px solid var(--border);border-radius:8px;
  padding:.75rem .9rem}
.ext-row{display:flex;align-items:center;justify-content:space-between;
  padding:.22rem 0;font-size:.72rem}
.ext-name{font-family:'JetBrains Mono',monospace;font-size:.68rem}
.ext-temp{font-family:'JetBrains Mono',monospace;font-size:.8rem;font-weight:700}

/* ── GLOBAL RANK STRIP ── */
.rank-strip{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:.65rem .8rem}
.rank-item{display:flex;align-items:center;gap:.5rem;padding:.18rem 0;
  border-bottom:1px solid rgba(255,255,255,.03);font-size:.72rem}
.rank-num{width:16px;font-family:'JetBrains Mono',monospace;
  font-size:.58rem;color:var(--muted)}
.rank-bar-wrap{flex:1;height:3px;background:var(--dim);border-radius:2px}
.rank-bar{height:3px;border-radius:2px}
.rank-val{width:45px;text-align:right;font-family:'JetBrains Mono',monospace;
  font-size:.65rem;font-weight:700}

/* RADAR HEADER */
.radar-head{display:flex;align-items:center;justify-content:space-between;
  padding:.8rem 1rem .4rem}
.radar-title{font-size:.62rem;letter-spacing:.12em;text-transform:uppercase;
  color:var(--muted);font-family:'JetBrains Mono',monospace;
  display:flex;align-items:center;gap:.5rem}
.radar-dot{width:7px;height:7px;border-radius:50%;background:var(--accent3);
  box-shadow:0 0 6px var(--accent3)}

/* ── STREAMLIT OVERRIDES ── */
[data-testid="stForm"]{border:none!important;padding:0!important;background:transparent!important}
[data-testid="stForm"]>div{padding:0!important;background:transparent!important}
[data-testid="stTextInput"] input{
  background:transparent!important;border:none!important;
  color:var(--text)!important;font-family:'Syne',sans-serif!important;
  font-size:.85rem!important;padding:0!important;box-shadow:none!important}
[data-testid="stTextInput"] input:focus{outline:none!important;box-shadow:none!important}
[data-testid="stTextInput"]>div,[data-testid="stTextInput"]>div>div{
  background:transparent!important;border:none!important;padding:0!important}
[data-testid="stTextInput"] label{display:none!important}
[data-testid="stButton"] button{
  background:var(--accent)!important;border:none!important;color:#04080f!important;
  font-family:'Syne',sans-serif!important;font-size:.82rem!important;
  font-weight:700!important;letter-spacing:.06em!important;
  padding:.42rem 1.3rem!important;border-radius:6px!important;
  transition:opacity .2s!important}
[data-testid="stButton"] button:hover{opacity:.85!important}
[data-testid="stAlert"]{
  background:rgba(255,77,109,.07)!important;
  border:1px solid rgba(255,77,109,.3)!important;
  border-radius:6px!important;color:var(--text)!important;
  font-size:.8rem!important;margin:.2rem 1.5rem!important}
[data-testid="column"]{padding:0!important}
.stColumns{gap:0!important}

/* SCROLLBAR */
::-webkit-scrollbar{width:4px}
::-webkit-scrollbar-track{background:var(--bg)}
::-webkit-scrollbar-thumb{background:var(--dim);border-radius:2px}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  COUNTRY DATA
# ─────────────────────────────────────────────
COUNTRY_DATA = {
    "Afghanistan":    {"lat": 33.9,  "lon":  67.7, "query": "Kabul",         "flag":"🇦🇫","region":"Asia"},
    "Argentina":      {"lat":-38.4,  "lon": -63.6, "query": "Buenos Aires",  "flag":"🇦🇷","region":"S.America"},
    "Australia":      {"lat":-25.3,  "lon": 133.8, "query": "Sydney",        "flag":"🇦🇺","region":"Oceania"},
    "Brazil":         {"lat":-14.2,  "lon": -51.9, "query": "Brasilia",      "flag":"🇧🇷","region":"S.America"},
    "Canada":         {"lat": 56.1,  "lon":-106.3, "query": "Ottawa",        "flag":"🇨🇦","region":"N.America"},
    "China":          {"lat": 35.9,  "lon": 104.2, "query": "Beijing",       "flag":"🇨🇳","region":"Asia"},
    "Denmark":        {"lat": 56.3,  "lon":   9.5, "query": "Copenhagen",    "flag":"🇩🇰","region":"Europe"},
    "Egypt":          {"lat": 26.8,  "lon":  30.8, "query": "Cairo",         "flag":"🇪🇬","region":"Africa"},
    "Ethiopia":       {"lat":  9.1,  "lon":  40.5, "query": "Addis Ababa",   "flag":"🇪🇹","region":"Africa"},
    "France":         {"lat": 46.2,  "lon":   2.2, "query": "Paris",         "flag":"🇫🇷","region":"Europe"},
    "Germany":        {"lat": 51.2,  "lon":  10.5, "query": "Berlin",        "flag":"🇩🇪","region":"Europe"},
    "Greenland":      {"lat": 71.7,  "lon": -42.6, "query": "Nuuk",          "flag":"🇬🇱","region":"Arctic"},
    "India":          {"lat": 20.6,  "lon":  78.9, "query": "New Delhi",     "flag":"🇮🇳","region":"Asia"},
    "Indonesia":      {"lat": -0.8,  "lon": 113.9, "query": "Jakarta",       "flag":"🇮🇩","region":"Asia"},
    "Iran":           {"lat": 32.4,  "lon":  53.7, "query": "Tehran",        "flag":"🇮🇷","region":"Asia"},
    "Japan":          {"lat": 36.2,  "lon": 138.2, "query": "Tokyo",         "flag":"🇯🇵","region":"Asia"},
    "Kenya":          {"lat": -0.0,  "lon":  37.9, "query": "Nairobi",       "flag":"🇰🇪","region":"Africa"},
    "Mexico":         {"lat": 23.6,  "lon":-102.6, "query": "Mexico City",   "flag":"🇲🇽","region":"N.America"},
    "Morocco":        {"lat": 31.8,  "lon":  -7.1, "query": "Rabat",         "flag":"🇲🇦","region":"Africa"},
    "Netherlands":    {"lat": 52.1,  "lon":   5.3, "query": "Amsterdam",     "flag":"🇳🇱","region":"Europe"},
    "New Zealand":    {"lat":-40.9,  "lon": 174.9, "query": "Wellington",    "flag":"🇳🇿","region":"Oceania"},
    "Nigeria":        {"lat":  9.1,  "lon":   8.7, "query": "Abuja",         "flag":"🇳🇬","region":"Africa"},
    "Norway":         {"lat": 60.5,  "lon":   8.5, "query": "Oslo",          "flag":"🇳🇴","region":"Europe"},
    "Pakistan":       {"lat": 30.4,  "lon":  69.3, "query": "Islamabad",     "flag":"🇵🇰","region":"Asia"},
    "Peru":           {"lat": -9.2,  "lon": -75.0, "query": "Lima",          "flag":"🇵🇪","region":"S.America"},
    "Poland":         {"lat": 51.9,  "lon":  19.1, "query": "Warsaw",        "flag":"🇵🇱","region":"Europe"},
    "Russia":         {"lat": 61.5,  "lon": 105.3, "query": "Moscow",        "flag":"🇷🇺","region":"Europe"},
    "Saudi Arabia":   {"lat": 23.9,  "lon":  45.1, "query": "Riyadh",        "flag":"🇸🇦","region":"Asia"},
    "South Africa":   {"lat":-30.6,  "lon":  22.9, "query": "Cape Town",     "flag":"🇿🇦","region":"Africa"},
    "South Korea":    {"lat": 35.9,  "lon": 127.8, "query": "Seoul",         "flag":"🇰🇷","region":"Asia"},
    "Spain":          {"lat": 40.5,  "lon":  -3.7, "query": "Madrid",        "flag":"🇪🇸","region":"Europe"},
    "Sweden":         {"lat": 60.1,  "lon":  18.6, "query": "Stockholm",     "flag":"🇸🇪","region":"Europe"},
    "Switzerland":    {"lat": 46.8,  "lon":   8.2, "query": "Bern",          "flag":"🇨🇭","region":"Europe"},
    "Turkey":         {"lat": 38.9,  "lon":  35.2, "query": "Ankara",        "flag":"🇹🇷","region":"Asia"},
    "Ukraine":        {"lat": 48.4,  "lon":  31.2, "query": "Kyiv",          "flag":"🇺🇦","region":"Europe"},
    "United Kingdom": {"lat": 55.4,  "lon":  -3.4, "query": "London",        "flag":"🇬🇧","region":"Europe"},
    "United States":  {"lat": 37.1,  "lon": -95.7, "query": "Washington",    "flag":"🇺🇸","region":"N.America"},
    "Venezuela":      {"lat":  6.4,  "lon": -66.6, "query": "Caracas",       "flag":"🇻🇪","region":"S.America"},
    "Vietnam":        {"lat": 14.1,  "lon": 108.3, "query": "Hanoi",         "flag":"🇻🇳","region":"Asia"},
}

FALLBACK = {
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

RECENT = [
    ("London, UK",    "United Kingdom", "2m ago"),
    ("New York, USA", "United States",  "15m ago"),
    ("Tokyo, JP",     "Japan",          "1h ago"),
    ("Sydney, AU",    "Australia",      "4h ago"),
    ("Mumbai, IN",    "India",          "5m ago"),
]

QUICK = [
    ("🇮🇳","India"),("🇺🇸","United States"),("🇧🇷","Brazil"),
    ("🇯🇵","Japan"),("🇷🇺","Russia"),("🇦🇺","Australia"),
    ("🇩🇪","Germany"),("🇨🇳","China"),("🇬🇧","United Kingdom"),("🇳🇴","Norway"),
]

# ─────────────────────────────────────────────
#  WEATHER FETCH
# ─────────────────────────────────────────────
@st.cache_data(ttl=1800, show_spinner=False)
def fetch_weather(query: str) -> dict | None:
    try:
        r = requests.get(WEATHER_API_URL,
            params={"key": WEATHER_API_KEY, "q": query, "aqi": "no"}, timeout=8)
        if r.status_code != 200:
            return None
        cur = r.json()["current"]
        return {
            "temp":       round(cur["temp_c"], 1),
            "feels_like": round(cur["feelslike_c"], 1),
            "wind":       round(cur["wind_kph"], 1),
            "humidity":   cur["humidity"],
            "precip":     round(cur["precip_mm"], 1),
            "condition":  cur["condition"]["text"],
            "uv":         cur.get("uv", 0),
            "cloud":      cur.get("cloud", 0),
            "wind_dir":   cur.get("wind_dir", "—"),
        }
    except:
        return None

# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────
if "selected_country" not in st.session_state:
    st.session_state.selected_country = None
if "error_msg" not in st.session_state:
    st.session_state.error_msg = ""
if "weather_loaded" not in st.session_state:
    st.session_state.weather_loaded = False

today_str = datetime.date.today().strftime("%d %b %Y")
now_str   = datetime.datetime.now().strftime("%H:%M UTC")

# ─────────────────────────────────────────────
#  NAVBAR
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="nav">
  <div class="nav-logo">🌐 <em>DUNIYA</em></div>
  <div class="nav-center">
    <span class="nav-link on">Globe</span>
    <span class="nav-link">Analytics</span>
    <span class="nav-link">Alerts</span>
  </div>
  <div class="nav-right">
    <span class="live-chip"><span class="ld"></span>LIVE · WeatherAPI</span>
    <span class="time-chip">📅 {today_str} · {now_str}</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SEARCH BAR
# ─────────────────────────────────────────────
st.markdown('<div class="search-bar">', unsafe_allow_html=True)
with st.form("sf", clear_on_submit=False):
    c1, c2 = st.columns([9, 1])
    with c1:
        st.markdown('<div class="s-box"><span class="s-icon">⌕</span>', unsafe_allow_html=True)
        query = st.text_input("q", placeholder="Search any country — India, Norway, Brazil…",
                              label_visibility="collapsed", key="sq")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        sbtn = st.form_submit_button("Search", use_container_width=True)

st.markdown("""
<div class="s-pills" style="margin-left:1rem">
  <span style="font-size:.58rem;color:var(--muted);font-family:'JetBrains Mono',monospace;margin-right:.2rem">Quick:</span>
  <span class="s-pill">🇮🇳 India</span>
  <span class="s-pill">🇺🇸 USA</span>
  <span class="s-pill">🇯🇵 Japan</span>
  <span class="s-pill">🇳🇴 Norway</span>
  <span class="s-pill">🇧🇷 Brazil</span>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

if sbtn and query:
    ql = query.strip().lower()
    match = next((c for c in COUNTRY_DATA if ql in c.lower()), None)
    if match:
        st.session_state.selected_country = match
        st.session_state.error_msg = ""
        st.switch_page("pages/country_analysis.py")
    else:
        st.session_state.error_msg = f'"{query}" not found. Try: India, Brazil, Japan…'

if st.session_state.error_msg:
    st.error(st.session_state.error_msg)

# ─────────────────────────────────────────────
#  WEATHER FETCH WITH LOADING SCREEN
# ─────────────────────────────────────────────
_total = len(COUNTRY_DATA)

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
                fb = FALLBACK.get(country, 15.0)
                out[country] = {"temp": fb, "feels_like": fb,
                                "wind": 10.0, "humidity": 60, "precip": 0.0,
                                "condition": "Unavailable", "uv": 0, "cloud": 0, "wind_dir": "—"}
            _fetched[0] = i + 1
        _result[0] = out
        _done[0]   = True

    t = threading.Thread(target=_bg_fetch, daemon=True)
    t.start()
    slot = st.empty()
    t0   = time.time()

    while not _done[0]:
        el   = int(time.time() - t0)
        mm, ss = el // 60, el % 60
        pct  = int(_fetched[0] / _total * 100)
        slot.markdown(f"""
        <div class="ld-wrap">
          <div class="ld-card">
            <span class="live-chip"><span class="ld"></span>LIVE · WeatherAPI.com</span>
            <div class="ld-title">⚡ FETCHING GLOBAL WEATHER</div>
            <div class="ld-timer">{mm:02d}:{ss:02d}</div>
            <div class="ld-sub">Pulling real-time data for {_total} countries<br>
              This only happens once — cached for 30 minutes</div>
            <div class="ld-prog">
              <div class="ld-prog-top">
                <span>COUNTRIES LOADED</span>
                <span>{_fetched[0]} / {_total} · {pct}%</span>
              </div>
              <div class="ld-track">
                <div class="ld-fill" style="width:{pct}%"></div>
              </div>
            </div>
            <div class="ld-hint">⏱ Cached 30 min · No loading on re-runs</div>
          </div>
        </div>""", unsafe_allow_html=True)
        time.sleep(0.4)

    t.join()
    slot.empty()
    CURRENT = _result[0]
    st.session_state["CURRENT"]    = CURRENT
    st.session_state["fetch_time"] = time.time()
    st.session_state.weather_loaded = True
else:
    CURRENT = st.session_state.get("CURRENT", {})
    if time.time() - st.session_state.get("fetch_time", 0) > 1800:
        st.session_state.weather_loaded = False
        st.rerun()

countries = list(COUNTRY_DATA.keys())

# ─────────────────────────────────────────────
#  COMPUTED STATS
# ─────────────────────────────────────────────
all_temps  = [CURRENT[c]["temp"]     for c in countries]
all_wind   = [CURRENT[c]["wind"]     for c in countries]
all_hum    = [CURRENT[c]["humidity"] for c in countries]
all_prec   = [CURRENT[c]["precip"]   for c in countries]
g_temp     = round(float(np.mean(all_temps)), 1)
g_wind     = round(float(np.mean(all_wind)),  1)
g_hum      = round(float(np.mean(all_hum)),   1)
g_prec     = round(float(np.mean(all_prec)),  1)
hottest    = max(countries, key=lambda c: CURRENT[c]["temp"])
coldest    = min(countries, key=lambda c: CURRENT[c]["temp"])
windiest   = max(countries, key=lambda c: CURRENT[c]["wind"])

# Rank top 8 hottest
top8 = sorted(countries, key=lambda c: CURRENT[c]["temp"], reverse=True)[:8]
max_t = CURRENT[top8[0]]["temp"]
min_t = CURRENT[top8[-1]]["temp"]

markers_json = json.dumps([
    {"n": c, "la": COUNTRY_DATA[c]["lat"], "lo": COUNTRY_DATA[c]["lon"],
     "t": CURRENT[c]["temp"], "cond": CURRENT[c]["condition"],
     "wind": CURRENT[c]["wind"], "hum": CURRENT[c]["humidity"]}
    for c in countries
])
avg_t = float(np.mean(all_temps))

# ─────────────────────────────────────────────
#  THREE-COLUMN LAYOUT
# ─────────────────────────────────────────────
st.markdown('<div class="outer">', unsafe_allow_html=True)

# ── LEFT PANEL ──
lhs, center, rhs = st.columns([2.0, 5.8, 2.2])

with lhs:
    st.markdown('<div class="panel-l">', unsafe_allow_html=True)

    # Recent
    st.markdown('<div class="sect-title">🕐 Recent</div>', unsafe_allow_html=True)
    for label, ckey, ago in RECENT:
        t = CURRENT[ckey]["temp"]
        col = "#ff4d6d" if t > 28 else "#00c8ff" if t < 5 else "#ffb700"
        st.markdown(f"""
        <div class="ri">
          <div class="ri-l">
            <span style="font-size:.75rem">{COUNTRY_DATA[ckey]['flag']}</span>
            <div>
              <div class="ri-name">{label}</div>
              <div class="ri-meta">{ago}</div>
            </div>
          </div>
          <div class="ri-temp" style="color:{col}">{t:.1f}°</div>
        </div>""", unsafe_allow_html=True)

    # Quick access
    st.markdown('<br><div class="sect-title">⚡ Quick Access</div>', unsafe_allow_html=True)
    st.markdown('<div class="qa-grid">', unsafe_allow_html=True)
    for flag, cname in QUICK:
        if st.button(f"{flag} {cname.split()[0]}", key=f"q_{cname}", use_container_width=True):
            st.session_state.selected_country = cname
            st.switch_page("pages/country_analysis.py")
    st.markdown('</div>', unsafe_allow_html=True)

    # Weather legend
    st.markdown("""
    <br>
    <div class="sect-title">🌡 Temp Scale</div>
    <div style="font-size:.6rem;font-family:'JetBrains Mono',monospace;
                color:var(--muted);line-height:2.2">
      <span style="color:#ff4d6d">■</span> &gt;28°C · Hot<br>
      <span style="color:#ffb700">■</span> 14–28°C · Moderate<br>
      <span style="color:#00c8ff">■</span> &lt;14°C · Cool<br>
      <span style="color:#9d7dff">■</span> &lt;0°C · Freezing
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ── CENTER: GLOBE ──
with center:
    st.markdown(f"""
    <div class="radar-head">
      <div class="radar-title"><span class="radar-dot"></span>WORLD WEATHER · LIVE GLOBE</div>
      <span style="font-size:.58rem;font-family:'JetBrains Mono',monospace;color:var(--muted)">
        Avg {avg_t:.1f}°C · {today_str}
      </span>
    </div>""", unsafe_allow_html=True)

    import streamlit.components.v1 as components
    globe_html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:100%;height:100%;overflow:hidden;background:#04080f}}
canvas{{position:absolute;top:0;left:0;display:block}}
#tip{{position:fixed;display:none;pointer-events:none;
  background:rgba(4,8,15,.97);border:1px solid rgba(0,200,255,.4);
  border-radius:9px;padding:10px 14px;color:#b8d4f0;
  font-family:monospace;font-size:12px;line-height:1.8;
  white-space:nowrap;z-index:99;box-shadow:0 6px 24px rgba(0,0,0,.7)}}
#tip b{{color:#00c8ff;display:block;font-size:13px;font-weight:700;margin-bottom:2px}}
#tip .meta{{font-size:10px;color:#2d4a6e}}
</style></head><body>
<canvas id="cv"></canvas><div id="tip"></div>
<script>
const MK={markers_json};
const DATE="{today_str}";
const cv=document.getElementById('cv');
const ctx=cv.getContext('2d');
let W,H,R,cx,cy;
function resize(){{
  W=document.documentElement.clientWidth||window.innerWidth;
  H=document.documentElement.clientHeight||window.innerHeight;
  const dpr=window.devicePixelRatio||1;
  cv.width=Math.round(W*dpr);
  cv.height=Math.round(H*dpr);
  cv.style.width=W+'px';
  cv.style.height=H+'px';
  ctx.setTransform(dpr,0,0,dpr,0,0);
  R=Math.floor(Math.min(W,H)*0.34);
  R=Math.min(R,Math.floor(W/2)-60,Math.floor(H/2)-40);
  R=Math.max(R,60);
  cx=Math.floor(W/2);
  cy=Math.floor(H/2);
}}
resize();
window.addEventListener('resize',resize);
// Also handle Streamlit iframe load timing
setTimeout(resize,100);
setTimeout(resize,400);

function tc(t){{
  const stops=[[0,[49,54,149]],[0.18,[69,117,180]],[0.36,[171,217,233]],
    [0.50,[224,243,248]],[0.60,[145,207,96]],[0.72,[254,224,139]],
    [0.84,[252,141,89]],[1,[215,48,39]]];
  const lo=-20,hi=35;
  const f=Math.max(0,Math.min(1,(t-lo)/(hi-lo)));
  for(let i=1;i<stops.length;i++){{
    const[f0,c0]=stops[i-1],[f1,c1]=stops[i];
    if(f<=f1){{const u=(f-f0)/(f1-f0);
      return[c0[0]+(c1[0]-c0[0])*u,c0[1]+(c1[1]-c0[1])*u,c0[2]+(c1[2]-c0[2])*u].map(Math.round);}}
  }}
  return[215,48,39];
}}

function proj(lat,lon,rl){{
  const phi=(90-lat)*Math.PI/180,th=(lon-rl)*Math.PI/180;
  const x=Math.sin(phi)*Math.sin(th),y=Math.cos(phi),z=Math.sin(phi)*Math.cos(th);
  return{{px:cx+R*x,py:cy-R*y,z,vis:z>0}};
}}

const LAND=[
  [[-168,72],[-140,70],[-125,50],[-118,32],[-110,23],[-87,16],[-83,10],[-77,8],
   [-80,25],[-90,30],[-97,26],[-105,20],[-117,32],[-120,35],[-124,46],[-130,54],
   [-140,60],[-158,60],[-168,72]],
  [[-45,60],[-20,63],[-18,70],[-20,76],[-30,83],[-50,83],[-65,80],[-72,75],
   [-68,65],[-55,60],[-45,60]],
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
  [[114,-22],[118,-20],[122,-18],[128,-15],[132,-12],[136,-12],[140,-17],
   [142,-18],[145,-15],[148,-20],[152,-25],[154,-28],[152,-35],[148,-38],
   [145,-38],[140,-38],[136,-35],[130,-32],[124,-32],[116,-32],[114,-28],[114,-22]],
];
const ICE=[
  [[-180,75],[-150,74],[-120,74],[-90,75],[-60,74],[-30,74],[0,74],[30,74],
   [60,74],[90,75],[120,74],[150,74],[180,75],[180,90],[0,90],[-180,90],[-180,75]],
  [[-180,-65],[-150,-64],[-120,-64],[-90,-65],[-60,-64],[-30,-64],[0,-64],
   [30,-64],[60,-64],[90,-65],[120,-64],[150,-64],[180,-65],[180,-90],[0,-90],
   [-180,-90],[-180,-65]],
];

const oc=document.createElement('canvas');
const oc2=oc.getContext('2d');
let rotLon=20,drag=false,dragX=0,velX=0;
cv.style.cursor='grab';
cv.addEventListener('mousedown',e=>{{drag=true;dragX=e.clientX;velX=0;cv.style.cursor='grabbing';}});
window.addEventListener('mouseup',()=>{{drag=false;cv.style.cursor='grab';}});
window.addEventListener('mousemove',e=>{{
  if(drag){{const dx=e.clientX-dragX;velX=dx*.5;rotLon=(rotLon-dx*.45+360)%360;dragX=e.clientX;}}
}});
cv.addEventListener('touchstart',e=>{{drag=true;dragX=e.touches[0].clientX;velX=0;}},{{passive:true}});
window.addEventListener('touchend',()=>drag=false);
window.addEventListener('touchmove',e=>{{
  if(drag){{const dx=e.touches[0].clientX-dragX;velX=dx*.5;rotLon=(rotLon-dx*.45+360)%360;dragX=e.touches[0].clientX;}}
}},{{passive:true}});

const tip=document.getElementById('tip');
cv.addEventListener('mousemove',e=>{{
  const r=cv.getBoundingClientRect(),mx=e.clientX-r.left,my=e.clientY-r.top;
  let found=false;
  for(const m of MK){{
    const p=proj(m.la,m.lo,rotLon);
    if(!p.vis)continue;
    const dx=mx-p.px,dy=my-p.py;
    if(dx*dx+dy*dy<160){{
      tip.innerHTML=`<b>${{m.n}}</b>🌡 ${{m.t.toFixed(1)}}°C · 💨 ${{m.wind}} km/h<div class="meta">💧 ${{m.hum}}% · ${{m.cond}} · ${{DATE}}</div>`;
      tip.style.display='block';tip.style.left=(e.clientX+16)+'px';tip.style.top=(e.clientY-12)+'px';
      cv.style.cursor='pointer';found=true;break;
    }}
  }}
  if(!found){{tip.style.display='none';if(!drag)cv.style.cursor='grab';}}
}});
cv.addEventListener('mouseleave',()=>tip.style.display='none');

function drawPoly(pts,fill,stroke,sw){{
  const dense=[];
  for(let i=0;i<pts.length;i++){{
    const[lo0,la0]=pts[i],[lo1,la1]=pts[(i+1)%pts.length];
    dense.push(pts[i]);
    const steps=Math.max(1,Math.round(Math.abs(lo1-lo0)/4));
    for(let s=1;s<steps;s++)dense.push([lo0+(lo1-lo0)*s/steps,la0+(la1-la0)*s/steps]);
  }}
  oc2.beginPath();let first=true;
  for(const[lo,la]of dense){{
    const p=proj(la,lo,rotLon);
    if(first){{oc2.moveTo(p.px,p.py);first=false;}}else oc2.lineTo(p.px,p.py);
  }}
  oc2.closePath();
  if(fill){{oc2.fillStyle=fill;oc2.fill();}}
  if(stroke){{oc2.strokeStyle=stroke;oc2.lineWidth=sw||.5;oc2.stroke();}}
}}

function draw(){{
  const dpr=window.devicePixelRatio||1;
  if(oc.width!==cv.width||oc.height!==cv.height){{
    oc.width=cv.width;oc.height=cv.height;
    oc2.setTransform(dpr,0,0,dpr,0,0);
  }}
  oc2.fillStyle='#04080f';oc2.fillRect(0,0,W,H);
  oc2.save();
  oc2.beginPath();oc2.arc(cx,cy,R,0,Math.PI*2);oc2.clip();
  const og=oc2.createRadialGradient(cx-R*.15,cy-R*.15,R*.02,cx,cy,R*1.01);
  og.addColorStop(0,'#162540');og.addColorStop(.35,'#0d1e35');
  og.addColorStop(.65,'#081525');og.addColorStop(1,'#040c18');
  oc2.fillStyle=og;oc2.fillRect(cx-R,cy-R,R*2,R*2);

  // Grid
  oc2.strokeStyle='rgba(0,200,255,0.06)';oc2.lineWidth=.4;
  for(let la=-60;la<=60;la+=30){{
    oc2.beginPath();let st=false;
    for(let lo=-180;lo<=180;lo+=2){{
      const p=proj(la,lo,rotLon);
      if(p.vis){{if(!st){{oc2.moveTo(p.px,p.py);st=true;}}else oc2.lineTo(p.px,p.py);}}else st=false;
    }}oc2.stroke();
  }}
  for(let lo=0;lo<360;lo+=30){{
    oc2.beginPath();let st=false;
    for(let la=-88;la<=88;la+=3){{
      const p=proj(la,lo,rotLon);
      if(p.vis){{if(!st){{oc2.moveTo(p.px,p.py);st=true;}}else oc2.lineTo(p.px,p.py);}}else st=false;
    }}oc2.stroke();
  }}
  // Equator
  oc2.strokeStyle='rgba(0,200,255,0.14)';oc2.lineWidth=.7;
  oc2.beginPath();let eq=false;
  for(let lo=-180;lo<=180;lo+=1.5){{
    const p=proj(0,lo,rotLon);
    if(p.vis){{if(!eq){{oc2.moveTo(p.px,p.py);eq=true;}}else oc2.lineTo(p.px,p.py);}}else eq=false;
  }}oc2.stroke();

  for(const p of LAND)drawPoly(p,'#0e2040','rgba(0,100,180,.55)',.6);
  for(const p of ICE)drawPoly(p,'rgba(180,220,245,.5)','rgba(140,200,235,.3)',.4);

  // Depth shading
  const shad=oc2.createRadialGradient(cx+R*.2,cy+R*.1,R*.25,cx,cy,R);
  shad.addColorStop(0,'rgba(0,0,0,0)');shad.addColorStop(.5,'rgba(0,0,0,0)');
  shad.addColorStop(1,'rgba(0,0,15,.78)');
  oc2.fillStyle=shad;oc2.fillRect(cx-R,cy-R,R*2,R*2);
  // Highlight
  const hl=oc2.createRadialGradient(cx-R*.25,cy-R*.25,0,cx-R*.08,cy-R*.08,R*.5);
  hl.addColorStop(0,'rgba(140,200,255,.07)');hl.addColorStop(1,'rgba(0,0,0,0)');
  oc2.fillStyle=hl;oc2.fillRect(cx-R,cy-R,R*2,R*2);

  // Markers
  const vis=MK.map(m=>{{const pt=proj(m.la,m.lo,rotLon);return{{m,p:pt}};}})
    .filter(x=>x.p.vis&&x.p.z>.05).sort((a,b)=>a.p.z-b.p.z);
  for(const{{m,p}}of vis){{
    const[r,g,b]=tc(m.t);
    const col=`rgb(${{r}},${{g}},${{b}})`;
    const sz=5+Math.min(Math.abs(m.t),35)*.07;
    const al=.55+p.z*.45;
    // Glow
    oc2.globalAlpha=.14*al;oc2.fillStyle=col;
    oc2.beginPath();oc2.arc(p.px,p.py,sz*3,0,Math.PI*2);oc2.fill();
    oc2.globalAlpha=.28*al;
    oc2.beginPath();oc2.arc(p.px,p.py,sz*1.8,0,Math.PI*2);oc2.fill();
    oc2.globalAlpha=.92*al;oc2.fillStyle=col;
    oc2.beginPath();oc2.arc(p.px,p.py,sz,0,Math.PI*2);oc2.fill();
    // Specula
    oc2.globalAlpha=.45*al;oc2.fillStyle='rgba(255,255,255,.9)';
    oc2.beginPath();oc2.arc(p.px-sz*.28,p.py-sz*.28,sz*.28,0,Math.PI*2);oc2.fill();
    // Outline
    oc2.globalAlpha=.18*al;oc2.strokeStyle='rgba(0,0,0,.8)';oc2.lineWidth=.8;
    oc2.beginPath();oc2.arc(p.px,p.py,sz,0,Math.PI*2);oc2.stroke();
  }}
  oc2.globalAlpha=1;oc2.restore();

  // Atmosphere
  const atm=oc2.createRadialGradient(cx,cy,R*.88,cx,cy,R*1.1);
  atm.addColorStop(0,'rgba(0,60,180,0)');atm.addColorStop(.4,'rgba(0,80,200,.16)');
  atm.addColorStop(.8,'rgba(0,60,160,.06)');atm.addColorStop(1,'rgba(0,40,140,0)');
  oc2.beginPath();oc2.arc(cx,cy,R*1.1,0,Math.PI*2);oc2.fillStyle=atm;oc2.fill();
  oc2.beginPath();oc2.arc(cx,cy,R+1,0,Math.PI*2);
  oc2.strokeStyle='rgba(0,120,220,.22)';oc2.lineWidth=1.5;oc2.stroke();

  // Colour bar
  const cbW=10,cbH=Math.min(110,R*.75);
  const cbX=cx+R+16,cbY=cy-cbH/2;
  if(cbX+40<W){{
    const cg=oc2.createLinearGradient(0,cbY,0,cbY+cbH);
    cg.addColorStop(0,'#d73027');cg.addColorStop(.2,'#fc8d59');
    cg.addColorStop(.4,'#fee090');cg.addColorStop(.55,'#e0f3f8');
    cg.addColorStop(.75,'#74add1');cg.addColorStop(1,'#313695');
    oc2.fillStyle=cg;oc2.beginPath();oc2.roundRect(cbX,cbY,cbW,cbH,3);oc2.fill();
    oc2.strokeStyle='rgba(255,255,255,.1)';oc2.lineWidth=.4;
    oc2.beginPath();oc2.roundRect(cbX,cbY,cbW,cbH,3);oc2.stroke();
    oc2.font='8px monospace';oc2.fillStyle='rgba(160,210,240,.65)';oc2.textAlign='left';
    oc2.fillText('°C',cbX,cbY-5);
    for(const[lbl,f]of[['35°',0],['15°',.38],['-5°',.76]]){{
      const ty=cbY+f*cbH+3;
      oc2.strokeStyle='rgba(160,210,240,.25)';oc2.lineWidth=.4;
      oc2.beginPath();oc2.moveTo(cbX-3,ty);oc2.lineTo(cbX+cbW+3,ty);oc2.stroke();
      oc2.fillStyle='rgba(160,210,240,.65)';oc2.fillText(lbl,cbX+cbW+4,ty+3);
    }}
  }}

  // Badge
  const AVG={avg_t:.1f};
  const badge=`⚡ LIVE · WeatherAPI.com  ·  Avg ${{AVG.toFixed(1)}}°C  ·  ${{DATE}}`;
  oc2.font='9.5px monospace';
  const bw=oc2.measureText(badge).width;
  const bx=cx-bw/2-10,by=cy+R+12,bww=bw+20,bh=17;
  if(by+bh<H-4){{
    oc2.fillStyle='rgba(4,8,15,.85)';
    oc2.beginPath();oc2.roundRect(bx,by,bww,bh,3);oc2.fill();
    oc2.strokeStyle='rgba(0,120,220,.2)';oc2.lineWidth=.4;
    oc2.beginPath();oc2.roundRect(bx,by,bww,bh,3);oc2.stroke();
    oc2.fillStyle='#00ff9d';oc2.beginPath();oc2.arc(bx+10,by+8.5,3,0,Math.PI*2);oc2.fill();
    oc2.fillStyle='rgba(160,210,240,.75)';oc2.textAlign='left';
    oc2.fillText(badge,bx+18,by+12);
  }}

  ctx.clearRect(0,0,W,H);ctx.drawImage(oc,0,0);
}}

const SPEED=0.08;
function loop(){{
  requestAnimationFrame(loop);
  if(!drag){{rotLon=(rotLon+SPEED)%360;velX*=.88;rotLon=(rotLon-velX*.15+360)%360;}}
  draw();
}}
loop();
</script></body></html>"""

    components.html(globe_html, height=480, scrolling=False)

# ── RIGHT PANEL ──
with rhs:
    st.markdown('<div class="panel-r">', unsafe_allow_html=True)
    st.markdown(f'<div class="sect-title">📡 Live Stats · {today_str}</div>', unsafe_allow_html=True)

    def stat_card(label, val, unit, sub, color="var(--accent)"):
        return f"""
        <div class="stat-card">
          <div class="sc-label">{label} <span style="color:{color}">●</span></div>
          <div class="sc-val" style="color:{color}">{val}<span class="sc-unit"> {unit}</span></div>
          <div class="sc-sub">{sub}</div>
          <div class="sc-live"><span class="sc-live-dot"></span>LIVE · {now_str}</div>
        </div>"""

    st.markdown(
        stat_card("🌡 GLOBAL MEAN TEMP", f"{g_temp}", "°C", "Live avg across 39 countries") +
        stat_card("💨 WIND SPEED AVG", f"{g_wind}", "km/h", "Global mean wind speed", "var(--purple)") +
        stat_card("💧 HUMIDITY AVG", f"{g_hum}", "%", "Average relative humidity", "var(--accent3)") +
        stat_card("🌧 PRECIPITATION", f"{g_prec}", "mm", "Global average rainfall", "#00aaff"),
        unsafe_allow_html=True
    )

    # Extremes
    h_t  = CURRENT[hottest]["temp"]
    c_t  = CURRENT[coldest]["temp"]
    w_w  = CURRENT[windiest]["wind"]
    h_fl = COUNTRY_DATA[hottest]["flag"]
    c_fl = COUNTRY_DATA[coldest]["flag"]
    w_fl = COUNTRY_DATA[windiest]["flag"]

    st.markdown(f"""
    <div class="sect-title">🔥❄️ Today's Extremes</div>
    <div class="ext-card">
      <div class="ext-row">
        <span>{h_fl} <span class="ext-name" style="color:#ff4d6d">{hottest}</span></span>
        <span class="ext-temp" style="color:#ff4d6d">{h_t:.1f}°C</span>
      </div>
      <div class="ext-row" style="border-top:1px solid var(--border)">
        <span>{c_fl} <span class="ext-name" style="color:#00c8ff">{coldest}</span></span>
        <span class="ext-temp" style="color:#00c8ff">{c_t:.1f}°C</span>
      </div>
      <div class="ext-row" style="border-top:1px solid var(--border)">
        <span>{w_fl} <span class="ext-name" style="color:var(--purple)">{windiest}</span></span>
        <span class="ext-temp" style="color:var(--purple)">{w_w:.0f} km/h</span>
      </div>
    </div>""", unsafe_allow_html=True)

    # Hottest 8 ranking
    st.markdown('<div class="sect-title">📊 Hottest Countries</div>', unsafe_allow_html=True)
    st.markdown('<div class="rank-strip">', unsafe_allow_html=True)
    span = (max_t - min_t) or 1
    for i, c in enumerate(top8):
        t = CURRENT[c]["temp"]
        pct = int((t - min_t) / span * 100)
        col = "#ff4d6d" if t > 28 else "#ffb700" if t > 20 else "#00c8ff"
        fl  = COUNTRY_DATA[c]["flag"]
        st.markdown(f"""
        <div class="rank-item">
          <span class="rank-num">{i+1}</span>
          <span style="font-size:.7rem">{fl}</span>
          <span style="flex:0 0 70px;font-size:.68rem;overflow:hidden;
                       text-overflow:ellipsis;white-space:nowrap">{c.split()[0]}</span>
          <div class="rank-bar-wrap">
            <div class="rank-bar" style="width:{pct}%;background:{col}"></div>
          </div>
          <span class="rank-val" style="color:{col}">{t:.1f}°</span>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # panel-r

st.markdown('</div>', unsafe_allow_html=True)  # outer