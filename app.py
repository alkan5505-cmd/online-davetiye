import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import os
import base64

# ---------------------------------------------------------
# Sayfa Yapılandırması (Page Config)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Gül&Ümit - Nişan Davetiyesi",
    page_icon="💍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# Lottie Animasyon Yükleyici (Lottie Loader)
# ---------------------------------------------------------
def load_lottie_url(url: str):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
    except Exception:
        return None
    return None

try:
    from streamlit_lottie import st_lottie
    LOTTIE_AVAILABLE = True
except ImportError:
    LOTTIE_AVAILABLE = False

# Lottie Animasyon Linkleri
LOTTIE_RINGS = "https://assets5.lottiefiles.com/packages/lf20_w6quzvgp.json" # Wedding rings / hearts
LOTTIE_CELEBRATE = "https://assets9.lottiefiles.com/packages/lf20_u4yrau.json" # Celebration

lottie_rings_json = load_lottie_url(LOTTIE_RINGS)
lottie_cel_json = load_lottie_url(LOTTIE_CELEBRATE)

# ---------------------------------------------------------
# Özel CSS Stilleri (Custom High-End Luxury Aesthetic)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Montserrat:wght@300;400;600&family=Playfair+Display:ital,wght@0,500;0,700;1,400&display=swap');

    /* Ana Arka Plan */
    .stApp {
        background: linear-gradient(135deg, #fdfbf7 0%, #f4eae1 50%, #fdfbf7 100%);
        font-family: 'Montserrat', sans-serif;
        color: #333333;
    }

    /* Banner Görsel Stili */
    .banner-card {
        width: 100%;
        display: flex;
        justify-content: center;
        margin-bottom: 25px;
    }
    .banner-card img {
        width: 100%;
        border-radius: 18px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        max-height: 240px;
        object-fit: cover;
        display: block;
    }

    /* Başlıklar ve Fontlar */
    .couple-title {
        font-family: 'Great Vibes', cursive;
        font-size: 4rem;
        font-style: italic;
        color: #b8860b;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 0px;
        text-shadow: 2px 2px 4px rgba(184, 134, 11, 0.15);
    }
    
    .subtitle {
        font-family: 'Playfair Display', serif;
        font-size: 1.4rem;
        font-style: italic;
        color: #5a4b41;
        text-align: center;
        margin-bottom: 25px;
    }

    /* Lüks Kart Tasarımı */
    .card {
        background-color: rgba(255, 255, 255, 0.85);
        border: 1px solid #e0d5c1;
        border-radius: 18px;
        padding: 25px;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        backdrop-filter: blur(8px);
        transition: transform 0.3s ease;
    }
    .card:hover {
        transform: translateY(-3px);
    }

    /* Sayaç Stilleri */
    .countdown-container {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin: 20px 0;
    }
    .countdown-box {
        background: linear-gradient(145deg, #ffffff, #f7f1e5);
        border: 1px solid #d4af37;
        border-radius: 12px;
        padding: 12px 18px;
        text-align: center;
        min-width: 75px;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.15);
    }
    .countdown-number {
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: #b8860b;
    }
    .countdown-label {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #7a6a5d;
    }

    /* Akış Zaman Çizelgesi */
    .timeline-item {
        border-left: 3px solid #d4af37;
        padding-left: 20px;
        margin-bottom: 20px;
        position: relative;
    }
    .timeline-time {
        font-weight: 600;
        color: #b8860b;
        font-size: 1.1rem;
    }
    .timeline-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.2rem;
        color: #333333;
    }

    /* Buton Tasarımı */
    .stButton>button {
        background: linear-gradient(135deg, #d4af37 0%, #aa7c11 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 25px;
        font-weight: 600;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 15px rgba(170, 124, 17, 0.3);
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #aa7c11 0%, #8b6508 100%);
        box-shadow: 0 6px 20px rgba(170, 124, 17, 0.4);
        color: #ffffff;
    }

    /* Mesaj Kartı */
    .msg-box {
        background-color: #fffdf9;
        border-left: 4px solid #d4af37;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    .msg-author {
        font-weight: 600;
        color: #5a4b41;
    }
    .msg-date {
        font-size: 0.75rem;
        color: #999;
    }

    /* Alt Bilgi */
    .footer {
        text-align: center;
        font-size: 0.85rem;
        color: #8c7a6b;
        margin-top: 40px;
        padding-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Veri Depolama Yapılandırması (CSV Veri Tabanı)
# ---------------------------------------------------------
LCV_FILE = "lcv_kayitlar.csv"
MSG_FILE = "tebrik_mesajlari.csv"

def init_files():
    if not os.path.exists(LCV_FILE):
        df_lcv = pd.DataFrame(columns=["Tarih", "Ad Soyad", "Katılım Durumu", "Kişi Sayısı", "Not"])
        df_lcv.to_csv(LCV_FILE, index=False, encoding="utf-8-sig")
    
    if not os.path.exists(MSG_FILE):
        df_msg = pd.DataFrame(columns=["Tarih", "Gönderen", "Mesaj"])
        df_msg.to_csv(MSG_FILE, index=False, encoding="utf-8-sig")

init_files()

def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

# ---------------------------------------------------------
# ÜST BÖLÜM: KARŞILAMA VE BAŞLIK
# ---------------------------------------------------------
banner_b64 = get_image_base64("sea_sunset_banner.png")
if banner_b64:
    st.markdown(f"""
    <div class='banner-card'>
        <img src='data:image/png;base64,{banner_b64}'>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("<div style='text-align: center; color: #d4af37; font-size: 1.8rem;'>🌊 🌅 🌊</div>", unsafe_allow_html=True)

st.markdown("<h1 class='couple-title'><i>Gül&Ümit</i></h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Nişanlanıyoruz...</p>", unsafe_allow_html=True)

rings_b64 = get_image_base64("engagement_rings_ribbon.png")
if rings_b64:
    st.markdown(f"""
    <div style='text-align: center; margin: 15px auto 25px auto;'>
        <img src='data:image/png;base64,{rings_b64}' style='width: 160px; height: 160px; border-radius: 50%; object-fit: cover; border: 3px solid #d4af37; box-shadow: 0 6px 20px rgba(212,175,55,0.25); display: block; margin: 0 auto;'>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("<div style='text-align: center; font-size: 3rem;'>💍</div>", unsafe_allow_html=True)

st.markdown("""
<div class='card' style='text-align: center;'>
    <p style='font-size: 1.1rem; line-height: 1.7; color: #4a3e35;'>
        <i>"Birbirimizin hayatına dokunduğumuz andan itibaren başlayan hikayemizi,<br>
        nişan törenimizle yeni bir sayfaya taşıyoruz. Yanımızda olmanız dileğiyle..."</i>
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# MÜZİK ÇALAR (İSTEĞE BAĞLI ARKA PLAN AMBİYANSI)
# ---------------------------------------------------------
# Telifsiz romantik piyano örneği
audio_url = "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=wedding-piano-112674.mp3"
st.audio(audio_url, format="audio/mp3")

# ---------------------------------------------------------
# GERİ SAYIM SAYACI (COUNTDOWN)
# ---------------------------------------------------------
st.markdown("<h3 style='text-align: center; font-family: Playfair Display; color: #5a4b41;'>Büyük Güne Kalan Zaman</h3>", unsafe_allow_html=True)

# Nişan Tarihi: 20 Ağustos 2026 - Saat 19:30
wedding_date = datetime(2026, 8, 20, 19, 30, 0)
now = datetime.now()
diff = wedding_date - now

if diff.total_seconds() > 0:
    days = diff.days
    hours = diff.seconds // 3600
    minutes = (diff.seconds % 3600) // 60
    seconds = diff.seconds % 60

    st.markdown(f"""
    <div class='countdown-container'>
        <div class='countdown-box'>
            <div class='countdown-number'>{days}</div>
            <div class='countdown-label'>Gün</div>
        </div>
        <div class='countdown-box'>
            <div class='countdown-number'>{hours}</div>
            <div class='countdown-label'>Saat</div>
        </div>
        <div class='countdown-box'>
            <div class='countdown-number'>{minutes}</div>
            <div class='countdown-label'>Dakika</div>
        </div>
        <div class='countdown-box'>
            <div class='countdown-number'>{seconds}</div>
            <div class='countdown-label'>Saniye</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("<div style='text-align:center; font-weight:bold; color:#b8860b;'>Bugün En Özel Günümüz! 🎉</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# DÜĞÜN PROGRAMI VE MEKAN BİLGİLERİ
# ---------------------------------------------------------
st.markdown("<hr style='border: 0; height: 1px; background: #e0d5c1; margin: 30px 0;'>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("<h3 style='font-family: Playfair Display; color: #5a4b41;'>📅 Tarih & Saat</h3>", unsafe_allow_html=True)
    st.markdown("""
    <div class='card'>
        <p style='font-size: 1.1rem; font-weight: 600; color: #b8860b;'>Nişan Töreni</p>
        <p style='font-size: 1rem; color: #333; margin-bottom: 8px;'><b>Tarih:</b> 20 Ağustos 2026, Perşembe</p>
        <p style='font-size: 1rem; color: #333; margin-bottom: 0;'><b>Saat:</b> 19:30</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("<h3 style='font-family: Playfair Display; color: #5a4b41;'>📍 Mekan & Konum</h3>", unsafe_allow_html=True)
    st.markdown("""
    <div class='card'>
        <p style='font-size: 1.1rem; font-weight: 600; color: #b8860b;'>Nazar Düğün Salonu</p>
        <p style='font-size: 0.95rem; color: #555;'>
            Sarıcalı Mah. Yunus Emre Cad. No:186<br>
            Çarşamba
        </p>
        <p style='font-size: 0.85rem; color: #777;'>Otopark Mevcuttur.</p>
    </div>
    """, unsafe_allow_html=True)
    
    maps_url = "https://maps.google.com/?q=Nazar+D%C3%BC%C4%9F%C3%BCn+Salonu+Sar%C4%B1cal%C4%B1+Mahallesi+Yunus+Emre+Caddesi+No:186"
    st.markdown(f"""
    <a href='{maps_url}' target='_blank' style='text-decoration: none;'>
        <button style='
            background: linear-gradient(135deg, #1B3B2B 0%, #2D5A42 100%);
            color: white; border: none; border-radius: 25px; padding: 10px 20px;
            font-weight: 600; cursor: pointer; width: 100%; box-shadow: 0 4px 12px rgba(27,59,43,0.3);'>
            🗺️ Google Maps'te Aç
        </button>
    </a>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# LCV / KATILIM DURUMU BİLDİRİM FORMU
# ---------------------------------------------------------
st.markdown("<hr style='border: 0; height: 1px; background: #e0d5c1; margin: 30px 0;'>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; font-family: Playfair Display; color: #5a4b41;'>💌 Katılım Durumu (LCV)</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 0.9rem; color: #777;'>Lütfen 15 Ağustos 2026 tarihine kadar katılım durumunuzu bildiriniz.</p>", unsafe_allow_html=True)

with st.form("lcv_form", clear_on_submit=True):
    col_name, col_status = st.columns(2)
    with col_name:
        guest_name = st.text_input("Adınız ve Soyadınız *")
    with col_status:
        attendance = st.selectbox("Katılım Durumu *", ["Büyük bir mutlulukla geleceğim 🎉", "Maalesef katılamayacağım 😔"])
    
    col_count, col_note = st.columns([1, 2])
    with col_count:
        guest_count = st.number_input("Gelecek Kişi Sayısı", min_value=1, max_value=6, value=1)
    with col_note:
        note = st.text_input("Özel Not / Mesaj (Varsa)")

    submit_lcv = st.form_submit_button("Katılım Bilgisini Gönder ✨")

    if submit_lcv:
        if guest_name.strip() == "":
            st.error("Lütfen adınızı ve soyadınızı giriniz.")
        else:
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
            new_row = pd.DataFrame([{
                "Tarih": now_str,
                "Ad Soyad": guest_name,
                "Katılım Durumu": attendance,
                "Kişi Sayısı": guest_count if "geleceğim" in attendance else 0,
                "Not": note
            }])
            new_row.to_csv(LCV_FILE, mode='a', header=False, index=False, encoding="utf-8-sig")
            
            st.balloons()
            st.success("Katılım bilginiz Gül&Ümit çiftine iletildi. Teşekkür ederiz! ❤️")

# ---------------------------------------------------------
# TEBRİK MESAJLARI & ANI DEFTERİ
# ---------------------------------------------------------
st.markdown("<hr style='border: 0; height: 1px; background: #e0d5c1; margin: 30px 0;'>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; font-family: Playfair Display; color: #5a4b41;'>📖 Anı Defteri & Tebrik Mesajları</h3>", unsafe_allow_html=True)

with st.form("msg_form", clear_on_submit=True):
    sender_name = st.text_input("İsminiz")
    message_text = st.text_area("Gül&Ümit Çiftine Güzel Dilekleriniz ✨", height=100)
    submit_msg = st.form_submit_button("Mesajı Anı Defterine Ekle 💖")

    if submit_msg:
        if sender_name.strip() == "" or message_text.strip() == "":
            st.error("Lütfen adınızı ve mesajınızı eksiksiz doldurunuz.")
        else:
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
            new_msg = pd.DataFrame([{
                "Tarih": now_str,
                "Gönderen": sender_name,
                "Mesaj": message_text
            }])
            new_msg.to_csv(MSG_FILE, mode='a', header=False, index=False, encoding="utf-8-sig")
            st.success("Tebrik mesajınız anı defterine eklendi! ✨")

# Yayınlanan Mesajları Listeleme
st.markdown("<h4 style='font-family: Playfair Display; color: #5a4b41; margin-top:25px;'>Gelen Dilekler</h4>", unsafe_allow_html=True)

if os.path.exists(MSG_FILE):
    df_msgs = pd.read_csv(MSG_FILE, encoding="utf-8-sig")
    if not df_msgs.empty:
        # Son mesajlar üstte görünsün
        for idx, row in df_msgs.iloc[::-1].iterrows():
            st.markdown(f"""
            <div class='msg-box'>
                <div style='display:flex; justify-content:space-between;'>
                    <span class='msg-author'>✍️ {row['Gönderen']}</span>
                    <span class='msg-date'>{row['Tarih']}</span>
                </div>
                <p style='margin-top: 8px; color: #444; font-size: 0.95rem;'>"{row['Mesaj']}"</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Henüz mesaj yazılmamış. İlk tebrik mesajını yazan siz olun! ✨")

# ---------------------------------------------------------
# YÖNETİCİ / ÇİFT ÖZEL PANELERİ (SIDEBAR)
# ---------------------------------------------------------
st.sidebar.title("🔒 Çift Paneli (Yönetici)")
admin_pass = st.sidebar.text_input("Giriş Şifresi", type="password")

if admin_pass == "gulumit2026":
    st.sidebar.success("Yönetici girişi başarılı!")
    st.sidebar.markdown("### 📊 LCV Katılım Özetleri")
    
    if os.path.exists(LCV_FILE):
        df_lcv = pd.read_csv(LCV_FILE, encoding="utf-8-sig")
        if not df_lcv.empty:
            total_responses = len(df_lcv)
            attending = df_lcv[df_lcv["Katılım Durumu"].str.contains("geleceğim", case=False, na=False)]
            total_guests = attending["Kişi Sayısı"].sum()
            
            st.sidebar.metric("Toplam Bildirim", f"{total_responses} Kisi")
            st.sidebar.metric("Gelecek Toplam Davetli", f"{int(total_guests)} Kişi")
            
            st.sidebar.dataframe(df_lcv)
            
            # Excel / CSV İndirme Butonu
            csv_data = df_lcv.to_csv(index=False, encoding="utf-8-sig").encode('utf-8-sig')
            st.sidebar.download_button(
                label="📥 LCV Kayıtlarını CSV İndir",
                data=csv_data,
                file_name="Gül_Ümit_LCV_Listesi.csv",
                mime="text/csv"
            )
        else:
            st.sidebar.info("Henüz LCV kaydı bulunmuyor.")

# ---------------------------------------------------------
# ALT BİLGİ (FOOTER)
# ---------------------------------------------------------
st.markdown("""
<div class='footer'>
    Gül&Ümit Online Davetiye • 2026 ❤️<br>
    <i>Sevgiyle ve Mutlulukla Hazırlandı</i>
</div>
""", unsafe_allow_html=True)
