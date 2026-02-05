import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

# -------------------------------------------------
# SAYFA AYARLARI
# -------------------------------------------------
st.set_page_config(page_title="Su Ayak İzi Takip Sistemi", page_icon="💧")
st.title("💧 Su Ayak İzi Takip ve Puan Sistemi")

# -------------------------------------------------
# SABİT DEĞERLER
# -------------------------------------------------
DUS_DK = 12
SIFON = 6
MUSLUK_DK = 6
CAMASIR = 50
BULASIK = 15
ORTALAMA = 150

DATA_FILE = "su_kayitlari.csv"

# -------------------------------------------------
# VERİ OKUMA / OLUŞTURMA
# -------------------------------------------------
try:
    df = pd.read_csv(DATA_FILE)
except:
    df = pd.DataFrame(columns=["Tarih", "Toplam Su (L)", "Puan"])

# -------------------------------------------------
# GÜNLÜK VERİ GİRİŞİ
# -------------------------------------------------
st.sidebar.header("📥 Günlük Veri Girişi")

dus = st.sidebar.number_input("Duş süresi (dk)", 0, 60, 10)
sifon = st.sidebar.number_input("Sifon sayısı", 0, 30, 5)
musluk = st.sidebar.number_input("Musluk süresi (dk)", 0, 60, 5)
camasir = st.sidebar.number_input("Çamaşır makinesi (adet)", 0, 5, 1)
bulasik = st.sidebar.number_input("Bulaşık makinesi (adet)", 0, 5, 1)

toplam_su = (
    dus * DUS_DK +
    sifon * SIFON +
    musluk * MUSLUK_DK +
    camasir * CAMASIR +
    bulasik * BULASIK
)

puan = max(0, int(ORTALAMA - toplam_su))

st.sidebar.markdown(f"### 💧 Toplam: **{toplam_su:.1f} L**")
st.sidebar.markdown(f"### ⭐ Günlük Puan: **{puan}**")

# -------------------------------------------------
# KAYDETME
# -------------------------------------------------
if st.sidebar.button("📅 Günlük Kaydı Kaydet"):
    yeni_kayit = pd.DataFrame([{
        "Tarih": date.today(),
        "Toplam Su (L)": toplam_su,
        "Puan": puan
    }])

    df = pd.concat([df, yeni_kayit], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    st.success("✅ Günlük kayıt başarıyla kaydedildi!")

# -------------------------------------------------
# VERİ GÖSTERİMİ
# -------------------------------------------------
st.subheader("📊 Kayıtlı Veriler")
st.dataframe(df)

# Eğer veri yoksa devam etme
if len(df) > 0:
    # -------------------------------------------------
    # TARİHİ INDEX YAP
    # -------------------------------------------------
    df["Tarih"] = pd.to_datetime(df["Tarih"])
    df = df.set_index("Tarih")

    # -------------------------------------------------
    # HAFTALIK ANALİZ
    # -------------------------------------------------
    st.subheader("📆 Haftalık Su Tüketimi")
    haftalik = df.resample("W").sum(numeric_only=True)

    fig1, ax1 = plt.subplots()
    ax1.plot(haftalik.index, haftalik["Toplam Su (L)"], marker="o")
    ax1.set_ylabel("Litre")
    ax1.set_xlabel("Hafta")
    st.pyplot(fig1)

    # -------------------------------------------------
    # AYLIK ANALİZ
    # -------------------------------------------------
    st.subheader("🗓️ Aylık Su Tüketimi")
    aylik = df.resample("M").sum(numeric_only=True)

    fig2, ax2 = plt.subplots()
    ax2.bar(aylik.index.astype(str), aylik["Toplam Su (L)"])
    ax2.set_ylabel("Litre")
    ax2.set_xlabel("Ay")
    st.pyplot(fig2)

    # -------------------------------------------------
    # PUAN SİSTEMİ
    # -------------------------------------------------
    st.subheader("🏆 Kullanıcı Puan Durumu")
    toplam_puan = df["Puan"].sum()

    st.metric("Toplam Puan", toplam_puan)

    if toplam_puan >= 500:
        st.success("🌟 Seviye: Su Dostu Uzman")
    elif toplam_puan >= 250:
        st.info("💚 Seviye: Bilinçli Kullanıcı")
    else:
        st.warning("💧 Seviye: Geliştirilebilir")

    # -------------------------------------------------
    # TASARRUF ÖNERİSİ
    # -------------------------------------------------
    st.subheader("🌱 Günlük Tasarruf Önerisi")
    if toplam_su > ORTALAMA:
        st.write("🔴 Bugün ortalamanın üzerindesin. Duş süresini kısaltmayı dene.")
    else:
        st.write("🟢 Harika! Bu şekilde devam edersen aylık ciddi su tasarrufu sağlarsın.")
