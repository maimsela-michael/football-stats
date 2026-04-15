import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# =============================================
# הגדרות בסיסיות
# =============================================

st.set_page_config(
    page_title="⚽ 5 הליגות הגדולות",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Heebo', sans-serif; }

    .main-header {
        text-align: center;
        padding: 28px 0 12px 0;
        background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
        border-radius: 20px;
        margin-bottom: 28px;
        border: 1px solid #30363d;
    }
    .main-header h1 {
        font-size: 2.6rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00ff88, #00aaff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .main-header p { color: #8b949e; font-size: 0.9rem; margin: 8px 0 0 0; }

    .league-card {
        background: linear-gradient(135deg, #1c2333, #1f2d3d);
        border-radius: 16px;
        padding: 20px;
        border: 1px solid #30363d;
        margin: 8px 0;
        text-align: center;
        transition: transform 0.2s;
    }
    .league-card:hover { transform: translateY(-4px); border-color: #00ff88; }
    .league-card h3 { color: white; font-size: 1rem; margin: 0 0 12px 0; }
    .leader { color: #00ff88; font-size: 1.1rem; font-weight: 700; margin: 8px 0; }
    .points-badge {
        background: linear-gradient(135deg, #00ff88, #00aaff);
        color: #0d1117;
        border-radius: 20px;
        padding: 4px 16px;
        font-weight: 700;
        font-size: 1.2rem;
        display: inline-block;
    }
    .stat-row { color: #8b949e; font-size: 0.85rem; margin: 4px 0; }

    .section-title {
        color: white;
        font-size: 1.5rem;
        font-weight: 700;
        padding: 20px 0 10px 0;
        border-bottom: 2px solid #30363d;
        margin-bottom: 20px;
    }

    .alert-card {
        background: linear-gradient(135deg, #1a1a0e, #2a2a0e);
        border: 1px solid #ffaa00;
        border-radius: 14px;
        padding: 16px 20px;
        margin: 10px 0;
    }
    .alert-card .alert-title { color: #ffaa00; font-weight: 700; font-size: 1rem; margin: 0 0 6px 0; }
    .alert-card .alert-body { color: #e0e0e0; font-size: 0.9rem; }
    .alert-card .alert-progress { color: #00ff88; font-weight: 600; }

    .record-card {
        background: linear-gradient(135deg, #1a0e2a, #2a0e3a);
        border: 1px solid #aa44ff;
        border-radius: 14px;
        padding: 16px 20px;
        margin: 10px 0;
    }
    .record-card .record-title { color: #aa44ff; font-weight: 700; font-size: 1rem; }
    .record-card .record-body { color: #e0e0e0; font-size: 0.9rem; }

    .match-card {
        background: #1c2333;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 14px 20px;
        margin: 6px 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .form-W {
        background: #00aa44;
        color: white;
        border-radius: 6px;
        padding: 3px 8px;
        font-weight: 700;
        font-size: 0.85rem;
        display: inline-block;
        margin: 2px;
    }
    .form-D {
        background: #aa8800;
        color: white;
        border-radius: 6px;
        padding: 3px 8px;
        font-weight: 700;
        font-size: 0.85rem;
        display: inline-block;
        margin: 2px;
    }
    .form-L {
        background: #aa2200;
        color: white;
        border-radius: 6px;
        padding: 3px 8px;
        font-weight: 700;
        font-size: 0.85rem;
        display: inline-block;
        margin: 2px;
    }

    div[data-testid="stMetricValue"] { color: #00ff88 !important; font-size: 1.8rem !important; }
    div[data-testid="metric-container"] {
        background: #1c2333;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: #0d1117;
        padding: 8px;
        border-radius: 12px;
        flex-wrap: wrap;
    }
    .stTabs [data-baseweb="tab"] {
        background: #1c2333;
        border-radius: 10px;
        color: #8b949e;
        font-size: 14px;
        font-weight: 600;
        padding: 8px 16px;
        border: 1px solid #30363d;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00ff88, #00aaff) !important;
        color: #0d1117 !important;
        border: none !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #00ff88, #00aaff);
        color: #0d1117;
        font-weight: 700;
        border: none;
        border-radius: 10px;
    }

    .compare-header {
        background: #1c2333;
        border-radius: 12px;
        padding: 12px 20px;
        text-align: center;
        font-size: 1.2rem;
        font-weight: 700;
        color: white;
        margin: 10px 0;
        border: 1px solid #30363d;
    }

    .api-info {
        background: #1c2333;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 12px;
        color: #8b949e;
        font-size: 0.8rem;
        text-align: center;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# =============================================
# קונפיגורציה
# =============================================

LEAGUES = {
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League": {"id": 39, "country": "England",  "color": "#3d86c8"},
    "🇪🇸 La Liga":              {"id": 140,"country": "Spain",    "color": "#c8233a"},
    "🇮🇹 Serie A":              {"id": 135,"country": "Italy",    "color": "#006ab3"},
    "🇩🇪 Bundesliga":           {"id": 78, "country": "Germany",  "color": "#d32f2f"},
    "🇫🇷 Ligue 1":              {"id": 61, "country": "France",   "color": "#0d47a1"},
}
SEASON = 2024

# שיאי עונה מפורסמים (לפי ליגה)
SEASON_RECORDS = {
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League": {"goals": 36, "holder": "Erling Haaland", "season": "2022/23"},
    "🇪🇸 La Liga":              {"goals": 50, "holder": "Lionel Messi",   "season": "2011/12"},
    "🇮🇹 Serie A":              {"goals": 36, "holder": "Gonzalo Higuaín","season": "2015/16"},
    "🇩🇪 Bundesliga":           {"goals": 41, "holder": "Robert Lewandowski","season": "2020/21"},
    "🇫🇷 Ligue 1":              {"goals": 29, "holder": "Kylian Mbappé",  "season": "2022/23"},
}

# =============================================
# API
# =============================================

def get_api_key():
    # בענן (Streamlit Cloud) — קורא מה-Secrets
    try:
        return st.secrets["RAPIDAPI_KEY"]
    except:
        pass
    # במחשב המקומי — קורא מקובץ
    try:
        with open("api_key.txt", "r") as f:
            return f.read().strip()
    except:
        return ""

API_KEY = get_api_key()
HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}
BASE_URL = "https://api-football-v1.p.rapidapi.com/v3"

@st.cache_data(ttl=3600 * 6, show_spinner=False)
def fetch_standings(league_id):
    try:
        r = requests.get(f"{BASE_URL}/standings",
                         headers=HEADERS,
                         params={"league": league_id, "season": SEASON},
                         timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data.get("response"):
                return data["response"][0]["league"]["standings"][0]
    except Exception as e:
        st.error(f"שגיאה: {e}")
    return []

@st.cache_data(ttl=3600 * 6, show_spinner=False)
def fetch_top_scorers(league_id):
    try:
        r = requests.get(f"{BASE_URL}/players/topscorers",
                         headers=HEADERS,
                         params={"league": league_id, "season": SEASON},
                         timeout=10)
        if r.status_code == 200:
            return r.json().get("response", [])
    except:
        pass
    return []

@st.cache_data(ttl=3600 * 6, show_spinner=False)
def fetch_top_assists(league_id):
    try:
        r = requests.get(f"{BASE_URL}/players/topassists",
                         headers=HEADERS,
                         params={"league": league_id, "season": SEASON},
                         timeout=10)
        if r.status_code == 200:
            return r.json().get("response", [])
    except:
        pass
    return []

@st.cache_data(ttl=3600 * 3, show_spinner=False)
def fetch_team_matches(team_id, last=5):
    """שליפת 5 המשחקים האחרונים של קבוצה"""
    try:
        r = requests.get(f"{BASE_URL}/fixtures",
                         headers=HEADERS,
                         params={"team": team_id, "last": last, "season": SEASON},
                         timeout=10)
        if r.status_code == 200:
            return r.json().get("response", [])
    except:
        pass
    return []

# =============================================
# פונקציות עזר
# =============================================

def get_all_teams_dict(selected_leagues):
    """מחזיר מילון: שם_קבוצה → {id, league}"""
    teams = {}
    for league_name in selected_leagues:
        info = LEAGUES.get(league_name)
        if not info:
            continue
        standings = fetch_standings(info["id"])
        for team in standings:
            teams[team["team"]["name"]] = {
                "id": team["team"]["id"],
                "league": league_name,
                "points": team["points"],
                "played": team["all"]["played"],
            }
    return teams

def format_form(form_str):
    """ממיר מחרוזת WWDLW לעיגולים צבעוניים + חץ מגמה"""
    if not form_str:
        return "—"

    last5 = form_str[-5:]

    # עיגולים לכל תוצאה
    circle_map = {"W": "🟢", "D": "🟡", "L": "🔴"}
    circles = " ".join(circle_map.get(c, "⚪") for c in last5)

    # חישוב נקודות ומגמה
    pts_total = last5.count("W") * 3 + last5.count("D")

    # מגמה: השוואת 2 המשחקים האחרונים מול 2 הראשונים
    if len(last5) >= 4:
        recent_pts  = last5[-2:].count("W") * 3 + last5[-2:].count("D")
        earlier_pts = last5[:2].count("W") * 3  + last5[:2].count("D")
        diff = recent_pts - earlier_pts
    else:
        diff = 0

    # בחירת סמל מגמה
    if pts_total >= 13:          # 4-5 ניצחונות
        trend = "🔥"
        label = "בשיא כושר"
    elif pts_total >= 10:        # בדרך כלל 3נ+תיקו
        trend = "⬆️"
        label = "פורמה טובה"
    elif diff >= 4:
        trend = "↗️"
        label = "בעלייה"
    elif diff >= 1:
        trend = "↗️"
        label = "בשיפור"
    elif diff == 0 and pts_total >= 5:
        trend = "➡️"
        label = "יציב"
    elif diff == 0:
        trend = "➡️"
        label = "מעורב"
    elif diff >= -3:
        trend = "↘️"
        label = "בירידה"
    else:
        trend = "⬇️"
        label = "במשבר"

    return circles, trend, label


def format_form_html(form_str):
    """גרסת HTML להצגה מלאה בממשק"""
    if not form_str:
        return "<span style='color:#8b949e'>—</span>"
    circles, trend, label = format_form(form_str)
    return (
        f"<span style='font-size:1.1rem; letter-spacing:2px;'>{circles}</span>"
        f"&nbsp;&nbsp;<span style='font-size:1.3rem;'>{trend}</span>"
        f"&nbsp;<span style='color:#8b949e; font-size:0.85rem;'>{label}</span>"
    )


def form_emoji_only(form_str):
    """גרסה קצרה לטבלאות: עיגולים + חץ בלבד"""
    if not form_str:
        return "—"
    circles, trend, _ = format_form(form_str)
    return f"{circles} {trend}"

def build_combined_standings(selected_leagues):
    """בונה טבלת דירוג משולבת לכל הליגות"""
    rows = []
    for league_name in selected_leagues:
        info = LEAGUES.get(league_name)
        if not info:
            continue
        standings = fetch_standings(info["id"])
        for team in standings:
            goals_for  = team["all"]["goals"]["for"]
            goals_ag   = team["all"]["goals"]["against"]
            played     = team["all"]["played"]
            pts        = team["points"]
            rows.append({
                "ליגה": league_name,
                "קבוצה": team["team"]["name"],
                "מ": played,
                "נ": team["all"]["win"],
                "ת": team["all"]["draw"],
                "ה": team["all"]["lose"],
                "הבקיעו": goals_for,
                "קיבלו": goals_ag,
                "הפרש": team["goalsDiff"],
                "נקודות": pts,
                "% הצלחה": round(pts / played / 3 * 100, 1) if played else 0,
                "פורמה": form_emoji_only(team.get("form", "")),
                "_team_id": team["team"]["id"],
            })
    if not rows:
        return pd.DataFrame()
    df = pd.DataFrame(rows)
    df = df.sort_values(["נקודות", "הפרש", "הבקיעו"], ascending=False).reset_index(drop=True)
    df.insert(0, "מקום", range(1, len(df) + 1))
    return df

def build_scorers_df(data, league_name, n):
    rows = []
    for i, entry in enumerate(data[:n]):
        p = entry["player"]
        s = entry["statistics"][0]
        goals   = s["goals"]["total"]   or 0
        assists = s["goals"]["assists"] or 0
        minutes = s["games"]["minutes"] or 1
        apps    = s["games"]["appearences"] or 0
        rows.append({
            "#": i + 1,
            "שחקן": p["name"],
            "ליגה": league_name,
            "קבוצה": s["team"]["name"],
            "גיל": p.get("age", "-"),
            "⚽ שערים": goals,
            "🎯 בישולים": assists,
            "🏆 G+A": goals + assists,
            "📊 מ\"ב": apps,
            "⏱️ שערים/90": round(goals / minutes * 90, 2) if minutes > 0 else 0,
        })
    return pd.DataFrame(rows)

def build_assists_df(data, league_name, n):
    rows = []
    for i, entry in enumerate(data[:n]):
        p = entry["player"]
        s = entry["statistics"][0]
        assists = s["goals"]["assists"] or 0
        goals   = s["goals"]["total"]   or 0
        rows.append({
            "#": i + 1,
            "שחקן": p["name"],
            "ליגה": league_name,
            "קבוצה": s["team"]["name"],
            "גיל": p.get("age", "-"),
            "🎯 בישולים": assists,
            "⚽ שערים": goals,
            "🏆 G+A": goals + assists,
            "📊 מ\"ב": s["games"]["appearences"] or 0,
        })
    return pd.DataFrame(rows)

# =============================================
# בדיקת מפתח API
# =============================================

if not API_KEY:
    st.markdown("""
    <div class="main-header">
        <h1>⚽ 5 הליגות הגדולות</h1>
        <p>סטטיסטיקות כדורגל בזמן אמת</p>
    </div>
    """, unsafe_allow_html=True)
    st.warning("⚠️ לא נמצא מפתח API. בצע את השלבים הבאים:")
    with st.expander("📋 הוראות קבלת מפתח API חינמי", expanded=True):
        st.markdown("""
        **שלב 1** – כנס ל-**https://rapidapi.com** והרשם חינם
        **שלב 2** – חפש **"API-Football"** ולחץ Subscribe (חינמי)
        **שלב 3** – העתק את **X-RapidAPI-Key** מתוך Apps
        **שלב 4** – הדבק כאן:
        """)
        key_in = st.text_input("מפתח API:", type="password", placeholder="הדבק כאן...")
        if st.button("💾 שמור"):
            if key_in:
                with open("api_key.txt", "w") as f:
                    f.write(key_in)
                st.success("✅ נשמר! רענן את הדף.")
                st.rerun()
    st.stop()

# =============================================
# כותרת ראשית
# =============================================

now = datetime.now().strftime("%d/%m/%Y %H:%M")
st.markdown(f"""
<div class="main-header">
    <h1>⚽ 5 הליגות הגדולות</h1>
    <p>עדכון אחרון: {now} | עונה 2024/25</p>
</div>
""", unsafe_allow_html=True)

# =============================================
# סרגל צד
# =============================================
with st.sidebar:
    st.markdown("### 🎛️ סינון ובקרה")
    st.markdown("---")
    selected_leagues = st.multiselect(
        "בחר ליגות:",
        list(LEAGUES.keys()),
        default=list(LEAGUES.keys())
    )
    st.markdown("---")
    num_players = st.slider("שחקנים בטבלה:", 5, 25, 10, 5)
    st.markdown("---")
    if st.button("🔄 רענן נתונים", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    st.markdown("""
    <div class="api-info">
        <b>מקור:</b> API-Football<br>
        <b>עונה:</b> 2024/25<br>
        <b>רענון:</b> כל 6 שעות
    </div>
    """, unsafe_allow_html=True)

active_leagues = [l for l in selected_leagues if l in LEAGUES]

# =============================================
# לשוניות
# =============================================

(tab_dash, tab_stand, tab_global, tab_scorers,
 tab_assists, tab_compare, tab_form, tab_records) = st.tabs([
    "📊 דשבורד",
    "🏆 דירוגים",
    "🌍 דירוג כולל",
    "⚽ כובשי שערים",
    "🎯 מבשלים",
    "⚖️ השוואת קבוצות",
    "📅 5 משחקים אחרונים",
    "🏅 שיאים והתראות",
])

# =============================================
# לשונית 1: דשבורד
# =============================================
with tab_dash:
    st.markdown('<div class="section-title">📊 סקירה כללית</div>', unsafe_allow_html=True)
    if not active_leagues:
        st.info("בחר ליגות בסרגל הצד")
    else:
        cols = st.columns(len(active_leagues))
        total_goals, total_matches = 0, 0
        for i, league_name in enumerate(active_leagues):
            with cols[i]:
                with st.spinner("טוען..."):
                    standings = fetch_standings(LEAGUES[league_name]["id"])
                if standings:
                    leader = standings[0]
                    second = standings[1] if len(standings) > 1 else None
                    gap = leader["points"] - second["points"] if second else 0
                    total_goals   += sum(t["all"]["goals"]["for"] for t in standings)
                    total_matches += sum(t["all"]["played"] for t in standings) // 2
                    st.markdown(f"""
                    <div class="league-card">
                        <h3>{league_name}</h3>
                        <div class="leader">🥇 {leader['team']['name']}</div>
                        <div class="points-badge">{leader['points']} נקודות</div>
                        <div class="stat-row">⚽ {leader['all']['played']} משחקים</div>
                        <div class="stat-row">🎯 {leader['all']['goals']['for']} שערים</div>
                        <div class="stat-row">📊 פער מהשני: {gap} נק'</div>
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("---")
        m1, m2, m3, m4 = st.columns(4)
        avg = round(total_goals / total_matches, 2) if total_matches else 0
        with m1: st.metric("⚽ סה\"כ שערים",        f"{total_goals:,}")
        with m2: st.metric("🏟️ סה\"כ משחקים",       f"{total_matches:,}")
        with m3: st.metric("📊 ממוצע שערים/משחק",  avg)
        with m4: st.metric("🏆 ליגות מוצגות",       len(active_leagues))

# =============================================
# לשונית 2: דירוגים (לפי ליגה)
# =============================================
with tab_stand:
    st.markdown('<div class="section-title">🏆 דירוגים לפי ליגה</div>', unsafe_allow_html=True)
    league_sel = st.selectbox("בחר ליגה:", active_leagues, key="stand_sel")
    if league_sel:
        with st.spinner("טוען..."):
            standings = fetch_standings(LEAGUES[league_sel]["id"])
        if standings:
            rows = []
            for team in standings:
                form = team.get("form", "") or ""
                rows.append({
                    "מקום": team["rank"],
                    "קבוצה": team["team"]["name"],
                    "מ": team["all"]["played"],
                    "נ": team["all"]["win"],
                    "ת": team["all"]["draw"],
                    "ה": team["all"]["lose"],
                    "הבקיעו": team["all"]["goals"]["for"],
                    "קיבלו": team["all"]["goals"]["against"],
                    "הפרש": team["goalsDiff"],
                    "נקודות": team["points"],
                    "% הצלחה": round(team["points"] / team["all"]["played"] / 3 * 100, 1) if team["all"]["played"] else 0,
                    "פורמה": form_emoji_only(form),
                })
            df = pd.DataFrame(rows)

            # גרף
            fig = px.bar(df, x="קבוצה", y="נקודות", color="נקודות",
                         color_continuous_scale="Viridis",
                         title=f"{league_sel} – נקודות לפי קבוצה")
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                              paper_bgcolor='rgba(28,35,51,1)',
                              font=dict(color='white'),
                              xaxis_tickangle=-45,
                              coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True)

            # מקרא פורמה
            st.markdown("""
            **מקרא פורמה:** &nbsp;
            🟢 ניצחון &nbsp;&nbsp;
            🟡 תיקו &nbsp;&nbsp;
            🔴 הפסד &nbsp;&nbsp; | &nbsp;&nbsp;
            🔥 בשיא &nbsp; ⬆️ פורמה טובה &nbsp; ↗️ בעלייה &nbsp; ➡️ יציב &nbsp; ↘️ בירידה &nbsp; ⬇️ במשבר
            """)

            # טבלה עם צביעה
            def color_row(row):
                pos = row["מקום"]
                tot = len(df)
                if pos <= 4:
                    return ['background-color: rgba(0,100,255,0.2)'] * len(row)
                elif pos == 5:
                    return ['background-color: rgba(255,140,0,0.2)'] * len(row)
                elif pos >= tot - 2:
                    return ['background-color: rgba(255,50,50,0.2)'] * len(row)
                return [''] * len(row)

            st.dataframe(df.style.apply(color_row, axis=1),
                         use_container_width=True, hide_index=True, height=580)
            st.markdown("""
            🔵 ליגת האלופות &nbsp;&nbsp; 🟠 ליגה האירופית &nbsp;&nbsp; 🔴 הורדה
            """)

# =============================================
# לשונית 3: דירוג כולל (כל הליגות ביחד)
# =============================================
with tab_global:
    st.markdown('<div class="section-title">🌍 דירוג כולל – כל הקבוצות מכל הליגות</div>',
                unsafe_allow_html=True)

    sort_by = st.radio("מיין לפי:", ["נקודות", "% הצלחה (אחוזי הצלחה)"], horizontal=True)

    with st.spinner("טוען כל הליגות..."):
        df_global = build_combined_standings(active_leagues)

    if df_global.empty:
        st.info("אין נתונים")
    else:
        sort_col = "נקודות" if sort_by == "נקודות" else "% הצלחה"
        df_show = df_global.sort_values([sort_col, "הפרש", "הבקיעו"],
                                        ascending=False).reset_index(drop=True)
        df_show.insert(0, "מקום", range(1, len(df_show) + 1))

        # הוצאת עמודות פנימיות
        display_cols = ["מקום", "ליגה", "קבוצה", "מ", "נ", "ת", "ה",
                        "הבקיעו", "קיבלו", "הפרש", "נקודות", "% הצלחה", "פורמה"]
        df_display = df_show[[c for c in display_cols if c in df_show.columns]]

        # פילטר לפי מקום
        top_n = st.slider("הצג TOP:", 10, len(df_display), 30, 5)
        df_display = df_display.head(top_n)

        # צביעה לפי ליגה
        league_colors = {
            "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League": "rgba(61,134,200,0.15)",
            "🇪🇸 La Liga":              "rgba(200,35,58,0.15)",
            "🇮🇹 Serie A":              "rgba(0,106,179,0.15)",
            "🇩🇪 Bundesliga":           "rgba(211,47,47,0.15)",
            "🇫🇷 Ligue 1":              "rgba(13,71,161,0.15)",
        }

        def color_global(row):
            bg = league_colors.get(row["ליגה"], "")
            return [f"background-color: {bg}"] * len(row)

        st.dataframe(df_display.style.apply(color_global, axis=1),
                     use_container_width=True, hide_index=True, height=600)

        # מקרא צבעים
        st.markdown("#### מקרא ליגות")
        leg_cols = st.columns(5)
        colors_hex = {"🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League": "#3d86c8",
                      "🇪🇸 La Liga": "#c8233a",
                      "🇮🇹 Serie A": "#006ab3",
                      "🇩🇪 Bundesliga": "#d32f2f",
                      "🇫🇷 Ligue 1": "#0d47a1"}
        for j, (lname, lcolor) in enumerate(colors_hex.items()):
            if lname in active_leagues:
                with leg_cols[j % 5]:
                    st.markdown(
                        f"<span style='display:inline-block;width:14px;height:14px;"
                        f"background:{lcolor};border-radius:3px;margin-left:6px;'></span>"
                        f" {lname}", unsafe_allow_html=True
                    )

        st.info(
            "💡 **הסבר:** נקודות מושוות ישירות אך כל ליגה שיחקה מספר שונה של משחקים. "
            "השתמש ב-'% הצלחה' לאינדיקציה הוגנת יותר — כמה אחוז מהנקודות האפשריות הקבוצה צברה."
        )

# =============================================
# לשונית 4: כובשי שערים
# =============================================
with tab_scorers:
    st.markdown('<div class="section-title">⚽ כובשי שערים מובילים</div>', unsafe_allow_html=True)
    view_sc = st.radio("תצוגה:", ["🌍 כל הליגות ביחד", "📋 לפי ליגה"], horizontal=True, key="sc_view")

    if view_sc == "🌍 כל הליגות ביחד":
        all_rows = []
        with st.spinner("טוען..."):
            for league_name in active_leagues:
                data = fetch_top_scorers(LEAGUES[league_name]["id"])
                if data:
                    all_rows.append(build_scorers_df(data, league_name, num_players))
        if all_rows:
            df_all = pd.concat(all_rows).sort_values("⚽ שערים", ascending=False).head(num_players)
            df_all.index = range(1, len(df_all) + 1)

            fig = px.bar(df_all.head(15), x="⚽ שערים", y="שחקן", color="ליגה",
                         orientation="h",
                         title="⚽ כובשי השערים המובילים – כל הליגות",
                         color_discrete_map={l: LEAGUES[l]["color"] for l in LEAGUES},
                         hover_data=["קבוצה", "🎯 בישולים"])
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                              paper_bgcolor='rgba(28,35,51,1)',
                              font=dict(color='white'),
                              yaxis=dict(autorange="reversed"), height=500)
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(df_all, use_container_width=True, height=400)
    else:
        cols_sc = st.columns(min(len(active_leagues), 3))
        for i, league_name in enumerate(active_leagues):
            with cols_sc[i % 3]:
                st.markdown(f"#### {league_name}")
                data = fetch_top_scorers(LEAGUES[league_name]["id"])
                if data:
                    df_tmp = build_scorers_df(data, league_name, num_players)
                    st.dataframe(df_tmp[["#","שחקן","קבוצה","⚽ שערים","🎯 בישולים"]],
                                 use_container_width=True, hide_index=True)

# =============================================
# לשונית 5: מבשלים
# =============================================
with tab_assists:
    st.markdown('<div class="section-title">🎯 מבשלים מובילים</div>', unsafe_allow_html=True)
    view_as = st.radio("תצוגה:", ["🌍 כל הליגות ביחד", "📋 לפי ליגה"], horizontal=True, key="as_view")

    if view_as == "🌍 כל הליגות ביחד":
        all_rows = []
        with st.spinner("טוען..."):
            for league_name in active_leagues:
                data = fetch_top_assists(LEAGUES[league_name]["id"])
                if data:
                    all_rows.append(build_assists_df(data, league_name, num_players))
        if all_rows:
            df_all = pd.concat(all_rows).sort_values("🎯 בישולים", ascending=False).head(num_players)
            df_all.index = range(1, len(df_all) + 1)

            fig = px.bar(df_all.head(15), x="🎯 בישולים", y="שחקן", color="ליגה",
                         orientation="h",
                         title="🎯 המבשלים המובילים – כל הליגות",
                         color_discrete_map={l: LEAGUES[l]["color"] for l in LEAGUES},
                         hover_data=["קבוצה", "⚽ שערים", "🏆 G+A"])
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                              paper_bgcolor='rgba(28,35,51,1)',
                              font=dict(color='white'),
                              yaxis=dict(autorange="reversed"), height=500)
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(df_all, use_container_width=True, height=400)
    else:
        cols_as = st.columns(min(len(active_leagues), 3))
        for i, league_name in enumerate(active_leagues):
            with cols_as[i % 3]:
                st.markdown(f"#### {league_name}")
                data = fetch_top_assists(LEAGUES[league_name]["id"])
                if data:
                    df_tmp = build_assists_df(data, league_name, num_players)
                    st.dataframe(df_tmp[["#","שחקן","קבוצה","🎯 בישולים","⚽ שערים","🏆 G+A"]],
                                 use_container_width=True, hide_index=True)

# =============================================
# לשונית 6: השוואת קבוצות
# =============================================
with tab_compare:
    st.markdown('<div class="section-title">⚖️ השוואת קבוצות</div>', unsafe_allow_html=True)

    with st.spinner("טוען רשימת קבוצות..."):
        all_teams = get_all_teams_dict(active_leagues)

    team_names = sorted(all_teams.keys())

    selected_teams = st.multiselect(
        "בחר 2 עד 4 קבוצות להשוואה:",
        team_names,
        max_selections=4,
        placeholder="הקלד שם קבוצה...",
        help="ניתן לבחור קבוצות מליגות שונות"
    )

    if len(selected_teams) < 2:
        st.info("👆 בחר לפחות 2 קבוצות כדי להשוות")
    else:
        # שליפת נתוני הקבוצות מהדירוג
        compare_rows = []
        for league_name in active_leagues:
            standings = fetch_standings(LEAGUES[league_name]["id"])
            for team in standings:
                if team["team"]["name"] in selected_teams:
                    compare_rows.append({
                        "קבוצה": team["team"]["name"],
                        "ליגה": league_name,
                        "מקום בליגה": team["rank"],
                        "משחקים": team["all"]["played"],
                        "ניצחונות": team["all"]["win"],
                        "תיקו": team["all"]["draw"],
                        "הפסדים": team["all"]["lose"],
                        "הבקיעו": team["all"]["goals"]["for"],
                        "קיבלו": team["all"]["goals"]["against"],
                        "הפרש שערים": team["goalsDiff"],
                        "נקודות": team["points"],
                        "% הצלחה": round(team["points"] / team["all"]["played"] / 3 * 100, 1) if team["all"]["played"] else 0,
                        "% ניצחונות": round(team["all"]["win"] / team["all"]["played"] * 100, 1) if team["all"]["played"] else 0,
                    })

        if compare_rows:
            df_cmp = pd.DataFrame(compare_rows)

            # כותרות קבוצות
            team_cols = st.columns(len(selected_teams))
            for i, row in df_cmp.iterrows():
                with team_cols[i]:
                    st.markdown(f"""
                    <div class="compare-header">
                        {row['קבוצה']}<br>
                        <small style="color:#8b949e;">{row['ליגה']}</small>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("---")

            # השוואת מדדים עיקריים
            metrics = [
                ("🏆 נקודות", "נקודות"),
                ("⚽ שערים הבקיעו", "הבקיעו"),
                ("🥅 שערים קיבלו", "קיבלו"),
                ("📊 % הצלחה", "% הצלחה"),
                ("✅ % ניצחונות", "% ניצחונות"),
                ("📍 מקום בליגה", "מקום בליגה"),
            ]

            for metric_label, col_name in metrics:
                mcols = st.columns([2] + [1] * len(selected_teams))
                with mcols[0]:
                    st.markdown(f"**{metric_label}**")
                values = [df_cmp[df_cmp["קבוצה"] == t][col_name].values[0]
                          if t in df_cmp["קבוצה"].values else "-"
                          for t in selected_teams]
                for j, val in enumerate(values):
                    with mcols[j + 1]:
                        # הדגשת הערך הגבוה (למעט מקום בליגה - שם נמוך=טוב)
                        try:
                            numeric_vals = [float(v) for v in values if v != "-"]
                            if numeric_vals:
                                best = min(numeric_vals) if col_name == "מקום בליגה" else max(numeric_vals)
                                is_best = float(val) == best
                            else:
                                is_best = False
                        except:
                            is_best = False

                        color = "#00ff88" if is_best else "white"
                        st.markdown(f"<div style='text-align:center; color:{color}; font-size:1.1rem; font-weight:700;'>{val}</div>",
                                    unsafe_allow_html=True)
                st.markdown("---")

            # גרף מכ"ם (Radar)
            st.markdown("#### 📡 גרף השוואתי (מכ\"ם)")
            categories = ["נקודות", "הבקיעו", "% הצלחה", "% ניצחונות"]

            fig_radar = go.Figure()
            colors_team = ["#00ff88", "#00aaff", "#ff6644", "#ffaa00"]

            for idx, team_name in enumerate(selected_teams):
                team_row = df_cmp[df_cmp["קבוצה"] == team_name]
                if team_row.empty:
                    continue
                r_vals = [float(team_row[c].values[0]) for c in categories]

                fig_radar.add_trace(go.Scatterpolar(
                    r=r_vals,
                    theta=categories,
                    fill='toself',
                    name=team_name,
                    line_color=colors_team[idx % len(colors_team)],
                    fillcolor=colors_team[idx % len(colors_team)].replace("ff", "33") if "#" in colors_team[idx] else colors_team[idx],
                    opacity=0.7
                ))

            fig_radar.update_layout(
                polar=dict(
                    bgcolor='rgba(28,35,51,1)',
                    radialaxis=dict(visible=True, color='white'),
                    angularaxis=dict(color='white')
                ),
                paper_bgcolor='rgba(28,35,51,1)',
                font=dict(color='white'),
                legend=dict(font=dict(color='white')),
                height=420
            )
            st.plotly_chart(fig_radar, use_container_width=True)

            # טבלה מלאה
            st.markdown("#### 📋 טבלה מלאה")
            st.dataframe(df_cmp.set_index("קבוצה"), use_container_width=True)

# =============================================
# לשונית 7: 5 משחקים אחרונים + פורמה
# =============================================
with tab_form:
    st.markdown('<div class="section-title">📅 5 משחקים אחרונים ופורמה</div>', unsafe_allow_html=True)

    # הסבר על פורמה
    with st.expander("❓ מה זה פורמה אחרונה?", expanded=False):
        st.markdown("""
        **פורמה** = תוצאות 5 המשחקים האחרונים של הקבוצה, מוצגות כרצף של תוצאות:

        | סמל | צבע | משמעות |
        |-----|-----|--------|
        | **נ** | 🟢 ירוק | ניצחון |
        | **ת** | 🟡 צהוב | תיקו |
        | **ה** | 🔴 אדום | הפסד |

        **דוגמה:** `נ נ ת ה נ` = ניצחו, ניצחו, תיקו, הפסידו, ניצחו (האחרון מימין)

        קבוצה עם פורמה `נ נ נ נ נ` = חמישה ניצחונות ברצף = "בשיא כושר"
        קבוצה עם פורמה `ה ה ה ה ה` = חמישה הפסדות ברצף = "במשבר"
        """)

    # בחירת קבוצה
    with st.spinner("טוען קבוצות..."):
        all_teams_form = get_all_teams_dict(active_leagues)

    team_for_form = st.selectbox(
        "בחר קבוצה:",
        sorted(all_teams_form.keys()),
        key="form_team",
        placeholder="הקלד שם קבוצה..."
    )

    if team_for_form:
        team_data = all_teams_form[team_for_form]
        team_id   = team_data["id"]
        team_league = team_data["league"]

        # פורמה מהדירוג
        standings = fetch_standings(LEAGUES[team_league]["id"])
        form_str = ""
        team_rank = None
        team_points = None

        for t in standings:
            if t["team"]["name"] == team_for_form:
                form_str   = t.get("form", "") or ""
                team_rank  = t["rank"]
                team_points = t["points"]
                break

        # הצגת פורמה
        col_info, col_form = st.columns([1, 2])
        with col_info:
            st.metric("מקום בליגה", f"#{team_rank}")
            st.metric("נקודות",     team_points)
            st.markdown(f"**ליגה:** {team_league}")

        with col_form:
            st.markdown("#### הפורמה האחרונה (5 משחקים):")
            if form_str:
                circles, trend, label = format_form(form_str)
                wins   = form_str[-5:].count("W")
                draws  = form_str[-5:].count("D")
                losses = form_str[-5:].count("L")

                # הצגה ציורית גדולה
                st.markdown(f"""
                <div style="
                    background: #1c2333;
                    border-radius: 16px;
                    padding: 24px 30px;
                    margin: 10px 0;
                    border: 1px solid #30363d;
                    text-align: center;
                ">
                    <div style="font-size: 2rem; letter-spacing: 8px; margin-bottom: 14px;">
                        {circles}
                    </div>
                    <div style="font-size: 3rem; margin-bottom: 8px;">{trend}</div>
                    <div style="
                        color: #00ff88;
                        font-size: 1.3rem;
                        font-weight: 700;
                        margin-bottom: 14px;
                    ">{label}</div>
                    <div style="color: #8b949e; font-size: 0.9rem;">
                        🟢 {wins} ניצחונות &nbsp;&nbsp;
                        🟡 {draws} תיקו &nbsp;&nbsp;
                        🔴 {losses} הפסדות
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # מקרא
                st.markdown("""
                <div style="color:#8b949e; font-size:0.8rem; margin-top:8px;">
                🟢 ניצחון &nbsp; 🟡 תיקו &nbsp; 🔴 הפסד &nbsp;|&nbsp;
                🔥 בשיא &nbsp; ⬆️ פורמה טובה &nbsp; ↗️ בעלייה &nbsp; ➡️ יציב &nbsp; ↘️ בירידה &nbsp; ⬇️ במשבר
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("אין נתוני פורמה")

        st.markdown("---")
        st.markdown(f"#### 📋 5 המשחקים האחרונים של {team_for_form}")

        with st.spinner("טוען משחקים..."):
            matches = fetch_team_matches(team_id, last=5)

        if matches:
            for match in reversed(matches):  # מהאחרון לראשון
                fixture  = match["fixture"]
                home     = match["teams"]["home"]
                away     = match["teams"]["away"]
                goals_h  = match["goals"]["home"]
                goals_a  = match["goals"]["away"]
                date_str = fixture["date"][:10]

                # קביעת תוצאה מנקודת מבט הקבוצה שנבחרה
                is_home = home["name"] == team_for_form
                our_goals = goals_h if is_home else goals_a
                opp_goals = goals_a if is_home else goals_h
                opponent  = away["name"] if is_home else home["name"]
                location  = "🏠 בית" if is_home else "✈️ חוץ"

                if goals_h is None or goals_a is None:
                    result_label = "⏳ טרם שוחק"
                    result_color = "#8b949e"
                elif our_goals > opp_goals:
                    result_label = "✅ ניצחון"
                    result_color = "#00aa44"
                elif our_goals == opp_goals:
                    result_label = "➖ תיקו"
                    result_color = "#aa8800"
                else:
                    result_label = "❌ הפסד"
                    result_color = "#aa2200"

                score = f"{goals_h} – {goals_a}" if goals_h is not None else "vs"

                st.markdown(f"""
                <div style="
                    background: #1c2333;
                    border: 1px solid #30363d;
                    border-right: 4px solid {result_color};
                    border-radius: 12px;
                    padding: 14px 20px;
                    margin: 8px 0;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                ">
                    <div>
                        <span style="color:#8b949e; font-size:0.85rem;">{date_str} | {location}</span><br>
                        <span style="color:white; font-weight:600; font-size:1rem;">
                            {home['name']} <span style="color:#00ff88;">{score}</span> {away['name']}
                        </span>
                    </div>
                    <div style="color:{result_color}; font-weight:700; font-size:1rem;">
                        {result_label}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("לא נמצאו משחקים אחרונים")

# =============================================
# לשונית 8: שיאים והתראות
# =============================================
with tab_records:
    st.markdown('<div class="section-title">🏅 שיאים והתראות עונה 2024/25</div>', unsafe_allow_html=True)

    st.info("🔔 המערכת מזהה שחקנים הקרובים לאבני דרך ושיאים חשובים בעונה הנוכחית")

    # ─────────────── טעינת כל נתוני הכובשים ───────────────
    all_scorers_data = []
    all_assists_data = []

    with st.spinner("טוען נתוני שחקנים..."):
        for league_name in active_leagues:
            sc = fetch_top_scorers(LEAGUES[league_name]["id"])
            if sc:
                df_tmp = build_scorers_df(sc, league_name, 20)
                all_scorers_data.append(df_tmp)

            ass = fetch_top_assists(LEAGUES[league_name]["id"])
            if ass:
                df_tmp2 = build_assists_df(ass, league_name, 20)
                all_assists_data.append(df_tmp2)

    if all_scorers_data and all_assists_data:
        df_sc_all  = pd.concat(all_scorers_data).sort_values("⚽ שערים", ascending=False)
        df_ass_all = pd.concat(all_assists_data).sort_values("🎯 בישולים", ascending=False)

        # ─── 1. שיא הכובשים בעונה לפי ליגה ─────────────────────
        st.markdown("### 📊 שיא הכובשים בעונה – כמה רחוק מהשיא ההיסטורי?")

        rec_cols = st.columns(len(active_leagues))
        for i, league_name in enumerate(active_leagues):
            with rec_cols[i % len(active_leagues)]:
                rec = SEASON_RECORDS.get(league_name)
                if not rec:
                    continue
                league_scorers = df_sc_all[df_sc_all["ליגה"] == league_name]
                if league_scorers.empty:
                    continue

                top_this = league_scorers.iloc[0]
                current_goals = int(top_this["⚽ שערים"])
                record_goals  = rec["goals"]
                pct = min(current_goals / record_goals, 1.0)
                gap = record_goals - current_goals

                st.markdown(f"**{league_name}**")
                st.markdown(f"""
                <div class="record-card">
                    <div class="record-title">🏅 שיא הליגה: {record_goals} שערים</div>
                    <div class="record-body">
                        מחזיק: {rec['holder']} ({rec['season']})<br>
                        <b>מוביל עכשיו:</b> {top_this['שחקן']} – {current_goals} שערים<br>
                        <b>פער:</b> {gap} שערים מהשיא
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.progress(pct, text=f"{int(pct*100)}% מהשיא")

        st.markdown("---")

        # ─── 2. התראות – קרוב לאבן דרך ───────────────────────
        st.markdown("### 🔔 שחקנים קרובים לאבני דרך")

        milestones_goals   = [5, 10, 15, 20, 25, 30, 35, 40, 50]
        milestones_assists = [5, 10, 15, 20]

        alerts = []

        for _, row in df_sc_all.iterrows():
            g = int(row["⚽ שערים"])
            a = int(row["🎯 בישולים"])
            for milestone in milestones_goals:
                if 0 < milestone - g <= 3 and g > 0:
                    alerts.append({
                        "type": "goals",
                        "player": row["שחקן"],
                        "league": row["ליגה"],
                        "team": row["קבוצה"],
                        "current": g,
                        "target": milestone,
                        "gap": milestone - g,
                        "label": f"⚽ {milestone} שערים בעונה"
                    })
                    break
            for milestone in milestones_assists:
                if 0 < milestone - a <= 2 and a > 0:
                    alerts.append({
                        "type": "assists",
                        "player": row["שחקן"],
                        "league": row["ליגה"],
                        "team": row["קבוצה"],
                        "current": a,
                        "target": milestone,
                        "gap": milestone - a,
                        "label": f"🎯 {milestone} בישולים בעונה"
                    })
                    break

        if alerts:
            for alert in alerts[:12]:  # מקסימום 12 התראות
                gap_word = "בישול אחד" if alert["gap"] == 1 else f"{alert['gap']} שערים" if alert["type"] == "goals" else f"{alert['gap']} בישולים"
                st.markdown(f"""
                <div class="alert-card">
                    <div class="alert-title">🔔 {alert['player']} – {alert['label']}</div>
                    <div class="alert-body">
                        {alert['team']} | {alert['league']}<br>
                        כרגע: <b>{alert['current']}</b> &nbsp;→&nbsp;
                        יעד: <b>{alert['target']}</b> &nbsp;|&nbsp;
                        <span class="alert-progress">חסר: {gap_word} בלבד!</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("אין שחקנים קרובים לאבני דרך כרגע")

        st.markdown("---")

        # ─── 3. מספרי שיא עונה ───────────────────────────────
        st.markdown("### 🥇 מובילי העונה 2024/25 עד כה")

        top_scorer  = df_sc_all.iloc[0] if not df_sc_all.empty else None
        top_assister = df_ass_all.iloc[0] if not df_ass_all.empty else None

        top_ga = df_sc_all.copy()
        top_ga["G+A"] = top_ga["⚽ שערים"] + top_ga["🎯 בישולים"]
        top_ga = top_ga.sort_values("G+A", ascending=False)
        top_ga_player = top_ga.iloc[0] if not top_ga.empty else None

        s1, s2, s3 = st.columns(3)

        if top_scorer is not None:
            with s1:
                st.markdown(f"""
                <div class="league-card">
                    <h3>👑 כובש השערים המוביל</h3>
                    <div class="leader">{top_scorer['שחקן']}</div>
                    <div class="stat-row">{top_scorer['קבוצה']}</div>
                    <div class="stat-row">{top_scorer['ליגה']}</div>
                    <div class="points-badge">⚽ {int(top_scorer['⚽ שערים'])}</div>
                </div>
                """, unsafe_allow_html=True)

        if top_assister is not None:
            with s2:
                st.markdown(f"""
                <div class="league-card">
                    <h3>🎩 המבשל המוביל</h3>
                    <div class="leader">{top_assister['שחקן']}</div>
                    <div class="stat-row">{top_assister['קבוצה']}</div>
                    <div class="stat-row">{top_assister['ליגה']}</div>
                    <div class="points-badge">🎯 {int(top_assister['🎯 בישולים'])}</div>
                </div>
                """, unsafe_allow_html=True)

        if top_ga_player is not None:
            with s3:
                st.markdown(f"""
                <div class="league-card">
                    <h3>⚡ מוביל G+A (שערים+בישולים)</h3>
                    <div class="leader">{top_ga_player['שחקן']}</div>
                    <div class="stat-row">{top_ga_player['קבוצה']}</div>
                    <div class="stat-row">{top_ga_player['ליגה']}</div>
                    <div class="points-badge">🏆 {int(top_ga_player['G+A'])}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")

        # ─── 4. כובשי שערים לפי גיל ──────────────────────────
        st.markdown("### 🧒 כובשים הצעירים ביותר (עד גיל 23)")

        young = df_sc_all.copy()
        young["גיל_מספר"] = pd.to_numeric(young["גיל"], errors="coerce")
        young = young[young["גיל_מספר"] <= 23].sort_values("⚽ שערים", ascending=False).head(10)

        if not young.empty:
            fig_young = px.bar(
                young,
                x="שחקן",
                y="⚽ שערים",
                color="ליגה",
                hover_data=["קבוצה", "גיל"],
                title="🧒 כובשים הצעירים ביותר בליגות – עד גיל 23",
                color_discrete_map={l: LEAGUES[l]["color"] for l in LEAGUES},
                text="⚽ שערים"
            )
            fig_young.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(28,35,51,1)',
                font=dict(color='white'),
                xaxis_tickangle=-30,
                height=400
            )
            st.plotly_chart(fig_young, use_container_width=True)
            st.dataframe(young[["שחקן","גיל","קבוצה","ליגה","⚽ שערים","🎯 בישולים","🏆 G+A"]],
                         use_container_width=True, hide_index=True)
        else:
            st.info("אין שחקנים צעירים עם שערים בנתונים הזמינים")
