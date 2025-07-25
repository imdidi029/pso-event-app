# components/interpretasi_tab.py
import streamlit as st
import numpy as np


def tampilkan_interpretasi_kesimpulan(final_gBest_position, final_gBest_fitness, indikator_names):
    st.header("📌 Interpretasi & Kesimpulan Keberhasilan Event")

    # --- Interpretasi Bobot Optimal ---
    st.subheader("🔍 Interpretasi Bobot Optimal (gBest)")
    gbest_df = {
        "Indikator": indikator_names,
        "Bobot gBest": final_gBest_position
    }
    
    # Normalisasi bobot (persentase)
    total_bobot = np.sum(final_gBest_position)
    bobot_persen = (final_gBest_position / total_bobot) * 100

    for i, indikator in enumerate(indikator_names):
        st.markdown(f"- **{indikator}**: Bobot optimal = `{final_gBest_position[i]:.4f}` \
            ({bobot_persen[i]:.2f}%)")

    # --- Kesimpulan Keberhasilan Event ---
    st.subheader("✅ Kesimpulan")
    
    # Klasifikasi keberhasilan berdasarkan fitness
    if final_gBest_fitness >= 0.80:
        status = "Sangat Berhasil"
        emoji = "🎉"
    elif final_gBest_fitness >= 0.60:
        status = "Berhasil"
        emoji = "✅"
    elif final_gBest_fitness >= 0.40:
        status = "Cukup Berhasil"
        emoji = "⚠️"
    else:
        status = "Kurang Berhasil"
        emoji = "❌"

    st.markdown(f"### {emoji} Event dinilai **{status}** dengan nilai fitness akhir: **{final_gBest_fitness:.4f}**")

    st.info("Interpretasi ini didasarkan pada bobot optimal hasil PSO dan fitness akhir sebagai indikator keberhasilan.")
