import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Aplikasi BMI & Kalori Harian", layout="centered")
st.title("🏋️‍♀️ Aplikasi Kira BMI & Kalori Makanan (Sehari)")

# --- Maklumat Pengguna ---
st.header("🧍 Maklumat Pengguna")
nama = st.text_input("Nama")
kelas = st.text_input("Kelas")
jantina = st.selectbox("Jantina", ["Lelaki", "Perempuan"])
berat = st.number_input("Berat (kg)", min_value=1.0, format="%.1f")
tinggi = st.number_input("Tinggi (cm)", min_value=1.0, format="%.1f")

if nama and kelas and berat > 0 and tinggi > 0:
    tinggi_m = tinggi / 100
    bmi = berat / (tinggi_m ** 2)
    st.subheader(f"📊 BMI anda: {bmi:.2f}")

    if bmi < 18.5:
        st.warning("Kategori: Kurang berat badan")
    elif bmi < 25:
        st.success("Kategori: Normal")
    elif bmi < 30:
        st.warning("Kategori: Berlebihan berat badan")
    else:
        st.error("Kategori: Obes")

    # Kalori harian disarankan ikut jantina
    if jantina == "Lelaki":
        kalori_harian = 2500
    else:
        kalori_harian = 2000

    # --- Senarai Makanan ---
    st.header("🍽️ Pilih Makanan yang Anda Makan Hari Ini")

    kalori_makanan = {
        "Nasi lemak (1 bungkus)": 400,
        "Roti canai (1 keping)": 300,
        "Mee goreng (1 pinggan)": 500,
        "Susu (1 gelas)": 120,
        "Telur rebus (1 biji)": 155,
        "Teh tarik (1 cawan)": 180,
        "Nasi putih (1 cawan)": 130,
        "Ayam goreng (1 ketul)": 240,
        "Ikan bakar (1 keping)": 180,
        "Sayur campur (1 senduk)": 50,
        "Air sirap (1 gelas)": 100,
        "Keropok lekor (3 batang)": 200,
        "Kuih karipap (1 biji)": 160,
        "Air milo (1 cawan)": 170,
        "Nasi goreng (1 pinggan)": 600,
        "Mee sup (1 mangkuk)": 350,
        "Buah epal (1 biji)": 95,
        "Buah pisang (1 biji)": 100,
        "Air kosong": 0,
    }

    pilihan = {}

    st.write("✅ Tandakan makanan yang anda makan hari ini:")
    for makanan, kalori in kalori_makanan.items():
        if st.checkbox(f"{makanan} — {kalori} kcal", key=makanan):
            pilihan[makanan] = kalori

    # --- Tambah Makanan Sendiri ---
    st.subheader("➕ Tambah Makanan Sendiri (Jika Tiada Dalam Senarai)")
    makanan_baru = st.text_input("Nama makanan tambahan:")
    kalori_baru = st.number_input("Kalori makanan tersebut (kcal):", min_value=0, step=10)

    if st.button("Tambah Makanan"):
        if makanan_baru and kalori_baru > 0:
            pilihan[makanan_baru] = kalori_baru
            st.success(f"✅ {makanan_baru} ditambah ({kalori_baru} kcal)")
        else:
            st.warning("⚠️ Sila isi nama & kalori sebelum tekan tambah.")

    # --- Paparan Hasil ---
    if pilihan:
        jumlah_kalori = sum(pilihan.values())
        baki_kalori = kalori_harian - jumlah_kalori
        baki_kalori = max(baki_kalori, 0)  # tak boleh kurang dari 0

        st.success(f"**Jumlah Kalori Hari Ini:** {jumlah_kalori:.2f} kcal")
        st.info(f"**Kalori Disarankan Harian:** {kalori_harian} kcal")
        st.info(f"**Kalori Baki yang Boleh Diambil:** {baki_kalori:.2f} kcal")

        df = pd.DataFrame([{
            "Nama": nama,
            "Kelas": kelas,
            "Berat (kg)": berat,
            "Tinggi (cm)": tinggi,
            "BMI": round(bmi, 2),
            "Jumlah Kalori (kcal)": jumlah_kalori,
            "Makanan": ", ".join(pilihan.keys())
        }])

        # --- Carta Pai ---
        fig, ax = plt.subplots(figsize=(6,6))
        labels = ['Kalori Diambil', 'Kalori Baki']
        sizes = [jumlah_kalori, baki_kalori]
        colors = ['#ff9999','#66b3ff']
        explode = (0.05, 0.05)
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90,
               colors=colors, explode=explode, shadow=True)
        ax.set_title("Peratusan Kalori Diambil vs Baki")

        # Info pengguna di bawah carta
        info = f"Nama: {nama} | Kelas: {kelas} | BMI: {bmi:.2f}"
        plt.figtext(0.5, -0.05, info, ha="center", fontsize=10, fontweight="bold")

        st.pyplot(fig)

        # --- Muat Turun CSV ---
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Muat Turun Data (CSV)",
            data=csv,
            file_name="data_kesihatan_harian.csv",
            mime="text/csv"
        )

        # --- Muat Turun Graf PNG ---
        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)
        st.download_button(
            "📸 Muat Turun Carta Pai (PNG)",
            data=buf,
            file_name="carta_pai_kalori.png",
            mime="image/png"
        )

    else:
        st.info("📝 Sila pilih sekurang-kurangnya satu makanan atau tambah makanan baru.")

else:
    st.info("📝 Sila lengkapkan Nama, Kelas, Jantina, Berat dan Tinggi terlebih dahulu.")
    
