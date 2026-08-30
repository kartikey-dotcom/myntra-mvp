"""
Myntra E-Commerce Platform & StyleSync™ Smart Wardrobe MVP
==========================================================
High-Fidelity Desktop E-Commerce Experience & Native 4-Screen Flow:
1. Storefront Homepage (Navigation, Ticket Promo Banner, Linen Collection Hero, 4-Category Grid)
2. Product Display Page (PDP - Rust Linen Blazer, Dynamic Size Picker, StyleSync AI Preview)
3. Wishlist Anchor & Smart Closet (Saved Blazer, Closet Inventory, 'Style with My Closet' CTA)
4. StyleSync AI Studio & WhatsApp Social Validation (Rule-of-3 Outfits & Interactive WhatsApp Poll)
"""

import time
from typing import TypedDict, List, Dict
import streamlit as st

# ==============================================================================
# 1. PAGE CONFIGURATION & DESIGN SYSTEM
# ==============================================================================

st.set_page_config(
    page_title="Myntra - Fashion, Shopping & Lifestyle",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    /* Global Reset */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        color: #282C3F;
        background-color: #FAFBFC;
    }

    /* Remove Streamlit default header/footer padding */
    header[data-testid="stHeader"] {
        background: transparent !important;
        height: 1.5rem !important;
        z-index: 1 !important;
    }
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    
    .block-container {
        max-width: 1240px !important;
        padding-top: 1rem !important;
        padding-bottom: 3.5rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
        margin: auto !important;
    }

    /* Custom Navbar Card */
    .myntra-nav-container {
        background: #FFFFFF;
        border-bottom: 1px solid #F0F0F2;
        padding: 0.8rem 1.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
        border-radius: 12px;
        margin-bottom: 1.2rem;
    }

    /* Brand Ribbon Logo */
    .brand-logo-wrap {
        display: flex;
        align-items: center;
        gap: 10px;
        cursor: pointer;
    }
    .brand-name-title {
        font-size: 1.45rem;
        font-weight: 900;
        letter-spacing: -0.5px;
        color: #282C3F;
    }
    .brand-pink-accent {
        color: #FF3F6C;
    }

    /* Ticket Promo Banner */
    .promo-ticket-box {
        background: linear-gradient(90deg, #FFF0F3 0%, #FFE8EE 50%, #FFF0F3 100%);
        border: 1.5px dashed #FFCCD7;
        border-radius: 14px;
        padding: 1.1rem 2rem;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        position: relative;
        box-shadow: 0 2px 10px rgba(255, 63, 108, 0.06);
    }
    .ticket-heading {
        font-size: 1.35rem;
        font-weight: 900;
        color: #D2691E;
        line-height: 1.2;
    }
    .ticket-sub {
        font-size: 0.85rem;
        font-weight: 600;
        color: #535766;
    }
    .coupon-pill {
        background: #FFFFFF;
        padding: 0.5rem 1.2rem;
        border-radius: 30px;
        font-size: 0.82rem;
        font-weight: 800;
        color: #282C3F;
        border: 1px solid #FFE0E6;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .coupon-code {
        color: #FF3F6C;
        font-weight: 900;
        letter-spacing: 0.5px;
    }

    /* Hero Banner */
    .hero-banner-container {
        background: #F4F1EA;
        border-radius: 16px;
        overflow: hidden;
        margin-bottom: 2rem;
        display: flex;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        border: 1px solid #EAE6DC;
    }
    .hero-img-col {
        flex: 1.1;
        min-height: 380px;
        background-size: cover;
        background-position: center top;
    }
    .hero-text-col {
        flex: 1;
        padding: 3rem 2.5rem;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: flex-start;
        background: #F4F1EA;
    }
    .hero-super-title {
        font-size: 0.82rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #FF3F6C;
        margin-bottom: 0.5rem;
    }
    .hero-main-title {
        font-size: 2.2rem;
        font-weight: 900;
        color: #282C3F;
        line-height: 1.15;
        letter-spacing: -0.5px;
        margin-bottom: 0.8rem;
    }
    .hero-description {
        font-size: 0.95rem;
        color: #535766;
        line-height: 1.5;
        margin-bottom: 1.5rem;
    }

    /* Category Cards */
    .category-card {
        background: #FFFFFF;
        border-radius: 14px;
        overflow: hidden;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
        border: 1px solid #F0F0F2;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        position: relative;
        text-decoration: none;
    }
    .category-img-box {
        height: 220px;
        background-size: cover;
        background-position: center top;
        position: relative;
    }
    .category-title-overlay {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(180deg, transparent 0%, rgba(40, 44, 63, 0.85) 100%);
        padding: 1.2rem 1rem 0.6rem 1rem;
        color: #FFFFFF;
        font-size: 1rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Section Headings */
    .section-header-wrap {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        margin: 2rem 0 1.2rem 0;
    }
    .section-title {
        font-size: 1.35rem;
        font-weight: 900;
        color: #282C3F;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    .section-subtitle {
        font-size: 0.85rem;
        color: #7E818C;
        font-weight: 500;
    }

    /* Product Cards & Wishlist Items */
    .product-grid-card {
        background: #FFFFFF;
        border: 1px solid #ECEEF0;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        display: flex;
        flex-direction: column;
        height: 100%;
    }
    .product-img-frame {
        height: 230px;
        background-size: cover;
        background-position: center top;
        position: relative;
    }
    .product-badge-pill {
        position: absolute;
        top: 10px;
        left: 10px;
        font-size: 0.68rem;
        font-weight: 800;
        padding: 3px 8px;
        border-radius: 4px;
        text-transform: uppercase;
    }
    .badge-in-closet {
        background: #282C3F;
        color: #FFFFFF;
    }
    .badge-suggested {
        background: #E8F8F5;
        color: #03A685;
        border: 1px solid #B8EADF;
    }
    .product-info-padding {
        padding: 12px 14px;
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .product-brand-text {
        font-size: 0.78rem;
        font-weight: 800;
        color: #282C3F;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .product-name-text {
        font-size: 0.86rem;
        color: #535766;
        font-weight: 500;
        margin: 2px 0 6px 0;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .product-price-row {
        display: flex;
        align-items: baseline;
        gap: 8px;
        margin-top: 4px;
    }
    .product-price-bold {
        font-size: 0.95rem;
        font-weight: 800;
        color: #282C3F;
    }
    .product-price-orig {
        font-size: 0.78rem;
        color: #94969F;
        text-decoration: line-through;
    }
    .product-price-disc {
        font-size: 0.75rem;
        font-weight: 800;
        color: #FF3F6C;
    }

    /* StyleSync Studio Collage Card */
    .look-card-container {
        background: #FFFFFF;
        border: 1.5px solid #EAEAEA;
        border-radius: 16px;
        padding: 1.2rem;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    .look-card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.8rem;
    }
    .look-card-title {
        font-size: 1.1rem;
        font-weight: 900;
        color: #282C3F;
    }
    .look-score-badge {
        font-size: 0.75rem;
        font-weight: 800;
        background: #FFF0F4;
        color: #FF3F6C;
        padding: 3px 8px;
        border-radius: 12px;
        border: 1px solid #FFCCD7;
    }

    /* WhatsApp Social Poll Card */
    .whatsapp-preview-box {
        background: #EFEAE2;
        border-radius: 16px;
        padding: 1.2rem;
        border: 1px solid #E0D8CC;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    }
    .whatsapp-bubble {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        position: relative;
    }
    .whatsapp-poll-btn {
        width: 100%;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        font-size: 0.88rem;
        font-weight: 700;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
        cursor: pointer;
        transition: all 0.2s;
    }

    /* Streamlit Button Custom Styler */
    div.stButton > button {
        border-radius: 8px !important;
        font-weight: 800 !important;
        letter-spacing: 0.3px !important;
        transition: all 0.15s ease-in-out !important;
    }
    div.stButton > button:hover {
        transform: translateY(-1px);
    }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ==============================================================================
# 2. DATA SCHEMAS & Wizard of Oz ASSETS
# ==============================================================================

class TargetItem(TypedDict):
    id: str
    name: str
    brand: str
    price: str
    original_price: str
    discount: str
    rating: str
    reviews: str
    image_url: str

TARGET_ITEM: TargetItem = {
    "id": "ITEM-9081",
    "name": "Rust Linen Relaxed-Fit Blazer",
    "brand": "MANGO MAN",
    "price": "₹3,499",
    "original_price": "₹4,999",
    "discount": "30% OFF",
    "rating": "4.2",
    "reviews": "124 Verified Customer Ratings",
    "image_url": "https://images.unsplash.com/photo-1598808503746-f34c53b9323e?w=800&auto=format&fit=crop&q=80"
}

IMAGE_HERO = "https://images.unsplash.com/photo-1598808503746-f34c53b9323e?w=1000&auto=format&fit=crop&q=80"
IMAGE_MEN_CAT = "https://images.unsplash.com/photo-1617137984095-74e4e5e3613f?w=600&auto=format&fit=crop&q=80"
IMAGE_WOMEN_CAT = "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=600&auto=format&fit=crop&q=80"
IMAGE_BEAUTY_CAT = "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=600&auto=format&fit=crop&q=80"
IMAGE_HOME_CAT = "https://images.unsplash.com/photo-1540555700478-4be289fbecef?w=600&auto=format&fit=crop&q=80"

IMAGE_OLIVE_SHIRT = "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=600&auto=format&fit=crop&q=80"
IMAGE_BLACK_TROUSERS = "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=600&auto=format&fit=crop&q=80"
IMAGE_WHITE_TANK = "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=600&auto=format&fit=crop&q=80"
IMAGE_LIGHT_DENIM = "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=600&auto=format&fit=crop&q=80"
IMAGE_FOSSIL_WATCH = "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=600&auto=format&fit=crop&q=80"
IMAGE_PUMA_SNEAKERS = "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=600&auto=format&fit=crop&q=80"

class WishlistProduct(TypedDict):
    id: str
    brand: str
    name: str
    price: str
    original_price: str
    discount: str
    rating: str
    image_url: str
    tag: str

WISHLIST_PRODUCTS: List[WishlistProduct] = [
    {
        "id": "W-101",
        "brand": "FOSSIL",
        "name": "Minimalist Chronograph Watch",
        "price": "₹6,495",
        "original_price": "₹9,995",
        "discount": "35% OFF",
        "rating": "4.6",
        "image_url": IMAGE_FOSSIL_WATCH,
        "tag": "In Closet (Ordered Jan 2024)"
    },
    {
        "id": "W-102",
        "brand": "H&M",
        "name": "Relaxed Fit Olive Linen Shirt",
        "price": "₹1,999",
        "original_price": "₹2,499",
        "discount": "20% OFF",
        "rating": "4.4",
        "image_url": IMAGE_OLIVE_SHIRT,
        "tag": "In Closet (Ordered Oct 2024)"
    },
    {
        "id": "W-103",
        "brand": "ZARA",
        "name": "Tailored Pleated Black Trousers",
        "price": "₹2,990",
        "original_price": "₹3,990",
        "discount": "25% OFF",
        "rating": "4.5",
        "image_url": IMAGE_BLACK_TROUSERS,
        "tag": "In Closet (Ordered Nov 2024)"
    },
    {
        "id": "W-104",
        "brand": "PUMA",
        "name": "Caven Classic Court Sneakers",
        "price": "₹2,749",
        "original_price": "₹4,999",
        "discount": "45% OFF",
        "rating": "4.3",
        "image_url": IMAGE_PUMA_SNEAKERS,
        "tag": "Suggested Style Match"
    },
    {
        "id": "W-105",
        "brand": "LEVIS",
        "name": "501 Light Wash Wide Denim",
        "price": "₹3,199",
        "original_price": "₹4,599",
        "discount": "30% OFF",
        "rating": "4.7",
        "image_url": IMAGE_LIGHT_DENIM,
        "tag": "Suggested Style Match"
    },
    {
        "id": "W-106",
        "brand": "MANGO",
        "name": "Ribbed Knit White Tank",
        "price": "₹1,290",
        "original_price": "₹1,690",
        "discount": "23% OFF",
        "rating": "4.1",
        "image_url": IMAGE_WHITE_TANK,
        "tag": "Suggested Style Match"
    }
]

# ==============================================================================
# 3. SESSION STATE & NAVIGATION MACHINE
# ==============================================================================

def init_session_state() -> None:
    """Initializes router state defaults ensuring compatibility with test_app.py."""
    if "current_view" not in st.session_state:
        st.session_state["current_view"] = "homepage"
    if "bag_count" not in st.session_state:
        st.session_state["bag_count"] = 2
    if "selected_size" not in st.session_state:
        st.session_state["selected_size"] = "40"
    if "poll_sent" not in st.session_state:
        st.session_state["poll_sent"] = False
    if "vote_feedback" not in st.session_state:
        st.session_state["vote_feedback"] = None
    if "toast_msg" not in st.session_state:
        st.session_state["toast_msg"] = None

init_session_state()

def set_view(view_name: str) -> None:
    st.session_state["current_view"] = view_name
    st.rerun()

# ==============================================================================
# 4. TOP NAVIGATION BAR COMPONENT
# ==============================================================================

def render_top_navbar() -> None:
    curr = st.session_state.get("current_view", "homepage")
    bag_num = st.session_state.get("bag_count", 2)

    # Top Brand Ribbon & Search Bar
    nav_col1, nav_col2, nav_col3, nav_col4 = st.columns([2.5, 4.5, 3, 2.5])
    
    with nav_col1:
        st.markdown(
            """
            <div style="display: flex; align-items: center; gap: 10px; margin-top: 4px;">
                <svg width="38" height="34" viewBox="0 0 45 42" fill="none">
                    <path d="M7 32L17.5 11H21.5L30 32H25.5L20.5 19.5L15.5 32H7Z" fill="#F48946"/>
                    <path d="M20.5 19.5L25.5 32H30L21.5 11H17.5L20.5 19.5Z" fill="#FF3F6C"/>
                    <path d="M17.5 11H21.5L19.5 15.5L17.5 11Z" fill="#E65A2C"/>
                    <path d="M15.5 32L24.5 11H28.5L38 32H33.5L28 19.5L23.5 32H15.5Z" fill="#FF3F6C" opacity="0.9"/>
                </svg>
                <div>
                    <span style="font-weight: 900; font-size: 1.3rem; color: #282C3F; letter-spacing: -0.5px;">myntra</span>
                    <span style="font-size: 0.65rem; font-weight: 800; background: #FFF0F4; color: #FF3F6C; border: 1px solid #FFD8E4; padding: 1px 5px; border-radius: 4px; margin-left: 4px;">STYLESYNC™</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with nav_col2:
        # Category Tabs
        b1, b2, b3, b4, b5 = st.columns(5)
        with b1:
            if st.button("HOME", key="nav_home", use_container_width=True):
                set_view("homepage")
        with b2:
            if st.button("MEN", key="nav_men", use_container_width=True):
                set_view("pdp")
        with b3:
            if st.button("WOMEN", key="nav_women", use_container_width=True):
                set_view("homepage")
        with b4:
            if st.button("STUDIO ✨", key="nav_studio", use_container_width=True):
                set_view("stylesync")
        with b5:
            if st.button("WISHLIST", key="nav_wl_tab", use_container_width=True):
                set_view("wishlist")

    with nav_col3:
        st.text_input("🔍 Search products, brands...", placeholder="Search for products, brands and more", label_visibility="collapsed", key="search_bar")

    with nav_col4:
        ic1, ic2 = st.columns(2)
        with ic1:
            if st.button(f"❤️ Wishlist (1)", key="top_wl_btn", use_container_width=True):
                set_view("wishlist")
        with ic2:
            st.button(f"🛍️ Bag ({bag_num})", key="top_bag_btn", use_container_width=True)

    # Journey Stepper Quick Navigator Bar
    st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
    step1, step2, step3, step4 = st.columns(4)
    with step1:
        if st.button("🏠 Storefront Home", use_container_width=True, type="primary" if curr == "homepage" else "secondary"):
            set_view("homepage")
    with step2:
        if st.button("🛍️ 1. Product PDP", use_container_width=True, type="primary" if curr == "pdp" else "secondary"):
            set_view("pdp")
    with step3:
        if st.button("❤️ 2. Wishlist & Closet", use_container_width=True, type="primary" if curr == "wishlist" else "secondary"):
            set_view("wishlist")
    with step4:
        if st.button("✨ 3. StyleSync AI Studio", use_container_width=True, type="primary" if curr == "stylesync" else "secondary"):
            set_view("stylesync")
    
    st.markdown("<hr style='margin: 0.8rem 0 1.5rem 0; border: none; border-top: 1px solid #ECEEF0;'>", unsafe_allow_html=True)


# ==============================================================================
# 5. SCREEN 1: HOMEPAGE STOREFRONT
# ==============================================================================

def render_homepage_view() -> None:
    # 1. Promo Ticket Banner
    st.markdown(
        """
        <div class="promo-ticket-box">
            <div>
                <div class="ticket-heading">GET 25% OFF</div>
                <div class="ticket-sub">Up To ₹200 Off On First StyleSync Wardrobe Match*</div>
            </div>
            <div class="coupon-pill">
                <span>COUPON CODE:</span>
                <span class="coupon-code">MYNTRASAVE</span>
                <span style="font-size: 1.2rem; margin-left: 6px;">🎟️</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 2. Linen Collection Hero Banner
    h_col1, h_col2 = st.columns([1.1, 1.2])
    with h_col1:
        st.image(
            IMAGE_HERO,
            caption="MANGO MAN • Rust Linen Capsule Collection",
            use_container_width=True
        )
    with h_col2:
        st.markdown(
            """
            <div style="padding: 1rem 0;">
                <span class="hero-super-title">NEW SEASON CAPSULE</span>
                <h1 class="hero-main-title">THE NEW LINEN<br>COLLECTION</h1>
                <p class="hero-description">
                    Breathable European flax tailored for effortless versatility. 
                    Paired seamlessly with your existing wardrobe through StyleSync™ AI.
                </p>
                <div style="display: flex; gap: 12px; margin-bottom: 1.5rem;">
                    <span style="font-size: 1.5rem; font-weight: 900; color: #282C3F;">₹3,499</span>
                    <span style="font-size: 1.1rem; color: #94969F; text-decoration: line-through; margin-top: 4px;">₹4,999</span>
                    <span style="font-size: 0.9rem; font-weight: 800; color: #FF3F6C; background: #FFF0F4; padding: 4px 10px; border-radius: 6px;">30% OFF</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        c_btn1, c_btn2 = st.columns(2)
        with c_btn1:
            if st.button("🔥 EXPLORE NOW", key="hero_explore_btn", type="primary", use_container_width=True):
                set_view("pdp")
        with c_btn2:
            if st.button("✨ Style with My Closet", key="hero_stylesync_btn", use_container_width=True):
                set_view("stylesync")

    # 3. Shop by Category Grid
    st.markdown(
        """
        <div class="section-header-wrap">
            <div>
                <div class="section-title">SHOP BY CATEGORY</div>
                <div class="section-subtitle">Curated trends designed to complement your current wardrobe</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    cat1, cat2, cat3, cat4 = st.columns(4)
    with cat1:
        st.image(IMAGE_MEN_CAT, use_container_width=True)
        st.markdown("<h4 style='margin: 6px 0 2px 0; font-weight: 800;'>MEN'S CASUALS</h4><p style='color: #7E818C; font-size: 0.8rem;'>Linens, Polos & Trousers</p>", unsafe_allow_html=True)
        if st.button("View Casuals →", key="cat_men_btn", use_container_width=True):
            set_view("pdp")

    with cat2:
        st.image(IMAGE_WOMEN_CAT, use_container_width=True)
        st.markdown("<h4 style='margin: 6px 0 2px 0; font-weight: 800;'>WOMEN'S WEAR</h4><p style='color: #7E818C; font-size: 0.8rem;'>Dresses, Tops & Coordinates</p>", unsafe_allow_html=True)
        if st.button("View Women →", key="cat_women_btn", use_container_width=True):
            set_view("pdp")

    with cat3:
        st.image(IMAGE_BEAUTY_CAT, use_container_width=True)
        st.markdown("<h4 style='margin: 6px 0 2px 0; font-weight: 800;'>BEAUTY & GROOMING</h4><p style='color: #7E818C; font-size: 0.8rem;'>Fragrance, Skincare & Grooming</p>", unsafe_allow_html=True)
        if st.button("View Beauty →", key="cat_beauty_btn", use_container_width=True):
            set_view("pdp")

    with cat4:
        st.image(IMAGE_HOME_CAT, use_container_width=True)
        st.markdown("<h4 style='margin: 6px 0 2px 0; font-weight: 800;'>HOME LIVING</h4><p style='color: #7E818C; font-size: 0.8rem;'>Modern Decor & Bedroom Accents</p>", unsafe_allow_html=True)
        if st.button("View Home →", key="cat_home_btn", use_container_width=True):
            set_view("pdp")


# ==============================================================================
# 6. SCREEN 2: PRODUCT DISPLAY PAGE (PDP)
# ==============================================================================

def render_pdp_view() -> None:
    # Breadcrumbs
    st.markdown(
        """
        <div style="font-size: 0.78rem; font-weight: 600; color: #7E818C; margin-bottom: 1.2rem;">
            <span>Home</span> / <span>Men</span> / <span>Topwear</span> / <span>Blazers</span> / 
            <span style="color: #282C3F; font-weight: 800;">MANGO MAN Rust Linen Blazer</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    col_img, col_details = st.columns([1.1, 1.2], gap="large")

    with col_img:
        st.image(TARGET_ITEM["image_url"], use_container_width=True)
        # Secondary Thumbnail row
        t1, t2, t3 = st.columns(3)
        with t1:
            st.image(TARGET_ITEM["image_url"], use_container_width=True)
        with t2:
            st.image(IMAGE_OLIVE_SHIRT, use_container_width=True)
        with t3:
            st.image(IMAGE_BLACK_TROUSERS, use_container_width=True)

    with col_details:
        st.markdown(f"<span style='font-size: 0.85rem; font-weight: 900; color: #FF3F6C; letter-spacing: 1px;'>{TARGET_ITEM['brand']}</span>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='font-size: 1.8rem; font-weight: 900; color: #282C3F; margin: 4px 0 10px 0;'>{TARGET_ITEM['name']}</h1>", unsafe_allow_html=True)
        
        # Ratings Pill
        st.markdown(
            f"""
            <div style="display: inline-flex; align-items: center; gap: 6px; background: #FAFAFA; border: 1px solid #EAEAEC; border-radius: 6px; padding: 4px 10px; font-size: 0.82rem; font-weight: 800; margin-bottom: 1rem;">
                <span style="color: #03A685;">★ {TARGET_ITEM['rating']}</span>
                <span style="color: #94969F;">|</span>
                <span style="color: #535766;">{TARGET_ITEM['reviews']}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Price Row
        st.markdown(
            f"""
            <div style="display: flex; align-items: baseline; gap: 12px; margin-bottom: 4px;">
                <span style="font-size: 1.8rem; font-weight: 900; color: #282C3F;">{TARGET_ITEM['price']}</span>
                <span style="font-size: 1.1rem; color: #94969F; text-decoration: line-through;">{TARGET_ITEM['original_price']}</span>
                <span style="font-size: 0.95rem; font-weight: 800; color: #FF5722; background: #FFF5F0; padding: 3px 8px; border-radius: 6px;">{TARGET_ITEM['discount']}</span>
            </div>
            <div style="font-size: 0.76rem; font-weight: 800; color: #03A685; margin-bottom: 1.5rem;">inclusive of all taxes</div>
            """,
            unsafe_allow_html=True
        )

        # Size Selector
        st.markdown("<div style='font-size: 0.84rem; font-weight: 900; color: #282C3F; margin-bottom: 8px;'>SELECT SIZE (CHEST)</div>", unsafe_allow_html=True)
        s1, s2, s3, s4 = st.columns(4)
        curr_size = st.session_state.get("selected_size", "40")
        with s1:
            if st.button("38", key="sz_38", type="primary" if curr_size == "38" else "secondary", use_container_width=True):
                st.session_state["selected_size"] = "38"
                st.rerun()
        with s2:
            if st.button("40 (Standard)", key="sz_40", type="primary" if curr_size == "40" else "secondary", use_container_width=True):
                st.session_state["selected_size"] = "40"
                st.rerun()
        with s3:
            if st.button("42", key="sz_42", type="primary" if curr_size == "42" else "secondary", use_container_width=True):
                st.session_state["selected_size"] = "42"
                st.rerun()
        with s4:
            if st.button("44", key="sz_44", type="primary" if curr_size == "44" else "secondary", use_container_width=True):
                st.session_state["selected_size"] = "44"
                st.rerun()

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        # Action Buttons
        btn_bag, btn_wish = st.columns([1.2, 1])
        with btn_bag:
            if st.button("🛍️ ADD TO BAG", key="pdp_add_bag_btn", type="primary", use_container_width=True):
                st.session_state["bag_count"] = st.session_state.get("bag_count", 2) + 1
                st.toast("✅ Rust Linen Blazer added to your shopping bag!")
                st.rerun()
        with btn_wish:
            if st.button("❤️ WISHLIST", key="pdp_add_wl_btn", use_container_width=True):
                st.toast("❤️ Added to Wishlist! Opening Smart Closet...")
                set_view("wishlist")

        # StyleSync AI Recommendation Box
        st.markdown(
            """
            <div style="background: linear-gradient(135deg, #FFF0F4 0%, #F5F0FF 100%); border: 1.5px solid #FFD8E4; border-radius: 12px; padding: 1.1rem; margin-top: 1.5rem;">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
                    <span style="font-size: 1.3rem;">✨</span>
                    <span style="font-size: 0.95rem; font-weight: 900; color: #282C3F;">StyleSync™ Smart Match Found!</span>
                </div>
                <p style="font-size: 0.82rem; color: #535766; margin-bottom: 0.8rem; line-height: 1.4;">
                    We detected <b>3 items in your purchase history</b> (Zara Trousers, Olive Linen Shirt, Fossil Watch) that create 3 full modular outfits with this blazer.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("✨ View 3 Wardrobe Outfits & WhatsApp Poll →", key="pdp_to_stylesync_btn", use_container_width=True):
            set_view("stylesync")


# ==============================================================================
# 7. SCREEN 3: WISHLIST & SMART CLOSET ANCHOR
# ==============================================================================

def render_wishlist_view() -> None:
    st.markdown(
        """
        <div class="section-header-wrap" style="margin-top: 0;">
            <div>
                <div class="section-title">MY WISHLIST & SAVED WARDROBE</div>
                <div class="section-subtitle">1 Target Anchor Garment • 6 Paired Wardrobe & Catalog Pieces</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 1. Target Anchor Garment Card
    w_col1, w_col2 = st.columns([1, 2.2])
    with w_col1:
        st.image(TARGET_ITEM["image_url"], caption="Wishlisted Anchor Item", use_container_width=True)
    with w_col2:
        st.markdown(
            f"""
            <div style="background: #FFFFFF; border: 1.5px solid #FFE0E6; border-radius: 14px; padding: 1.4rem; box-shadow: 0 4px 14px rgba(255, 63, 108, 0.05);">
                <span style="font-size: 0.72rem; font-weight: 900; background: #FF3F6C; color: #FFFFFF; padding: 3px 8px; border-radius: 4px; text-transform: uppercase;">ANCHOR ITEM</span>
                <h2 style="font-size: 1.35rem; font-weight: 900; color: #282C3F; margin: 8px 0 4px 0;">{TARGET_ITEM['brand']} {TARGET_ITEM['name']}</h2>
                <div style="display: flex; align-items: baseline; gap: 10px; margin-bottom: 0.8rem;">
                    <span style="font-size: 1.4rem; font-weight: 900; color: #282C3F;">{TARGET_ITEM['price']}</span>
                    <span style="font-size: 0.95rem; color: #94969F; text-decoration: line-through;">{TARGET_ITEM['original_price']}</span>
                    <span style="font-size: 0.85rem; font-weight: 800; color: #FF3F6C;">({TARGET_ITEM['discount']})</span>
                </div>
                <p style="font-size: 0.84rem; color: #535766; line-height: 1.4; margin-bottom: 1.2rem;">
                    Unlocks <b>3 modular outfits</b> using clothes you already own in your closet. Zero styling hesitation!
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("✨ Style with My Closet (Run StyleSync AI) →", key="wl_run_ai_btn", type="primary", use_container_width=True):
            with st.spinner("✨ StyleSync AI analyzing your wardrobe purchase history & color harmonies..."):
                time.sleep(0.8)
            set_view("stylesync")

    # 2. Curated Wardrobe & Wishlist Grid
    st.markdown(
        """
        <div class="section-header-wrap">
            <div>
                <div class="section-title">YOUR CLOSET INVENTORY & WISHLIST MATCHES</div>
                <div class="section-subtitle">Auto-synced from your order history and saved items</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    g1, g2, g3 = st.columns(3)
    for idx, item in enumerate(WISHLIST_PRODUCTS[:3]):
        with [g1, g2, g3][idx]:
            st.image(item["image_url"], use_container_width=True)
            st.markdown(
                f"""
                <div style="padding: 4px 0 10px 0;">
                    <span style="font-size: 0.7rem; font-weight: 800; padding: 2px 6px; border-radius: 4px; {'background: #282C3F; color: #FFF;' if 'Closet' in item['tag'] else 'background: #E8F8F5; color: #03A685;'}">
                        {item['tag']}
                    </span>
                    <div style="font-weight: 800; font-size: 0.9rem; color: #282C3F; margin-top: 4px;">{item['brand']}</div>
                    <div style="font-size: 0.82rem; color: #535766;">{item['name']}</div>
                    <div style="font-weight: 800; font-size: 0.9rem; color: #282C3F; margin-top: 2px;">{item['price']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    g4, g5, g6 = st.columns(3)
    for idx, item in enumerate(WISHLIST_PRODUCTS[3:6]):
        with [g4, g5, g6][idx]:
            st.image(item["image_url"], use_container_width=True)
            st.markdown(
                f"""
                <div style="padding: 4px 0 10px 0;">
                    <span style="font-size: 0.7rem; font-weight: 800; padding: 2px 6px; border-radius: 4px; {'background: #282C3F; color: #FFF;' if 'Closet' in item['tag'] else 'background: #E8F8F5; color: #03A685;'}">
                        {item['tag']}
                    </span>
                    <div style="font-weight: 800; font-size: 0.9rem; color: #282C3F; margin-top: 4px;">{item['brand']}</div>
                    <div style="font-size: 0.82rem; color: #535766;">{item['name']}</div>
                    <div style="font-weight: 800; font-size: 0.9rem; color: #282C3F; margin-top: 2px;">{item['price']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )


# ==============================================================================
# 8. SCREEN 4: STYLESYNC AI STUDIO & WHATSAPP SOCIAL POLL
# ==============================================================================

def render_stylesync_view() -> None:
    st.markdown(
        """
        <div class="section-header-wrap" style="margin-top: 0;">
            <div>
                <div class="section-title">✨ STYLESYNC™ AI WARDROBE STUDIO</div>
                <div class="section-subtitle">3 Complete Rule-of-3 Outfits Generated from Your Closet + WhatsApp Peer Poll Loop</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 3 Curated Rule-of-3 Outfit Collages
    l_col1, l_col2, l_col3 = st.columns(3)

    # Look 1
    with l_col1:
        st.markdown(
            """
            <div class="look-card-container">
                <div class="look-card-header">
                    <span class="look-card-title">Look 1: Sunset Linen</span>
                    <span class="look-score-badge">98% Match</span>
                </div>
                <div style="font-size: 0.75rem; font-weight: 700; color: #03A685; margin-bottom: 8px;">
                    ✅ 100% Owned Pieces (Extra Cost: ₹0)
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.image(TARGET_ITEM["image_url"], caption="Anchor: Rust Linen Blazer (₹3,499)", use_container_width=True)
        img_sub1, img_sub2 = st.columns(2)
        with img_sub1:
            st.image(IMAGE_OLIVE_SHIRT, caption="H&M Olive Shirt (In Closet)", use_container_width=True)
        with img_sub2:
            st.image(IMAGE_BLACK_TROUSERS, caption="Zara Trousers (In Closet)", use_container_width=True)
        
        if st.button("💬 Poll Look 1 on WhatsApp", key="poll_look_1_btn", type="primary", use_container_width=True):
            st.session_state["poll_sent"] = True
            st.session_state["poll_look_title"] = "Look 1: Sunset Linen"
            st.rerun()

    # Look 2
    with l_col2:
        st.markdown(
            """
            <div class="look-card-container">
                <div class="look-card-header">
                    <span class="look-card-title">Look 2: Urban Brunch</span>
                    <span class="look-score-badge">94% Match</span>
                </div>
                <div style="font-size: 0.75rem; font-weight: 700; color: #535766; margin-bottom: 8px;">
                    ✨ 2 Closet + 1 Wishlist Add-on
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.image(TARGET_ITEM["image_url"], caption="Anchor: Rust Linen Blazer (₹3,499)", use_container_width=True)
        img_sub3, img_sub4 = st.columns(2)
        with img_sub3:
            st.image(IMAGE_WHITE_TANK, caption="Mango Tank (Wishlist)", use_container_width=True)
        with img_sub4:
            st.image(IMAGE_PUMA_SNEAKERS, caption="Puma Sneakers (Wishlist)", use_container_width=True)

        if st.button("💬 Poll Look 2 on WhatsApp", key="poll_look_2_btn", use_container_width=True):
            st.session_state["poll_sent"] = True
            st.session_state["poll_look_title"] = "Look 2: Urban Brunch"
            st.rerun()

    # Look 3
    with l_col3:
        st.markdown(
            """
            <div class="look-card-container">
                <div class="look-card-header">
                    <span class="look-card-title">Look 3: Smart Business</span>
                    <span class="look-score-badge">91% Match</span>
                </div>
                <div style="font-size: 0.75rem; font-weight: 700; color: #03A685; margin-bottom: 8px;">
                    ✅ Formal Office Friday Ready
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.image(TARGET_ITEM["image_url"], caption="Anchor: Rust Linen Blazer (₹3,499)", use_container_width=True)
        img_sub5, img_sub6 = st.columns(2)
        with img_sub5:
            st.image(IMAGE_FOSSIL_WATCH, caption="Fossil Watch (In Closet)", use_container_width=True)
        with img_sub6:
            st.image(IMAGE_LIGHT_DENIM, caption="Levi's Denim (Wishlist)", use_container_width=True)

        if st.button("💬 Poll Look 3 on WhatsApp", key="poll_look_3_btn", use_container_width=True):
            st.session_state["poll_sent"] = True
            st.session_state["poll_look_title"] = "Look 3: Smart Business"
            st.rerun()

    st.markdown("<hr style='margin: 2rem 0; border: none; border-top: 1px solid #ECEEF0;'>", unsafe_allow_html=True)

    # WhatsApp Social Loop Simulator Section
    st.markdown(
        """
        <div class="section-header-wrap">
            <div>
                <div class="section-title">📱 WHATSAPP SOCIAL VALIDATION LOOP ("BUY OR DROP")</div>
                <div class="section-subtitle">Prevent off-platform leakage: Let trusted friends vote directly on your curated outfit</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    wa_col1, wa_col2 = st.columns([1.2, 1])

    with wa_col1:
        look_name = st.session_state.get("poll_look_title", "Look 1: Sunset Linen")
        st.markdown(
            f"""
            <div class="whatsapp-preview-box">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
                    <span style="font-size: 1.4rem;">💬</span>
                    <span style="font-weight: 900; color: #075E54; font-size: 1rem;">WhatsApp Style Group • Live Peer Poll</span>
                </div>
                <div class="whatsapp-bubble">
                    <div style="font-weight: 800; font-size: 0.95rem; color: #282C3F; margin-bottom: 4px;">
                        "Hey guys! Thinking of buying this MANGO MAN Rust Linen Blazer. Styled it with my Zara trousers on Myntra StyleSync. Buy or Drop?"
                    </div>
                    <div style="font-size: 0.75rem; color: #878B94; margin-bottom: 8px;"><b>{look_name}</b> • Match Rating 98%</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        v1, v2 = st.columns(2)
        with v1:
            if st.button("🔥 BUY IT! (84% Votes)", key="vote_buy_btn", type="primary", use_container_width=True):
                st.session_state["vote_feedback"] = "buy"
                st.toast("🎉 5 Friends voted 'BUY IT'! High peer confidence score.")
                st.rerun()
        with v2:
            if st.button("👎 DROP IT (16% Votes)", key="vote_drop_btn", use_container_width=True):
                st.session_state["vote_feedback"] = "drop"
                st.toast("Peer feedback registered.")
                st.rerun()

    with wa_col2:
        feedback = st.session_state.get("vote_feedback", None)
        if feedback == "buy":
            st.success("🌟 **Peer Confidence Verified!** 5 of 6 friends recommend buying. Ready to complete order with 1-click checkout.")
            if st.button("🛍️ PROCEED TO CHECKOUT (₹3,499)", key="wa_checkout_btn", type="primary", use_container_width=True):
                st.balloons()
                st.toast("Order placed successfully with StyleSync savings!")
        elif feedback == "drop":
            st.info("💡 Friends suggested checking out alternative colors or exploring other casual jackets.")
        else:
            st.markdown(
                """
                <div style="background: #FFFFFF; border: 1px solid #ECEEF0; border-radius: 12px; padding: 1.2rem;">
                    <div style="font-weight: 800; color: #282C3F; margin-bottom: 6px;">How the WhatsApp Loop Works:</div>
                    <ul style="font-size: 0.82rem; color: #535766; padding-left: 1.2rem; line-height: 1.6;">
                        <li>Generates a clean visual card pairing your wishlisted item + owned pieces.</li>
                        <li>Friends vote with one tap without leaving their chat app.</li>
                        <li>Live results stream back directly to Myntra checkout.</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True
            )


# ==============================================================================
# 9. FOOTER COMPONENT
# ==============================================================================

def render_footer() -> None:
    st.markdown(
        """
        <div style="margin-top: 3.5rem; padding-top: 2rem; border-top: 1.5px solid #F0F0F2; background: #FAFBFC;">
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 2rem; font-size: 0.82rem; color: #696B79; margin-bottom: 2rem;">
                <div>
                    <h5 style="color: #282C3F; font-weight: 800; margin-bottom: 0.8rem; text-transform: uppercase;">ONLINE SHOPPING</h5>
                    <p style="margin: 4px 0;">Men • Women • Kids</p>
                    <p style="margin: 4px 0;">Home & Living • Beauty</p>
                    <p style="margin: 4px 0;">StyleSync AI Wardrobe</p>
                </div>
                <div>
                    <h5 style="color: #282C3F; font-weight: 800; margin-bottom: 0.8rem; text-transform: uppercase;">CUSTOMER POLICIES</h5>
                    <p style="margin: 4px 0;">Contact Us • FAQ</p>
                    <p style="margin: 4px 0;">T&C • Terms Of Use</p>
                    <p style="margin: 4px 0;">Track Orders • Shipping</p>
                </div>
                <div>
                    <h5 style="color: #282C3F; font-weight: 800; margin-bottom: 0.8rem; text-transform: uppercase;">EXPERIENCE MYNTRA APP</h5>
                    <p style="margin: 4px 0;">📱 Available on iOS & Android</p>
                    <p style="margin: 4px 0;">⚡ Fast 100% Genuine Guarantee</p>
                </div>
                <div>
                    <h5 style="color: #282C3F; font-weight: 800; margin-bottom: 0.8rem; text-transform: uppercase;">100% ORIGINAL</h5>
                    <p style="margin: 4px 0;">Guarantee for all products</p>
                    <p style="margin: 4px 0;">Return within 14 days</p>
                </div>
            </div>
            <div style="text-align: center; color: #94969F; font-size: 0.78rem; border-top: 1px solid #ECEEF0; padding-top: 1.2rem;">
                © 2026 www.myntra.com. All rights reserved. Myntra StyleSync™ Portfolio MVP.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==============================================================================
# 10. MAIN ROUTER
# ==============================================================================

def main() -> None:
    render_top_navbar()

    current_view = st.session_state.get("current_view", "homepage")

    if current_view == "homepage":
        render_homepage_view()
    elif current_view == "pdp":
        render_pdp_view()
    elif current_view == "wishlist":
        render_wishlist_view()
    elif current_view == "stylesync":
        render_stylesync_view()
    else:
        render_homepage_view()

    render_footer()


if __name__ == "__main__":
    main()
