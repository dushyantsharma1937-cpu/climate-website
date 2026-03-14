import streamlit as st
import plotly.graph_objects as go
import numpy as np
import datetime, requests, os, sys, json, gzip, base64

WEATHER_API_KEY = "ec0aaf3d97ea407cbd7130905261403"
WEATHER_API_URL = "http://api.weatherapi.com/v1/current.json"

NCEP_PATH = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ncep_data.json.gz")
)

st.set_page_config(
    page_title="DUNIYA · Country Analysis",
    page_icon="📊",
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
  background:var(--bg)!important;color:var(--text)!important;font-family:'Syne',sans-serif}
[data-testid="stHeader"],[data-testid="stSidebar"],[data-testid="stToolbar"],
#MainMenu,footer{display:none!important}
[data-testid="stMainBlockContainer"]{padding:.9rem 1.3rem!important;max-width:100%!important}

.top-bar{display:flex;align-items:flex-start;justify-content:space-between;
  padding:.5rem 0 1rem;border-bottom:1px solid var(--border);margin-bottom:.9rem;
  flex-wrap:wrap;gap:.6rem;position:relative}
.top-bar::after{content:'';position:absolute;bottom:-1px;left:0;width:80px;
  height:2px;background:linear-gradient(90deg,var(--accent),transparent)}
.tb-country{font-size:1.8rem;font-weight:800;letter-spacing:-.02em}
.tb-sub{font-size:.6rem;letter-spacing:.1em;text-transform:uppercase;
  color:var(--muted);font-family:'JetBrains Mono',monospace;margin-top:.15rem}
.tb-tag{font-size:.58rem;font-family:'JetBrains Mono',monospace;
  padding:.14rem .55rem;border-radius:3px;border:1px solid;
  color:var(--accent);border-color:rgba(0,200,255,.35);background:rgba(0,200,255,.06)}
.tb-tag.nc{color:var(--warn);border-color:rgba(255,183,0,.35);background:rgba(255,183,0,.06)}
.live-badge{display:inline-flex;align-items:center;gap:5px;font-size:.58rem;
  font-family:'JetBrains Mono',monospace;color:var(--accent3);letter-spacing:.08em;
  background:rgba(0,255,157,.06);border:1px solid rgba(0,255,157,.2);
  border-radius:3px;padding:2px 8px}
.lb-dot{width:4px;height:4px;border-radius:50%;background:var(--accent3);animation:p 1.5s infinite}
@keyframes p{0%,100%{opacity:1}50%{opacity:.15}}
.tb-stats{display:flex;gap:1.3rem;flex-wrap:wrap;align-items:center}
.ts{text-align:right}
.ts-l{font-size:.56rem;letter-spacing:.1em;text-transform:uppercase;
  color:var(--muted);font-family:'JetBrains Mono',monospace}
.ts-v{font-size:1.05rem;font-weight:800;font-family:'JetBrains Mono',monospace}

.mode-wrap{display:flex;align-items:center;gap:.8rem;margin-bottom:.8rem}
.mode-label{font-size:.58rem;font-family:'JetBrains Mono',monospace;
  color:var(--muted);letter-spacing:.1em;text-transform:uppercase}
.mode-strip{display:flex;background:var(--card);border:1px solid var(--border);
  border-radius:8px;overflow:hidden}
.m-btn{font-size:.68rem;font-family:'JetBrains Mono',monospace;letter-spacing:.06em;
  padding:.38rem 1.05rem;cursor:pointer;color:var(--muted);border:none;
  background:transparent;transition:all .18s;white-space:nowrap;text-decoration:none;display:block}
.m-btn.on{background:rgba(0,200,255,.12);color:var(--accent);
  box-shadow:inset 0 -2px 0 var(--accent)}
.m-div{width:1px;background:var(--border)}

.pill-row{display:flex;gap:.6rem;margin-bottom:.75rem;flex-wrap:wrap}
.pill{flex:1;min-width:110px;background:var(--card);border:1px solid var(--border);
  border-radius:8px;padding:.6rem .85rem;position:relative;overflow:hidden}
.pill::after{content:'';position:absolute;top:0;left:0;right:0;height:2px}
.pill.live::after{background:linear-gradient(90deg,var(--accent3),transparent)}
.pill.nc::after{background:linear-gradient(90deg,var(--warn),transparent)}
.pill.wind::after{background:linear-gradient(90deg,var(--purple),transparent)}
.pill.hot::after{background:linear-gradient(90deg,var(--accent2),transparent)}
.pill.cold::after{background:linear-gradient(90deg,#60a5fa,transparent)}
.pl{font-size:.56rem;letter-spacing:.1em;text-transform:uppercase;
  color:var(--muted);font-family:'JetBrains Mono',monospace}
.pv{font-size:1.18rem;font-weight:800;font-family:'JetBrains Mono',monospace;
  color:var(--text);line-height:1.2}
.ps{font-size:.56rem;display:block;margin-top:2px;font-family:'JetBrains Mono',monospace}
.ps.live{color:var(--accent3)}.ps.nc{color:var(--warn)}.ps.wind{color:var(--purple)}

.alert{background:rgba(0,200,255,.04);border:1px solid rgba(0,200,255,.15);
  border-radius:7px;padding:.6rem .85rem;display:flex;gap:.5rem;
  align-items:flex-start;margin-top:.5rem;font-size:.75rem;color:var(--muted);line-height:1.6}
.alert.wind{background:rgba(157,125,255,.04);border-color:rgba(157,125,255,.15)}
.alert.nc{background:rgba(255,183,0,.04);border-color:rgba(255,183,0,.15)}
.ai{font-size:.8rem;flex-shrink:0;margin-top:.05rem}
.ab{color:var(--accent);font-weight:700}
.ab.wind{color:var(--purple)}.ab.nc{color:var(--warn)}

.sh{display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:.7rem}
.sh-t{font-size:1rem;font-weight:700}
.sh-t span{margin-right:.3rem}
.sh-s{font-size:.58rem;letter-spacing:.1em;text-transform:uppercase;
  color:var(--muted);font-family:'JetBrains Mono',monospace;margin-top:.1rem}

.nc-box{background:var(--card);border:1px solid rgba(255,183,0,.2);
  border-radius:8px;padding:.8rem .9rem;margin-top:.6rem;position:relative;overflow:hidden}
.nc-box::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,var(--warn),transparent)}
.nc-head{font-size:.6rem;letter-spacing:.12em;text-transform:uppercase;
  color:var(--warn);font-family:'JetBrains Mono',monospace;margin-bottom:.55rem}
.nc-row{display:flex;align-items:center;gap:.5rem;padding:.18rem 0;
  border-bottom:1px solid rgba(255,255,255,.02)}
.nc-t{width:28px;font-size:.6rem;font-family:'JetBrains Mono',monospace;color:var(--muted)}
.nc-bar{flex:1;height:4px;background:rgba(255,255,255,.04);border-radius:2px}
.nc-v{width:52px;text-align:right;font-size:.65rem;font-family:'JetBrains Mono',monospace;font-weight:700}

.mini-grid{display:grid;grid-template-columns:1fr 1fr;gap:.45rem;margin-top:.6rem}
.mini-card{background:var(--card);border:1px solid var(--border);border-radius:7px;
  padding:.55rem .7rem;position:relative;overflow:hidden}
.mini-card::before{content:'';position:absolute;top:0;left:0;bottom:0;width:2px}
.mini-card.uv::before{background:var(--warn)}
.mini-card.cloud::before{background:var(--muted)}
.mini-card.vis::before{background:var(--accent)}
.mini-card.pres::before{background:var(--accent2)}
.mc-l{font-size:.54rem;letter-spacing:.1em;text-transform:uppercase;
  color:var(--muted);font-family:'JetBrains Mono',monospace}
.mc-v{font-size:1.05rem;font-weight:800;font-family:'JetBrains Mono',monospace;margin-top:.1rem}
.mc-s{font-size:.56rem;color:var(--muted);font-family:'JetBrains Mono',monospace}

.leg-bar{height:6px;border-radius:3px;margin:.3rem 0 .15rem}
.leg-bar.temp{background:linear-gradient(90deg,#ff4d6d,#ff8c00,#ffcc00,#44aaff,#00c8ff)}
.leg-bar.wind{background:linear-gradient(90deg,#6d28d9,#9d7dff,#c4b5fd,#ede9fe)}
.leg-lbl{display:flex;justify-content:space-between;font-size:.56rem;
  font-family:'JetBrains Mono',monospace;color:var(--muted)}

[data-testid="stPlotlyChart"]{background:transparent!important;border:none!important}
[data-testid="stButton"] button{background:transparent!important;
  border:1px solid var(--border)!important;color:var(--muted)!important;
  border-radius:6px!important;font-family:'Syne',sans-serif!important;
  font-size:.8rem!important;font-weight:700!important;padding:.3rem .9rem!important;
  transition:all .2s!important}
[data-testid="stButton"] button:hover{border-color:var(--accent)!important;color:var(--accent)!important}
[data-testid="column"]{padding:0!important}
::-webkit-scrollbar{width:3px}
::-webkit-scrollbar-track{background:var(--bg)}
::-webkit-scrollbar-thumb{background:var(--dim);border-radius:2px}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  COUNTRY META  (flags + regions only — no lat/lon needed for NCEP)
# ─────────────────────────────────────────────
COUNTRY_META = {
    "Afghanistan":   {"flag":"🇦🇫","region":"Asia"},
    "Argentina":     {"flag":"🇦🇷","region":"S.America"},
    "Australia":     {"flag":"🇦🇺","region":"Oceania"},
    "Brazil":        {"flag":"🇧🇷","region":"S.America"},
    "Canada":        {"flag":"🇨🇦","region":"N.America"},
    "China":         {"flag":"🇨🇳","region":"Asia"},
    "Denmark":       {"flag":"🇩🇰","region":"Europe"},
    "Egypt":         {"flag":"🇪🇬","region":"Africa"},
    "Ethiopia":      {"flag":"🇪🇹","region":"Africa"},
    "France":        {"flag":"🇫🇷","region":"Europe"},
    "Germany":       {"flag":"🇩🇪","region":"Europe"},
    "Greenland":     {"flag":"🇬🇱","region":"Arctic"},
    "India":         {"flag":"🇮🇳","region":"Asia"},
    "Indonesia":     {"flag":"🇮🇩","region":"Asia"},
    "Iran":          {"flag":"🇮🇷","region":"Asia"},
    "Japan":         {"flag":"🇯🇵","region":"Asia"},
    "Kenya":         {"flag":"🇰🇪","region":"Africa"},
    "Mexico":        {"flag":"🇲🇽","region":"N.America"},
    "Morocco":       {"flag":"🇲🇦","region":"Africa"},
    "Netherlands":   {"flag":"🇳🇱","region":"Europe"},
    "New Zealand":   {"flag":"🇳🇿","region":"Oceania"},
    "Nigeria":       {"flag":"🇳🇬","region":"Africa"},
    "Norway":        {"flag":"🇳🇴","region":"Europe"},
    "Pakistan":      {"flag":"🇵🇰","region":"Asia"},
    "Peru":          {"flag":"🇵🇪","region":"S.America"},
    "Poland":        {"flag":"🇵🇱","region":"Europe"},
    "Russia":        {"flag":"🇷🇺","region":"Europe"},
    "Saudi Arabia":  {"flag":"🇸🇦","region":"Asia"},
    "South Africa":  {"flag":"🇿🇦","region":"Africa"},
    "South Korea":   {"flag":"🇰🇷","region":"Asia"},
    "Spain":         {"flag":"🇪🇸","region":"Europe"},
    "Sweden":        {"flag":"🇸🇪","region":"Europe"},
    "Switzerland":   {"flag":"🇨🇭","region":"Europe"},
    "Turkey":        {"flag":"🇹🇷","region":"Asia"},
    "Ukraine":       {"flag":"🇺🇦","region":"Europe"},
    "United Kingdom":{"flag":"🇬🇧","region":"Europe"},
    "United States": {"flag":"🇺🇸","region":"N.America"},
    "Venezuela":     {"flag":"🇻🇪","region":"S.America"},
    "Vietnam":       {"flag":"🇻🇳","region":"Asia"},
}

# WeatherAPI city queries (for live current conditions only)
CITY_QUERY = {
    "Afghanistan":"Kabul","Argentina":"Buenos Aires","Australia":"Sydney",
    "Brazil":"Brasilia","Canada":"Ottawa","China":"Beijing","Denmark":"Copenhagen",
    "Egypt":"Cairo","Ethiopia":"Addis Ababa","France":"Paris","Germany":"Berlin",
    "Greenland":"Nuuk","India":"New Delhi","Indonesia":"Jakarta","Iran":"Tehran",
    "Japan":"Tokyo","Kenya":"Nairobi","Mexico":"Mexico City","Morocco":"Rabat",
    "Netherlands":"Amsterdam","New Zealand":"Wellington","Nigeria":"Abuja",
    "Norway":"Oslo","Pakistan":"Islamabad","Peru":"Lima","Poland":"Warsaw",
    "Russia":"Moscow","Saudi Arabia":"Riyadh","South Africa":"Cape Town",
    "South Korea":"Seoul","Spain":"Madrid","Sweden":"Stockholm","Switzerland":"Bern",
    "Turkey":"Ankara","Ukraine":"Kyiv","United Kingdom":"London",
    "United States":"Washington","Venezuela":"Caracas","Vietnam":"Hanoi",
}

# Bounding boxes for NCEP grid lookup (lat_min, lat_max, lon_min, lon_max)
COUNTRY_BOUNDS = {
    "Afghanistan":   ( 29,  38,  60,  75),
    "Argentina":     (-55, -21, -74, -53),
    "Australia":     (-44, -10, 113, 154),
    "Brazil":        (-33,   5, -73, -34),
    "Canada":        ( 42,  83,-141, -52),
    "China":         ( 18,  53,  74, 135),
    "Denmark":       ( 54,  58,   8,  15),
    "Egypt":         ( 22,  31,  25,  37),
    "Ethiopia":      (  3,  15,  33,  48),
    "France":        ( 42,  51,  -5,   8),
    "Germany":       ( 47,  55,   6,  15),
    "Greenland":     ( 60,  84, -57, -17),
    "India":         (  8,  37,  68,  97),
    "Indonesia":     (-11,   6,  95, 141),
    "Iran":          ( 25,  40,  44,  63),
    "Japan":         ( 30,  45, 130, 146),
    "Kenya":         ( -5,   5,  34,  42),
    "Mexico":        ( 14,  33,-118, -86),
    "Morocco":       ( 27,  36, -13,  -1),
    "Netherlands":   ( 50,  54,   3,   7),
    "New Zealand":   (-47, -34, 166, 178),
    "Nigeria":       (  4,  14,   3,  15),
    "Norway":        ( 57,  71,   4,  32),
    "Pakistan":      ( 23,  37,  60,  77),
    "Peru":          (-18,  -1, -81, -68),
    "Poland":        ( 49,  55,  14,  24),
    "Russia":        ( 50,  77,  30, 180),
    "Saudi Arabia":  ( 16,  33,  36,  56),
    "South Africa":  (-35, -22,  16,  33),
    "South Korea":   ( 33,  38, 125, 130),
    "Spain":         ( 35,  44,  -9,   5),
    "Sweden":        ( 55,  69,  11,  24),
    "Switzerland":   ( 45,  48,   6,  11),
    "Turkey":        ( 36,  43,  26,  45),
    "Ukraine":       ( 44,  53,  22,  40),
    "United Kingdom":( 49,  61,  -8,   2),
    "United States": ( 24,  49,-125, -66),
    "Venezuela":     (  0,  12, -73, -59),
    "Vietnam":       (  8,  23, 102, 110),
}

MONTH_LABELS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

# Sub-national state data (kept for map view)
STATE_DATA = {
    "India":{"Andhra Pradesh":{"temp":29.5,"wind":14.2,"lat":15.9,"lon":79.7},"Arunachal Pr.":{"temp":15.2,"wind":9.8,"lat":28.2,"lon":94.7},"Assam":{"temp":24.1,"wind":11.3,"lat":26.2,"lon":92.9},"Bihar":{"temp":27.3,"wind":12.1,"lat":25.1,"lon":85.3},"Chhattisgarh":{"temp":27.8,"wind":10.5,"lat":21.3,"lon":81.9},"Goa":{"temp":27.9,"wind":17.6,"lat":15.3,"lon":74.1},"Gujarat":{"temp":28.4,"wind":18.3,"lat":22.3,"lon":72.6},"Haryana":{"temp":24.7,"wind":14.9,"lat":29.1,"lon":76.1},"Himachal Pr.":{"temp":13.5,"wind":10.2,"lat":31.1,"lon":77.2},"Jharkhand":{"temp":26.9,"wind":11.8,"lat":23.6,"lon":85.3},"Karnataka":{"temp":24.8,"wind":13.4,"lat":15.3,"lon":75.7},"Kerala":{"temp":27.2,"wind":15.8,"lat":9.0,"lon":76.6},"Madhya Pr.":{"temp":26.5,"wind":11.6,"lat":22.9,"lon":78.7},"Maharashtra":{"temp":27.1,"wind":14.7,"lat":19.7,"lon":75.7},"Manipur":{"temp":20.3,"wind":9.1,"lat":24.7,"lon":93.9},"Meghalaya":{"temp":18.6,"wind":10.3,"lat":25.5,"lon":91.4},"Mizoram":{"temp":21.5,"wind":9.7,"lat":23.2,"lon":92.9},"Nagaland":{"temp":19.8,"wind":8.9,"lat":26.2,"lon":94.6},"Odisha":{"temp":28.7,"wind":13.9,"lat":20.9,"lon":85.1},"Punjab":{"temp":22.9,"wind":15.3,"lat":31.1,"lon":75.3},"Rajasthan":{"temp":29.8,"wind":16.5,"lat":27.0,"lon":74.2},"Sikkim":{"temp":12.1,"wind":8.5,"lat":27.5,"lon":88.5},"Tamil Nadu":{"temp":29.0,"wind":16.2,"lat":11.1,"lon":78.7},"Telangana":{"temp":30.1,"wind":13.6,"lat":18.0,"lon":79.6},"Tripura":{"temp":24.5,"wind":10.4,"lat":23.9,"lon":91.9},"Uttar Pr.":{"temp":26.1,"wind":12.8,"lat":26.8,"lon":80.9},"Uttarakhand":{"temp":17.4,"wind":11.1,"lat":30.1,"lon":79.3},"West Bengal":{"temp":26.7,"wind":13.2,"lat":22.5,"lon":88.3},"Delhi":{"temp":25.8,"wind":15.0,"lat":28.7,"lon":77.1},"J&K":{"temp":8.5,"wind":10.6,"lat":33.7,"lon":75.3},"Ladakh":{"temp":1.2,"wind":8.9,"lat":34.2,"lon":77.6}},
    "United States":{"Alabama":{"temp":17.8,"wind":13.5,"lat":32.8,"lon":-86.8},"Alaska":{"temp":-3.2,"wind":14.2,"lat":64.2,"lon":-153.4},"Arizona":{"temp":20.5,"wind":15.6,"lat":34.0,"lon":-111.1},"California":{"temp":16.8,"wind":16.3,"lat":36.8,"lon":-119.4},"Colorado":{"temp":8.1,"wind":17.2,"lat":39.0,"lon":-105.5},"Florida":{"temp":22.8,"wind":17.3,"lat":27.7,"lon":-81.5},"Georgia":{"temp":17.9,"wind":13.4,"lat":32.2,"lon":-83.4},"Illinois":{"temp":10.7,"wind":16.8,"lat":40.0,"lon":-89.2},"Kansas":{"temp":12.5,"wind":20.1,"lat":38.5,"lon":-98.4},"Louisiana":{"temp":20.1,"wind":14.7,"lat":31.2,"lon":-91.8},"Michigan":{"temp":7.9,"wind":16.8,"lat":44.3,"lon":-85.4},"Minnesota":{"temp":4.8,"wind":17.5,"lat":46.4,"lon":-93.1},"Montana":{"temp":4.9,"wind":17.8,"lat":46.9,"lon":-110.4},"New York":{"temp":9.0,"wind":15.3,"lat":42.9,"lon":-75.5},"N Dakota":{"temp":2.9,"wind":21.2,"lat":47.5,"lon":-100.4},"Ohio":{"temp":10.9,"wind":15.7,"lat":40.4,"lon":-82.7},"Oklahoma":{"temp":15.6,"wind":19.3,"lat":35.6,"lon":-97.5},"Oregon":{"temp":9.2,"wind":14.8,"lat":43.9,"lon":-120.6},"Tennessee":{"temp":14.8,"wind":13.5,"lat":35.9,"lon":-86.7},"Texas":{"temp":19.3,"wind":17.8,"lat":31.1,"lon":-97.6},"Washington":{"temp":8.6,"wind":14.3,"lat":47.4,"lon":-120.5},"Wyoming":{"temp":4.2,"wind":19.7,"lat":43.0,"lon":-107.6}},
    "Australia":{"New S Wales":{"temp":18.5,"wind":17.2,"lat":-31.3,"lon":146.0},"Victoria":{"temp":14.9,"wind":18.5,"lat":-36.9,"lon":144.4},"Queensland":{"temp":23.8,"wind":15.6,"lat":-22.6,"lon":144.1},"S Australia":{"temp":18.2,"wind":19.3,"lat":-30.0,"lon":135.8},"W Australia":{"temp":20.5,"wind":17.8,"lat":-25.7,"lon":121.6},"Tasmania":{"temp":10.2,"wind":20.1,"lat":-41.9,"lon":146.3},"N Territory":{"temp":27.3,"wind":15.2,"lat":-19.5,"lon":133.4},"ACT":{"temp":12.8,"wind":16.4,"lat":-35.5,"lon":149.0}},
    "Brazil":{"Amazonas":{"temp":27.1,"wind":9.5,"lat":-3.4,"lon":-65.3},"Para":{"temp":26.8,"wind":10.2,"lat":-3.8,"lon":-52.5},"Mato Grosso":{"temp":26.3,"wind":11.4,"lat":-12.6,"lon":-55.9},"Minas Gerais":{"temp":21.5,"wind":12.3,"lat":-18.5,"lon":-44.6},"Bahia":{"temp":24.7,"wind":13.1,"lat":-13.3,"lon":-41.7},"Sao Paulo":{"temp":20.8,"wind":13.5,"lat":-22.3,"lon":-48.8},"Rio de Janeiro":{"temp":23.6,"wind":14.2,"lat":-22.4,"lon":-43.2},"Goias":{"temp":24.9,"wind":12.0,"lat":-15.8,"lon":-49.5},"Maranhao":{"temp":27.3,"wind":11.6,"lat":-5.3,"lon":-44.4},"Rio G Sul":{"temp":17.2,"wind":15.3,"lat":-29.7,"lon":-53.4}},
    "Russia":{"Moscow":{"temp":4.5,"wind":14.2,"lat":55.5,"lon":37.5},"St Peters":{"temp":4.1,"wind":15.1,"lat":59.9,"lon":30.3},"W Siberia":{"temp":-5.3,"wind":13.8,"lat":57.0,"lon":70.0},"E Siberia":{"temp":-12.1,"wind":12.5,"lat":62.0,"lon":110.0},"Yakutia":{"temp":-16.4,"wind":10.2,"lat":63.0,"lon":129.0},"Ural":{"temp":1.8,"wind":14.6,"lat":57.0,"lon":59.0},"Volga":{"temp":6.2,"wind":15.3,"lat":51.0,"lon":46.0},"Krasnodar":{"temp":12.5,"wind":16.4,"lat":45.0,"lon":39.0},"Far East":{"temp":-2.8,"wind":13.7,"lat":51.0,"lon":135.0},"Murmansk":{"temp":-1.2,"wind":16.2,"lat":68.0,"lon":33.0}},
    "Canada":{"BC":{"temp":8.5,"wind":14.3,"lat":53.7,"lon":-127.6},"Alberta":{"temp":2.3,"wind":17.5,"lat":53.9,"lon":-116.6},"Saskatchewan":{"temp":0.5,"wind":19.8,"lat":52.9,"lon":-106.5},"Manitoba":{"temp":-0.8,"wind":18.3,"lat":53.8,"lon":-98.8},"Ontario":{"temp":5.6,"wind":15.6,"lat":49.3,"lon":-84.7},"Quebec":{"temp":2.1,"wind":15.2,"lat":53.0,"lon":-73.5},"Nova Scotia":{"temp":6.8,"wind":17.1,"lat":45.1,"lon":-62.9},"Nunavut":{"temp":-14.3,"wind":16.4,"lat":70.3,"lon":-86.5},"Yukon":{"temp":-3.9,"wind":13.5,"lat":63.0,"lon":-136.0},"NWT":{"temp":-8.5,"wind":14.6,"lat":64.8,"lon":-124.8}},
    "China":{"Xinjiang":{"temp":7.2,"wind":15.6,"lat":41.2,"lon":85.3},"Tibet":{"temp":0.5,"wind":13.2,"lat":31.5,"lon":88.4},"Inner Mong":{"temp":2.8,"wind":19.2,"lat":44.1,"lon":113.9},"Heilongjng":{"temp":1.5,"wind":15.8,"lat":47.9,"lon":128.1},"Sichuan":{"temp":14.6,"wind":11.3,"lat":30.1,"lon":103.0},"Yunnan":{"temp":15.7,"wind":12.4,"lat":25.1,"lon":101.5},"Guangdong":{"temp":22.3,"wind":16.5,"lat":23.4,"lon":113.3},"Beijing":{"temp":12.5,"wind":15.2,"lat":39.9,"lon":116.4},"Shanghai":{"temp":16.8,"wind":16.8,"lat":31.2,"lon":121.5},"Hainan":{"temp":24.6,"wind":18.3,"lat":19.2,"lon":109.7}},
}

# ─────────────────────────────────────────────
#  NCEP LOADER — reads grid, extracts all 39 countries implicitly
# ─────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_all_ncep(path: str) -> dict | None:
    """
    Load ncep_data.json.gz and extract seasonal temperature series
    for all 39 countries using bounding-box area averaging.
    No explicit lat/lon passed — grid coordinates drive everything.
    Returns dict: country -> {mean, min, max, range, cells, series, peak_m, cold_m, lats, lons}
    """
    try:
        # Support both plain JSON and gzip
        try:
            with gzip.open(path, "rb") as f:
                ncep = json.loads(f.read())
        except (OSError, gzip.BadGzipFile):
            with open(path, "r") as f:
                ncep = json.load(f)

        lats_g = np.array(ncep["lats"])
        lons_g = np.array(ncep["lons"])
        tmin   = ncep["tmin"]; tmax = ncep["tmax"]
        nlat   = ncep["nlat"]; nlon = ncep["nlon"]; nt = ncep["nt"]

        raw  = base64.b64decode(ncep["data_b64"])
        arr  = np.frombuffer(raw, dtype=np.uint8).reshape(nt, nlat, nlon).astype(np.float32)
        arr  = tmin + arr / 255.0 * (tmax - tmin)

        results = {}
        for country, (lat1, lat2, lon1, lon2) in COUNTRY_BOUNDS.items():
            # NCEP lons are 0–360 — normalise input
            nlon1 = lon1 % 360
            nlon2 = lon2 % 360

            li = np.where((lats_g >= lat1) & (lats_g <= lat2))[0]
            if nlon1 <= nlon2:
                lj = np.where((lons_g >= nlon1) & (lons_g <= nlon2))[0]
            else:                      # wraps 0° meridian (e.g. Canada, USA West)
                lj = np.where((lons_g >= nlon1) | (lons_g <= nlon2))[0]

            if len(li) == 0 or len(lj) == 0:
                continue

            sub     = arr[:, li, :][:, :, lj]          # (nt, n_lat, n_lon)
            series  = [round(float(np.mean(sub[t])), 2) for t in range(nt)]
            mean_t  = round(float(np.mean(sub)), 2)
            min_t   = round(float(np.min(sub)),  2)
            max_t   = round(float(np.max(sub)),  2)

            results[country] = {
                "mean":    mean_t,
                "min":     min_t,
                "max":     max_t,
                "range":   round(max_t - min_t, 2),
                "cells":   len(li) * len(lj),
                "series":  series,                      # 12 monthly means
                "peak_m":  int(np.argmax(series)),      # hottest month index
                "cold_m":  int(np.argmin(series)),      # coldest month index
                "lats":    [round(float(v), 1) for v in lats_g[li]],
                "lons":    [round(float(v), 1) for v in lons_g[lj]],
            }
        return results
    except Exception as e:
        return None


@st.cache_data(ttl=1800, show_spinner=False)
def fetch_live(query: str) -> dict | None:
    """Fetch current conditions from WeatherAPI."""
    try:
        r = requests.get(WEATHER_API_URL,
            params={"key": WEATHER_API_KEY, "q": query, "aqi": "no"}, timeout=8)
        if r.status_code != 200: return None
        c = r.json()["current"]
        return {
            "temp":       round(c["temp_c"], 1),
            "feels_like": round(c["feelslike_c"], 1),
            "wind":       round(c["wind_kph"], 1),
            "wind_dir":   c.get("wind_dir", "—"),
            "humidity":   c["humidity"],
            "precip":     round(c["precip_mm"], 1),
            "pressure":   c.get("pressure_mb", 0),
            "visibility": c.get("vis_km", 0),
            "uv":         c.get("uv", 0),
            "cloud":      c.get("cloud", 0),
            "condition":  c["condition"]["text"],
        }
    except: return None


def uv_label(uv):
    if uv <= 2:  return "Low",      "var(--accent3)"
    elif uv <= 5: return "Moderate", "var(--warn)"
    elif uv <= 7: return "High",     "#ff8c00"
    elif uv <= 10: return "Very High","var(--accent2)"
    else:          return "Extreme",  "#cc0033"

def beaufort(kmh):
    if kmh < 2:   return "≈","Calm"
    elif kmh < 12: return "⇒","Light"
    elif kmh < 29: return "↗↗","Moderate"
    elif kmh < 50: return "↑↑↑","Fresh"
    elif kmh < 62: return "🌀","Near Gale"
    else:           return "🌀🌀","Gale+"

def temp_color_css(t):
    if t > 35:  return "#ff2200"
    elif t > 28: return "#ff6600"
    elif t > 20: return "#ff8c00"
    elif t > 10: return "#44aaff"
    elif t > 0:  return "#00c8ff"
    else:        return "#9d7dff"

# ─────────────────────────────────────────────
#  GUARD
# ─────────────────────────────────────────────
qp = st.query_params
if "country" in qp and qp["country"]:
    st.session_state.selected_country = qp["country"]

if "selected_country" not in st.session_state or not st.session_state.selected_country:
    st.warning("No country selected.")
    if st.button("← Back to Globe"): st.switch_page("app.py")
    st.stop()

country = st.session_state.selected_country
if country not in COUNTRY_META:
    st.error(f"'{country}' not found.")
    if st.button("← Back to Globe"): st.switch_page("app.py")
    st.stop()

mode    = qp.get("mode", "temperature")
is_wind = mode == "wind"
is_ncep = mode == "ncep"

flag   = COUNTRY_META[country]["flag"]
region = COUNTRY_META[country]["region"]
today_str = datetime.date.today().strftime("%d %b %Y")
now_str   = datetime.datetime.now().strftime("%H:%M")

# ─────────────────────────────────────────────
#  LOAD ALL NCEP DATA (all 39 countries at once, cached)
# ─────────────────────────────────────────────
ALL_NC = load_all_ncep(NCEP_PATH) if os.path.exists(NCEP_PATH) else None
NC_AVAILABLE = ALL_NC is not None and country in (ALL_NC or {})

nc = ALL_NC.get(country, {}) if ALL_NC else {}
nc_series  = nc.get("series",  [])
nc_mean    = nc.get("mean",    0.0)
nc_min     = nc.get("min",     0.0)
nc_max     = nc.get("max",     0.0)
nc_range   = nc.get("range",   0.0)
nc_cells   = nc.get("cells",   0)
nc_peak_m  = nc.get("peak_m",  6)
nc_cold_m  = nc.get("cold_m",  0)
nc_lats    = nc.get("lats",    [])
nc_lons    = nc.get("lons",    [])

# ─────────────────────────────────────────────
#  FETCH LIVE WEATHER
# ─────────────────────────────────────────────
query  = CITY_QUERY.get(country, country)
live   = fetch_live(query)
api_ok = live is not None

if not api_ok:
    live = {"temp": nc_mean, "feels_like": nc_mean, "wind": 12.0, "wind_dir": "—",
            "humidity": 60, "precip": 0.0, "pressure": 1013, "visibility": 10.0,
            "uv": 3, "cloud": 40, "condition": "Using NCEP estimate"}
cur = live

# ─────────────────────────────────────────────
#  SEASONAL TREND  — purely from NCEP series
#  x-axis: 12 months (Jan–Dec)
#  y-axis: NCEP spatial mean for that month
# ─────────────────────────────────────────────
months     = list(range(12))
month_lbls = MONTH_LABELS

# If NCEP available: use real series. Else: flat line from live temp.
if NC_AVAILABLE and nc_series:
    trend_vals  = nc_series            # 12 real monthly means from grid
    y_axis_lbl  = "NCEP Grid Temp (°C)"
    trend_title = f"Monthly Temperature Climatology · {nc_cells} grid cells"
    trend_sub   = "Source: NCEP-NCAR Reanalysis · Spatial mean over country bounding box"
else:
    trend_vals  = [cur["temp"]] * 12
    y_axis_lbl  = "Temperature (°C)"
    trend_title = "Temperature"
    trend_sub   = "NCEP data unavailable — showing live temp"

# Wind synthetic trend (NCEP has no wind data in this file)
day_seed  = datetime.date.today().toordinal()
rng_np    = np.random.default_rng(day_seed)
WIND_BASE = {c: round(10 + rng_np.uniform(5, 15), 1) for c in COUNTRY_META}
wind_vals = [round(WIND_BASE[country] + rng_np.uniform(-3, 3), 1) for _ in range(12)]
wind_vals[datetime.date.today().month - 1] = cur["wind"]

# Sub-national
day_seed2 = day_seed + 1
rng2 = np.random.default_rng(day_seed2)
STATE_CURR = {}
for ck, states in STATE_DATA.items():
    STATE_CURR[ck] = {
        s: {"temp": round(v["temp"] + rng2.uniform(-2.5, 2.5), 1),
            "wind": round(v["wind"] + rng2.uniform(-3, 3), 1),
            "lat": v["lat"], "lon": v["lon"]}
        for s, v in states.items()
    }

import urllib.parse
enc = urllib.parse.quote(country)

# ─────────────────────────────────────────────
#  BACK BUTTON
# ─────────────────────────────────────────────
bc, _ = st.columns([1, 11])
with bc:
    if st.button("← Globe"): st.switch_page("app.py")

# ─────────────────────────────────────────────
#  TOP BAR
# ─────────────────────────────────────────────
api_tag = "WeatherAPI ⚡ LIVE" if api_ok else "NCEP ESTIMATE"
api_col = "rgba(0,200,255,.35)" if api_ok else "rgba(255,183,0,.35)"
nc_tag  = f"NCEP ✓ · {nc_cells} cells" if NC_AVAILABLE else "NCEP NOT FOUND"

uv_lbl, uv_col   = uv_label(cur["uv"])
bft_sym, bft_lbl = beaufort(cur["wind"])

# Delta: live vs NCEP mean for current month
cur_month = datetime.date.today().month - 1
nc_cur_month = nc_series[cur_month] if nc_series else nc_mean
delta     = round(cur["temp"] - nc_cur_month, 1)
delta_sgn = "+" if delta >= 0 else ""
delta_col = "#ff8c00" if delta > 0 else "#60a5fa"

st.markdown(f"""
<div class="top-bar">
  <div>
    <div class="tb-country">{flag} {country}</div>
    <div class="tb-sub">{region} · {today_str}</div>
    <div style="display:flex;gap:.5rem;margin-top:.4rem;flex-wrap:wrap">
      <span class="tb-tag" style="border-color:{api_col}">{api_tag}</span>
      <span class="tb-tag nc">{nc_tag}</span>
      <span class="live-badge"><span class="lb-dot"></span>LIVE {now_str}</span>
    </div>
  </div>
  <div class="tb-stats">
    <div class="ts">
      <div class="ts-l">LIVE TEMP</div>
      <div class="ts-v" style="color:var(--accent3)">{cur['temp']:.1f}°C
        <span style="font-size:.65rem;color:{delta_col}">{delta_sgn}{delta:.1f}</span>
      </div>
    </div>
    <div class="ts">
      <div class="ts-l">NCEP {MONTH_LABELS[cur_month].upper()}</div>
      <div class="ts-v" style="color:var(--warn)">{nc_cur_month:.1f}°C</div>
    </div>
    <div class="ts">
      <div class="ts-l">FEELS LIKE</div>
      <div class="ts-v" style="color:var(--accent)">{cur['feels_like']:.1f}°C</div>
    </div>
    <div class="ts">
      <div class="ts-l">WIND</div>
      <div class="ts-v" style="color:var(--purple)">{cur['wind']:.0f}
        <span style="font-size:.65rem;color:var(--muted)"> km/h {bft_sym}</span>
      </div>
    </div>
    <div class="ts">
      <div class="ts-l">HUMIDITY</div>
      <div class="ts-v">{cur['humidity']}<span style="font-size:.7rem;color:var(--muted)">%</span></div>
    </div>
    <div class="ts">
      <div class="ts-l">UV</div>
      <div class="ts-v" style="color:{uv_col}">{cur['uv']} <span style="font-size:.65rem">{uv_lbl}</span></div>
    </div>
    <div class="ts">
      <div class="ts-l">CONDITION</div>
      <div class="ts-v" style="font-size:.82rem">{cur['condition']}</div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  MODE TOGGLE
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="mode-wrap">
  <span class="mode-label">View</span>
  <div class="mode-strip">
    <a href="?mode=temperature&country={enc}" style="text-decoration:none">
      <div class="m-btn {'on' if not is_wind and not is_ncep else ''}">🌡 Seasonal</div>
    </a><div class="m-div"></div>
    <a href="?mode=wind&country={enc}" style="text-decoration:none">
      <div class="m-btn {'on' if is_wind else ''}">💨 Wind</div>
    </a><div class="m-div"></div>
    <a href="?mode=ncep&country={enc}" style="text-decoration:none">
      <div class="m-btn {'on' if is_ncep else ''}">📊 NCEP Grid</div>
    </a>
  </div>
</div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
#  NCEP FULL-PAGE MODE — detailed grid breakdown
# ═══════════════════════════════════════════════════
if is_ncep:
    st.markdown(f"""
    <div class="sh">
      <div>
        <div class="sh-t"><span>📊</span>NCEP Grid Analysis · {country}</div>
        <div class="sh-s">Bounding box area-mean · {nc_cells} grid cells · 12-month series</div>
      </div>
    </div>""", unsafe_allow_html=True)

    if not NC_AVAILABLE:
        st.markdown("""<div style="background:rgba(255,183,0,.06);border:1px solid rgba(255,183,0,.2);
          border-radius:8px;padding:2rem;text-align:center;font-family:'JetBrains Mono',monospace;
          font-size:.82rem;color:var(--warn)">
          📂 ncep_data.json.gz not found in project root
          </div>""", unsafe_allow_html=True)
        st.stop()

    # 4 top pills
    st.markdown(f"""
    <div class="pill-row">
      <div class="pill nc">
        <div class="pl">ANNUAL MEAN</div>
        <div class="pv" style="color:var(--warn)">{nc_mean:.1f}°C</div>
        <span class="ps nc">▸ {nc_cells} GRID CELLS</span>
      </div>
      <div class="pill nc">
        <div class="pl">HOTTEST MONTH</div>
        <div class="pv" style="color:#ff6b35">{nc_series[nc_peak_m]:.1f}°C</div>
        <span class="ps nc">▸ {MONTH_LABELS[nc_peak_m].upper()}</span>
      </div>
      <div class="pill nc">
        <div class="pl">COLDEST MONTH</div>
        <div class="pv" style="color:#60a5fa">{nc_series[nc_cold_m]:.1f}°C</div>
        <span class="ps nc">▸ {MONTH_LABELS[nc_cold_m].upper()}</span>
      </div>
      <div class="pill live">
        <div class="pl">LIVE TODAY</div>
        <div class="pv" style="color:var(--accent3)">{cur['temp']:.1f}°C</div>
        <span class="ps live">▸ WeatherAPI ⚡</span>
      </div>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])
    with col1:
        # Full 12-month bar chart with live overlay
        fig_nc = go.Figure()
        bar_colors = [temp_color_css(v) for v in nc_series]
        fig_nc.add_hline(y=nc_mean, line_color="rgba(255,183,0,.4)", line_width=1.5,
                         line_dash="dot",
                         annotation_text=f"annual mean {nc_mean:.1f}°C",
                         annotation_font=dict(color="#ffb700", size=9),
                         annotation_position="top left")

        # Bar for NCEP monthly means
        fig_nc.add_trace(go.Bar(
            x=MONTH_LABELS, y=nc_series,
            marker_color=bar_colors,
            marker_line=dict(color="rgba(0,0,0,0)"),
            name="NCEP Monthly Mean",
            hovertemplate="<b>%{x}</b><br>NCEP: %{y:.2f}°C<extra></extra>",
        ))

        # Live temp overlay — current month as star
        cm_label = MONTH_LABELS[cur_month]
        fig_nc.add_trace(go.Scatter(
            x=[cm_label], y=[cur["temp"]], mode="markers",
            name=f"⚡ Live {today_str}",
            marker=dict(size=14, color="#00ff9d", symbol="star",
                        line=dict(color="#04080f", width=1.5)),
            hovertemplate=f"<b>Live · {today_str}</b><br>{cur['temp']:.1f}°C<br>{cur['condition']}<extra></extra>",
        ))

        fig_nc.update_layout(
            paper_bgcolor="#0c1525", plot_bgcolor="#0c1525",
            margin=dict(l=5, r=10, t=35, b=5), height=300,
            title=dict(text=f"NCEP Seasonal Climatology · {country} · {nc_cells} grid cells",
                       font=dict(size=10, color="#2d4a6e"), x=.01),
            xaxis=dict(tickfont=dict(color="#2d4a6e", size=9, family="JetBrains Mono"),
                       gridcolor="rgba(19,33,58,.5)", linecolor="#13213a"),
            yaxis=dict(title=dict(text="°C", font=dict(color="#2d4a6e", size=9)),
                       tickfont=dict(color="#2d4a6e", size=8, family="JetBrains Mono"),
                       ticksuffix="°C", gridcolor="rgba(19,33,58,.5)", zeroline=False),
            legend=dict(bgcolor="rgba(0,0,0,0)",
                        font=dict(color="#2d4a6e", size=9, family="JetBrains Mono"),
                        orientation="h", x=.5, xanchor="center", y=-0.2),
            hoverlabel=dict(bgcolor="#080e1a", bordercolor="#ffb700",
                            font=dict(color="#b8d4f0", size=12, family="Syne")),
            bargap=0.25,
        )
        st.plotly_chart(fig_nc, use_container_width=True, config={"displayModeBar": False})

    with col2:
        # Month-by-month table
        st.markdown('<div class="nc-box"><div class="nc-head">📅 Monthly Breakdown</div>', unsafe_allow_html=True)
        for i, (m, v) in enumerate(zip(MONTH_LABELS, nc_series)):
            bw   = int((v - nc_min) / max(nc_range, 1) * 100)
            col3 = temp_color_css(v)
            is_cur = "→ " if i == cur_month else "  "
            st.markdown(f"""
            <div class="nc-row">
              <div class="nc-t" style="color:{'var(--accent3)' if i==cur_month else 'var(--muted)'}">{is_cur}{m}</div>
              <div class="nc-bar"><div style="width:{bw}%;height:4px;background:{col3};border-radius:2px"></div></div>
              <div class="nc-v" style="color:{col3}">{v:.1f}°C</div>
            </div>""", unsafe_allow_html=True)

        lat_str = ", ".join(f"{v}°" for v in nc_lats[:5]) + ("…" if len(nc_lats) > 5 else "")
        lon_str = ", ".join(f"{v}°" for v in nc_lons[:5]) + ("…" if len(nc_lons) > 5 else "")
        st.markdown(f"""
        <div style="margin-top:.65rem;font-size:.6rem;font-family:'JetBrains Mono',monospace;
                    color:var(--muted);line-height:2.1">
          CELLS: <span style="color:var(--warn)">{nc_cells}</span>
          &nbsp;·&nbsp; RANGE: <span style="color:var(--warn)">Δ{nc_range:.1f}°C</span><br>
          LATS: <span style="color:var(--accent);font-size:.55rem">{lat_str}</span><br>
          LONS: <span style="color:var(--accent);font-size:.55rem">{lon_str}</span>
        </div></div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="alert nc">
      <span class="ai">📊</span>
      <div><span class="ab nc">NCEP: </span>
        <b>{country}</b> annual mean <b>{nc_mean:.1f}°C</b> from <b>{nc_cells} grid cells</b>.
        Hottest: <b>{MONTH_LABELS[nc_peak_m]} {nc_series[nc_peak_m]:.1f}°C</b> ·
        Coldest: <b>{MONTH_LABELS[nc_cold_m]} {nc_series[nc_cold_m]:.1f}°C</b> ·
        Seasonal range: <b>Δ{nc_range:.1f}°C</b>.
        Live ({MONTH_LABELS[cur_month]}): <b>{cur['temp']:.1f}°C</b>
        vs NCEP climatology <b>{nc_cur_month:.1f}°C</b>
        ({delta_sgn}{delta:.1f}°C anomaly).
      </div>
    </div>""", unsafe_allow_html=True)

    st.stop()

# ═══════════════════════════════════════════════════
#  MAIN 2-COL LAYOUT
# ═══════════════════════════════════════════════════
lhs, rhs = st.columns([1, 1], gap="large")

# ─── LHS — SEASONAL / WIND CHART ───
with lhs:
    if not is_wind:
        st.markdown(f"""
        <div class="sh">
          <div>
            <div class="sh-t"><span>〰</span>Seasonal Temperature Climatology</div>
            <div class="sh-s">{'NCEP · ' + str(nc_cells) + ' grid cells · Jan–Dec' if NC_AVAILABLE else 'Live estimate'}</div>
          </div>
        </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="pill-row">
          <div class="pill nc">
            <div class="pl">ANNUAL MEAN</div>
            <div class="pv" style="color:var(--warn)">{nc_mean:.1f}°C</div>
            <span class="ps nc">▸ NCEP {nc_cells} CELLS</span>
          </div>
          <div class="pill {'hot' if nc_series[nc_peak_m] > 25 else 'nc'}">
            <div class="pl">PEAK · {MONTH_LABELS[nc_peak_m].upper()}</div>
            <div class="pv" style="color:#ff6b35">{nc_series[nc_peak_m]:.1f}°C</div>
            <span class="ps nc">▸ HOTTEST MONTH</span>
          </div>
          <div class="pill live">
            <div class="pl">LIVE · {MONTH_LABELS[cur_month].upper()}</div>
            <div class="pv" style="color:var(--accent3)">{cur['temp']:.1f}°C</div>
            <span class="ps live">▸ WeatherAPI ⚡</span>
          </div>
        </div>""", unsafe_allow_html=True)

        fig = go.Figure()

        # Shaded area fill
        ymin = min(trend_vals) - 4
        fig.add_trace(go.Scatter(
            x=MONTH_LABELS + MONTH_LABELS[::-1],
            y=trend_vals + [ymin] * 12,
            fill="toself", fillcolor="rgba(0,255,157,.05)",
            line=dict(color="rgba(0,0,0,0)"), showlegend=False, hoverinfo="skip"))

        # NCEP seasonal line
        marker_colors = [temp_color_css(v) for v in trend_vals]
        fig.add_trace(go.Scatter(
            x=MONTH_LABELS, y=trend_vals,
            mode="lines+markers", name="NCEP Monthly",
            line=dict(color="#00ff9d", width=2.5, shape="spline", smoothing=.8),
            marker=dict(size=8, color=marker_colors,
                        line=dict(color="#04080f", width=1.2)),
            hovertemplate="<b>%{x}</b><br>NCEP: %{y:.1f}°C<extra></extra>",
            showlegend=False))

        # Annual mean line
        fig.add_hline(y=nc_mean, line_color="rgba(255,183,0,.3)", line_width=1.2,
                      line_dash="dot")

        # Live today marker on current month
        fig.add_trace(go.Scatter(
            x=[MONTH_LABELS[cur_month]], y=[cur["temp"]],
            mode="markers", name=f"⚡ Live {today_str}",
            marker=dict(size=14, color="#00ff9d", symbol="star",
                        line=dict(color="#04080f", width=1.5)),
            hovertemplate=f"<b>Live · {today_str}</b><br>{cur['temp']:.1f}°C · {cur['condition']}<extra></extra>",
            showlegend=True))

        # Peak annotation
        fig.add_annotation(
            x=MONTH_LABELS[nc_peak_m], y=nc_series[nc_peak_m],
            text=f"  Peak {nc_series[nc_peak_m]:.1f}°C",
            showarrow=True, arrowhead=2, arrowcolor="#00c8ff", arrowsize=.7,
            ax=28, ay=-30, font=dict(color="#00c8ff", size=9, family="JetBrains Mono"),
            bgcolor="rgba(8,14,26,.9)", bordercolor="#00c8ff", borderwidth=1, borderpad=3)

        fig.update_layout(
            paper_bgcolor="#0c1525", plot_bgcolor="#0c1525",
            margin=dict(l=5, r=10, t=8, b=5), height=295, showlegend=True,
            legend=dict(bgcolor="rgba(0,0,0,0)",
                font=dict(color="#2d4a6e", size=9, family="JetBrains Mono"),
                orientation="h", x=.5, xanchor="center", y=-0.18),
            xaxis=dict(tickfont=dict(color="#2d4a6e", size=8, family="JetBrains Mono"),
                gridcolor="rgba(19,33,58,.6)", zeroline=False, linecolor="#13213a"),
            yaxis=dict(tickfont=dict(color="#2d4a6e", size=8, family="JetBrains Mono"),
                ticksuffix="°", gridcolor="rgba(19,33,58,.6)", zeroline=False,
                range=[ymin, max(trend_vals + [cur["temp"]]) + 4]),
            hoverlabel=dict(bgcolor="#080e1a", bordercolor="#00ff9d",
                font=dict(color="#b8d4f0", size=12, family="Syne")))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        # Alert
        sc = STATE_CURR.get(country)
        nc_note = (f" NCEP annual mean: <b>{nc_mean:.1f}°C</b> · "
                   f"Peak <b>{MONTH_LABELS[nc_peak_m]}</b> · "
                   f"Coldest <b>{MONTH_LABELS[nc_cold_m]}</b>.") if NC_AVAILABLE else ""
        if sc:
            hs = max(sc.items(), key=lambda x: x[1]["temp"])[0]
            alert_txt = (f"Hottest region today: <b>{hs}</b> ({sc[hs]['temp']:.1f}°C). "
                        f"Live national: <b>{cur['temp']:.1f}°C</b> ({cur['condition']}).{nc_note}")
        else:
            alert_txt = (f"Live: <b>{cur['temp']:.1f}°C</b> · {cur['condition']} · "
                        f"Feels {cur['feels_like']:.1f}°C.{nc_note}")
        st.markdown(f"""
        <div class="alert">
          <span class="ai">ℹ</span>
          <div><span class="ab">Seasonal: </span>{alert_txt}</div>
        </div>""", unsafe_allow_html=True)

        # NCEP mini bars (all 12 months)
        if NC_AVAILABLE:
            st.markdown(f"""
            <div class="nc-box">
              <div class="nc-head">📊 NCEP Monthly · {nc_cells} cells · Jan–Dec</div>
              <div style="display:flex;gap:.3rem;align-items:flex-end;width:100%">""",
                unsafe_allow_html=True)
            v_min2 = min(nc_series); v_max2 = max(nc_series); span2 = max(v_max2 - v_min2, 1)
            bars = ""
            for i, (m, v) in enumerate(zip(MONTH_LABELS, nc_series)):
                bh   = max(4, int((v - v_min2) / span2 * 45))
                bc2  = temp_color_css(v)
                bold = "font-weight:700;" if i == cur_month else ""
                bars += f"""<div style="flex:1;text-align:center">
                  <div style="font-size:.5rem;font-family:'JetBrains Mono',monospace;
                    color:{bc2};margin-bottom:2px;{bold}">{v:.0f}°</div>
                  <div style="height:{bh}px;background:{bc2};
                    border-radius:2px 2px 0 0;opacity:{'.95' if i==cur_month else '.7'}"></div>
                  <div style="font-size:.48rem;font-family:'JetBrains Mono',monospace;
                    color:{'var(--accent3)' if i==cur_month else 'var(--muted)'};margin-top:3px">{m[:1]}</div>
                </div>"""
            st.markdown(f"""
              <div style="display:flex;gap:.3rem;align-items:flex-end;
                width:100%;margin-bottom:.3rem">{bars}</div>
              <div style="font-size:.56rem;color:var(--muted);
                font-family:'JetBrains Mono',monospace;margin-top:.3rem">
                Mean: <span style="color:#ffb700">{nc_mean:.1f}°C</span>
                &nbsp;·&nbsp; Range: <span style="color:#ffb700">Δ{nc_range:.1f}°C</span>
                &nbsp;·&nbsp; Cells: <span style="color:var(--accent)">{nc_cells}</span>
                &nbsp;·&nbsp; Source: NCEP-NCAR
              </div>
            </div>""", unsafe_allow_html=True)

        # Extra metric cards
        uv_l2, uv_c2 = uv_label(cur["uv"])
        st.markdown(f"""
        <div class="mini-grid">
          <div class="mini-card uv">
            <div class="mc-l">UV Index</div>
            <div class="mc-v" style="color:{uv_c2}">{cur['uv']} · {uv_l2}</div>
            <div class="mc-s">Solar irradiance</div>
          </div>
          <div class="mini-card cloud">
            <div class="mc-l">Cloud Cover</div>
            <div class="mc-v" style="color:var(--muted)">{cur['cloud']}%</div>
            <div class="mc-s">Sky coverage</div>
          </div>
          <div class="mini-card vis">
            <div class="mc-l">Visibility</div>
            <div class="mc-v" style="color:var(--accent)">{cur['visibility']} km</div>
            <div class="mc-s">Horizontal range</div>
          </div>
          <div class="mini-card pres">
            <div class="mc-l">Pressure</div>
            <div class="mc-v" style="color:var(--accent2)">{cur['pressure']} hPa</div>
            <div class="mc-s">Sea level</div>
          </div>
        </div>""", unsafe_allow_html=True)

    else:
        # Wind chart (month axis, synthetic monthly wind)
        st.markdown(f"""
        <div class="sh">
          <div>
            <div class="sh-t"><span>💨</span>Monthly Wind Speed</div>
            <div class="sh-s">Estimated seasonal pattern · Jan–Dec</div>
          </div>
        </div>""", unsafe_allow_html=True)

        w_mean = round(float(np.mean(wind_vals)), 1)
        bft_s, bft_l = beaufort(cur["wind"])
        st.markdown(f"""
        <div class="pill-row">
          <div class="pill wind">
            <div class="pl">MONTHLY AVG</div>
            <div class="pv" style="color:var(--purple)">{w_mean:.1f} km/h</div>
            <span class="ps wind">▸ SEASONAL MEAN</span>
          </div>
          <div class="pill wind">
            <div class="pl">PEAK MONTH</div>
            <div class="pv" style="color:var(--purple)">{max(wind_vals):.1f} km/h</div>
            <span class="ps wind">▸ {MONTH_LABELS[wind_vals.index(max(wind_vals))].upper()}</span>
          </div>
          <div class="pill live">
            <div class="pl">LIVE WIND</div>
            <div class="pv" style="color:var(--purple)">{cur['wind']:.1f} km/h</div>
            <span class="ps live">▸ {bft_s} {bft_l} · WeatherAPI ⚡</span>
          </div>
        </div>""", unsafe_allow_html=True)

        fig_w = go.Figure()
        fig_w.add_trace(go.Scatter(
            x=MONTH_LABELS + MONTH_LABELS[::-1],
            y=wind_vals + [min(wind_vals) - 2] * 12,
            fill="toself", fillcolor="rgba(157,125,255,.06)",
            line=dict(color="rgba(0,0,0,0)"), showlegend=False, hoverinfo="skip"))
        fig_w.add_trace(go.Scatter(
            x=MONTH_LABELS, y=wind_vals,
            mode="lines+markers", name="Monthly Wind",
            line=dict(color="#9d7dff", width=2.2, shape="spline", smoothing=.8),
            marker=dict(size=7, color="#9d7dff",
                        line=dict(color="#04080f", width=1.2)),
            hovertemplate="<b>%{x}</b><br>%{y:.1f} km/h<extra></extra>",
            showlegend=False))
        fig_w.add_trace(go.Scatter(
            x=[MONTH_LABELS[cur_month]], y=[cur["wind"]],
            mode="markers", name=f"⚡ Live {today_str}",
            marker=dict(size=14, color="#c4b5fd", symbol="star",
                        line=dict(color="#04080f", width=1.5)),
            hovertemplate=f"<b>Live · {today_str}</b><br>{cur['wind']:.1f} km/h · {bft_l}<extra></extra>",
            showlegend=True))
        fig_w.update_layout(
            paper_bgcolor="#0c1525", plot_bgcolor="#0c1525",
            margin=dict(l=5, r=10, t=8, b=5), height=295, showlegend=True,
            legend=dict(bgcolor="rgba(0,0,0,0)",
                font=dict(color="#2d4a6e", size=9, family="JetBrains Mono"),
                orientation="h", x=.5, xanchor="center", y=-.15),
            xaxis=dict(tickfont=dict(color="#2d4a6e", size=8, family="JetBrains Mono"),
                gridcolor="rgba(19,33,58,.6)", zeroline=False, linecolor="#13213a"),
            yaxis=dict(tickfont=dict(color="#2d4a6e", size=8, family="JetBrains Mono"),
                ticksuffix=" km/h", gridcolor="rgba(19,33,58,.6)", zeroline=False),
            hoverlabel=dict(bgcolor="#080e1a", bordercolor="#9d7dff",
                font=dict(color="#b8d4f0", size=12, family="Syne")))
        st.plotly_chart(fig_w, use_container_width=True, config={"displayModeBar": False})

        sc = STATE_CURR.get(country)
        if sc:
            ws = max(sc.items(), key=lambda x: x[1]["wind"])
            cs = min(sc.items(), key=lambda x: x[1]["wind"])
            ws2, wl2 = beaufort(ws[1]["wind"]); cs2, cl2 = beaufort(cs[1]["wind"])
            alert_txt = (f"Windiest region: <b>{ws[0]}</b> {ws2} {ws[1]['wind']:.1f} km/h ({wl2}). "
                        f"Calmest: <b>{cs[0]}</b> {cs2} {cs[1]['wind']:.1f} km/h. "
                        f"Live: <b>⚡{cur['wind']:.1f} km/h {bft_s}</b>.")
        else:
            alert_txt = f"Live: <b>⚡{bft_s} {cur['wind']:.1f} km/h</b> ({bft_l}) from {cur['wind_dir']}."
        st.markdown(f"""
        <div class="alert wind">
          <span class="ai">💨</span>
          <div><span class="ab wind">Wind: </span>{alert_txt}</div>
        </div>""", unsafe_allow_html=True)

# ─── RHS — MAP ───
with rhs:
    metric_lbl = "Wind" if is_wind else "Temperature"
    st.markdown(f"""
    <div class="sh">
      <div>
        <div class="sh-t"><span>🗺</span>Geospatial {metric_lbl}</div>
        <div class="sh-s">Sub-national · {today_str}</div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="pill-row">
      <div class="pill {'live' if not is_wind else 'wind'}">
        <div class="pl">LIVE TEMP</div>
        <div class="pv" style="color:var(--accent3)">{cur['temp']:.1f}°C</div>
        <span class="ps live">● WeatherAPI ⚡</span>
      </div>
      <div class="pill wind">
        <div class="pl">LIVE WIND</div>
        <div class="pv" style="color:var(--purple)">{cur['wind']:.0f} km/h</div>
        <span class="ps wind">● WeatherAPI ⚡</span>
      </div>
      <div class="pill nc">
        <div class="pl">NCEP {MONTH_LABELS[cur_month].upper()}</div>
        <div class="pv" style="color:var(--warn)">{nc_cur_month:.1f}°C</div>
        <span class="ps nc">{'● ' + str(nc_cells) + ' grid cells' if NC_AVAILABLE else '○ NOT LOADED'}</span>
      </div>
    </div>""", unsafe_allow_html=True)

    def tc_hex(t):
        if t > 35:  return "#ff2200"
        elif t > 28: return "#ff6600"
        elif t > 20: return "#ff8c00"
        elif t > 10: return "#44aaff"
        elif t > 0:  return "#00c8ff"
        else:        return "#9d7dff"

    def wc_hex(w):
        if w > 25: return "#6d28d9"
        elif w > 20: return "#7c3aed"
        elif w > 15: return "#9d7dff"
        elif w > 10: return "#c4b5fd"
        else:        return "#ede9fe"

    # Map coords per country (only needed for the map pin, not NCEP)
    MAP_COORDS = {
        "Afghanistan":(33.9,67.7),"Argentina":(-38.4,-63.6),"Australia":(-25.3,133.8),
        "Brazil":(-14.2,-51.9),"Canada":(56.1,-106.3),"China":(35.9,104.2),
        "Denmark":(56.3,9.5),"Egypt":(26.8,30.8),"Ethiopia":(9.1,40.5),
        "France":(46.2,2.2),"Germany":(51.2,10.5),"Greenland":(71.7,-42.6),
        "India":(20.6,78.9),"Indonesia":(-0.8,113.9),"Iran":(32.4,53.7),
        "Japan":(36.2,138.2),"Kenya":(0.0,37.9),"Mexico":(23.6,-102.6),
        "Morocco":(31.8,-7.1),"Netherlands":(52.1,5.3),"New Zealand":(-40.9,174.9),
        "Nigeria":(9.1,8.7),"Norway":(60.5,8.5),"Pakistan":(30.4,69.3),
        "Peru":(-9.2,-75.0),"Poland":(51.9,19.1),"Russia":(61.5,105.3),
        "Saudi Arabia":(23.9,45.1),"South Africa":(-30.6,22.9),"South Korea":(35.9,127.8),
        "Spain":(40.5,-3.7),"Sweden":(60.1,18.6),"Switzerland":(46.8,8.2),
        "Turkey":(38.9,35.2),"Ukraine":(48.4,31.2),"United Kingdom":(55.4,-3.4),
        "United States":(37.1,-95.7),"Venezuela":(6.4,-66.6),"Vietnam":(14.1,108.3),
    }
    clat, clon = MAP_COORDS.get(country, (0, 0))

    sc = STATE_CURR.get(country)
    if sc:
        sn = list(sc.keys())
        st2 = [sc[s]["temp"] for s in sn]
        sw2 = [sc[s]["wind"] for s in sn]
        sla = [sc[s]["lat"]  for s in sn]
        slo = [sc[s]["lon"]  for s in sn]
        vals = sw2 if is_wind else st2
        colors = [wc_hex(v) if is_wind else tc_hex(v) for v in vals]
        vmin2, vmax2 = min(vals), max(vals)
        def bsz2(v): return 16 + (v - vmin2) / max(vmax2 - vmin2, 1) * 22
        htexts = [f"<b>{s}</b><br>🌡 {t:.1f}°C · 💨 {beaufort(w)[0]} {w:.1f} km/h"
                  for s, t, w in zip(sn, st2, sw2)]
        fig_m = go.Figure()
        fig_m.add_trace(go.Scattergeo(
            lat=sla, lon=slo, hoverinfo="skip", mode="markers", showlegend=False,
            marker=dict(size=[bsz2(v)+8 for v in vals], color=colors, opacity=.12,
                        line=dict(width=0))))
        fig_m.add_trace(go.Scattergeo(
            lat=sla, lon=slo, text=htexts, hoverinfo="text",
            mode="markers+text",
            textfont=dict(size=6.5, color="rgba(184,212,240,.4)", family="JetBrains Mono"),
            textposition="bottom center", showlegend=False,
            marker=dict(size=[bsz2(v) for v in vals], color=colors, opacity=.88,
                        line=dict(color="rgba(255,255,255,.1)", width=1))))

        SCOPE = {"India":("asia",20.5,78.9,3.2),"United States":("north america",38,-96,2.5),
                 "Australia":("world",-25,134,3),"Brazil":("south america",-14,-53,2.8),
                 "Russia":("world",62,100,1.8),"Canada":("north america",57,-100,2.4),
                 "China":("asia",35,104,2.8)}
        scope, mc_lat, mc_lon, zoom = SCOPE.get(country, ("world", clat, clon, 3.0))
        fig_m.update_layout(
            geo=dict(scope=scope, projection_type="natural earth",
                showland=True, landcolor="#091520", showocean=True, oceancolor="#050c16",
                showcountries=True, countrycolor="#13213a", showcoastlines=True,
                coastlinecolor="#182d48", showframe=False, bgcolor="#0c1525",
                showlakes=True, lakecolor="#050c16",
                center=dict(lat=mc_lat, lon=mc_lon), projection_scale=zoom),
            paper_bgcolor="#0c1525", margin=dict(l=0,r=0,t=5,b=5),
            height=320, showlegend=False,
            hoverlabel=dict(bgcolor="#080e1a", bordercolor="#00c8ff",
                font=dict(color="#b8d4f0", size=12, family="Syne")))
        st.plotly_chart(fig_m, use_container_width=True, config={"displayModeBar": False})

        if is_wind:
            st.markdown("""<div style="margin-top:.35rem">
              <div class="leg-bar wind"></div>
              <div class="leg-lbl"><span>STRONG &gt;25km/h</span><span>MODERATE</span><span>CALM &lt;10</span></div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""<div style="margin-top:.35rem">
              <div class="leg-bar temp"></div>
              <div class="leg-lbl"><span>HOT &gt;35°C</span><span>MODERATE</span><span>COOL/FREEZE</span></div>
            </div>""", unsafe_allow_html=True)

        ht_s = max(zip(sn, st2), key=lambda x: x[1])
        ld_s = min(zip(sn, st2), key=lambda x: x[1])
        wd_s = max(zip(sn, sw2), key=lambda x: x[1])
        st.markdown(f"""
        <div style="display:flex;gap:1rem;flex-wrap:wrap;margin-top:.4rem;
            font-size:.7rem;font-family:'JetBrains Mono',monospace;color:var(--muted)">
          <span>⚡ <b style="color:var(--accent3)">{cur['temp']:.1f}°C</b> · {cur['condition']}</span>
          <span>🔥 <b style="color:#ff4d6d">{ht_s[0]}</b> {ht_s[1]:.1f}°C</span>
          <span>❄️ <b style="color:#00c8ff">{ld_s[0]}</b> {ld_s[1]:.1f}°C</span>
          {'<span>📊 NCEP <b style="color:var(--warn)">' + f"{nc_cur_month:.1f}°C" + '</b></span>' if NC_AVAILABLE else ''}
        </div>""", unsafe_allow_html=True)
    else:
        # Single dot map for countries without sub-national data
        dv = cur["wind"] if is_wind else cur["temp"]
        dc = wc_hex(dv) if is_wind else tc_hex(dv)
        ht = (f"<b>{country}</b><br>🌡 {cur['temp']:.1f}°C · {cur['condition']}<br>"
              f"💨 {cur['wind']:.1f} km/h · {cur['wind_dir']}<br>"
              f"💧 {cur['humidity']}% · 🌧 {cur['precip']:.1f}mm"
              + (f"<br>📊 NCEP {MONTH_LABELS[cur_month]}: {nc_cur_month:.1f}°C" if NC_AVAILABLE else ""))
        fig_m = go.Figure(go.Scattergeo(
            lat=[clat], lon=[clon], text=[ht], hoverinfo="text", mode="markers",
            marker=dict(size=36, color=[dv],
                colorscale=([[0,"#c4b5fd"],[.5,"#9d7dff"],[1,"#6d28d9"]] if is_wind
                            else [[0,"#9d7dff"],[.25,"#00c8ff"],[.55,"#ffcc00"],[1,"#ff3300"]]),
                cmin=5 if is_wind else -20, cmax=35 if is_wind else 40,
                line=dict(color=dc, width=2), opacity=.9)))
        fig_m.update_layout(
            geo=dict(showland=True, landcolor="#091520", showocean=True, oceancolor="#050c16",
                showcountries=True, countrycolor="#13213a", showframe=False, bgcolor="#0c1525",
                center=dict(lat=clat, lon=clon), projection_scale=3),
            paper_bgcolor="#0c1525", margin=dict(l=0,r=20,t=5,b=5), height=320)
        st.plotly_chart(fig_m, use_container_width=True, config={"displayModeBar": False})
        st.markdown(f"""
        <div style="display:flex;gap:1rem;flex-wrap:wrap;margin-top:.4rem;
            font-size:.7rem;font-family:'JetBrains Mono',monospace;color:var(--muted)">
          <span>⚡ <b style="color:var(--accent3)">{cur['temp']:.1f}°C</b></span>
          <span>💨 <b>{cur['wind']:.0f} km/h</b></span>
          <span>💧 <b>{cur['humidity']}%</b></span>
          {'<span>📊 NCEP <b style="color:var(--warn)">' + f"{nc_cur_month:.1f}°C" + '</b></span>' if NC_AVAILABLE else ''}
        </div>""", unsafe_allow_html=True)