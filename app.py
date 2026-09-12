import streamlit as st
import pandas as pd
import os
from urllib.parse import quote
from datetime import datetime

# ===== Page & Company =====
st.set_page_config(page_title="MEDCARE LABS Company Store", page_icon="🧬", layout="wide")

COMPANY = {
    "name": "MEDCARE LABS Company Store",
    "tagline": "--WE CARE FOR YOUR HEALTH--",
    "address": "Berger, Lagos",
    "whatsapp": "2347070496138",
    "founder": "Feyisara Olatunji",
    "email": "feyishababe@gmail.com"
}

USD_RATE = 1500

if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'page' not in st.session_state:
    st.session_state.page = "home"
if 'selected_product' not in st.session_state:
    st.session_state.selected_product = None

# ===== BEAUTY CSS - Medical Blue & White =====
st.markdown("""
<style>
.stApp { background: #f8fbff; }
.med-banner {
    background: linear-gradient(135deg, #0a4da1 0%, #0e8ecf 100%);
    color: white; padding: 30px; border-radius: 20px; text-align: center;
    box-shadow: 0 8px 25px rgba(10,77,161,0.25);
}
.med-banner h1 { font-size: 32px; margin: 0; letter-spacing: 1px; }
.med-banner p { opacity: 0.9; margin: 5px 0; }
.product-card {
    background: white; border-radius: 18px; padding: 16px;
    border: 1px solid #e0e7ff; box-shadow: 0 6px 18px rgba(0,0,0,0.06);
    transition: 0.2s; height: 100%;
}
.product-card:hover { transform: translateY(-4px); box-shadow: 0 12px 30px rgba(0,0,0,0.12); }
.price-ngn { color: #0a7e07; font-weight: 800; font-size: 20px; }
.price-usd { color: #64748b; font-size: 13px; }
.stock-in { background: #dcfce7; color: #166534; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; }
.stock-out { background: #fee2e2; color: #991b1b; padding: 4px 12px; border-radius: 20px; font-size: 12px; }
.footer { text-align:center; color:#64748b; padding: 30px; margin-top: 40px; border-top: 1px solid #e2e8f0; }
</style>
""", unsafe_allow_html=True)

# ===== Banner =====
st.markdown(f"""
<div class="med-banner">
<h1>🧬 {COMPANY['name']}</h1>
<h3>{COMPANY['tagline']}</h3>
<p>📍 {COMPANY['address']} | 📞 {COMPANY['phone']} | 💬 {COMPANY['whatsapp']}</p>
</div>
""", unsafe_allow_html=True)

# ===== LOAD PRODUCTS FROM GOOGLE DRIVE SHEET (Not Hardcoded) =====
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Yt_tCJ752RyYBpRlZJzh9pFBQAKM3gyo/export?format=csv"

def drive_to_direct(link):
    if not isinstance(link, str) or not link: return ""
    if "drive.google.com" in link:
        try:
            if "/d/" in link:
                fid = link.split("/d/")[1].split("/")[0]
            else:
                fid = link.split("id=")[1].split("&")[0]
            return f"https://drive.google.com/uc?export=view&id={fid}"
        except:
            return link
    return link

def clean_price(v):
    if pd.isna(v): return 0
    s = str(v).replace("₦","").replace("$","").replace(",","").replace("NGN","").strip()
    try: return float(s)
    except: return 0

@st.cache_data(ttl=120)
def load_products():
    df = pd.read_csv(SHEET_URL)
    df.columns = [c.strip() for c in df.columns]
    # Map any column names you use
    rename = {}
    for c in df.columns:
        l = c.lower()
        if "price" in l or "cost" in l: rename[c] = "Price"
        elif l in ["name","product","item","product name"]: rename[c] = "Name"
        elif "desc" in l or "spec" in l or "use" in l: rename[c] = "Description"
        elif "image" in l or "photo" in l or "picture" in l or "link" in l: rename[c] = "Image"
        elif "categ" in l or "type" in l: rename[c] = "Category"
        elif "stock" in l or "avail" in l: rename[c] = "Stock"
        elif "id" == l or "code" in l: rename[c] = "ID"
    df = df.rename(columns=rename)
    if "Price" not in df.columns: df["Price"] = 0
    if "Name" not in df.columns: df["Name"] = "Lab Equipment"
    if "Description" not in df.columns: df["Description"] = "Quality laboratory equipment"
    if "Category" not in df.columns: df["Category"] = "General"
    if "Stock" not in df.columns: df["Stock"] = "In Stock"
    if "Image" not in df.columns: df["Image"] = ""
    if "ID" not in df.columns: df["ID"] = df.index

    df["Price"] = df["Price"].apply(clean_price)
    df["Image"] = df["Image"].apply(drive_to_direct)
    return df

df = load_products()

# ===== Founder Image (NO ADMIN HINT) =====
def get_founder_image():
    for fname in ["founder.jpg","founder.png","feyisara.jpg","profile.jpg","mothers_business.jpg"]:
        if os.path.exists(fname):
            return fname
    return None

# ===== Sidebar =====
with st.sidebar:
    st.title("MEDCARE LABS")
    st.write(COMPANY['tagline'])
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = "home"
        st.session_state.selected_product = None
        st.rerun()
    if st.button(f"🧺 Cart ({len(st.session_state.cart)})", use_container_width=True):
        st.session_state.page = "cart"
        st.rerun()
    if st.button("💬 WhatsApp Us", use_container_width=True):
        st.markdown(f"[Chat Now](https://wa.me/{COMPANY['whatsapp']})")
    st.divider()
    st.write(f"📍 {COMPANY['address']}")
    st.write(f"📞 {COMPANY['phone']}")

# ===== Home / Shop =====
if st.session_state.page == "home":
    colA, colB = st.columns([1,2])
    with colA:
        fimg = get_founder_image()
        if fimg:
            st.image(fimg, caption=COMPANY['founder'], use_container_width=True)
        else:
            st.image("https://cdn-icons-png.flaticon.com/512/3774/3774294.png", width=180)
    with colB:
        st.subheader("Supplier of laboratory equipment and medical devices")
        st.write("We supply microscopes, centrifuges, analyzers, BH-70P and more. Trusted by labs nationwide from Berger, Lagos.")
        st.write("**Business WhatsApp:** 0707 049 6138 - Human to human support")

    st.divider()

    # Search & Filters - Part 4
    c1, c2, c3 = st.columns([2,1,1])
    with c1:
        search = st.text_input("🔍 Search by product name", placeholder="Search microscope, centrifuge, analyzer...")
    with c2:
        cats = ["All"] + sorted(df["Category"].astype(str).unique().tolist())
        sel_cat = st.selectbox("Category", cats)
    with c3:
        sort_opt = st.selectbox("Price filter", ["Default", "Low to High", "High to Low"])

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
            # Beautiful Product Card
            with st.container(border=True):
                img = row.get("Image","")
                if img and "http" in str(img):
                    st.image(img, use_container_width=True)
                else:
                    st.image("https://images.unsplash.com/photo-1582719471384-894fbb16e074?w=400", use_container_width=True)

                st.markdown(f"**{row['Name']}**")
                st.caption(f"{str(row['Description'])[:90]}")

                stock = str(row.get("Stock","In Stock"))
                if "out" in stock.lower():
                    st.markdown(f"<span class='stock-out'>Out of Stock</span>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<span class='stock-in'>In Stock</span>", unsafe_allow_html=True)

                usd = float(row.get("Price",0))
                # Handle if price is already in NGN (if >1000 assume NGN, convert)
                if usd > 1000:
                    ngn = usd
                    usd_calc = usd / USD_RATE
                else:
                    usd_calc = usd
                    ngn = usd * USD_RATE

                st.markdown(f"<div class='price-ngn'>₦{ngn:,.0f}</div><div class='price-usd'>${usd_calc:,.2f}</div>", unsafe_allow_html=True)
                st.caption(f"ID: {row.get('ID','')} | {row.get('Category','')}")

                b1, b2 = st.columns(2)
                with b1:
                    if st.button("Details", key=f"det_{i}", use_container_width=True):
                        st.session_state.selected_product = row.to_dict()
                        st.session_state.page = "details"
                        st.rerun()
                with b2:
                    if "out" not in stock.lower():
                        if st.button("Add to Cart", key=f"add_{i}", type="primary", use_container_width=True):
                            found=False
                            for it in st.session_state.cart:
                                if it["Name"]==row["Name"]:
                                    it["qty"]+=1
                                    found=True
                            if not found:
                                st.session_state.cart.append({"Name":row["Name"],"Price":usd_calc,"PriceNGN":ngn,"qty":1})
                            st.toast(f"Added {row['Name']}")

# ===== Details Page =====
elif st.session_state.page == "details":
    if st.button("← Back to Products"):
        st.session_state.page = "home"
        st.rerun()
    p = st.session_state.selected_product
    if p:
        c1,c2 = st.columns(2)
        with c1:
            if p.get("Image"): st.image(p["Image"], use_container_width=True)
        with c2:
            st.title(p["Name"])
            st.write(f"**Category:** {p.get('Category')}")
            st.write(f"**Stock Status:** {p.get('Stock')}")
            st.write(f"**Specs / Use:** {p.get('Description')}")
            usd = float(p.get("Price",0))
            ngn = usd*USD_RATE if usd<1000 else usd
            usd_show = usd if usd<1000 else usd/USD_RATE
            st.write(f"### 💰 ${usd_show:.2f} / ₦{ngn:,.0f}")
            if st.button("Add to Cart 🛒", use_container_width=True, type="primary"):
                st.session_state.cart.append({"Name":p["Name"],"Price":usd_show,"PriceNGN":ngn,"qty":1})
                st.session_state.page = "cart"
                st.rerun()

# ===== Cart + WhatsApp + Customer Data =====
elif st.session_state.page == "cart":
    if st.button("← Continue Shopping"):
        st.session_state.page = "home"
        st.rerun()
    st.header("🛒 Shopping Cart and WhatsApp Shopping")
    if not st.session_state.cart:
        st.info("Your cart is empty")
    else:
        total_usd = 0
        total_ngn = 0
        for idx, item in enumerate(st.session_state.cart):
            col1,col2,col3,col4 = st.columns([3,1,1,1])
            with col1: st.write(f"**{item['Name']}** - ${item['Price']:.2f}")
            with col2:
                if st.button("➖", key=f"m_{idx}"):
                    item["qty"] = max(1, item["qty"]-1)
                    st.rerun()
            with col3: st.write(f"Qty: {item['qty']}")
            with col4:
                if st.button("➕", key=f"p_{idx}"):
                    item["qty"]+=1
                    st.rerun()
            total_usd += item["Price"]*item["qty"]
            total_ngn += item.get("PriceNGN", item["Price"]*USD_RATE)*item["qty"]

        st.divider()
        st.subheader(f"Total: ${total_usd:.2f} | ₦{total_ngn:,.0f} - Automatic sum in $ and Naira")

        # Customer Data Collection - Part 6
        st.subheader("Customer Data Collection")
        cust_name = st.text_input("Customer Name (like Manager_Name)", placeholder="Your full name")
        branch = st.text_input("Branch Office / Delivery Location (like Branch_Office)", placeholder="e.g. Berger, Lagos - Your delivery address")

        if cust_name and branch:
            machine_list = ", ".join([f"{x['Name']} x{x['qty']}" for x in st.session_state.cart])
            # Using f-string like you requested
            order_summary = f"Most Important Machine: {machine_list}"

            wa_text = f"""Hello MEDCARE LABS {COMPANY['tagline']}
NEW ORDER:
Customer Name: {cust_name}
Branch Office / Delivery Location: {branch}
{order_summary}
"""
            for it in st.session_state.cart:
                wa_text += f"- {it['Name']} x{it['qty']} = ${it['Price']*it['qty']:.2f} / NGN {it.get('PriceNGN',0)*it['qty']:,.0f}\n"
            wa_text += f"\nTOTAL: ${total_usd:.2f} / ₦{total_ngn:,.0f}\nDelivery: Nationwide from Berger, Lagos\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M')}"

            wa_url = f"https://wa.me/{COMPANY['whatsapp']}?text={quote(wa_text)}"
            st.link_button("🟢 WhatsApp Order Button - One-click order to 0707 049 6138", wa_url, use_container_width=True, type="primary")
        else:
            st.warning("Enter Customer Name and Delivery Location to enable WhatsApp order")

        if st.button("Clear Cart"):
            st.session_state.cart = []
            st.rerun()

# ===== Footer - Part 10 =====
st.markdown(f"""
<div class="footer">
© 2026 MEDCARE LABS - WE CARE FOR YOUR HEALTH<br>
Products for medical laboratory use only<br>
Secure HTTPS | Works on Chrome, Safari, Google Search<br>
Payment: WhatsApp negotiation / Bank transfer / Pay on delivery | Delivery: Nationwide from Berger, Lagos<br>
Direct WhatsApp chat: Human to human, no bot | Order Tracking: Via WhatsApp conversation | Support: 0707 049 6138
</div>
""", unsafe_allow_html=True)
