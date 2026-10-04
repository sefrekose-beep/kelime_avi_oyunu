import streamlit as st
import random

st.set_page_config(page_title="Kelime Avı", page_icon="🕹️", layout="centered")

# --- 1. ÖZEL STİL (DAHA ÖZGÜN ARAYÜZ) ---
st.markdown("""
<style>
    .word-card {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        color: #f8fafc;
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
        margin-bottom: 20px;
    }
    .word-display {
        font-family: 'Courier New', monospace;
        font-size: 2.2rem;
        letter-spacing: 8px;
        font-weight: 700;
        color: #38bdf8;
    }
    .clue-tag {
        display: inline-block;
        background-color: #334155;
        color: #cbd5e1;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. BİRLEŞİK KELİME VE İPUCU HAVUZU ---
TUM_KELIMELER = [
    # Kimya & Fen
    ("ATOM", "Kimya & Fen"),
    ("MOLEKÜL", "Kimya & Fen"),
    ("REAKTÖR", "Kimya & Fen"),
    ("KATALİZÖR", "Kimya & Fen"),
    ("ÇÖZELTİ", "Kimya & Fen"),
    ("BASINÇ", "Kimya & Fen"),
    ("ENERJİ", "Kimya & Fen"),
    # Şehirler
    ("İSTANBUL", "Coğrafya & Şehir"),
    ("ANKARA", "Coğrafya & Şehir"),
    ("İZMİR", "Coğrafya & Şehir"),
    ("KOCAELİ", "Coğrafya & Şehir"),
    ("ELAZIĞ", "Coğrafya & Şehir"),
    ("BURSA", "Coğrafya & Şehir"),
    # Yiyecek & Meyve
    ("ŞEFTALİ", "Meyve"),
    ("MANDALİNA", "Meyve"),
    ("PORTAKAL", "Meyve"),
    ("KARPUZ", "Meyve"),
    ("KESTANE", "Atıştırmalık"),
    # Kültür & Teknoloji
    ("PUSULA", "Keşif & Alet"),
    ("TEKNOLOJİ", "Bilişim"),
    ("YAZILIM", "Bilişim"),
    ("GEZEGEN", "Uzay & Astronomi"),
    ("ROBOT", "Mühendislik"),
    ("FELSEFE", "Sosyal Bilim"),
]

# --- 3. OYUN BAŞLATMA ---
def yeni_oyun():
    secim = random.choice(TUM_KELIMELER)
    st.session_state.gizli_kelime = secim[0]
    st.session_state.ipucu = secim[1]
    st.session_state.tahminler = []
    st.session_state.kalan_can = 6
    st.session_state.durum = "oyun"  # "oyun", "kazandi", "kaybetti"

if "gizli_kelime" not in st.session_state:
    yeni_oyun()

# --- 4. CAN VE KELİME KARTI ---
kalpler = "❤️ " * st.session_state.kalan_can + "🖤 " * (6 - st.session_state.kalan_can)

# Görünecek harfleri hazırla
gorunen_kelime = ""
tamamlandi = True
for h in st.session_state.gizli_kelime:
    if h in st.session_state.tahminler:
        gorunen_kelime += f"{h} "
    else:
        gorunen_kelime += "_ "
        tamamlandi = False

st.markdown(f"""
<div class="word-card">
    <div class="clue-tag">💡 İpucu: {st.session_state.ipucu}</div>
    <div style="font-size: 1.2rem; margin-bottom: 15px;">{kalpler}</div>
    <div class="word-display">{gorunen_kelime.strip()}</div>
</div>
""", unsafe_allow_html=True)

# Kazanma / Kaybetme Tespiti
if tamamlandi and st.session_state.durum == "oyun":
    st.session_state.durum = "kazandi"
elif st.session_state.kalan_can <= 0 and st.session_state.durum == "oyun":
    st.session_state.durum = "kaybetti"

# --- 5. OYUN İÇİ ETKİLEŞİM ---
if st.session_state.durum == "oyun":
    sekme1, sekme2 = st.tabs(["⌨️ Harf Tablası", "🎯 Direkt Tahmin"])

    # SEKME 1: BUTONLU KLAVYE
    with sekme1:
        alfabe = [
            "A", "B", "C", "Ç", "D", "E", "F", "G", "Ğ", "H", "I", "İ", 
            "J", "K", "L", "M", "N", "O", "Ö", "P", "R", "S", "Ş", "T", 
            "U", "Ü", "V", "Y", "Z"
        ]
        
        # Harfleri 6 sütunluk grid düzenine bölelim
        cols = st.columns(6)
        for i, harf in enumerate(alfabe):
            with cols[i % 6]:
                kullanildi = harf in st.session_state.tahminler
                if st.button(harf, key=f"btn_{harf}", disabled=kullanildi, use_container_width=True):
                    st.session_state.tahminler.append(harf)
                    if harf not in st.session_state.gizli_kelime:
                        st.session_state.kalan_can -= 1
                    st.rerun()

    # SEKME 2: KELİME ÇÖZÜCÜ
    with sekme2:
        with st.form("direkt_tahmin", clear_on_submit=True):
            tahmin_input = st.text_input("Aklındaki kelimeyi yaz:").strip().upper()
            gonder = st.form_submit_button("Kelimeyi Kilitle 🔓", use_container_width=True)

        if gonder and tahmin_input:
            if tahmin_input == st.session_state.gizli_kelime:
                st.session_state.durum = "kazandi"
                st.rerun()
            else:
                st.session_state.kalan_can -= 2
                st.toast(f"'{tahmin_input}' yanlış! 2 can kaybettin.", icon="⚠️")
                st.rerun()

# --- 6. OYUN SONU EKRANI ---
if st.session_state.durum == "kazandi":
    st.balloons()
    st.success(f"🏆 Harika iş! Kelimeyi çözdün: **{st.session_state.gizli_kelime}**")
elif st.session_state.durum == "kaybetti":
    st.error(f"💀 Maalesef kaybettin! Doğru kelime: **{st.session_state.gizli_kelime}**")

if st.session_state.durum != "oyun":
    if st.button("Sıradaki Kelimeye Geç ⏭️", use_container_width=True):
        yeni_oyun()
        st.rerun()