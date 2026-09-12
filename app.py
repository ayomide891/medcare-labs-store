import streamlit as st
import pandas as pd
import os
from urllib.parse import quote

st.set_page_config(page_title="MEDCARE LABS Company Store", page_icon="🧬", layout="wide")

COMPANY = {
    "name": "MEDCARE LABS Company Store",
    "tagline": "--WE CARE FOR YOUR HEALTH--",
    "address": "Berger, Lagos",
    "whatsapp": "2347070496138",
    "whatsapp_display": "0707 049 6138",
    "founder": "Feyisara Olatunji"
}
USD_RATE = 1500

if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'page' not in st.session_state:
    st.session_state.page = "home"
if 'selected_product' not in st.session_state:
    st.session_state.selected_product = None

st.markdown("""
<style>
.stApp { background: #f8fbff; }
.med-banner { background: linear-gradient(135deg, #0a4da1 0%, #0e8ecf 100%); color: white; padding: 28px; border-radius: 20px; text-align: center; }
.footer { text-align:center; color:#64748b; padding: 25px; margin-top: 30px; border-top: 1px solid #e2e8f0; }
.price-ngn { color: #0a7e07; font-weight: 800; font-size: 19px; }
.price-usd { color: #64748b; font-size: 13px; }
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="med-banner">
<h1>🧬 {COMPANY['name']}</h1>
<h3>{COMPANY['tagline']}</h3>
<p>📍 {COMPANY['address']} | 💬 Business WhatsApp {COMPANY['whatsapp_display']}</p>
</div>
""", unsafe_allow_html=True)

SHEET_URL = "https://docs.google.com/spreadsheets/d/1Yt_tCJ752RyYBpRlZJzh9pFBQAKM3gyo/export?format=csv"

def drive_to_direct(link):
    try:
        if not isinstance(link, str) or not link:
            return ""
        if "drive.google.com" in link:
            if "/d/" in link:
                fid = link.split("/d/")[1].split("/")[0]
            else:
                fid = link.split("id=")[1].split("&")[0]
            return f"https://drive.google.com/uc?export=view&id={fid}"
        return link
    except:
        return ""

def safe_price(v):
    try:
        if v is None:
            return 0
        s = str(v).strip()
        if s == "" or s.lower() in ["nan","none"]:
            return 0
        s = s.replace("₦","").replace("$","").replace(",","").replace("NGN","").strip()
        return float(s)
    except:
        return 0

def load_products():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = [c.strip() for c in df.columns]
        rename = {}
        for c in df.columns:
            l = c.lower()
            if "price" in l or "cost" in l:
                rename[c] = "Price"
            elif l in ["name","product","item","product name"]:
                rename[c] = "Name"
            elif "desc" in l or "spec" in l:
                rename[c] = "Description"
            elif "image" in l or "photo" in l or "picture" in l or "link" in l:
                rename[c] = "Image"
            elif "categ" in l or "type" in l:
                rename[c] = "Category"
            elif "stock" in l:
                rename[c] = "Stock"
            elif l == "id" or "code" in l:
                rename[c] = "ID"
        df = df.rename(columns=rename)
        if "Price" not in df.columns: df["Price"] = 0
        if "Name" not in df.columns: df["Name"] = "Lab Product"
        if "Description" not in df.columns: df["Description"] = "Quality lab equipment"
        if "Category" not in df.columns: df["Category"] = "General"
        if "Stock" not in df.columns: df["Stock"] = "In Stock"
        if "Image" not in df.columns: df["Image"] = ""
        if "ID" not in df.columns: df["ID"] = range(len(df))
        df["Price"] = df["Price"].apply(safe_price)
        df["Image"] = df["Image"].apply(drive_to_direct)
        df = df.dropna(subset=["Name"])
        return df
    except:
        return pd.DataFrame([
            {"ID":"001","Name":"Binocular Microscope","Price":50,"Description":"2000X LED microscope","Category":"Microscope","Stock":"In Stock","Image":""},
        ])

df = load_products()

def get_founder_image():
    for fname in ["founder.jpg","founder.png","feyisara.jpg","profile.jpg"]:
        if os.path.exists(fname):
            return fname
    return None

with st.sidebar:
    st.title("MEDCARE LABS")
    if st.button("🏠 Home", use_container_width=True):
