from io import BytesIO
import streamlit as st
import pandas as pd
import numpy as np

def read_r1_r2_file(uploaded_file):
    excel_data = uploaded_file.read()
    xl = pd.ExcelFile(BytesIO(excel_data))
    df = xl.parse(xl.sheet_names[0], header=None)

    num_particles = 200         # Jumlah baris data per iterasi  
    num_dimensions = 21         # Jumlah kolom dimensi r1/r2  
    max_iter = 50               # Total iterasi  

    r1_dict = {}  
    r2_dict = {}  

    for iterasi in range(max_iter):  
        start_col = 1 + iterasi * 26       # Kolom B = index 1  
        end_col = start_col + num_dimensions  

        r1_start_row = 1                   # B2 = row index 1  
        r1_end_row = r1_start_row + num_particles  

        r2_start_row = 210                 # B211 = row index 210  
        r2_end_row = r2_start_row + num_particles  

        try:  
            r1_block = df.iloc[r1_start_row:r1_end_row, start_col:end_col].values  
            r2_block = df.iloc[r2_start_row:r2_end_row, start_col:end_col].values  
        except Exception as e:  
            raise ValueError(f"Gagal mengambil data r1/r2 untuk iterasi {iterasi+1}: {e}")  

        if r1_block.shape != (num_particles, num_dimensions):  
            raise ValueError(f"r1 iterasi {iterasi+1} tidak berukuran (200, 21): {r1_block.shape}")  
        if r2_block.shape != (num_particles, num_dimensions):  
            raise ValueError(f"r2 iterasi {iterasi+1} tidak berukuran (200, 21): {r2_block.shape}")  

        r1_dict[iterasi + 1] = {idx: r1_block[idx] for idx in range(num_particles)}  
        r2_dict[iterasi + 1] = {idx: r2_block[idx] for idx in range(num_particles)}  

    return r1_dict, r2_dict

def upload_r1_r2_tab():
    st.header("2. Unggah Nilai r1 & r2")
    uploaded_file = st.file_uploader("Unggah file Excel yang berisi nilai r1 dan r2", type=["xlsx"])
    
    if uploaded_file is not None:  
        try:  
            r1_dict, r2_dict = read_r1_r2_file(uploaded_file)  
            st.session_state['r1_values'] = r1_dict  
            st.session_state['r2_values'] = r2_dict  
            st.success("Nilai r1 dan r2 berhasil diunggah dan dibaca.")  
        except Exception as e:  
            st.error(f"Gagal membaca file: {e}")
