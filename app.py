import streamlit as st
import pandas as pd
import os
from urllib.parse import quote

st.set_page_config(page_title="MEDCARE LABS Company Store", page_icon="🧬", layout="wide")

COMPANY_NAME = "MEDCARE LABS Company Store"
TAGLINE = "--WE CARE FOR YOUR HEALTH--"
WHATSAPP = "2347070496138"
DISPLAY = "0707 049 6138"
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
.footer { text-align:center; color:#64748b; padding: 20px; margin-top: 30px; border-top: 1px solid #e2e8f0; }
.price-ngn { color: #0a7e07; font-weight: 800; font-size: 18px; }
</style>
""", unsafe_allow_html=True)

st.markdown(f"<div class='med-banner'><h1>{COMPANY_NAME}</h1><h3>{TAGLINE}</h3><p>Berger, Lagos | WhatsApp {DISPLAY}</p></div>", unsafe_allow_html=True)

SHEET_URL = "https://docs.google.com/spreadsheets/d/1Yt_tCJ752RyYBpRlZJzh9pFBQAKM3gyo/export?format=csv"

def drive_to_direct(link):
    try:
        if not isinstance(link, str) or link == "":
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
        s = s.replace("₦","").replace("$","").replace(",","").replace("NGN","")
        return float(s)
    except:
        return 0

def load_products():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = [c.strip() for c in df.columns]
        # rename
        new_cols = {}
        for c in df.columns:
            low = c.lower()
            if "price" in low or "cost" in low:
                new_cols[c] = "Price"
            if low in ["name","product","item"]:
                new_cols[c] = "Name"
            if "desc" in low or "spec" in low:
                new_cols[c] = "Description"
            if "image" in low or "photo" in low or "link" in low:
                new_cols[c] = "Image"
            if "categ" in low:
                new_cols[c] = "Category"
            if "stock" in low:
                new_cols[c] = "Stock"
            if low == "id":
                new_cols[c] = "ID"
        df = df.rename(columns=new_cols)
        # fill missing
        if "Price" not in df.columns:
            df["Price"] = 0
        if "Name" not in df.columns:
            df["Name"] = "Lab Product"
        if "Description" not in df.columns:
            df["Description"] = "Quality lab equipment"
        if "Category" not in df.columns:
            df["Category"] = "General"
        if "Stock" not in df.columns:
            df["Stock"] = "In Stock"
        if "Image" not in df.columns:
            df["Image"] = ""
        if "ID" not in df.columns:
            df["ID"] = list
