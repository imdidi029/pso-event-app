import streamlit as st
import pandas as pd
import numpy as np

def upload_data_tab():
    """
    Menampilkan tab untuk mengunggah data kuesioner mentah,
    melakukan normalisasi (berbasis min-max per kolom),
    dan menghitung skor rata-rata indikator.
    """
    st.header("1. Unggah Data Kuesioner")
    st.write("Silakan unggah file Excel Anda yang berisi data responden dan indikator.")
    st.info("Pastikan struktur file Excel Anda sesuai dengan penjelasan:\n"
            "- Kolom A adalah 'Responden', Kolom B-V adalah 21 indikator.\n"
            "**Sistem akan otomatis membaca sheet pertama dari file Excel yang diunggah.**")

    uploaded_file = st.file_uploader("Pilih file Excel (Data Raw)", type=["xlsx"], key="data_raw_uploader")

    if uploaded_file is not None:
        try:
            # Membaca sheet pertama dari file Excel yang diunggah
            df_raw = pd.read_excel(uploaded_file, sheet_name=0)

            # Mendapatkan nama sheet pertama yang sebenarnya dibaca
            xls = pd.ExcelFile(uploaded_file)
            sheet_name_read = xls.sheet_names[0]

            st.success(f"File 'Data Raw' dari sheet pertama ('{sheet_name_read}') berhasil diunggah!")

            st.subheader("Pratinjau Data Mentah")
            st.dataframe(df_raw.head())

            # Asumsi kolom indikator adalah B sampai V (indeks 1 sampai 21)
            indicator_cols = df_raw.columns[1:22].tolist() # Kolom B hingga V

            df_normalized = df_raw.copy()
            min_max_log = {}

            for col in indicator_cols:
                # Mengisi NaN dengan rata-rata kolom sebelum normalisasi
                if df_normalized[col].isnull().any():
                    col_mean = df_normalized[col].mean()
                    df_normalized[col].fillna(col_mean, inplace=True)

                col_min = df_normalized[col].min()
                col_max = df_normalized[col].max()

                if col_max != col_min:
                    # Normalisasi dan pembulatan ke 4 desimal sesuai Excel
                    df_normalized[col] = np.round((df_normalized[col] - col_min) / (col_max - col_min), 4)
                else:
                    df_normalized[col] = 0.0 # Jika min dan max sama, semua nilai adalah 0 setelah normalisasi

                min_max_log[col] = {"min": col_min, "max": col_max}

            st.subheader("Data Normalisasi (0–1, Metode Min–Max per Indikator)")
            st.dataframe(df_normalized.head())

            # Simpan ke session_state
            st.session_state['normalized_data'] = df_normalized
            st.session_state['normalisasi_log'] = min_max_log

            # Hitung skor rata-rata per indikator (hasil akhir)
            avg_scores_full = df_normalized[indicator_cols].mean().values
            st.session_state['avg_scores_full'] = avg_scores_full

            st.subheader("Skor Rata-rata Indikator (Setelah Normalisasi)")
            avg_scores_df = pd.DataFrame([avg_scores_full], columns=indicator_cols)
            st.dataframe(avg_scores_df)

            st.success("Data berhasil diproses dan disimpan.")
            st.info("Anda bisa melanjutkan ke tab 'Unggah r1 & r2'.")

        except Exception as e:
            st.error(f"Terjadi kesalahan saat membaca atau memproses file: {e}")
            st.warning("Pastikan file Excel Anda memiliki sheet pertama dengan struktur data yang benar.")