import streamlit as st
import pandas as pd
import os
import time
from fpdf import FPDF
from datetime import datetime

# --- 1. PENGATURAN HALAMAN ---
st.set_page_config(page_title="Admin Panel", layout="wide", page_icon="⚖️")

# --- PERBAIKAN PATH JALUR DATABASE ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir) 

DB_PESANAN = os.path.join(parent_dir, 'database_pesanan.csv')
DB_MENU = os.path.join(parent_dir, 'database_menu.csv')
ASSETS_DIR = os.path.join(parent_dir, 'Assets')

# --- 2. FUNGSI CETAK STRUK ---
def generate_receipt(row):
    pdf = FPDF(format=(80, 150))
    pdf.add_page()
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "ES TELER FATIMAH", ln=True, align='C')
    pdf.set_font("Arial", '', 8)
    pdf.cell(0, 5, f"Waktu: {row['Waktu']}", ln=True, align='C')
    pdf.cell(0, 5, "-"*30, ln=True, align='C')
    
    pdf.set_font("Arial", '', 9)
    items = str(row['Produk']).split(", ")
    for item in items:
        pdf.cell(0, 7, item, ln=True)
    
    pdf.cell(0, 5, "-"*30, ln=True, align='C')
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 10, f"TOTAL: IDR {row['Total']:,}", ln=True, align='R')
    pdf.set_font("Arial", 'I', 8)
    pdf.cell(0, 10, "Terima kasih atas kunjungannya!", ln=True, align='C')
    
    return pdf.output(dest='S').encode('latin-1')

# --- 3. CSS MODERN & SMOOTH UI ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #fcfcfd; }
    .admin-header {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 2.5rem; border-radius: 20px; color: white; margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    div[data-testid="stMetric"] {
        background: white; padding: 1.5rem; border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03); border: 1px solid #f1f5f9;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: #f1f5f9; padding: 6px; border-radius: 12px; }
    .stTabs [data-baseweb="tab"] { height: 45px; border-radius: 8px; color: #64748b; font-weight: 600; }
    .stTabs [aria-selected="true"] { background-color: white !important; color: #0f172a !important; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SISTEM LOGIN ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def logout():
    st.session_state.authenticated = False
    st.rerun()

if not st.session_state.authenticated:
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>🔐 Welcome to Admin</h2>", unsafe_allow_html=True)
        with st.form("login_form"):
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.form_submit_button("Masuk ke Dashboard", use_container_width=True):
                if u == "admin" and p == "admin":
                    st.session_state.authenticated = True
                    st.rerun()
                else: st.error("Akses ditolak!")
else:
    # --- HEADER ---
    st.markdown("""
        <div class="admin-header">
            <h1 style='margin:0; font-weight:700;'>Admin Dashboard</h1>
            <p style='opacity:0.7; margin-top:5px;'>Monitor pesanan dan inventori secara real-time.</p>
        </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["💎 Laporan Penjualan", "🛠️ Kelola Inventori", "➕ Tambah Produk"])

    # --- TAB 1: LAPORAN PENJUALAN ---
    with tab1:
        # Tombol Refresh Manual
        col_ref, _ = st.columns([1, 4])
        if col_ref.button("🔄 Refresh Data Pesanan", use_container_width=True):
            st.toast("Data diperbarui!")
            time.sleep(0.5)
            st.rerun()

        if os.path.exists(DB_PESANAN):
            # Membaca file pesanan
            df_p = pd.read_csv(DB_PESANAN)
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Omzet Total", f"IDR {df_p['Total'].sum():,}")
            c2.metric("Total Pesanan", len(df_p))
            c3.metric("Status Server", "🟢 Aktif")
            
            st.write("### 📜 Riwayat Transaksi Terbaru")
            # Urutkan dari yang terbaru (reverse)
            for index, row in df_p.iloc[::-1].iterrows():
                with st.expander(f"Order {row['Waktu']} - IDR {row['Total']:,}"):
                    st.write(f"**Item:** {row['Produk']}")
                    st.download_button(
                        label="🖨️ Download Struk (PDF)",
                        data=generate_receipt(row),
                        file_name=f"struk_{index}.pdf",
                        mime="application/pdf",
                        key=f"print_{index}"
                    )
            
            st.markdown("---")
            if st.button("🗑️ Hapus Semua Riwayat", type="secondary"):
                os.remove(DB_PESANAN)
                st.rerun()
        else:
            st.info("Belum ada transaksi masuk. Gunakan tombol refresh jika pesanan baru belum muncul.")

    # --- TAB 2: KELOLA INVENTORI ---
    with tab2:
        st.write("### 🛠️ Pengaturan Produk")
        if os.path.exists(DB_MENU):
            df_m = pd.read_csv(DB_MENU)
            edited_df = st.data_editor(
                df_m, 
                use_container_width=True, 
                hide_index=True, 
                num_rows="dynamic",
                column_config={
                    "id": st.column_config.NumberColumn("ID", disabled=True),
                    "stok": st.column_config.NumberColumn("Sisa Stok", min_value=0),
                    "harga": st.column_config.NumberColumn("Harga (IDR)", format="IDR %d"),
                }
            )
            if st.button("💾 Simpan Perubahan Inventori", type="primary", use_container_width=True):
                edited_df.to_csv(DB_MENU, index=False)
                st.success("Inventori berhasil diperbarui!")
                st.rerun()
        else: st.error("File database_menu.csv tidak ditemukan.")

    # --- TAB 3: TAMBAH PRODUK ---
    with tab3:
        st.write("### ➕ Tambah Menu Baru")
        with st.form("add_menu_form", clear_on_submit=True):
            col_a, col_b = st.columns(2)
            with col_a:
                new_nama = st.text_input("Nama Produk")
                new_harga = st.number_input("Harga (IDR)", min_value=0, step=1000)
            with col_b:
                new_stok = st.number_input("Stok awal", min_value=0, value=10)
                uploaded_file = st.file_uploader("Foto Produk", type=['jpg', 'jpeg', 'png'])
            
            new_desc = st.text_area("Deskripsi Singkat")
            if st.form_submit_button("🚀 Daftarkan Produk Baru", use_container_width=True):
                if new_nama and uploaded_file:
                    img_path = os.path.join(ASSETS_DIR, uploaded_file.name)
                    with open(img_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    df_m = pd.read_csv(DB_MENU)
                    new_id = df_m['id'].max() + 1 if not df_m.empty else 1
                    new_row = {
                        "id": new_id, "nama": new_nama, "harga": new_harga,
                        "img": uploaded_file.name, "stok": new_stok, "desc": new_desc
                    }
                    df_m = pd.concat([df_m, pd.DataFrame([new_row])], ignore_index=True)
                    df_m.to_csv(DB_MENU, index=False)
                    st.success(f"Berhasil menambahkan {new_nama}!")
                    st.rerun()
                else: st.warning("Mohon isi Nama Produk dan Upload Gambar.")

    # Sidebar Logout
    with st.sidebar:
        st.write(f"Logged in as: **Admin**")
        if st.button("Secure Logout", use_container_width=True):
            logout()