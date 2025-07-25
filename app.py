# app.py

import streamlit as st
from components.upload_tab import upload_data_tab
from components.upload_r1_r2_tab import upload_r1_r2_tab
from components.upload_initial_pso_states_tab import upload_initial_pso_states_tab
from components.evaluasi_pso_tab import evaluasi_pso_tab
from components.visualisasi_tab import visualisasi_tab

def main():
    """
    Fungsi utama aplikasi Streamlit.
    Mengatur konfigurasi halaman dan tab navigasi.
    """
    st.set_page_config(
        page_title="Sistem Evaluasi Keberhasilan Event dengan PSO",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("Sistem Evaluasi Keberhasilan Event!")
    st.markdown("---")

    # Inisialisasi semua variabel di session_state jika belum ada
    if 'normalized_data' not in st.session_state:
        st.session_state['normalized_data'] = None
    if 'avg_scores_full' not in st.session_state:
        st.session_state['avg_scores_full'] = None
    if 'r1_values' not in st.session_state:
        st.session_state['r1_values'] = None
    if 'r2_values' not in st.session_state:
        st.session_state['r2_values'] = None
    # Inisialisasi untuk data awal PSO
    if 'initial_pso_positions' not in st.session_state:
        st.session_state['initial_pso_positions'] = None
    if 'initial_pso_velocities' not in st.session_state:
        st.session_state['initial_pso_velocities'] = None

    if 'pso_log_df' not in st.session_state:
        st.session_state['pso_log_df'] = None
    if 'final_gBest_position' not in st.session_state:
        st.session_state['final_gBest_position'] = None
    if 'final_gBest_fitness' not in st.session_state:
        st.session_state['final_gBest_fitness'] = None

    # Membuat tab navigasi
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "1. Unggah Data Kuesioner",
        "2. Unggah Nilai r1 & r2",
        "3. Unggah Kondisi Awal PSO",
        "4. Evaluasi PSO",
        "5. Visualisasi"
    ])

    with tab1:
        upload_data_tab()

    with tab2:
        upload_r1_r2_tab()
    
    with tab3:
        upload_initial_pso_states_tab()

    with tab4:
        evaluasi_pso_tab()
    
    with tab5:
       visualisasi_tab()

if __name__ == "__main__":
    main()