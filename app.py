import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="MEDCARE LABS STORE", layout="wide")

COMPANY = {
    "name": "MEDCARE LABS",
    "address": "Berger, Lagos, Nigeria",
    "phone": "09142981813",
    "email": "feyishababe@gmail.com",
    "founder": "Feyisara Olatunji",
    "whatsapp": "2347070496138"}

if 'page' not in st.session_state:
    st.session_state.page = "welcome"
if 'cart' not in st.session_state:
    st.session_state.cart = []

# --- GOOGLE SHEET FOR PRODUCTS ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Yt_tCJ752RyYBpRlZJzh9pFBQAKM3gyo/export?format=csv"

def convert_drive_link(link):
    """Convert Google Drive share link to direct image link"""
    if not isinstance(link, str):
        return link
    if "drive.google.com" in link and "id=" in link:
        try:
            file_id = link.split("id=")[1].split("&")[0]
            return f"https://drive.google.com/uc?export=view&id={file_id}"
        except:
            return link
    if "drive.google.com" in link and "/d/" in link:
        try:
            file_id = link.split("/d/")[1].split("/")[0]
            return f"https://drive.google.com/uc?export=view&id={file_id}"
        except:
            return link
    return link

@st.cache_data(ttl=60)
def load_products():
    try:
        df = pd.read_csv(SHEET_URL)
        # Clean column names
        df.columns = [c.strip() for c in df.columns]
        # Convert drive images if you have Image column
        if "Image" in df.columns:
            df["Image"] = df["Image"].apply(convert_drive_link)
        if "Image_URL" in df.columns:
            df["Image_URL"] = df["Image_URL"].apply(convert_drive_link)
        return df
    except Exception as e:
        st.error(f"Could not load Sheet: {e}")
        # Fallback
        data = [
            ["MED-LAB-001", "Binocular Microscope", "Professional lab microscope", "50000", ""],
            ["MED-LAB-002", "Centrifuge Machine", "Sample preparation centrifuge", "75000", ""],
        ]
        return pd.DataFrame(data, columns=["ID", "Name", "Description", "Price", "Image"])

df = load_products()

# --- Founder image helper (NO ADMIN HINT) ---
def get_founder_image():
    for fname in ["founder.jpg", "founder.png", "feyisara.jpg", "profile.jpg"]:
        if os.path.exists(fname):
            return fname
    return None

# --- SIDEBAR ---
st.sidebar.title(COMPANY["name"])
st.sidebar.write(COMPANY["address"])
if st.sidebar.button("🏠 Home"):
    st.session_state.page = "welcome"
if st.sidebar.button("🛒 Shop Products"):
    st.session_state.page = "shop"
if st.sidebar.button(f"🧺 Cart ({len(st.session_state.cart)})"):
    st.session_state.page = "cart"

st.sidebar.divider()
st.sidebar.write(f"📞 {COMPANY['phone']}")
st.sidebar.write(f"📧 {COMPANY['email']}")

# --- PAGES ---
if st.session_state.page == "welcome":
    st.title(f"Welcome to {COMPANY['name']}")
    st.subheader(f"Founded by {COMPANY['founder']}")

    col1, col2 = st.columns([1, 2])
    with col1:
        founder_img = get_founder_image()
        if founder_img:
            st.image(founder_img, caption=COMPANY["founder"], width=250)
        else:
            st.info("Add founder.jpg to GitHub repo to show your picture")

    with col2:
        st.write("### Quality Lab Equipment in Lagos")
        st.write("We supply microscopes, centrifuges, and all laboratory essentials.")
        st.write(f"**WhatsApp:** {COMPANY['whatsapp']}")
        if st.button("Start Shopping →"):
            st.session_state.page = "shop"
            st.rerun()

elif st.session_state.page == "shop":
    st.title("Our Products")
    st.write(f"Loaded {len(df)} products from Google Sheet")

    cols = st.columns(3)
    for i, row in df.iterrows():
        with cols[i % 3]:
            # Handle different possible column names
            name = row.get("Name", row.get("name", "Product"))
            price = row.get("Price", row.get("price", "0"))
            desc = row.get("Description", row.get("description", ""))
            img = row.get("Image", row.get("Image_URL", row.get("image", "")))

            if pd.notna(img) and img!= "":
                st.image(img, use_container_width=True)

            st.write(f"**{name}**")
            st.write(f"{desc}")
            st.write(f"**₦{price}**")

            if st.button("Add to Cart", key=f"add_{i}"):
                st.session_state.cart.append(row.to_dict())
                st.success(f"Added {name}")

elif st.session_state.page == "cart":
    st.title("Your Cart")
    if not st.session_state.cart:
        st.write("Cart is empty")
        if st.button("Go to Shop"):
            st.session_state.page = "shop"
            st.rerun()
    else:
        total = 0
        for item in st.session_state.cart:
            price_str = str(item.get("Price", item.get("price", "0"))).replace(",", "")
            try:
                total += float(price_str)
            except:
                pass
            st.write(f"- {item.get('Name')} - ₦{item.get('Price')}")

        st.divider()
        st.write(f"**Total: ₦{total}**")

        wa_text = f"Hello {COMPANY['name']}, I want to order: "
        for item in st.session_state.cart:
            wa_text += f"{item.get('Name')}, "
        wa_link = f"https://wa.me/{COMPANY['whatsapp']}?text={wa_text}"

        st.link_button("Order via WhatsApp", wa_link)

        if st.button("Clear Cart"):
            st.session_state.cart = []
            st.rerun()
