"""
Myntra "StyleSync" MVP - 3-Screen Vision-to-Code Mobile Prototype
================================================================
Exact implementation of the 3-screen high-fidelity mobile storyboard:
1. Screen 1: Discovery (PDP - Product Display Page)
2. Screen 2: The Wishlist Anchor (Save to Wishlist & Smart Recommendations)
3. Screen 3: StyleSync AI Results & Social Loop (Rule-of-3 Collages & WhatsApp Peer Poll)
"""

import time
from typing import TypedDict, List, Dict
import streamlit as st

# ==============================================================================
# 1. PAGE CONFIGURATION & 420px MOBILE APP DESIGN SYSTEM
# ==============================================================================

st.set_page_config(
    page_title="Myntra StyleSync",
    page_icon="🛍️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    /* Global reset */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        color: #282C3F;
        background-color: #ECECEE;
    }

    /* Hide default Streamlit top header bar & decoration */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Force 420px Mobile Screen Simulation */
    .block-container {
        max-width: 420px !important;
        padding-top: 0.8rem !important;
        padding-bottom: 2rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
        background-color: #FFFFFF;
        min-height: 100vh;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
        border-radius: 18px;
        margin: auto;
    }

    /* Screen 1: Top Navigation Bar */
    .pdp-top-nav {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 6px 4px 10px 4px;
    }
    .nav-circle-btn {
        width: 34px;
        height: 34px;
        border-radius: 50%;
        background: #F4F4F6;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.95rem;
        cursor: pointer;
    }
    .pdp-nav-right {
        display: flex;
        gap: 8px;
    }

    /* PDP Hero Image & Carousel Dots */
    .pdp-hero-box {
        position: relative;
        width: 100%;
        background-color: #F8F3EE;
        border-radius: 12px;
        overflow: hidden;
        margin-bottom: 12px;
        text-align: center;
    }
    .pdp-hero-img {
        width: 100%;
        height: 380px;
        object-fit: cover;
        display: block;
    }
    .carousel-dots {
        display: flex;
        justify-content: center;
        gap: 5px;
        padding: 8px 0;
    }
    .dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #D4D5D9;
    }
    .dot-active {
        background: #FF3F6C !important;
        width: 14px !important;
        border-radius: 4px !important;
    }

    /* PDP Details Grid */
    .pdp-title-row {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 6px;
    }
    .pdp-brand-title {
        font-size: 1.05rem;
        font-weight: 900;
        color: #282C3F;
        letter-spacing: -0.2px;
    }
    .pdp-sub-title {
        font-size: 0.82rem;
        color: #535766;
        margin-top: 1px;
    }
    .pdp-rating-card {
        border: 1px solid #EAEAEC;
        border-radius: 6px;
        padding: 4px 8px;
        text-align: center;
        background: #FFFFFF;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }
    .pdp-rating-star {
        font-size: 0.76rem;
        font-weight: 800;
        color: #282C3F;
        display: flex;
        align-items: center;
        gap: 3px;
    }
    .pdp-rating-count {
        font-size: 0.65rem;
        color: #878B94;
        margin-top: 1px;
    }

    /* Pricing */
    .pdp-price-row {
        display: flex;
        align-items: baseline;
        gap: 8px;
        margin: 4px 0 2px 0;
    }
    .pdp-price-bold {
        font-size: 1.25rem;
        font-weight: 900;
        color: #282C3F;
    }
    .pdp-mrp {
        font-size: 0.85rem;
        color: #94969F;
        text-decoration: line-through;
    }
    .pdp-discount-tag {
        font-size: 0.76rem;
        font-weight: 800;
        color: #FF3F6C;
        background: #FFF0F4;
        padding: 2px 6px;
        border-radius: 4px;
    }
    .pdp-tax-note {
        font-size: 0.68rem;
        font-weight: 700;
        color: #03A685;
        margin-bottom: 12px;
    }

    /* Size Selector */
    .size-section-header {
        display: flex;
        justify-content: space-between;
        font-size: 0.78rem;
        font-weight: 800;
        margin: 12px 0 8px 0;
        color: #282C3F;
    }
    .size-chart-link {
        color: #FF3F6C;
        font-size: 0.74rem;
        cursor: pointer;
    }
    .size-pills-row {
        display: flex;
        gap: 8px;
        margin-bottom: 14px;
    }
    .size-circle {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        border: 1px solid #D4D5D9;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.78rem;
        font-weight: 700;
        color: #282C3F;
        background: #FFFFFF;
        position: relative;
    }
    .size-circle-active {
        border: 1.5px solid #FF3F6C !important;
        color: #FF3F6C !important;
        background: #FFF0F4 !important;
    }
    .size-disabled {
        color: #C4C5C9 !important;
        border-color: #E8E8EC !important;
        text-decoration: line-through;
    }
    .few-left-badge {
        position: absolute;
        top: -8px;
        font-size: 0.55rem;
        font-weight: 800;
        color: #E24444;
        background: #FFF0F0;
        padding: 1px 4px;
        border-radius: 4px;
        white-space: nowrap;
    }

    /* Delivery & Services Box */
    .delivery-box {
        border-top: 1px solid #F0F0F2;
        padding-top: 12px;
        margin-top: 10px;
    }
    .delivery-title {
        font-size: 0.82rem;
        font-weight: 800;
        color: #282C3F;
        margin-bottom: 8px;
    }
    .pin-input-mock {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 1px solid #D4D5D9;
        border-radius: 8px;
        padding: 8px 12px;
        font-size: 0.78rem;
        color: #878B94;
        margin-bottom: 10px;
    }
    .pin-check-btn {
        color: #FF3F6C;
        font-weight: 800;
        font-size: 0.75rem;
    }
    .service-point {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.74rem;
        color: #535766;
        margin-bottom: 5px;
    }

    /* Screen 2: Wishlist Top Header */
    .wishlist-header-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 6px 0 12px 0;
        border-bottom: 1px solid #F0F0F2;
        margin-bottom: 12px;
    }
    .wishlist-header-title {
        font-size: 0.95rem;
        font-weight: 800;
        color: #8A1550;
    }

    /* Wishlist Anchor Card */
    .wishlist-hero-card {
        background: #F9F5F0;
        border-radius: 12px;
        padding: 12px;
        position: relative;
        margin-bottom: 18px;
    }
    .wishlist-heart-fav {
        position: absolute;
        top: 18px;
        right: 18px;
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: #FFFFFF;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.95rem;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
    }
    .wishlist-hero-img {
        width: 100%;
        height: 340px;
        object-fit: cover;
        border-radius: 8px;
        display: block;
        margin-bottom: 10px;
    }
    .wishlist-card-brand {
        font-size: 0.75rem;
        font-weight: 800;
        color: #282C3F;
    }
    .wishlist-card-title {
        font-size: 0.8rem;
        color: #535766;
        margin: 2px 0 4px 0;
    }
    .wishlist-card-price {
        font-size: 0.92rem;
        font-weight: 800;
        color: #282C3F;
        margin-bottom: 8px;
    }

    /* Screen 2 "More from Wishlist" Grid */
    .more-wishlist-title {
        font-size: 0.88rem;
        font-weight: 800;
        color: #282C3F;
        margin-bottom: 10px;
    }
    .more-card {
        background: #F9FAFB;
        border-radius: 10px;
        padding: 8px;
        border: 1px solid #ECEEF0;
        position: relative;
    }
    .more-img {
        width: 100%;
        height: 140px;
        object-fit: cover;
        border-radius: 6px;
        display: block;
    }
    .more-fav-icon {
        position: absolute;
        top: 12px;
        right: 12px;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        background: #FFFFFF;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.7rem;
    }
    .more-brand {
        font-size: 0.72rem;
        font-weight: 800;
        color: #282C3F;
        margin-top: 5px;
    }
    .more-name {
        font-size: 0.68rem;
        color: #7E818C;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .more-price {
        font-size: 0.78rem;
        font-weight: 800;
        color: #282C3F;
        margin-top: 2px;
    }

    /* Screen 3: StyleSync AI Results Header */
    .stylesync-top-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 4px 0 10px 0;
        border-bottom: 1px solid #F0F0F2;
        margin-bottom: 12px;
    }
    .stylesync-logo-pink {
        font-size: 1.1rem;
        font-weight: 900;
        color: #FF3F6C;
        letter-spacing: -0.3px;
    }
    .ai-sync-heading {
        font-size: 1.1rem;
        font-weight: 900;
        color: #282C3F;
        margin-bottom: 2px;
    }
    .ai-sync-subtext {
        font-size: 0.76rem;
        color: #696E79;
        line-height: 1.35;
        margin-bottom: 14px;
    }

    /* Screen 3: Rule-of-3 Outfit Cards & Layered Collages */
    .look-card-screen3 {
        background: #FFFFFF;
        border: 1px solid #ECEEF0;
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 14px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }
    .look-card-top-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 4px;
    }
    .look-card-title {
        font-size: 0.88rem;
        font-weight: 800;
        color: #282C3F;
    }
    .look-badges-group {
        display: flex;
        gap: 6px;
        margin-bottom: 10px;
    }
    .badge-dark-owned {
        background: #282C3F;
        color: #FFFFFF;
        font-size: 0.65rem;
        font-weight: 700;
        padding: 3px 7px;
        border-radius: 4px;
    }
    .badge-offline {
        background: #F3E8FF;
        color: #7E22CE;
        font-size: 0.65rem;
        font-weight: 700;
        padding: 3px 7px;
        border-radius: 4px;
        border: 1px solid #E4CDFC;
    }
    .badge-fit-match {
        background: #E8F8F5;
        color: #03A685;
        font-size: 0.65rem;
        font-weight: 700;
        padding: 3px 7px;
        border-radius: 4px;
        border: 1px solid #B8EADF;
    }
    .badge-suggested-green {
        background: #ECFDF5;
        color: #047857;
        font-size: 0.65rem;
        font-weight: 700;
        padding: 3px 7px;
        border-radius: 4px;
    }

    /* Collage Stacks */
    .collage-container {
        position: relative;
        height: 230px;
        background: #FAF6F0;
        border-radius: 10px;
        overflow: hidden;
        margin-bottom: 10px;
    }
    .collage-base-blazer {
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 190px;
        height: 190px;
        object-fit: cover;
        border-radius: 8px;
        opacity: 0.95;
    }
    .collage-item-left {
        position: absolute;
        top: 14px;
        left: 14px;
        width: 140px;
        height: 140px;
        object-fit: cover;
        border-radius: 8px;
        border: 2px solid #FFFFFF;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.10);
        z-index: 2;
    }
    .collage-item-right {
        position: absolute;
        top: 35px;
        right: 14px;
        width: 155px;
        height: 155px;
        object-fit: cover;
        border-radius: 8px;
        border: 2px solid #FFFFFF;
        box-shadow: 0 6px 14px rgba(0, 0, 0, 0.12);
        z-index: 3;
    }
    .look-description-text {
        font-size: 0.74rem;
        color: #535766;
        line-height: 1.35;
    }

    /* Screen 3: WhatsApp Group Poll Section */
    .whatsapp-crew-box {
        border: 1.5px dashed #25D366;
        background-color: #F2FCF5;
        border-radius: 14px;
        padding: 14px;
        margin-top: 18px;
        margin-bottom: 16px;
    }
    .whatsapp-crew-title {
        font-size: 0.86rem;
        font-weight: 800;
        color: #0E7569;
        display: flex;
        align-items: center;
        gap: 6px;
        margin-bottom: 4px;
    }
    .whatsapp-crew-sub {
        font-size: 0.74rem;
        color: #535766;
        line-height: 1.35;
        margin-bottom: 10px;
    }
    .whatsapp-bubble-frame {
        background: #DCF8C6;
        border-radius: 10px 10px 2px 10px;
        padding: 12px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
        font-size: 0.80rem;
        color: #111B21;
        margin-top: 10px;
    }
    .whatsapp-poll-row {
        background: rgba(255, 255, 255, 0.85);
        border: 1px solid #C4E2B2;
        border-radius: 6px;
        padding: 6px 8px;
        margin-top: 5px;
        font-size: 0.74rem;
    }

    /* Bottom Navigation Bar (Visual Mockup) */
    .mobile-tab-bar {
        display: flex;
        justify-content: space-around;
        align-items: center;
        border-top: 1px solid #ECEEF0;
        padding: 10px 0 4px 0;
        margin-top: 20px;
        background: #FFFFFF;
    }
    .tab-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        font-size: 0.65rem;
        font-weight: 700;
        color: #696E79;
        gap: 2px;
    }
    .tab-active {
        color: #FF3F6C !important;
    }

    /* Primary Streamlit Button (Myntra Pink Gradient) */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #FF3F6C 0%, #FF527B 100%) !important;
        color: #FFFFFF !important;
        font-size: 0.88rem !important;
        font-weight: 800 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.65rem 1rem !important;
        box-shadow: 0 4px 12px rgba(255, 63, 108, 0.28) !important;
        width: 100% !important;
    }
    div.stButton > button[kind="primary"]:hover {
        box-shadow: 0 6px 16px rgba(255, 63, 108, 0.40) !important;
    }

    /* Secondary Streamlit Button (WhatsApp Green) */
    div.stButton > button[kind="secondary"] {
        background-color: #25D366 !important;
        color: #FFFFFF !important;
        font-size: 0.88rem !important;
        font-weight: 800 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.65rem 1rem !important;
        box-shadow: 0 4px 12px rgba(37, 211, 102, 0.28) !important;
        width: 100% !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        box-shadow: 0 6px 16px rgba(37, 211, 102, 0.40) !important;
    }

    /* Back Button Override */
    div.stButton > button:not([kind="primary"]):not([kind="secondary"]) {
        background-color: #FFFFFF !important;
        color: #282C3F !important;
        border: 1px solid #D4D5D9 !important;
        border-radius: 8px !important;
        font-size: 0.78rem !important;
        font-weight: 700 !important;
        padding: 0.4rem 0.8rem !important;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ==============================================================================
# 2. DATA SCHEMAS & WIZARD OF OZ DATASET
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

# Target Wishlisted Item (Mango Man Rust Linen Blazer)
TARGET_ITEM: TargetItem = {
    "id": "ITEM-9081",
    "name": "Rust Linen Relaxed-Fit Blazer",
    "brand": "MANGO MAN",
    "price": "₹3,499",
    "original_price": "₹4,999",
    "discount": "30% OFF",
    "rating": "4.2",
    "reviews": "124 Ratings",
    "image_url": "https://images.unsplash.com/photo-1598808503746-f34c53b9323e?w=800&auto=format&fit=crop&q=80"
}

# Image Assets for Collages & Wishlist recommendations
IMAGE_OLIVE_SHIRT = "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=400&auto=format&fit=crop&q=80"
IMAGE_BLACK_TROUSERS = "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=400&auto=format&fit=crop&q=80"
IMAGE_WHITE_TANK = "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=400&auto=format&fit=crop&q=80"
IMAGE_LIGHT_DENIM = "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=400&auto=format&fit=crop&q=80"
IMAGE_FOSSIL_WATCH = "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=400&auto=format&fit=crop&q=80"
IMAGE_PUMA_SNEAKERS = "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400&auto=format&fit=crop&q=80"


# ==============================================================================
# 3. ROUTER & STATE MACHINE
# ==============================================================================

def init_session_state() -> None:
    """Initializes session router defaults."""
    if "current_view" not in st.session_state:
        st.session_state["current_view"] = "pdp"
    if "poll_sent" not in st.session_state:
        st.session_state["poll_sent"] = False
    if "vote_feedback" not in st.session_state:
        st.session_state["vote_feedback"] = None

def navigate_to(view_name: str) -> None:
    """Transitions state machine to another screen."""
    st.session_state["current_view"] = view_name
    st.rerun()

init_session_state()


# ==============================================================================
# 4. SCREEN 1: DISCOVERY (PRODUCT DISPLAY PAGE - PDP)
# ==============================================================================

def render_screen_pdp() -> None:
    """Renders Screen 1: Discovery (PDP)."""
    # Top Navigation
    st.markdown(
        """<div class="pdp-top-nav">
<div class="nav-circle-btn">←</div>
<div class="pdp-nav-right">
<div class="nav-circle-btn">↗</div>
<div class="nav-circle-btn">🛍️</div>
</div>
</div>""",
        unsafe_allow_html=True
    )

    # Hero Image with Carousel Dots
    st.markdown(
        f"""<div class="pdp-hero-box">
<img src="{TARGET_ITEM['image_url']}" class="pdp-hero-img" alt="{TARGET_ITEM['name']}"/>
<div class="carousel-dots">
<div class="dot dot-active"></div>
<div class="dot"></div>
<div class="dot"></div>
<div class="dot"></div>
</div>
</div>""",
        unsafe_allow_html=True
    )

    # Product Title & Rating Card Row
    st.markdown(
        f"""<div class="pdp-title-row">
<div>
<div class="pdp-brand-title">{TARGET_ITEM['brand']}</div>
<div class="pdp-sub-title">{TARGET_ITEM['name']}</div>
</div>
<div class="pdp-rating-card">
<div class="pdp-rating-star">⭐ {TARGET_ITEM['rating']}</div>
<div class="pdp-rating-count">{TARGET_ITEM['reviews']}</div>
</div>
</div>

<div class="pdp-price-row">
<span class="pdp-price-bold">{TARGET_ITEM['price']}</span>
<span class="pdp-mrp">{TARGET_ITEM['original_price']}</span>
<span class="pdp-discount-tag">{TARGET_ITEM['discount']}</span>
</div>
<div class="pdp-tax-note">Inclusive of all taxes</div>

<div class="size-section-header">
<span>SELECT SIZE</span>
<span class="size-chart-link">SIZE CHART</span>
</div>
<div class="size-pills-row">
<div class="size-circle">
<span class="few-left-badge">Few Left</span>
38
</div>
<div class="size-circle size-circle-active">40</div>
<div class="size-circle">42</div>
<div class="size-circle">44</div>
<div class="size-circle size-disabled">46</div>
</div>

<div class="delivery-box">
<div class="delivery-title">Delivery & Services 🚚</div>
<div class="pin-input-mock">
<span>Enter PIN code</span>
<span class="pin-check-btn">CHECK</span>
</div>
<div class="service-point">🛍️ 100% Original Products</div>
<div class="service-point">₹ Pay on delivery might be available</div>
</div>""",
        unsafe_allow_html=True
    )

    st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)

    # Action Bar
    col_wish, col_bag = st.columns([1, 1])
    with col_wish:
        if st.button("🤍 WISHLIST", use_container_width=True):
            navigate_to("wishlist_anchor")
    with col_bag:
        if st.button("🛍️ ADD TO BAG", type="primary", use_container_width=True):
            st.toast("🛍️ Added Blazer to your Shopping Bag!")


# ==============================================================================
# 5. SCREEN 2: THE WISHLIST ANCHOR
# ==============================================================================

def render_screen_wishlist_anchor() -> None:
    """Renders Screen 2: The Wishlist Anchor."""
    # Top Navigation Header with Back button
    col_back, col_title, col_search = st.columns([1, 4, 1])
    with col_back:
        if st.button("←", use_container_width=True):
            navigate_to("pdp")
    with col_title:
        st.markdown("<div style='text-align: center; font-weight: 800; font-size: 0.95rem; color: #8A1550; padding-top: 6px;'>Wishlist (24 Items)</div>", unsafe_allow_html=True)
    with col_search:
        st.markdown("<div style='text-align: right; font-size: 1rem; padding-top: 6px;'>🔍</div>", unsafe_allow_html=True)

    # Saved Blazer Hero Card
    st.markdown(
        f"""<div class="wishlist-hero-card">
<div class="wishlist-heart-fav">❤️</div>
<img src="{TARGET_ITEM['image_url']}" class="wishlist-hero-img" alt="{TARGET_ITEM['name']}"/>
<div class="wishlist-card-brand">{TARGET_ITEM['brand']}</div>
<div class="wishlist-card-title">{TARGET_ITEM['name']}</div>
<div class="wishlist-card-price">{TARGET_ITEM['price']}</div>
</div>""",
        unsafe_allow_html=True
    )

    # The StyleSync Trigger Button
    if st.button("✨ Style with My Closet & Wishlist", type="primary", use_container_width=True):
        with st.spinner("Analyzing closet..."):
            time.sleep(1.5)
        navigate_to("stylesync_results")

    # "More from your Wishlist" Section
    st.markdown("<div class='more-wishlist-title' style='margin-top: 18px;'>More from your Wishlist</div>", unsafe_allow_html=True)
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.markdown(
            f"""<div class="more-card">
<div class="more-fav-icon">❤️</div>
<img src="{IMAGE_FOSSIL_WATCH}" class="more-img" alt="Fossil Watch"/>
<div style="font-size: 0.65rem; color: #282C3F; font-weight: 700; margin-top: 4px;">⭐ 4.8</div>
<div class="more-brand">Fossil</div>
<div class="more-name">Minimalist Analog Watch</div>
<div class="more-price">₹ 8,495</div>
</div>""",
            unsafe_allow_html=True
        )
    with m_col2:
        st.markdown(
            f"""<div class="more-card">
<div class="more-fav-icon">❤️</div>
<img src="{IMAGE_PUMA_SNEAKERS}" class="more-img" alt="Puma RS-X"/>
<div style="font-size: 0.65rem; color: #282C3F; font-weight: 700; margin-top: 4px;">⭐ 4.5</div>
<div class="more-brand">Puma</div>
<div class="more-name">RS-X Retro Sneakers</div>
<div class="more-price">₹ 5,999 <span style="font-size: 0.68rem; color: #94969F; text-decoration: line-through;">₹9,999</span></div>
</div>""",
            unsafe_allow_html=True
        )


# ==============================================================================
# 6. SCREEN 3: STYLESYNC AI RESULTS & SOCIAL LOOP
# ==============================================================================

def render_screen_stylesync_results() -> None:
    """Renders Screen 3: StyleSync AI Results & Social Loop."""
    # Top Bar
    col_menu, col_logo, col_back = st.columns([1, 3, 1])
    with col_menu:
        st.markdown("<div style='font-size: 1.1rem; padding-top: 4px;'>☰</div>", unsafe_allow_html=True)
    with col_logo:
        st.markdown("<div style='text-align: center;' class='stylesync-logo-pink'>StyleSync</div>", unsafe_allow_html=True)
    with col_back:
        if st.button("←", use_container_width=True, help="Back to Wishlist"):
            navigate_to("wishlist_anchor")

    # Header Copy
    st.markdown(
        """<div>
<div class="ai-sync-heading">AI Wardrobe Sync</div>
<div class="ai-sync-subtext">We styled your rust blazer with pieces you own and suggested fresh combos.</div>
</div>""",
        unsafe_allow_html=True
    )

    # Look 1: Smart Casual Card (Stacked Collage)
    st.markdown(
        f"""<div class="look-card-screen3">
<div class="look-card-top-row">
<span class="look-card-title">Smart Casual</span>
<span style="font-size: 0.9rem;">🤍</span>
</div>
<div class="look-badges-group">
<span class="badge-dark-owned">✔ 2 of 3 pieces owned</span>
<span class="badge-offline">📸 Offline Closet</span>
</div>
<div class="collage-container">
<img src="{TARGET_ITEM['image_url']}" class="collage-base-blazer" alt="Blazer"/>
<img src="{IMAGE_OLIVE_SHIRT}" class="collage-item-left" alt="Olive Shirt"/>
<img src="{IMAGE_BLACK_TROUSERS}" class="collage-item-right" alt="Black Trousers"/>
</div>
<div class="look-description-text">
The rust linen blazer pairs perfectly with your olive shirt and black tailored trousers for an effortless office-to-dinner transition.
</div>
</div>""",
        unsafe_allow_html=True
    )

    # Look 2: Weekend Brunch Card (Stacked Collage)
    st.markdown(
        f"""<div class="look-card-screen3">
<div class="look-card-top-row">
<span class="look-card-title">Weekend Brunch</span>
<span style="font-size: 0.9rem;">🤍</span>
</div>
<div class="look-badges-group">
<span class="badge-suggested-green">Suggested Pairings</span>
<span class="badge-fit-match">🎯 98% Match</span>
</div>
<div class="collage-container">
<img src="{TARGET_ITEM['image_url']}" class="collage-base-blazer" alt="Blazer"/>
<img src="{IMAGE_WHITE_TANK}" class="collage-item-left" alt="White Tank"/>
<img src="{IMAGE_LIGHT_DENIM}" class="collage-item-right" alt="Wide Leg Denim"/>
</div>
<div class="look-description-text">
Dress down the rust blazer with a crisp white tank and light wash wide-leg denim for a warm, breezy weekend aesthetic.
</div>
</div>""",
        unsafe_allow_html=True
    )

    # WhatsApp Social Validation Section
    st.markdown(
        """<div class="whatsapp-crew-box">
<div class="whatsapp-crew-title">
<span>💬</span> Can't decide? Ask your crew.
</div>
<div class="whatsapp-crew-sub">
Generate a poll and send it instantly to your WhatsApp friends to help you choose the best look.
</div>
</div>""",
        unsafe_allow_html=True
    )

    # WhatsApp Send Poll Action
    if not st.session_state.get("poll_sent", False):
        if st.button("💬 Send Buy or Drop Poll to WhatsApp", type="secondary", use_container_width=True):
            st.balloons()
            st.session_state["poll_sent"] = True
            st.rerun()

    # WhatsApp Chat Bubble Preview
    if st.session_state.get("poll_sent", False):
        st.markdown(
            """<div class="whatsapp-bubble-frame">
<div style="font-size: 0.76rem; font-weight: 800; color: #075E54; margin-bottom: 4px;">
📱 WhatsApp Group Poll (Recipient Preview)
</div>
<strong>"Help me choose! Getting this Rust Linen Blazer:"</strong>
<div class="whatsapp-poll-row">
<strong>1️⃣ Look 1: Smart Casual</strong><br/>
<span style="color: #555; font-size: 0.70rem;">Blazer + Olive Shirt + Black Trousers</span>
</div>
<div class="whatsapp-poll-row">
<strong>2️⃣ Look 2: Weekend Brunch</strong><br/>
<span style="color: #555; font-size: 0.70rem;">Blazer + White Tank + Wide-Leg Denim</span>
</div>
<div class="whatsapp-poll-row">
<strong>❌ Drop It</strong> <span style="color: #888; font-size: 0.70rem;">(Skip this purchase)</span>
</div>
<div style="font-size: 0.65rem; color: #667781; text-align: right; margin-top: 4px;">Just now &nbsp;✓✓</div>
</div>""",
            unsafe_allow_html=True
        )

        st.caption("Simulate friend votes:")
        s_col1, s_col2, s_col3 = st.columns(3)
        with s_col1:
            if st.button("🔥 Vote 1", use_container_width=True):
                st.session_state["vote_feedback"] = "🎉 **Priya voted for Look 1: Smart Casual**."
        with s_col2:
            if st.button("✨ Vote 2", use_container_width=True):
                st.session_state["vote_feedback"] = "🎉 **Rahul voted for Look 2: Weekend Brunch**."
        with s_col3:
            if st.button("🛑 Drop", use_container_width=True):
                st.session_state["vote_feedback"] = "💡 **Tanya suggested dropping this purchase.**"

        if st.session_state.get("vote_feedback"):
            st.info(st.session_state["vote_feedback"])

    # Mobile Tab Bar Navigation (Visual Mockup)
    st.markdown(
        """<div class="mobile-tab-bar">
<div class="tab-item"><span>🏠</span>Home</div>
<div class="tab-item"><span>▦</span>Categories</div>
<div class="tab-item"><span>🛍️</span>Studio</div>
<div class="tab-item tab-active"><span>✦</span>Explore</div>
<div class="tab-item"><span>👤</span>Profile</div>
</div>""",
        unsafe_allow_html=True
    )


# ==============================================================================
# 7. MAIN ORCHESTRATION ROUTER
# ==============================================================================

def main() -> None:
    """Main execution router."""
    init_session_state()
    current_view = st.session_state.get("current_view", "pdp")

    if current_view == "pdp":
        render_screen_pdp()
    elif current_view == "wishlist_anchor":
        render_screen_wishlist_anchor()
    elif current_view == "stylesync_results":
        render_screen_stylesync_results()
    else:
        render_screen_pdp()


if __name__ == "__main__":
    main()
