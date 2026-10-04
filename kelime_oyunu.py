import streamlit as st
import random

st.set_page_config(page_title="Adam Asmaca", page_icon="🕹️", layout="centered")

# --- 1. STİL AYARLARI ---
st.markdown("""
<style>
    .game-card {
        background-color: #0f172a;
        border: 2px solid #3b82f6;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
    }
    .word-text {
        font-family: monospace;
        font-size: 2.2rem;
        letter-spacing: 10px;
        font-weight: bold;
        color: #38bdf8;
        margin: 12px 0;
    }
    .badge-ok {
        background-color: #059669;
        color: white;
        padding: 4px 10px;
        margin: 2px;
        border-radius: 6px;
        font-weight: bold;
        display: inline-block;
    }
    .badge-no {
        background-color: #4b5563;
        color: #d1d5db;
        padding: 4px 10px;
        margin: 2px;
        border-radius: 6px;
        font-weight: bold;
        text-decoration: line-through;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. HATA VERMEYEN DİNAMİK SVG ÇİZİMİ ---
def cizim_svg(can):
    parcalar = []
    # Temel Direk ve Darağacı
    parcalar.append('<line x1="20" y1="230" x2="100" y2="230" stroke="#94a3b8" stroke-width="5" stroke-linecap="round"/>')
    parcalar.append('<line x1="50" y1="230" x2="50" y2="20" stroke="#94a3b8" stroke-width="5"/>')
    parcalar.append('<line x1="50" y1="20" x2="150" y2="20" stroke="#94a3b8" stroke-width="5"/>')
    parcalar.append('<line x1="50" y1="60" x2="90" y2="20" stroke="#94a3b8" stroke-width="4"/>')
    parcalar.append('<line x1="150" y1="20" x2="150" y2="60" stroke="#cbd5e1" stroke-width="3" stroke-dasharray="2,2"/>')

    # Can azaldıkça eklenen vücut parçaları
    if can <= 5: # Kafa
        parcalar.append('<circle cx="150" cy="80" r="20" stroke="#f87171" stroke-width="4" fill="none"/>')
    if can <= 4: # Gövde
        parcalar.append('<line x1="150" y1="100" x2="150" y2="160" stroke="#f87171" stroke-width="4"/>')
    if can <= 3: # Sol Kol
        parcalar.append('<line x1="150" y1="115" x2="120" y2="145" stroke="#f87171" stroke-width="4" stroke-linecap="round"/>')
    if can <= 2: # Sağ Kol
        parcalar.append('<line x1="150" y1="115" x2="180" y2="145" stroke="#f87171" stroke-width="4" stroke-linecap="round"/>')
    if can <= 1: # Sol Bacak
        parcalar.append('<line x1="150" y1="160" x2="125" y2="210" stroke="#f87171" stroke-width="4" stroke-linecap="round"/>')
    if can <= 0: # Sağ Bacak
        parcalar.append('<line x1="150" y1="160" x2="175" y2="210" stroke="#f87171" stroke-width="4" stroke-linecap="round"/>')

    svg_govde = "".join(parcalar)
    return f'<div style="display:flex; justify-content:center;"><svg width="200" height="240" viewBox="0 0 200 240">{svg_govde}</svg></div>'

# --- 3. KELİME LİSTESİ ---
TUM_KELIMELER = [
    ("ATOM", "Kimya & Fizik"),
    ("MOLEKÜL", "Kimya & Biyoloji"),
    ("REAKTÖR", "Kimya Mühendisliği"),
    ("KATALİZÖR", "Tepkime Hızlandırıcı"),
    ("ÇÖZELTİ", "Homojen Karışım"),
    ("İSTANBUL", "Boğazı Olan Şehir"),
    ("ANKARA", "Başkent"),
    ("İZMİR", "Ege Bölgesi"),
    ("KOCAELİ", "Sanayi Şehri"),
    ("ELAZIĞ", "Doğu Anadolu"),
    ("PORTAKAL", "Kış Meyvesi"),
    ("PUSULA", "Yön Gösterici"),
    ("YAZILIM", "Kod Dünyası"),
    ("GEZEGEN", "Gök Cismi")
]

# --- 4. OYUN KURULUMU ---
def yeni_oyun():
    secilen = random.choice(TUM_KELIMELER)
    st.session_state.gizli_kelime = secilen[0]
    st.session_state.ipucu = secilen[1]
    st.session_state.tahminler = []
    st.session_state.kalan_can = 6
    st.session_state.durum = "oyun"

if "gizli_kelime" not in st.session_state:
    yeni_oyun()

# --- 5. GÖRSEL ÇİZİM VE KART ---
st.markdown(cizim_svg(st.session_state.kalan_can), unsafe_allow_html=True)

# Çizgileri ve harfleri hazırla
gorunen = ""
kazandi_mi = True
for h in st.session_state.gizli_kelime:
    if h in st.session_state.tahminler:
        gorunen += f"{h} "
    else:
        gorunen += "_ "
        kazandi_mi = False

kalpler = "❤️ " * st.session_state.kalan_can + "🖤 " * (6 - st.session_state.kalan_can)

st.markdown(f"""
<div class="game-card">
    <div style="color: #93c5fd; font-size: 0.95rem;">💡 <b>İpucu:</b> {st.session_state.ipucu}</div>
    <div style="font-size: 1.1rem; margin: 8px 0;">{kalpler}</div>
    <div class="word-text">{gorunen.strip()}</div>
</div>
""", unsafe_allow_html=True)

# Kazanma ve Kaybetme Kontrolü
if kazandi_mi and st.session_state.durum == "oyun":
    st.session_state.durum = "kazandi"
elif st.session_state.kalan_can <= 0 and st.session_state.durum == "oyun":
    st.session_state.durum = "kaybetti"

# --- 6. GİRİŞ VE TAHMİN ALANI ---
if st.session_state.durum == "oyun":
    with st.form("tahmin_formu", clear_on_submit=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            giris = st.text_input("Harf veya Kelime", placeholder="Harf veya tüm kelimeyi yaz...", label_visibility="collapsed")
        with col2:
            buton = st.form_submit_button("Tahmin Et 🚀", use_container_width=True)

    if buton and giris:
        # Türkçe karakterleri büyüterek alalım
        giris_temiz = giris.strip().replace("i", "İ").replace("ı", "I").upper()

        # Tek harf girildiyse
        if len(giris_temiz) == 1:
            if giris_temiz in st.session_state.tahminler:
                st.toast(f"'{giris_temiz}' zaten denendi!", icon="⚠️")
            else:
                st.session_state.tahminler.append(giris_temiz)
                if giris_temiz not in st.session_state.gizli_kelime:
                    st.session_state.kalan_can -= 1
                    st.toast(f"'{giris_temiz}' harfi yok!", icon="❌")
                else:
                    st.toast(f"'{giris_temiz}' harfi doğru!", icon="✅")
                st.rerun()

        # Tüm kelime girildiyse
        else:
            if giris_temiz == st.session_state.gizli_kelime:
                st.session_state.durum = "kazandi"
                st.rerun()
            else:
                st.session_state.kalan_can -= 2
                st.toast(f"'{giris_temiz}' doğru kelime değil! 2 can gitti.", icon="⚠️")
                st.rerun()

# --- 7. KULLANILAN HARFLER ---
if st.session_state.tahminler:
    rozetler = ""
    for h in st.session_state.tahminler:
        if h in st.session_state.gizli_kelime:
            rozetler += f'<span class="badge-ok">{h}</span>'
        else:
            rozetler += f'<span class="badge-no">{h}</span>'
    
    st.markdown(f"<div style='text-align:center;'>Denenenler:<br>{rozetler}</div>", unsafe_allow_html=True)

# --- 8. OYUN SONU ---
if st.session_state.durum == "kazandi":
    st.balloons()
    st.success(f"🎉 Tebrikler! Kelime: **{st.session_state.gizli_kelime}**")
elif st.session_state.durum == "kaybetti":
    st.error(f"💀 Asıldın! Doğru kelime: **{st.session_state.gizli_kelime}**")

if st.session_state.durum != "oyun":
    if st.button("Yeni Kelime 🔄", use_container_width=True):
        yeni_oyun()
        st.rerun()
