import streamlit as st
import streamlit.components.v1 as components
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

# GitHub kullanıcı adınız
GITHUB_KULLANICI_ADI = "alkan5505-cmd"
video_url = f"https://raw.githubusercontent.com/{GITHUB_KULLANICI_ADI}/online-davetiye/main/giris.mp4"
muzik_url = f"https://raw.githubusercontent.com/{GITHUB_KULLANICI_ADI}/online-davetiye/main/dugun_muzigi.mp3"

audio_url = "https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=wedding-piano-112674.mp3"
audio_file = "dugun_muzigi.mp3"

# ---------------------------------------------------------
# Özel CSS Stilleri (Sade & Lüks Krem Tema)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Montserrat:wght@300;400;600&family=Playfair+Display:ital,wght@0,500;0,700;1,400&display=swap');

    /* Streamlit Üst ve Yan Boşlukları Sıfırlama */
    .stAppViewMainBlockContainer, [data-testid="stMainBlockContainer"], .block-container, [data-testid="stHeader"] {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        margin-top: 0rem !important;
        max-width: 100% !important;
    }

    /* Sade ve Şık Krem Renkli Arka Plan (#f7f3ed) */
    [data-testid="stAppViewContainer"], .stApp, html, body, [data-testid="stMain"], [data-testid="stMainBlockContainer"], [data-testid="stHeader"] {
        background-color: #f7f3ed !important;
        background-image: none !important;
        font-family: 'Montserrat', sans-serif;
        color: #333333;
    }

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

    .card {
        background-color: rgba(255, 255, 255, 0.88);
        border: 1px solid #e0d5c1;
        border-radius: 18px;
        padding: 25px;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        backdrop-filter: blur(10px);
    }

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

    /* Lüks Mürdüm & Altın Sarısı Işıltılı Kaligrafik Buton Tasarımı */
    div.stButton {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
        margin: 0 auto !important;
    }
    div.stButton > button {
        background: linear-gradient(135deg, #581845 0%, #4a0e2e 50%, #6a1b44 100%) !important;
        color: #f3e5ab !important;
        border: 2px solid #d4af37 !important;
        border-radius: 35px !important;
        padding: 12px 42px !important;
        font-family: 'Great Vibes', cursive, 'Playfair Display', serif !important;
        font-size: 2.3rem !important;
        font-weight: 500 !important;
        letter-spacing: 1px !important;
        box-shadow: 0 10px 30px rgba(74, 14, 46, 0.4), 0 0 15px rgba(212, 175, 55, 0.3) !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        width: auto !important;
        min-width: 260px !important;
        max-width: 380px !important;
        margin: 0 auto !important;
        display: inline-block !important;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.4) !important;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #d4af37 0%, #aa7c11 50%, #581845 100%) !important;
        color: #ffffff !important;
        border-color: #f3e5ab !important;
        box-shadow: 0 14px 35px rgba(212, 175, 55, 0.5), 0 0 25px rgba(212, 175, 55, 0.6) !important;
        transform: translateY(-3px) scale(1.04) !important;
    }

    /* Standart Ses Çalarını Gizleme (Müzik Arka Planda Gizlice Çalar) */
    .stAudio, audio {
        display: none !important;
    }

    /* Sol Yan Menüyü (Sidebar) ve Sol Üstteki Ok Simgesini Tamamen Gizleme */
    [data-testid="stSidebar"], section[data-testid="stSidebar"] {
        display: none !important;
    }
    [data-testid="collapsedControl"], [data-testid="stSidebarCollapseButton"] {
        display: none !important;
    }

    /* Telefonda Sağ Alt Köşedeki Streamlit Rozet ve Profil/Taç İkonlarını Gizleme */
    [data-testid="stStatusWidget"], .stAppViewerToolbar, .viewerBadge_container__1A522, [class*="viewerBadge"], [class*="profile"], [class*="badge"], [data-testid="stElementToolbar"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
    }

    /* Sağ Üst Köşedeki Streamlit Üst Menüsünü (Üç Nokta, GitHub ve Share Butonları) Gizleme */
    header[data-testid="stHeader"], [data-testid="stHeader"], #MainMenu {
        visibility: hidden !important;
        display: none !important;
    }

    /* Videoyu Kapsayan Div */
    .video-hero-card {
        position: relative !important;
        width: 100% !important;
        max-width: 440px !important;
        height: 75vh !important;
        max-height: 620px !important;
        min-height: 460px !important;
        margin: 15px auto 25px auto !important;
        border-radius: 25px !important;
        overflow: hidden !important;
        border: 3px solid #ffffff !important;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.25), 0 0 20px rgba(212, 175, 55, 0.35) !important;
        background: #1a1a1a !important;
    }

    /* Videonun Alt Kısmında Ortalanmış Buton (position: absolute; bottom: 30px; left: 50%; transform: translateX(-50%)) */
    .hero-btn-container {
        position: absolute !important;
        bottom: 30px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        z-index: 99 !important;
        width: 85% !important;
        max-width: 320px !important;
    }

    .hero-btn-container div.stButton > button {
        background: linear-gradient(135deg, #581845 0%, #4a0e2e 50%, #6a1b44 100%) !important;
        color: #f3e5ab !important;
        font-family: 'Great Vibes', cursive, 'Playfair Display', serif !important;
        font-size: 2.2rem !important;
        font-weight: 500 !important;
        padding: 10px 30px !important;
        border-radius: 35px !important;
        border: 2px solid #d4af37 !important;
        box-shadow: 0 10px 30px rgba(88, 24, 69, 0.6), 0 0 20px rgba(212, 175, 55, 0.5) !important;
        transition: all 0.3s ease-in-out !important;
        width: 100% !important;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.6) !important;
        cursor: pointer !important;
        letter-spacing: 1px !important;
    }

    .hero-btn-container div.stButton > button:hover {
        background: linear-gradient(135deg, #d4af37 0%, #aa7c11 50%, #581845 100%) !important;
        color: #ffffff !important;
        border-color: #f3e5ab !important;
        box-shadow: 0 14px 35px rgba(212, 175, 55, 0.7), 0 0 30px rgba(212, 175, 55, 0.8) !important;
        transform: translateY(-3px) scale(1.03) !important;
    }

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
# 1. SESSION_STATE İÇİNDE 'opened' TANIMLAMA (Varsayılan: False)
# ---------------------------------------------------------
if "opened" not in st.session_state:
    st.session_state.opened = False

# ---------------------------------------------------------
# KONTROL AKIŞI
# ---------------------------------------------------------
if not st.session_state.opened:
    # ---------------------------------------------------------
    # 2. VİDEO KARTI VE ÜZERİNDEKİ OVERLAY KATMANI (GITHUB RAW LINK / YEREL)
    # ---------------------------------------------------------
    st.markdown(f"""
    <div class="video-hero-card">
        <video autoplay loop muted playsinline style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: 1;">
            <source src="{video_url}" type="video/mp4">
            <source src="giris.mp4" type="video/mp4">
        </video>
        <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 2; background: linear-gradient(to bottom, rgba(0,0,0,0.5) 0%, rgba(0,0,0,0.15) 45%, rgba(0,0,0,0.7) 100%); display: flex; flex-direction: column; align-items: center; padding: 35px 15px; box-sizing: border-box;">
            <div style="text-align: center; width: 100%;">
                <h1 style="font-family: 'Great Vibes', cursive; font-size: 4rem; font-style: italic; color: #f3e5ab; margin: 0; text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.85), 0 0 15px rgba(212, 175, 55, 0.65);"><i>Gül&Ümit</i></h1>
                <p style="font-family: 'Playfair Display', serif; font-size: 1.25rem; color: #ffffff; margin-top: 8px; text-shadow: 1px 1px 6px rgba(0, 0, 0, 0.9);">Nişan Davetiyemize Hoş Geldiniz...</p>
            </div>
        </div>
        <div class="hero-btn-container">
    """, unsafe_allow_html=True)

    if st.button("Davetiyeyi Aç", use_container_width=True, key="hero_btn_open"):
        st.session_state.opened = True
        st.rerun()

    st.markdown("</div></div>", unsafe_allow_html=True)

else:
    # ---------------------------------------------------------
    # 4. TEK SEFERLİK ÇAKIŞMASIZ ARKA PLAN MÜZİĞİ (SESSION STATE KONTROLLÜ)
    # ---------------------------------------------------------
    if 'muzik_calindi' not in st.session_state:
        st.session_state['muzik_calindi'] = True
        st.markdown(f'<audio id="bg-audio" autoplay loop style="display:none;"><source src="{muzik_url}" type="audio/mp3"></audio>', unsafe_allow_html=True)

    # ---------------------------------------------------------
    # ÜST BÖLÜM: DOĞAL STİCKER KARİKATÜR GÖRSELİ VE BAŞLIK
    # ---------------------------------------------------------
    if os.path.exists("karikatur_yeni.png"):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image("karikatur_yeni.png", use_container_width=True)

    st.markdown("<h1 class='couple-title'><i>Gül&Ümit</i></h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Nişanlanıyoruz...</p>", unsafe_allow_html=True)

    if os.path.exists("engagement_rings_ribbon.png"):
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.image("engagement_rings_ribbon.png", use_container_width=True)
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
    # GERİ SAYIM SAYACI (CANLI JAVASCRIPT COUNTDOWN)
    # ---------------------------------------------------------
    st.markdown("<h3 class='notranslate' translate='no' style='text-align: center; font-family: Playfair Display, serif; color: #5a4b41; margin-bottom: 5px;'>Büyük Güne Kalan Zaman</h3>", unsafe_allow_html=True)

    components.html("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Montserrat:wght@400;600&display=swap');
        
        body {
            margin: 0;
            padding: 0;
            background: transparent;
            font-family: 'Montserrat', sans-serif;
        }

        .countdown-container {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 12px;
            padding: 5px 0;
            flex-wrap: wrap;
        }

        .countdown-box {
            background: linear-gradient(145deg, #ffffff, #f7f1e5);
            border: 1px solid #d4af37;
            border-radius: 12px;
            padding: 10px 14px;
            text-align: center;
            min-width: 65px;
            box-shadow: 0 4px 15px rgba(212, 175, 55, 0.15);
            box-sizing: border-box;
        }

        .countdown-number {
            font-family: 'Playfair Display', serif;
            font-size: 1.7rem;
            font-weight: 700;
            color: #b8860b;
            line-height: 1.1;
        }

        .countdown-label {
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            color: #7a6a5d;
            margin-top: 2px;
        }

        /* Mobil Ekranlar İçin Otomatik Uyumlu (Responsive) @media Kuralları */
        @media (max-width: 480px) {
            .countdown-container {
                gap: 6px;
            }
            .countdown-box {
                padding: 8px 10px;
                min-width: 55px;
                border-radius: 10px;
            }
            .countdown-number {
                font-size: 1.3rem;
            }
            .countdown-label {
                font-size: 0.62rem;
                letter-spacing: 0.5px;
            }
        }

        @media (max-width: 340px) {
            .countdown-container {
                gap: 4px;
            }
            .countdown-box {
                padding: 6px 8px;
                min-width: 48px;
            }
            .countdown-number {
                font-size: 1.1rem;
            }
            .countdown-label {
                font-size: 0.58rem;
            }
        }
    </style>

    <div class='countdown-container' id='timer-wrap'>
        <div class='countdown-box'>
            <div class='countdown-number' id='cd-days'>0</div>
            <div class='countdown-label notranslate' translate='no'>GÜN</div>
        </div>
        <div class='countdown-box'>
            <div class='countdown-number' id='cd-hours'>00</div>
            <div class='countdown-label notranslate' translate='no'>SAAT</div>
        </div>
        <div class='countdown-box'>
            <div class='countdown-number' id='cd-minutes'>00</div>
            <div class='countdown-label notranslate' translate='no'>DAKİKA</div>
        </div>
        <div class='countdown-box'>
            <div class='countdown-number' id='cd-seconds'>00</div>
            <div class='countdown-label notranslate' translate='no'>SANİYE</div>
        </div>
    </div>

    <script>
        var targetDate = new Date('2026-08-20T20:00:00').getTime();

        function updateTimer() {
            var now = new Date().getTime();
            var diff = targetDate - now;

            if (diff <= 0) {
                var wrap = document.getElementById('timer-wrap');
                if (wrap) {
                    wrap.innerHTML = "<div style='text-align:center; font-weight:bold; color:#b8860b; font-size: 1.2rem;'>Bugün En Özel Günümüz! 🎉</div>";
                }
                return;
            }

            var days = Math.floor(diff / (1000 * 60 * 60 * 24));
            var hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            var minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
            var seconds = Math.floor((diff % (1000 * 60)) / 1000);

            var dEl = document.getElementById('cd-days');
            var hEl = document.getElementById('cd-hours');
            var mEl = document.getElementById('cd-minutes');
            var sEl = document.getElementById('cd-seconds');

            if (dEl) dEl.innerText = days;
            if (hEl) hEl.innerText = hours < 10 ? '0' + hours : hours;
            if (mEl) mEl.innerText = minutes < 10 ? '0' + minutes : minutes;
            if (sEl) sEl.innerText = seconds < 10 ? '0' + seconds : seconds;
        }

        updateTimer();
        setInterval(updateTimer, 1000);
    </script>
    """, height=110)

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
            <p style='font-size: 1rem; color: #333; margin-bottom: 0;'><b>Saat:</b> 20:00</p>
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
                    "Ad Soyad": guest_name.strip(),
                    "Katılım Durumu": attendance,
                    "Kişi Sayısı": int(guest_count) if "geleceğim" in attendance else 0,
                    "Not": note.strip()
                }])
                new_row.to_csv(LCV_FILE, mode='a', header=False, index=False, encoding="utf-8-sig")
                
                st.balloons()
                st.success("Katılım bilginiz Gül&Ümit çiftine başarıyla kaydedildi. Teşekkür ederiz! ❤️")
                st.rerun()

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
                    "Gönderen": sender_name.strip(),
                    "Mesaj": message_text.strip()
                }])
                new_msg.to_csv(MSG_FILE, mode='a', header=False, index=False, encoding="utf-8-sig")
                st.success("Tebrik mesajınız anı defterine başarıyla eklendi! ✨")
                st.rerun()

    # Yayınlanan Mesajları Listeleme (CSV'den Kalıcı Okuma)
    st.markdown("<h4 style='font-family: Playfair Display; color: #5a4b41; margin-top:25px;'>Gelen Dilekler</h4>", unsafe_allow_html=True)

    if os.path.exists(MSG_FILE):
        try:
            df_msgs = pd.read_csv(MSG_FILE, encoding="utf-8-sig")
            df_msgs = df_msgs.dropna(subset=["Gönderen", "Mesaj"])
            if not df_msgs.empty:
                # Son mesajlar üstte görünsün
                for idx, row in df_msgs.iloc[::-1].iterrows():
                    gonderen = str(row['Gönderen']).strip()
                    mesaj = str(row['Mesaj']).strip()
                    tarih = str(row['Tarih']).strip() if 'Tarih' in row and pd.notna(row['Tarih']) else ""
                    st.markdown(f"""
                    <div class='msg-box'>
                        <div style='display:flex; justify-content:space-between; align-items:center;'>
                            <span class='msg-author'>✍️ {gonderen}</span>
                            <span class='msg-date'>{tarih}</span>
                        </div>
                        <p style='margin-top: 8px; color: #444; font-size: 0.95rem; line-height: 1.5;'>"{mesaj}"</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Henüz mesaj yazılmamış. İlk tebrik mesajını yazan siz olun! ✨")
        except Exception:
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
