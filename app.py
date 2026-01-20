import streamlit as st
import os
import pandas as pd
from datetime import datetime
import time # Penting untuk memberikan jeda notifikasi

# --- 1. PENGATURAN HALAMAN ---
st.set_page_config(page_title="ES TELER FATIMAH", layout="wide", page_icon="🍧")

# Path Database
DB_MENU = os.path.join(os.getcwd(), 'database_menu.csv')
DB_PESANAN = os.path.join(os.getcwd(), 'database_pesanan.csv')

# Load Data Menu
if os.path.exists(DB_MENU):
    menu_data = pd.read_csv(DB_MENU).to_dict('records')
else:
    menu_data = [
        {"id": 1, "nama": "Es Teler Signature", "harga": 10000, "img": "Es_Telercup1.jpeg", "stok": 10, "desc": "Perpaduan alpukat mentega, nangka manis, dan kelapa muda dengan krimer rahasia."},
        {"id": 2, "nama": "Kopi Gula Aren", "harga": 12000, "img": "Es_Kopisusu_gula_aren.jpeg", "stok": 5, "desc": "Espresso premium dengan susu segar dan pemanis gula aren alami pilihan."}
    ]
    pd.DataFrame(menu_data).to_csv(DB_MENU, index=False)

# --- 2. CSS CUSTOM: SHOPEE STYLE PREMIUM ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&family=Playfair+Display:ital,wght@0,700;1,700&display=swap');
    
    .stApp { background-color: #f8fafc; }
    html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }

    .hero-container {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 80px 40px;
        border-radius: 40px;
        text-align: center;
        margin: -4rem -2rem 3rem -2rem;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    }
    
    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: 3.5rem !important;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 10px;
    }

    /* KARTU PRODUK */
    div[data-testid="column"] > div {
        background: #ffffff;
        padding: 0px;
        border-radius: 24px;
        border: 1px solid #f1f5f9;
        transition: all 0.3s ease;
        overflow: hidden;
    }

    div[data-testid="column"] > div:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px -12px rgba(0, 0, 0, 0.1);
    }

    [data-testid="stImage"] img {
        width: 100% !important;
        aspect-ratio: 1 / 1 !important;
        object-fit: cover !important;
    }

    .product-card-body {
        padding: 16px;
        text-align: center;
    }

    .prod-name { 
        font-weight: 700; 
        font-size: 1.15rem; 
        color: #0f172a; 
        margin-bottom: 4px !important;
        min-height: 2.8rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .prod-desc { 
        font-weight: 300; 
        font-size: 0.8rem; 
        color: #64748b; 
        margin-bottom: 12px !important; 
        line-height: 1.3;
        font-style: italic;
        min-height: 3.2rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .price-tag { color: #10b981; font-weight: 800; font-size: 1.4rem; margin-bottom: 0px !important; }
    .sold-out-tag { color: #ef4444; font-weight: 800; font-size: 1.4rem; margin-bottom: 0px !important; }

    div.stButton > button {
        background: #0f172a; color: #ffffff; border-radius: 12px;
        font-weight: 600; padding: 10px; border: none; width: 100%;
        margin-top: 10px;
    }
    div.stButton > button:hover { background: #10b981; color: white; }
    div.stButton > button:disabled { background-color: #f1f5f9 !important; color: #94a3b8 !important; }

    .section-header {
        font-family: 'Playfair Display', serif; font-size: 2rem; font-weight: 700;
        color: #0f172a; margin-bottom: 30px; border-left: 6px solid #10b981; padding-left: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HERO SECTION ---
st.markdown("""
    <div class="hero-container">
        <div style="color: #94a3b8; letter-spacing: 2px; text-transform: uppercase; font-weight: 300; font-size: 0.8rem;">The Art of Refreshment</div>
        <div class="hero-title">ES TELER FATIMAH</div>
        <p style="color: #94a3b8; font-size: 1rem; opacity: 0.8;">Nikmati kemewahan rasa dalam setiap tegukan premium.</p>
    </div>
    """, unsafe_allow_html=True)

# --- 4. DAFTAR MENU ---
st.markdown('<div class="section-header">Daftar Menu</div>', unsafe_allow_html=True)

if menu_data:
    cols = st.columns(3, gap="large")
    for idx, item in enumerate(menu_data):
        with cols[idx % 3]:
            img_path = os.path.join("Assets", str(item['img']))
            if os.path.exists(img_path):
                st.image(img_path, use_container_width=True)
            else:
                st.error("Image Missing")
            
            deskripsi = item.get('desc', 'Kesegaran istimewa pilihan keluarga.')
            stok_sekarang = item.get('stok', 1)
            
            if stok_sekarang <= 0:
                price_html = f'<div class="sold-out-tag">SOLD OUT</div>'
                btn_label = "Habis Terjual"
                is_disabled = True
            else:
                price_html = f'<div class="price-tag">IDR {int(item["harga"]):,}</div>'
                btn_label = "Masukan Keranjang"
                is_disabled = False

            st.markdown(f"""
                <div class="product-card-body">
                    <div class="prod-name">{item['nama']}</div>
                    <div class="prod-desc">{deskripsi}</div>
                    {price_html}
                </div>
            """, unsafe_allow_html=True)
            
            if st.button(btn_label, key=f"btn_{idx}", disabled=is_disabled):
                if 'cart' not in st.session_state: st.session_state.cart = {}
                st.session_state.cart[item['nama']] = st.session_state.cart.get(item['nama'], 0) + 1
                st.toast(f"🌟 {item['nama']} ditambahkan!")

# --- 5. SIDEBAR KERANJANG ---
with st.sidebar:
    st.markdown("<h2 style='font-family: Playfair Display; font-size: 1.8rem;'>Keranjang saya</h2>", unsafe_allow_html=True)
    st.divider()
    
    if 'cart' not in st.session_state or not st.session_state.cart:
        st.info("keranjang mu kosong silahkan order terlebih dahulu.")
    else:
        total_belanja = 0
        sum_items = []
        for name, qty in list(st.session_state.cart.items()):
            price = next((m['harga'] for m in menu_data if m['nama'] == name), 0)
            subtotal = price * qty
            total_belanja += subtotal
            sum_items.append(f"{name} ({qty}x)")
            
            st.markdown(f"""
                <div style="background: white; padding: 12px; border-radius: 12px; margin-bottom: 8px; border: 1px solid #f1f5f9;">
                    <span style="font-weight: 600; color: #0f172a; font-size: 0.9rem;">{name}</span><br>
                    <span style="color: #64748b; font-size: 0.8rem;">{qty}x — IDR {subtotal:,}</span>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Remove", key=f"del_{name}"):
                del st.session_state.cart[name]
                st.rerun()
        
        st.divider()
        st.markdown(f"<h3 style='text-align: right; color: #0f172a; font-size: 1.2rem;'>Total: IDR {total_belanja:,}</h3>", unsafe_allow_html=True)
        
        if st.button("Place Order Now", use_container_width=True, type="primary"):
            waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_order = pd.DataFrame([[waktu, ", ".join(sum_items), total_belanja, "Selesai"]], 
                                    columns=["Waktu", "Produk", "Total", "Status"])
            
            if not os.path.exists(DB_PESANAN): 
                new_order.to_csv(DB_PESANAN, index=False)
            else: 
                new_order.to_csv(DB_PESANAN, mode='a', index=False, header=False)
            
            # Reset Keranjang
            st.session_state.cart = {}
            
            # Efek Visual Berhasil
            st.balloons()
            st.success("✅ Order Placed Successfully!")
            st.toast("Pesanan Anda sedang kami proses.")
            
            # Beri jeda agar user melihat notifikasi sebelum halaman reload
            time.sleep(2.5)
            st.rerun()