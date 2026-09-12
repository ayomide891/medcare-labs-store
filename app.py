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

# ===== LOAD FROM GOOGLE SHEET - FIXED ERROR =====
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
    except Exception as e:
        return pd.DataFrame([
            {"ID":"001","Name":"Binocular Microscope","Price":50,"Description":"2000X LED microscope","Category":"Microscope","Stock":"In Stock","Image":""},
            {"ID":"002","Name":"Centrifuge Machine","Price":80,"Description":"Lab centrifuge 4000rpm","Category":"Centrifuge","Stock":"In Stock","Image":""},
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
        st.session_state.page = "home"
        st.rerun()
    if st.button(f"🧺 Cart ({len(st.session_state.cart)})", use_container_width=True):
        st.session_state.page = "cart"
        st.rerun()
    st.divider()
    st.write(f"📍 {COMPANY['address']}")
    st.write(f"💬 {COMPANY['whatsapp_display']}")

if st.session_state.page == "home":
    c1, c2 = st.columns([1,2])
    with c1:
        fimg = get_founder_image()
        if fimg:
            st.image(fimg, use_container_width=True)
    with c2:
        st.write("### Supplier of laboratory equipment and medical devices")
        st.write("Trusted by labs nationwide from Berger, Lagos.")
        st.write(f"**Business WhatsApp: {COMPANY['whatsapp_display']}** - Human to human support")

    st.divider()
    s1, s2, s3 = st.columns([2,1,1])
    with s1:
        search = st.text_input("🔍 Search", placeholder="Microscope, centrifuge...")
    with s2:
        cats = ["All"] + sorted(df["Category"].astype(str).unique().tolist())
        sel_cat = st.selectbox("Category", cats)
    with s3:
        sort_opt = st.selectbox("Price", ["Default","Low to High","High to Low"])

    filtered = df.copy()
    if search:
        filtered = filtered[filtered["Name"].astype(str).str.contains(search, case=False, na=False)]
    if sel_cat!= "All":
        filtered = filtered[filtered["Category"] == sel_cat]
    if sort_opt == "Low to High":
        filtered = filtered.sort_values("Price")
    elif sort_opt == "High to Low":
        filtered = filtered.sort_values("Price", ascending=False)

    st.subheader(f"Our Products - {len(filtered)} items")
    cols = st.columns(3)
    for idx, (i, row) in enumerate(filtered.iterrows()):
        with cols[idx % 3]:
            with st.container(border=True):
                img = row.get("Image","")
                if img and "http" in str(img):
                    st.image(img, use_container_width=True)
                else:
                    st.image("https://images.unsplash.com/photo-1582719471384-894fbb16e074?w=400", use_container_width=True)
                st.write(f"**{row['Name']}**")
                st.caption(str(row['Description'])[:80])
                usd = float(row.get("Price",0))
                ngn = usd*USD_RATE if usd < 1000 else usd
                usd_show = usd if usd < 1000 else usd/USD_RATE
                st.markdown(f"<div class='price-ngn'>₦{ngn:,.0f}</div><div class='price-usd'>${usd_show:.2f}</div>", unsafe_allow_html=True)
                b1, b2 = st.columns(2)
                with b1:
                    if st.button("Details", key=f"d_{i}", use_container_width=True):
                        st.session_state.selected_product = row.to_dict()
                        st.session_state.page = "details"
                        st.rerun()
                with b2:
                    if st.button("Add to Cart", key=f"a_{i}", type="primary", use_container_width=True):
                        found=False
                        for it in st.session_state.cart:
                            if it["Name"]==row["Name"]:
                                it["qty"]+=1
                                found=True
                        if not found:
                            st.session_state.cart.append({"Name":row["Name"],"Price":usd_show,"PriceNGN":ngn,"qty":1})
                        st.toast("Added!")

elif st.session_state.page == "details":
    if st.button("← Back"):
        st.session_state.page = "home"
        st.rerun()
    p = st.session_state.selected_product
    if p:
        c1,c2 = st.columns(2)
        with c1:
            if p.get("Image"): st.image(p["Image"], use_container_width=True)
        with c2:
            st.title(p["Name"])
            st.write(p["Description"])
            usd = float(p.get("Price",0))
            ngn = usd*USD_RATE if usd < 1000 else usd
            st.write(f"### ${usd if usd<1000 else usd/USD_RATE:.2f} / ₦{ngn:,.0f}")
            if st.button("Add to Cart 🛒", type="primary", use_container_width=True):
                st.session_state.cart.append({"Name":p["Name"],"Price":usd if usd<1000 else usd/USD_RATE,"PriceNGN":ngn,"qty":1})
                st.session_state.page = "cart"
                st.rerun()

elif st.session_state.page == "cart":
    if st.button("← Continue Shopping"):
        st.session_state.page = "home"
        st.rerun()
    st.header("🛒 Cart + WhatsApp Shopping")
    if not st.session_state.cart:
        st.info("Cart empty")
    else:
        total_usd=0
        total_ngn=0
        for idx, item in enumerate(st.session_state.cart):
            c1,c2,c3,c4 = st.columns([3,1,1,1])
            with c1: st.write(f"**{item['Name']}**")
            with c2:
                if st.button("➖", key=f"mm_{idx}"):
                    item["qty"]=max(1,item["qty"]-1)
                    st.rerun()
            with c3
