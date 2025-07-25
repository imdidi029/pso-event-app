import streamlit as st
import pandas as pd
import numpy as np

def Ringkasan_Event(final_gbest_position, final_gbest_fitness, avg_scores, threshold=0.7):
    st.header("📌 Ringkasan Keberhasilan Event")

    # 1. Info nilai fitness akhir
    st.subheader("1. Nilai Fitness Akhir")
    st.write(f"**Fitness Tertinggi (gBest):** {final_gbest_fitness:.6f}")

    # 2. Interpretasi keberhasilan
    st.subheader("2. Status Keberhasilan")
    if final_gbest_fitness >= threshold:
        st.success(f"Event dinilai **BERHASIL** karena fitness {final_gbest_fitness:.4f} ≥ threshold {threshold:.2f}")
        status = "BERHASIL"
    else:
        st.warning(f"Event dinilai **BELUM OPTIMAL** karena fitness {final_gbest_fitness:.4f} < threshold {threshold:.2f}")
        status = "BELUM OPTIMAL"

    # 3. Kontribusi indikator (persentase bobot)
    st.subheader("3. Distribusi Bobot Optimal Tiap Indikator")
    gbest_normalized = final_gbest_position / np.sum(final_gbest_position)
    if isinstance(avg_scores, pd.DataFrame):
        indicator_names = avg_scores.columns.tolist()
    else:
        indicator_names = [f"x{i+1}" for i in range(len(final_gbest_position))]

    df_kontribusi = pd.DataFrame({
        "Indikator": indicator_names,
        "Bobot Optimal": gbest_normalized
    }).sort_values(by="Bobot Optimal", ascending=False).reset_index(drop=True)
    st.dataframe(df_kontribusi.style.format({"Bobot Optimal": "{:.4f}"}))

    # 4. Simpulan akhir
    st.subheader("4. Simpulan")
    st.markdown(f"""
    Berdasarkan simulasi PSO, diperoleh bobot optimal yang memaksimalkan nilai fitness. Dengan fitness akhir sebesar 
    **{final_gbest_fitness:.4f}**, event ini secara keseluruhan dinilai **{status}**.

    Bobot optimal ini menunjukkan kontribusi relatif dari masing-masing indikator dalam keberhasilan event.
    """)
