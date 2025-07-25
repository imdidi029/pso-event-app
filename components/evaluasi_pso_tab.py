import streamlit as st
import pandas as pd
from pso_engine import PSO  # Pastikan kamu sudah import PSO

def evaluasi_pso_tab():
    st.header("4. Evaluasi Keberhasilan Event dengan PSO")
    st.write("Atur parameter PSO dan jalankan simulasi.")

    if 'normalized_data' not in st.session_state or st.session_state['normalized_data'] is None:
        st.warning("Mohon unggah file 'Data Raw' terlebih dahulu di tab '1. Unggah Data Kuesioner'.")
        return
    if 'avg_scores_full' not in st.session_state or st.session_state['avg_scores_full'] is None:
        st.warning("Data rata-rata skor belum tersedia. Mohon unggah file 'Data Raw' terlebih dahulu di tab '1. Unggah Data Kuesioner'.")
        return
    if 'r1_values' not in st.session_state or st.session_state['r1_values'] is None:
        st.warning("Mohon unggah file 'Nilai r1 & r2' terlebih dahulu di tab '2. Unggah Nilai r1 & r2'.")
        return
    if 'r2_values' not in st.session_state or st.session_state['r2_values'] is None:
        st.warning("Nilai r2 belum tersedia. Mohon unggah file 'Nilai r1 & r2' terlebih dahulu di tab '2. Unggah Nilai r1 & r2'.")
        return

    avg_scores_full = st.session_state['avg_scores_full']
    r1_values = st.session_state['r1_values']
    r2_values = st.session_state['r2_values']
    df_raw = st.session_state['normalized_data']
    indicator_column_names = df_raw.columns[1:22].tolist()
    num_dimensions = len(avg_scores_full)

    default_num_particles = 200
    default_num_iterations = 10
    default_w = 0.3
    default_c1 = 0.9
    default_c2 = 1.5

    col1, col2, col3 = st.columns(3)
    with col1:
        num_particles = st.number_input("Jumlah Partikel (N)", min_value=1, value=default_num_particles, step=1)
    with col2:
        num_iterations = st.number_input("Jumlah Iterasi (T)", min_value=1, value=default_num_iterations, step=1)
    with col3:
        initialization_option = st.radio(
            "Inisialisasi Bobot & Kecepatan Awal:",
            ("Gunakan data unggahan", "Hasilkan secara acak"),
            key="pso_init_option"
        )

    col4, col5, col6 = st.columns(3)
    with col4:
        w = st.slider("Bobot Inersia (w)", min_value=0.0, max_value=1.0, value=default_w, step=0.01)
    with col5:
        c1 = st.slider("Koefisien Kognitif (c1)", min_value=0.0, max_value=5.0, value=default_c1, step=0.1)
    with col6:
        c2 = st.slider("Koefisien Sosial (c2)", min_value=0.0, max_value=5.0, value=default_c2, step=0.1)

    initial_positions = None
    initial_velocities = None

    if initialization_option == "Gunakan data unggahan":
        if 'initial_pso_positions' in st.session_state and st.session_state['initial_pso_positions'] is not None:
            initial_positions = st.session_state['initial_pso_positions']
            st.success(f"Menggunakan {initial_positions.shape[0]} bobot awal dari unggahan.")
        else:
            st.warning("Bobot acak awal belum diunggah. Akan menggunakan bobot acak jika tombol 'Jalankan PSO' ditekan.")
            initialization_option = "Hasilkan secara acak"

        if 'initial_pso_velocities' in st.session_state and st.session_state['initial_pso_velocities'] is not None:
            initial_velocities = st.session_state['initial_pso_velocities']
            st.success(f"Menggunakan {initial_velocities.shape[0]} kecepatan awal dari unggahan.")
        else:
            st.warning("Kecepatan awal belum diunggah. Akan menggunakan kecepatan acak jika tombol 'Jalankan PSO' ditekan.")
            initialization_option = "Hasilkan secara acak"

    if st.button("Jalankan PSO"):
        if initialization_option == "Gunakan data unggahan" and initial_positions is not None:
            if num_particles > initial_positions.shape[0]:
                st.warning(f"Jumlah partikel ({num_particles}) melebihi jumlah bobot awal yang diunggah ({initial_positions.shape[0]}). "
                           f"Jumlah partikel akan disesuaikan menjadi {initial_positions.shape[0]}.")
                num_particles = initial_positions.shape[0]

        st.info("Simulasi PSO sedang berjalan, mohon tunggu...")

        pso = PSO(
            num_particles=num_particles,
            num_dimensions=num_dimensions,
            w=w,
            c1=c1,
            c2=c2,
            avg_scores=avg_scores_full,
            r1_values_dict=r1_values,
            r2_values_dict=r2_values,
            initial_positions_all_particles=initial_positions if initialization_option == "Gunakan data unggahan" else None,
            initial_velocities_all_particles=initial_velocities if initialization_option == "Gunakan data unggahan" else None
        )

        log_df_raw, final_gBest_position, final_gBest_fitness = pso.run(num_iterations)
        log_df = pd.DataFrame(log_df_raw)  # ← FIX UTAMA

        st.session_state['pso_log_df'] = log_df
        st.session_state['final_gBest_position'] = final_gBest_position
        st.session_state['final_gBest_fitness'] = final_gBest_fitness

        st.success("Simulasi PSO selesai!")
    
    if 'pso_log_df' in st.session_state and st.session_state['pso_log_df'] is not None:
        log_df = pd.DataFrame(st.session_state['pso_log_df'])  # ← FIX TAMBAHAN
        final_gBest_position = st.session_state['final_gBest_position']
        final_gBest_fitness = st.session_state['final_gBest_fitness']

        def rekap_log(log_df_input):
            log_df_input = pd.DataFrame(log_df_input)
            summary = []
            prev_max_fitness = None
            for iterasi, group in log_df_input.groupby("ITERASI"):
                max_fit = group["FITNESS"].max()
                partikel_max = group.loc[group["FITNESS"].idxmax()]["PARTIKEL"]
                avg_fit = group["FITNESS"].mean()
                update_pbest_count = (group["Status pBest"] == "UPDATE").sum()
                delta_fit = max_fit - prev_max_fitness if prev_max_fitness is not None else 0
                prev_max_fitness = max_fit
                summary.append({
                    "Iterasi": iterasi,
                    "Fitness Max": max_fit,
                    "Partikel Fitness Max": partikel_max,
                    "Jumlah Update pBest": update_pbest_count,
                    "Fitness Average": avg_fit,
                    "ΔFitness": delta_fit,
                })
            return pd.DataFrame(summary)

        df_summary = rekap_log(log_df)

        from components.visualisasi_tab import tampilkan_bonus_visualisasi
        tampilkan_bonus_visualisasi(final_gBest_position, indicator_column_names, log_df, df_summary)
        
        from components.event_summary_tab import Ringkasan_Event
        Ringkasan_Event(final_gBest_position, final_gBest_fitness, st.session_state['avg_scores_full'])

        from components.interpretasi_tab import tampilkan_interpretasi_kesimpulan
        tampilkan_interpretasi_kesimpulan(final_gBest_position, final_gBest_fitness, indicator_column_names)
        
        st.subheader("📊 Rekap Global PSO per Iterasi")
        st.dataframe(df_summary)

        csv_summary = df_summary.to_csv(index=False, decimal='.', sep=';')
        st.download_button(
            label="Download Rekap Global sebagai CSV",
            data=csv_summary,
            file_name="rekap_pso_global.csv",
            mime="text/csv",
            key="download_summary_csv"
        )

        st.subheader("📈 Visualisasi Fitness Max dan Average")
        fitness_chart = df_summary.set_index("Iterasi")[["Fitness Max", "Fitness Average"]]
        st.line_chart(fitness_chart)

        st.subheader("📜 Log Iterasi Detail")
        st.dataframe(log_df)

        csv_log_detail = log_df.to_csv(index=False, float_format='%.6f', decimal='.', sep=';')
        st.download_button(
            label="Download Log Iterasi Detail sebagai CSV",
            data=csv_log_detail,
            file_name="log_pso_detail.csv",
            mime="text/csv",
            key="download_log_csv"
        )

        st.subheader("Hasil Akhir (gBest)")
        st.write("Bobot Optimal (gBest Position):")
        gBest_weights_df = pd.DataFrame([final_gBest_position], columns=indicator_column_names)
        st.dataframe(gBest_weights_df.round(4))  # tampilkan 4 decimal

        csv_gbest_weights = gBest_weights_df.round(4).to_csv(index=False, float_format='%.4f', decimal='.', sep=';')
        st.download_button(
            label="Download Bobot Optimal (gBest) sebagai CSV",
            data=csv_gbest_weights,
            file_name="gbest_weights.csv",
            mime="text/csv",
            key="download_gbest_csv"
        )

        st.write(f"Fitness gBest Akhir: **{final_gBest_fitness:.4f}**")
