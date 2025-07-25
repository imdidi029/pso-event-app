# components/upload_initial_pso_states_tab.py

import streamlit as st
import pandas as pd
import numpy as np

def upload_initial_pso_states_tab():
    """
    Menampilkan tab untuk mengunggah file Excel berisi bobot acak awal dan kecepatan awal
    untuk inisialisasi partikel PSO.
    """
    st.header("3. Unggah Kondisi Awal PSO (Bobot & Kecepatan)")
    st.write("Silakan unggah file Excel yang berisi 'Bobot Acak Awal' dan 'Kecepatan Awal' Anda.")
    st.info(
        "Sistem akan otomatis membaca sheet pertama dari file Excel yang diunggah.\n"
        "Pastikan sheet pertama berisi data bobot acak awal (200 baris x 21 kolom).\n"
        "Pastikan sheet kedua berisi data kecepatan awal (200 baris x 21 kolom).\n"
        "Atau, Anda bisa mengunggah file Excel terpisah untuk masing-masing.\n\n"
        "**Catatan:** Unggahan ini **opsional**. Jika Anda memilih 'Hasilkan secara acak' di tab '4. Evaluasi PSO', Anda tidak perlu mengunggah file ini."
    )

    # Unggah untuk Bobot Acak Awal (Sheet 3 di Excel Anda)
    uploaded_weights_file = st.file_uploader(
        "Pilih file Excel untuk Bobot Acak Awal (misal: Sheet '3. Bobot Acak Awal')",
        type=["xlsx"],
        key="initial_weights_uploader"
    )

    if uploaded_weights_file is not None:
        try:
            # Baca dengan header di baris pertama
            df_weights = pd.read_excel(uploaded_weights_file, sheet_name=0, header=0)
            xls_weights = pd.ExcelFile(uploaded_weights_file)
            sheet_name_weights = xls_weights.sheet_names[0]
            st.success(f"File 'Bobot Acak Awal' dari sheet '{sheet_name_weights}' berhasil diunggah!")

            # Ambil 200 baris pertama data, kolom B sampai V (indeks 1-21)
            initial_weights = df_weights.iloc[0:200, 1:22].values

            # Konversi ke float dan tangani non-numerik
            clean_weights = np.empty_like(initial_weights, dtype=float)
            for row_idx, row in enumerate(initial_weights):
                for col_idx, val in enumerate(row):
                    try:
                        clean_weights[row_idx, col_idx] = float(val)
                    except (ValueError, TypeError):
                        clean_weights[row_idx, col_idx] = 0.0
            initial_weights = clean_weights
            initial_weights[np.isnan(initial_weights)] = 0.0

            st.session_state['initial_pso_positions'] = initial_weights
            st.subheader("Pratinjau Bobot Acak Awal (Beberapa Baris Awal)")
            st.dataframe(pd.DataFrame(initial_weights).head())

        except Exception as e:
            st.error(f"Terjadi kesalahan saat membaca file Bobot Acak Awal: {e}")
            st.warning("Pastikan sheet pertama berisi bobot acak awal dan strukturnya benar (200 baris x 21 kolom data).")
    else:
        st.info("Silakan unggah file Excel untuk Bobot Acak Awal.")

    st.markdown("---")  # Pemisah

    # Unggah untuk Kecepatan Awal (Sheet 5 di Excel Anda)
    uploaded_velocities_file = st.file_uploader(
        "Pilih file Excel untuk Kecepatan Awal (misal: Sheet '5. Kecepatan awal')",
        type=["xlsx"],
        key="initial_velocities_uploader"
    )

    if uploaded_velocities_file is not None:
        try:
            # Baca dengan header di baris pertama
            df_velocities = pd.read_excel(uploaded_velocities_file, sheet_name=0, header=0)
            xls_velocities = pd.ExcelFile(uploaded_velocities_file)
            sheet_name_velocities = xls_velocities.sheet_names[0]
            st.success(f"File 'Kecepatan Awal' dari sheet '{sheet_name_velocities}' berhasil diunggah!")

            # Ambil 200 baris pertama data, kolom B sampai V (indeks 1-21)
            initial_velocities = df_velocities.iloc[0:200, 1:22].values

            # Konversi ke float dan tangani non-numerik
            clean_velocities = np.empty_like(initial_velocities, dtype=float)
            for row_idx, row in enumerate(initial_velocities):
                for col_idx, val in enumerate(row):
                    try:
                        clean_velocities[row_idx, col_idx] = float(val)
                    except (ValueError, TypeError):
                        clean_velocities[row_idx, col_idx] = 0.0
            initial_velocities = clean_velocities
            initial_velocities[np.isnan(initial_velocities)] = 0.0

            st.session_state['initial_pso_velocities'] = initial_velocities
            st.subheader("Pratinjau Kecepatan Awal (Beberapa Baris Awal)")
            st.dataframe(pd.DataFrame(initial_velocities).head())

        except Exception as e:
            st.error(f"Terjadi kesalahan saat membaca file Kecepatan Awal: {e}")
            st.warning("Pastikan sheet pertama berisi kecepatan awal dan strukturnya benar (200 baris x 21 kolom data).")
    else:
        st.info("Silakan unggah file Excel untuk Kecepatan Awal.")
