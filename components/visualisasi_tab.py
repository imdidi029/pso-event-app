import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px

def tampilkan_bonus_visualisasi(final_gBest_position, indicator_names, log_df, df_summary):
    st.subheader("📈 Visualisasi Tambahan")

    # Bar Chart Horizontal gBest
    st.markdown("### 📊 Bar Chart: Bobot gBest per Indikator")
    fig_bar_horizontal, ax = plt.subplots(figsize=(10, 6))  # lebar=10, tinggi=6 inci
    ax.barh(indicator_names, final_gBest_position, color='cornflowerblue')
    ax.set_xlabel("Bobot")
    ax.set_title("Bobot Optimal gBest per Indikator")
    ax.invert_yaxis()  # agar indikator paling atas tampil pertama
    for i, v in enumerate(final_gBest_position):
        if v > 0.0001:
            ax.text(v + 0.01, i, f"{v:.4f}", va='center')
    st.pyplot(fig_bar_horizontal)

    # Radar Chart gBest
    st.markdown("### 🌐 Radar Chart: gBest Optimal terhadap Indikator")
    try:
        final_gBest_position = np.array(final_gBest_position, dtype=float)
        if np.any(np.isnan(final_gBest_position)):
            st.warning("Radar Chart tidak dapat ditampilkan karena terdapat nilai NaN pada bobot.")
        else:
            radar_fig = go.Figure()
            radar_fig.add_trace(go.Scatterpolar(
                r=final_gBest_position,
                theta=indicator_names,
                fill='toself',
                name='gBest'
            ))
            radar_fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                showlegend=False,
                height=500
            )
            st.plotly_chart(radar_fig, use_container_width=True, key="radar_chart_gbest")
    except Exception as e:
        st.warning(f"Radar Chart gagal ditampilkan: {e}")

    # Scatter Plot Jumlah Update pBest vs Fitness Max
    if df_summary is not None:
        st.markdown("### 🔍 Scatter Plot: Jumlah Update pBest vs Fitness Max")
        scatter_fig = px.scatter(df_summary,
                                 x="Jumlah Update pBest",
                                 y="Fitness Max",
                                 color="Iterasi",
                                 size="ΔFitness",
                                 title="Hubungan Update pBest dan Peningkatan Fitness")
        st.plotly_chart(scatter_fig, use_container_width=True, key="scatter_update_pbest")

    # Heatmap Distribusi Fitness antar Partikel
    st.markdown("### 🔥 Heatmap: Distribusi Fitness antar Partikel")
    try:
        df_log = pd.DataFrame(log_df)
        df_heatmap = df_log[["ITERASI", "PARTIKEL", "FITNESS"]]
        heatmap_df = df_heatmap.pivot(index="PARTIKEL", columns="ITERASI", values="FITNESS")
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.heatmap(heatmap_df, cmap="YlGnBu", cbar_kws={'label': 'Fitness'}, ax=ax)
        ax.set_title("Distribusi Fitness per Partikel")
        st.pyplot(fig, clear_figure=True)
    except Exception as e:
        st.warning(f"Heatmap tidak dapat ditampilkan: {e}")

def visualisasi_tab():
    st.header("5. Visualisasi Hasil PSO")

    if 'pso_log_df' not in st.session_state or st.session_state['pso_log_df'] is None:
        st.warning("Silakan jalankan simulasi PSO terlebih dahulu di tab 'Evaluasi PSO'.")
        return

    final_gBest_position = st.session_state['final_gBest_position']
    final_gBest_fitness = st.session_state['final_gBest_fitness']
    avg_scores_full = st.session_state['avg_scores_full']
    log_df = st.session_state['pso_log_df']
    df_summary = st.session_state.get('rekap_log_df', None)

    # Ambil nama indikator dari dataframe atau fallback
    if isinstance(avg_scores_full, pd.DataFrame):
        indicator_names = avg_scores_full.columns.tolist()
    else:
        indicator_names = [f"x{i+1}" for i in range(len(final_gBest_position))]

    tampilkan_bonus_visualisasi(final_gBest_position, indicator_names, log_df, df_summary)
