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

