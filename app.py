import streamlit as st
import pandas as pd
import os
from urllib.parse import quote

st.set_page_config(page_title="MEDCARE LABS Official Store", layout="centered")

USD_RATE = 1500
WHATSAPP = "2347070496138"
DISPLAY = "0707 049 6138"
EMAIL = "feyishababe@gmail.com"

if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'show_store' not in st.session_state:
    st.session_state.show_store = False

SHEET_URL = "https://docs.google.com/spreadsheets/d/1Yt_tCJ752RyYBpRlZJzh9pFBQAKM3gyo/export?format=csv"

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

@st.cache_data
def load_products():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = [c.strip() for c in df.columns]
        # normalize
        rename = {}
        for c in df.columns:
            low = c.lower()
            if "price" in low:
                rename[c] = "Price"
            elif low in ["name","product","item","product name"]:
                rename[c] = "Name"
            elif "id" == low or "code" in low:
                rename[c] = "ID"
            elif "categ" in low or "type" in low:
                rename[c] = "Category"
            elif "desc" in low:
                rename[c] = "Description"
        df = df.rename(columns=rename)
        df["Price"] = df["Price"].apply(safe_price)
        return df
    except:
        return pd.DataFrame([
            {"ID":"MED-LAB-001","Name":"Centrifuge Machine","Price":185,"Category":"Sample Prep","Description":"Lab centrifuge"},
            {"ID":"MED-LAB-002","Name":"Spectrophotometer","Price":380,"Category":"Analytical","Description":"Lab spectro"},
            {"ID":"MED-LAB-007","Name":"Analytical Balance","Price":420,"Category":"Measurement","Description":"Precision balance"},
            {"ID":"MED-LAB-009","Name":"Micropipette Set","Price":55,"Category":"Liquid Handling","Description":"Micropipette"},
            {"ID":"MED-LAB-011","Name":"Vortex Mixer","Price":125,"Category":"Sample Prep","Description":"Vortex"},
            {"ID":"MED-LAB-013","Name":"Refrig Centrifuge","Price":1950,"Category":"Sample Prep","Description":"Refrigerated"},
        ])

df = load_products()

def get_founder_image():
    for f in ["IMG_0262.jpeg", "IMG_0262.jpg", "founder.jpg", "founder.png", "feyisara.jpg"]:
        if os.path.exists(f):
            return f
    return None


# ---- BEAUTIFUL ORIGINAL DESIGN ----
if not st.session_state.show_store:
    st.markdown("<h2 style='color:#0a3d6b; text-align:center;'>Welcome Valued Customer</h2>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center;'>Welcome to<br>MEDCARE LABS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:gray;'>Berger, Lagos | Trusted Lab Equipment Supplier</p>", unsafe_allow_html=True)

    fimg = get_founder_image()
    if fimg:
        st.image(fimg, caption="Meet Feyisara Olatunji", use_container_width=True)
    else:
        st.image("https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=600", use_container_width=True)

    st.markdown("""
    <div style='background:#e6f4ea; padding:12px; border-radius:10px;'>
    <b>👩‍🔬 Founder & CEO: Feyisara Olatunji</b><br>

    </div>
    """, unsafe_allow_html=True)

    st.subheader("Meet Feyisara Olatunji")
    st.write("Dear Valued Customer,")
    st.write("On behalf of the entire MEDCARE family, I warmly welcome you to our official online store.")
    st.write("I am Feyisara Olatunji, founder of MEDCARE LABS. My journey started with a simple vision: to make high-quality, reliable laboratory equipment accessible to every hospital, clinic, and research lab in Nigeria.")
    st.write("From our base in Berger, Lagos, Nigeria, we have served hundreds of clients who trust us for authenticity and after-sales support.")
    st.write("Every product you see in this store has been carefully selected for durability, accuracy, and value for money. Whether you are setting up a new lab or upgrading your current facility, my team and I are here to support you.")
    st.write("Thank you for choosing us. We value your trust.")
    st.write("Warmly,")
    st.write("**Feyisara Olatunji Founder & CEO, MEDCARE LABS**")

    st.markdown(f"📍 Berger, Lagos, Nigeria | 📞 {DISPLAY} | {EMAIL}")

    if st.button("CONTINUE TO STORE →", type="primary", use_container_width=True):
        st.session_state.show_store = True
        st.rerun()

else:
    st.markdown("<h2 style='text-align:center;'>MEDCARE LABS - Official Store</h2>", unsafe_allow_html=True)
    if st.button("← Back to Welcome"):
        st.session_state.show_store = False
        st.rerun()

    # Search
    search = st.text_input("Search products", placeholder="Microscope, centrifuge...")

    filtered = df.copy()
    if search:
        filtered = filtered[filtered["Name"].astype(str).str.contains(search, case=False, na=False)]

    for i, row in filtered.iterrows():
        price_usd = float(row.get("Price",0))
        # if price is already NGN big, convert to USD for display
        if price_usd > 1000:
            usd_show = price_usd / USD_RATE
            ngn_show = price_usd
        else:
            usd_show = price_usd
            ngn_show = price_usd * USD_RATE

        with st.container(border=True):
            st.write(f"**{row.get('Name','Product')}**")
            st.caption(f"{row.get('ID','MED-LAB')} | {row.get('Category','General')}")
            st.write(f"💰 ${usd_show:.0f} | ₦{ngn_show:,.0f}")
            if st.button("Add to Cart", key=f"add_{i}"):
                st.session_state.cart.append({
                    "Name": row.get('Name'),
                    "USD": usd_show,
                    "NGN": ngn_show
                })
                st.toast(f"Added {row.get('Name')}")

    # YOUR ORDER
    if st.session_state.cart:
        st.divider()
        st.subheader("🛒 Your Order")
        # Build table
        order_df = pd.DataFrame(st.session_state.cart)
        # group by name to sum qty like video
        summary = {}
        for item in st.session_state.cart:
            key = item["Name"]
            if key not in summary:
                summary[key] = {"USD": item["USD"], "NGN": item["NGN"], "qty": 0}
            summary[key]["qty"] += 1

        total_usd = 0
        total_ngn = 0
        st.markdown("| Name | USD | NGN |")
        st.markdown("|---|---|---|")
        for name, val in summary.items():
            usd_total = val["USD"] * val["qty"]
            ngn_total = val["NGN"] * val["qty"]
            total_usd += usd_total
            total_ngn += ngn_total
            # if qty >1 show once per qty as in video
            for _ in range(val["qty"]):
                st.write(f"{name} | {val['USD']:.0f} | {val['NGN']:.0f}")

        st.write(f"**Total: ${total_usd:.0f} / ₦{total_ngn:,.0f}**")

        # WhatsApp message exactly like video
        wa_lines = []
        for name in summary:
            # repeat for qty to match video style
            for _ in range(summary[name]["qty"]):
                wa_lines.append(f"- {name}")

        wa_text = f"Hello MEDCARE LABS, I want to order:\n"
        for line in wa_lines:
            wa_text += f"{line}\n"
        wa_text += f"Total ${total_usd:.0f}"

        wa_url = f"https://wa.me/{WHATSAPP}?text={quote(wa_text)}"
        st.link_button("📲 WhatsApp Order", wa_url, type="primary", use_container_width=True)

        if st.button("Clear Cart"):
            st.session_state.cart = []
            st.rerun()

    st.markdown(f"<p style='text-align:center; font-size:12px; color:gray; margin-top:30px;'>© 2026 MEDCARE LABS | Founded by Feyisara Olatunji<br>| Berger, Lagos, Nigeria | WhatsApp: {DISPLAY}</p>", unsafe_allow_html=True)
