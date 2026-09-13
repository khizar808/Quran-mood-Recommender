"""
🕌 Quran Verse Recommender by Mood
"""

import streamlit as st
import streamlit.components.v1 as components
from recommender import recommend_by_mood, get_mood_options

st.set_page_config(page_title="Quran Mood Recommender", page_icon="🕌",
                   layout="centered", initial_sidebar_state="collapsed")

# ── Audio ──────────────────────────────────────────────────────────────────────
def get_audio_html(surah_number, ayah):
    ayah_str = str(ayah).strip()
    if "-" in ayah_str:
        ayah_str = ayah_str.split("-")[0].strip()
    url = f"https://everyayah.com/data/Alafasy_128kbps/{str(surah_number).zfill(3)}{ayah_str.zfill(3)}.mp3"
    return f'<audio controls style="width:100%;margin-top:10px;border-radius:8px;accent-color:#c9a84c;"><source src="{url}" type="audio/mpeg"></audio>'

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Lora:wght@400;500;600&family=Inter:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: linear-gradient(160deg, #0f1923 0%, #1a2a1a 50%, #0f1923 100%); min-height: 100vh; }
.header-container { text-align: center; padding: 2.5rem 1rem 1rem; }
.app-title { font-family: 'Amiri', serif; font-size: 2.8rem; margin: 0; letter-spacing: 2px; }
.title-bg { background:#1a3a6b; -webkit-text-fill-color:#f5c842; padding:0.2rem 0.8rem; border-radius:8px; }
.app-subtitle { font-family:'Lora',serif; font-size:1.05rem; color:#b8d4b8; margin-top:0.3rem; font-style:italic; }
.bismillah {
    font-family:'Amiri',serif; font-size:1.9rem;
    background:linear-gradient(90deg,#f5c842,#ffe066,#f5c842); background-size:200% auto;
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
    animation:shimmer 6s linear infinite; text-align:center; margin:0.5rem 0 2rem;
}
@keyframes shimmer { 0%{background-position:0% center} 100%{background-position:300% center} }
.gold-divider {
    height:1px; background:linear-gradient(to right,transparent,#f5c842aa,transparent);
    margin:1.5rem 0; border:none; box-shadow:0 0 8px rgba(245,200,66,0.25);
}
.section-label { font-family:'Lora',serif; font-size:1.1rem; color:#c8e6c8; text-align:center; margin-bottom:1rem; font-weight:500; }
div.stButton > button {
    background:rgba(245,200,66,0.1)!important; border:1px solid rgba(245,200,66,0.45)!important;
    color:#ffe57a!important; border-radius:50px!important; font-size:0.88rem!important;
    padding:0.5rem 1.2rem!important; transition:all 0.25s!important; width:100%!important;
}
div.stButton > button:hover {
    background:rgba(245,200,66,0.25)!important; border-color:#f5c842!important;
    color:#fff!important; transform:translateY(-2px)!important; box-shadow:0 6px 24px rgba(245,200,66,0.3)!important;
}
.verse-card {
    background:linear-gradient(135deg,rgba(245,200,66,0.08),rgba(138,200,138,0.05));
    border:1px solid rgba(245,200,66,0.3); border-left:3px solid #f5c842;
    border-radius:12px; padding:1.5rem 1.8rem; margin:1rem 0;
    box-shadow:0 4px 24px rgba(245,200,66,0.08); transition:transform 0.2s,box-shadow 0.2s;
}
.verse-card:hover { transform:translateY(-2px); box-shadow:0 8px 32px rgba(245,200,66,0.18); }
.verse-surah { font-family:'Lora',serif; font-size:0.8rem; color:#f5c842; text-transform:uppercase; letter-spacing:2px; margin-bottom:0.8rem; font-weight:600; }
.verse-arabic { font-family:'Amiri',serif; font-size:1.7rem; color:#fff8e1; text-align:right; direction:rtl; line-height:2; margin-bottom:1rem; border-bottom:1px solid rgba(245,200,66,0.2); padding-bottom:1rem; }
.verse-english { font-family:'Lora',serif; font-size:1.05rem; color:#eedfa8; font-style:italic; line-height:1.7; margin-bottom:0.6rem; }
.verse-urdu { font-size:1.0rem; color:#a8d5a8; direction:rtl; text-align:right; line-height:1.9; margin-bottom:1rem; }
.verse-reflection { background:rgba(138,200,138,0.1); border-radius:8px; padding:0.8rem 1rem; font-size:0.88rem; color:#a8d5a8; line-height:1.6; border-left:2px solid rgba(138,200,138,0.5); }
.verse-reflection::before { content:"💚 Reflection: "; font-weight:600; color:#7ecf7e; }
.result-header { text-align:center; font-family:'Lora',serif; font-size:1.2rem; color:#f5c842; margin:2rem 0 1rem; font-style:italic; }
.badge { display:inline-block; background:rgba(245,200,66,0.2); color:#f5c842; padding:0.15rem 0.6rem; border-radius:20px; font-size:0.75rem; border:1px solid rgba(245,200,66,0.5); margin-left:0.5rem; }
.footer { text-align:center; color:#a0b8a0; font-size:0.78rem; margin-top:3rem; padding-bottom:2rem; }
#MainMenu{visibility:hidden;} footer{visibility:hidden;} header{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-container">
    <div class="bismillah">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</div>
    <h1 class="app-title"><span class="title-bg">🕌 Quran Verse Recommender</span></h1>
    <p class="app-subtitle">Find peace in Allah's words — based on how you feel today</p>
</div>
<div class="gold-divider"></div>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
for k, v in {"results": [], "selected_mood": ""}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Mood buttons ───────────────────────────────────────────────────────────────
st.markdown('<p class="section-label">How are you feeling right now?</p>', unsafe_allow_html=True)
mood_options = get_mood_options()
for row in [mood_options[i:i+3] for i in range(0, len(mood_options), 3)]:
    cols = st.columns(len(row))
    for col, mood in zip(cols, row):
        with col:
            if st.button(mood, key=f"btn_{mood}"):
                st.session_state.selected_mood = mood
                st.session_state.results = recommend_by_mood(mood, top_n=4)

# ── Results ────────────────────────────────────────────────────────────────────
if st.session_state.results:
    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
    st.markdown(f'<p class="result-header">Verses for {st.session_state.selected_mood}</p>', unsafe_allow_html=True)

    for i, verse in enumerate(st.session_state.results, 1):
        st.markdown(f"""
        <div class="verse-card">
            <div class="verse-surah">Surah {verse['surah_name']} &nbsp;·&nbsp; Ayah {verse['ayah']} <span class="badge">#{i}</span></div>
            <div class="verse-arabic">{verse['arabic']}</div>
            <div class="verse-english">"{verse['english']}"</div>
            <div class="verse-urdu">{verse['urdu']}</div>
            <div class="verse-reflection">{verse['reflection']}</div>
        </div>
        """, unsafe_allow_html=True)
        components.html(get_audio_html(verse['surah_number'], verse['ayah']), height=72)

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
    _, col2, _ = st.columns([1, 1, 1])
    with col2:
        if st.button("🔄 Search Again", use_container_width=True):
            st.session_state.results = []
            st.session_state.selected_mood = ""
            st.rerun()

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <p style="font-family:'Amiri',serif;font-size:1.1rem;color:#f5c842;text-shadow:0 0 12px rgba(245,200,66,0.35);">
        وَنُنَزِّلُ مِنَ الْقُرْآنِ مَا هُوَ شِفَاءٌ وَرَحْمَةٌ
    </p>
    <p style="font-size:0.75rem;color:#c8dfc8;margin-top:0.2rem;">
        "And We send down from the Quran that which is healing and mercy." — Al-Isra 17:82
    </p>
</div>
""", unsafe_allow_html=True)