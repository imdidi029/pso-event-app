import streamlit as st
import pandas as pd
import os
import shutil
from io import BytesIO
from zipfile import ZipFile
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from plotly import graph_objects as go


def export_hasil_tab():
    st.header("7. Ekspor Seluruh Hasil Evaluasi")

    if 'log_df' not in st.session_state:
        st.warning("Silakan jalankan simulasi PSO terlebih dahulu.")
        return

    log_df = st.session_state['log_df']
    df_summary = st.session_state.get('df_summary', pd.DataFrame())
    gbest_vector = st.session_state['final_gBest_position']
    gbest_fitness = st.session_state['final_gBest_fitness']
    indicator_names = st.session_state['indicator_column_names']

    if isinstance(log_df, list):
        log_df = pd.DataFrame(log_df)

    export_dir = "temp_export"
    os.makedirs(export_dir, exist_ok=True)
    visual_dir = os.path.join(export_dir, "visualisasi")
    os.makedirs(visual_dir, exist_ok=True)

    # 1. Simpan CSV
    log_df.to_csv(os.path.join(export_dir, "log_iterasi_global.csv"), index=False, sep=';', float_format='%.6f')
    df_summary.to_csv(os.path.join(export_dir, "rekap_iterasi_global.csv"), index=False, sep=';', float_format='%.6f')

    df_gbest = pd.DataFrame([gbest_vector], columns=indicator_names)
    df_gbest["FITNESS"] = gbest_fitness
    df_gbest.to_csv(os.path.join(export_dir, "bobot_gbest.csv"), index=False, sep=';', float_format='%.6f')

    # 2. Simpan Interpretasi
    text_interpretasi = f"""
== Ringkasan Evaluasi ==

Fitness Global Tertinggi: {gbest_fitness:.4f}

Kesimpulan:
- Nilai fitness menunjukkan rata-rata skor keberhasilan event terhadap bobot indikator optimal.
- Semakin tinggi fitness maka semakin tinggi keberhasilan event terhadap target persepsi ideal.

Bobot indikator optimal:
"""
    for i, nilai in enumerate(gbest_vector):
        text_interpretasi += f"- {indicator_names[i]}: {nilai:.4f}\n"

    with open(os.path.join(export_dir, "interpretasi.txt"), "w", encoding='utf-8') as f:
        f.write(text_interpretasi)

    # 3. Simpan Visualisasi
    # Heatmap kontribusi dimensi
    contrib = gbest_vector / np.sum(gbest_vector)
    fig1, ax1 = plt.subplots(figsize=(6, 8))
    sns.barplot(y=indicator_names, x=contrib, ax=ax1, palette="Blues_r")
    ax1.set_title("Kontribusi Dimensi terhadap Fitness")
    plt.tight_layout()
    fig1.savefig(os.path.join(visual_dir, "bar_kontribusi_dimensi.png"))
    plt.close(fig1)

    # Radar Chart
    fig2 = go.Figure()
    fig2.add_trace(go.Scatterpolar(
        r=gbest_vector,
        theta=indicator_names,
        fill='toself',
        name='Bobot Optimal gBest'
    ))
    fig2.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=False,
        title="Radar Chart - Bobot gBest"
    )
    fig2.write_image(os.path.join(visual_dir, "radar_chart.png"))

    # Scatter pBest update vs fitness
    iterasi_ke = pd.DataFrame(log_df)
    iterasi_ke = iterasi_ke[iterasi_ke["ITERASI"] > 0]
    scatter_df = iterasi_ke[["ITERASI", "PARTIKEL", "FITNESS", "Status pBest"]]
    warna = scatter_df["Status pBest"].map({"UPDATE": "green", "TETAP": "gray"})

    fig3, ax3 = plt.subplots(figsize=(8, 5))
    scatter_df.plot(kind='scatter', x="ITERASI", y="FITNESS", color=warna, ax=ax3)
    ax3.set_title("Fitness vs Status pBest")
    plt.tight_layout()
    fig3.savefig(os.path.join(visual_dir, "scatter_fitness_vs_update.png"))
    plt.close(fig3)

    # 4. Kompresi ZIP
    zip_buffer = BytesIO()
    with ZipFile(zip_buffer, 'w') as zip_file:
        for root, dirs, files in os.walk(export_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, export_dir)
                zip_file.write(file_path, arcname)

    st.success("Berhasil menyiapkan file ZIP hasil evaluasi")

    st.download_button(
        label="📦 Unduh Semua Hasil (.zip)",
        data=zip_buffer.getvalue(),
        file_name="hasil_evaluasi_event.zip",
        mime="application/zip"
    )

    # Cleanup
    shutil.rmtree(export_dir)
