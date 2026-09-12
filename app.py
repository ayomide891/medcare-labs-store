import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="MEDCARE LABS - Official Store", page_icon="🧬", layout="wide")

COMPANY = {
    "name": "MEDCARE LABS",
    "address": "Berger, Lagos, Nigeria",
    "phone": "09142981813",
    "email": "feyishababe@gmail.com",
    "founder": "Feyisara Olatunji",
    "whatsapp": "2349142981813"
}

if 'page' not in st.session_state:
    st.session_state.page = "welcome"
if 'cart' not in st.session_state:
    st.session_state.cart = []

data = [
["MED-LAB-001","Binocular Microscope","Microscopy",320,480000,"In Stock",15],
["MED-LAB-002","Centrifuge Machine","Sample Prep",185,277500,"In Stock",12],
["MED-LAB-003","Autoclave 50L","Sterilization",890,1335000,"In Stock",8],
["MED-LAB-004","Spectrophotometer","Analytical",2450,3675000,"In Stock",5],
["MED-LAB-005","Incubator 80L","Culture",650,975000,"In Stock",10],
["MED-LAB-006","pH Meter","Measurement",95,142500,"In Stock",25],
["MED-LAB-007","Analytical Balance","Measurement",420,630000,"In Stock",9],
["MED-LAB-008","Hot Air Oven 30L","Sterilization",380,570000,"In Stock",7],
["MED-LAB-009","Micropipette Set","Liquid Handling",55,82500,"In Stock",40],
["MED-LAB-010","Water Bath 8 Hole","Culture",210,315000,"In Stock",11],
["MED-LAB-011","Vortex Mixer","Sample Prep",125,187500,"In Stock",18],
["MED-LAB-012","Mag Stirrer Hot Plate","Sample Prep",165,247500,"In Stock",14],
["MED-LAB-013","Refrig Centrifuge","Sample Prep",1950,2925000,"In Stock",4],
["MED-LAB-014","Biosafety Cabinet","Safety",2850,4275000,"In Stock",3],
["MED-LAB-015","PCR Thermal Cycler","Molecular",4200,6300000,"In Stock",2],
["MED-LAB-016","Gel Doc System","Molecular",7800,11700000,"In Stock",2],
["MED-LAB-017","Lab Refrigerator 150L","Storage",950,1425000,"In Stock",6],
["MED-LAB-018","Deep Freezer -86C","Storage",3200,4800000,"In Stock",3],
["MED-LAB-019","Hematology Analyzer","Diagnostic",3600,5400000,"In Stock",4],
["MED-LAB-020","Chemistry Analyzer","Diagnostic",1850,2775000,"In Stock",5],
]
df = pd.DataFrame(data, columns=["ID","Name","Category","USD","NGN","Status","Qty"])

# --- Helper to get founder image ---
def get_founder_image():
    # Check if you uploaded IMG
    if os.path.exists("IMG_0262.jpeg"):
        return "IMG_0262.jpeg"
    if os.path.exists("founder.jpg"):
        return "founder.jpg"
    if os.path.exists("founder.png"):
        return "founder.png"
    # Placeholder if not yet uploaded
    return "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=400&h=400&fit=crop"
    
    

# --   WELCOME PAGE ---
if st.session_state.page == "welcome":
    st.markdown("<h1 style='text-align:center; color:#0a4a7a; margin-top:20px;'>Welcome Valued Customer</h1>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align:center;'>Welcome to {COMPANY['name']}</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:gray;'>Berger, Lagos | Trusted Lab Equipment Supplier</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1,1.6], gap="large")
    
    with col1:
        img = get_founder_image()
        st.image(img, caption=f"Meet {COMPANY['founder']}", use_container_width=True)
        st.success(f"👩‍🔬 Founder & CEO: {COMPANY['founder']}")
        
        # Admin hint
        with st.expander("🔧 Founder: How to add your real picture"):
            st.write("1. Go to GitHub repo `medcare-labs-store`")
            st.write("2. Tap Add file → Upload files")
            st.write("3. Upload your best photo named exactly: `founder.jpg`")
            st.write("4. Commit → Your picture will appear automatically here!")
            upload = st.file_uploader("Preview your picture now (temporary)", type=["jpg","png"])
            if upload:
                st.image(upload, caption="Preview - Upload this to GitHub as founder.jpg to save")
    
    with col2:
        st.markdown(f"### Meet {COMPANY['founder']}")
        st.write(f"""
        **Dear Valued Customer,**

        On behalf of the entire {COMPANY['name']} family, I warmly welcome you to our official online store.

        I am **{COMPANY['founder']}**, founder of {COMPANY['name']}. My journey started with a simple vision: to make high-quality, reliable laboratory equipment accessible to every hospital, clinic, and research lab in Nigeria.

        From our base in **{COMPANY['address']}**, we have served hundreds of clients who trust us for authenticity and after-sales support.

        Every product you see in this store has been carefully selected for durability, accuracy, and value for money. Whether you are setting up a new lab or upgrading your current facility, my team and I are here to support you.

        Thank you for choosing us. We value your trust.

        **Warmly,**
        **{COMPANY['founder']}**
        *Founder & CEO, {COMPANY['name']}*
        """)
        st.markdown("---")
        st.write(f"📍 {COMPANY['address']} | 📞 {COMPANY['phone']} | ✉️ {COMPANY['email']}")

    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("🛒 CONTINUE TO STORE →", use_container_width=True, type="primary"):
        st.session_state.page = "store"
        st.rerun()

# --- STORE PAGE ---
else:
    c1, c2, c3 = st.columns([3,1,1])
    with c1:
        st.title(f"{COMPANY['name']} 🧬")
        st.caption(f"{COMPANY['address']} | {COMPANY['phone']}")
    with c2:
        if st.button("🏠 Welcome Page"): 
            st.session_state.page = "welcome"
            st.rerun()
    with c3:
        st.metric("Cart", len(st.session_state.cart))

    s1, s2 = st.columns(2)
    with s1: search = st.text_input("🔍 Search")
    with s2: cat = st.selectbox("Category", ["All"] + sorted(df["Category"].unique().tolist()))

    filtered = df.copy()
    if search: filtered = filtered[filtered.apply(lambda r: search.lower() in str(r.values).lower(), axis=1)]
    if cat != "All": filtered = filtered[filtered["Category"]==cat]

    st.markdown(f"**{len(filtered)} Products Available**")
    cols = st.columns(2)
    for i, row in filtered.iterrows():
        with cols[i % 2]:
            with st.container(border=True):
                st.markdown(f"**{row['Name']}**")
                st.caption(f"{row['ID']} | {row['Category']}")
                st.write(f"💵 ${row['USD']} | ₦{row['NGN']:,}")
                if st.button(f"Add to Cart", key=f"add_{row['ID']}", use_container_width=True):
                    st.session_state.cart.append(row.to_dict())
                    st.toast(f"Added {row['Name']}")

    st.divider()
    st.subheader("🛒 Your Order")
    if not st.session_state.cart:
        st.info("Cart empty")
    else:
        cart_df = pd.DataFrame(st.session_state.cart)
        st.dataframe(cart_df[["Name","USD","NGN"]], hide_index=True, use_container_width=True)
        total_usd = cart_df["USD"].sum()
        total_ngn = cart_df["NGN"].sum()
        st.write(f"**Total: ${total_usd} / ₦{total_ngn:,}**")
        msg = f"Hello MEDCARE LABS, I want to order:%0A" + "%0A".join([f"- {x['Name']}" for x in st.session_state.cart]) + f"%0ATotal ${total_usd}"
        st.link_button("📲 WhatsApp Order", f"https://wa.me/{COMPANY['whatsapp']}?text={msg}", type="primary", use_container_width=True)
        if st.button("Clear Cart"):
            st.session_state.cart = []
            st.rerun()

    st.markdown("---")
    st.markdown(f"<center>© 2026 {COMPANY['name']} | Founded by {COMPANY['founder']} | {COMPANY['address']}</center>", unsafe_allow_html=True)
