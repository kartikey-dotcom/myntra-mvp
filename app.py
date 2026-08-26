"""
Myntra "StyleSync" MVP - Two-Screen User Journey Router (PDP -> Wishlist)
========================================================================
High-Fidelity AI-Powered Smart Closet & Social Validation System.

Routing Architecture:
- Screen 1: Product Display Page (PDP) -> "Mango Man Rust Linen Blazer" with Hero Image & Size Selection.
- Transition Action: "❤️ Save to Wishlist" routes seamlessly into Screen 2.
- Screen 2: The StyleSync Wishlist -> AI Wardrobe Matcher, Rule-of-3 Lookbook, and WhatsApp Social Loop.
- Return Action: "← Back to Product" allows infinite bi-directional evaluation.
"""

import time
from typing import TypedDict, List, Dict
import streamlit as st

# ==============================================================================
# 1. PAGE CONFIGURATION & GLOBAL CSS DESIGN SYSTEM
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

    /* Global Typography & Theme */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        color: #282C3F;
        background-color: #F4F4F6;
    }

    /* Hide default Streamlit top header bar */
    header[data-testid="stHeader"] {
        background: transparent !important;
        height: 2.2rem !important;
        z-index: 1 !important;
    }

    /* Main Container (Desktop / Tablet Standard) */
    .block-container {
        max-width: 860px !important;
        padding-top: 3.2rem !important;
        padding-bottom: 3rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
        background-color: #FFFFFF;
        min-height: 100vh;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.05);
        border-radius: 16px;
    }

    /* Brand Header Bar */
    .brand-header-wrap {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.2rem 0 1.2rem 0;
        border-bottom: 1.5px solid #F0F0F2;
        margin-bottom: 1.5rem;
    }
    .brand-lockup-left {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .brand-title-group {
        display: flex;
        flex-direction: column;
    }
    .brand-main-title {
        display: flex;
        align-items: center;
        gap: 6px;
        line-height: 1.1;
    }
    .brand-wordmark {
        font-size: 1.45rem;
        font-weight: 900;
        letter-spacing: -0.6px;
        color: #282C3F;
    }
    .brand-stylesync-tag {
        font-size: 1.25rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FF3F6C 0%, #FF7A00 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.3px;
    }
    .brand-ai-badge {
        font-size: 0.65rem;
        font-weight: 800;
        color: #FF3F6C;
        background: #FFF0F4;
        border: 1px solid #FFD8E4;
        border-radius: 4px;
        padding: 2px 6px;
        margin-left: 2px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .brand-subtext {
        font-size: 0.73rem;
        color: #878B94;
        font-weight: 500;
        margin-top: 2px;
    }
    .wishlist-pill {
        background: #FFF0F4;
        color: #FF3F6C;
        font-size: 0.82rem;
        font-weight: 700;
        padding: 6px 14px;
        border-radius: 20px;
        border: 1px solid #FFD8E4;
        display: flex;
        align-items: center;
        gap: 6px;
        box-shadow: 0 1px 4px rgba(255, 63, 108, 0.08);
    }

    /* Screen 1: Product Display Page (PDP) Layout */
    .pdp-hero-container {
        display: grid;
        grid-template-columns: 360px 1fr;
        gap: 28px;
        margin-bottom: 2rem;
        align-items: start;
    }
    @media (max-width: 768px) {
        .pdp-hero-container {
            grid-template-columns: 1fr;
        }
    }
    .pdp-hero-img {
        width: 100%;
        height: 480px;
        object-fit: cover;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
    }
    .pdp-brand-tag {
        font-size: 0.85rem;
        font-weight: 800;
        color: #94969F;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .pdp-product-title {
        font-size: 1.45rem;
        font-weight: 800;
        color: #282C3F;
        margin: 4px 0 8px 0;
        line-height: 1.25;
    }
    .pdp-rating-chip {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        font-size: 0.78rem;
        font-weight: 700;
        color: #282C3F;
        background: #FFFFFF;
        border: 1px solid #E0E0E4;
        border-radius: 4px;
        padding: 4px 8px;
        margin-bottom: 12px;
    }
    .pdp-price-wrap {
        display: flex;
        align-items: baseline;
        gap: 10px;
        margin: 8px 0 16px 0;
    }
    .pdp-price-current {
        font-size: 1.6rem;
        font-weight: 800;
        color: #282C3F;
    }
    .pdp-price-mrp {
        font-size: 1.05rem;
        color: #94969F;
        text-decoration: line-through;
    }
    .pdp-discount-badge {
        font-size: 0.88rem;
        font-weight: 700;
        color: #FF3F6C;
        background: #FFF0F4;
        padding: 3px 8px;
        border-radius: 6px;
    }
    .pdp-size-picker {
        margin: 16px 0;
    }
    .pdp-size-title {
        font-size: 0.8rem;
        font-weight: 700;
        color: #282C3F;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .pdp-size-options {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
    }
    .pdp-size-circle {
        width: 42px;
        height: 42px;
        border-radius: 50%;
        border: 1.5px solid #D4D5D9;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.82rem;
        font-weight: 700;
        color: #282C3F;
        background: #FFFFFF;
        cursor: pointer;
    }
    .pdp-size-selected {
        border-color: #FF3F6C !important;
        color: #FF3F6C !important;
        background: #FFF0F4 !important;
    }
    .pdp-perks-box {
        background: #F9FAFB;
        border: 1px solid #ECEEF0;
        border-radius: 10px;
        padding: 12px;
        margin: 16px 0;
        font-size: 0.78rem;
        color: #535766;
        line-height: 1.5;
    }

    /* Screen 2: StyleSync Wishlist Product Card */
    .product-card {
        background: #FFFFFF;
        border-radius: 14px;
        border: 1px solid #EAEAEC;
        padding: 18px;
        box-shadow: 0 4px 16px rgba(40, 44, 63, 0.05);
        margin-bottom: 1.25rem;
    }
    .anchor-grid {
        display: grid;
        grid-template-columns: 140px 1fr;
        gap: 20px;
        align-items: center;
    }
    .anchor-img {
        width: 140px;
        height: 186px;
        object-fit: cover;
        border-radius: 10px;
        background-color: #F5F5F6;
    }
    .anchor-details {
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .anchor-brand {
        font-size: 0.78rem;
        font-weight: 700;
        color: #94969F;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    .anchor-title {
        font-size: 1.25rem;
        font-weight: 800;
        color: #282C3F;
        margin: 4px 0 6px 0;
        line-height: 1.25;
    }
    .anchor-price-row {
        display: flex;
        align-items: baseline;
        gap: 8px;
        margin: 4px 0 8px 0;
    }
    .anchor-price-now {
        font-size: 1.35rem;
        font-weight: 800;
        color: #282C3F;
    }
    .anchor-price-orig {
        font-size: 0.95rem;
        color: #94969F;
        text-decoration: line-through;
    }
    .anchor-discount {
        font-size: 0.82rem;
        font-weight: 700;
        color: #FF3F6C;
        background: #FFF0F4;
        padding: 3px 8px;
        border-radius: 6px;
    }

    /* Custom Badges (Pill-shaped) */
    .badge-owned {
        background-color: #E8F8F5;
        color: #03A685;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 14px;
        display: inline-block;
        margin-top: 6px;
        border: 1px solid #B8EADF;
    }
    .badge-offline {
        background-color: #F3E8FF;
        color: #7E22CE;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 14px;
        display: inline-block;
        margin-top: 6px;
        border: 1px solid #E4CDFC;
    }
    .badge-wishlist {
        background-color: #FFF4EE;
        color: #FF905A;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 14px;
        display: inline-block;
        margin-top: 6px;
        border: 1px solid #FFE0D0;
    }
    .badge-fit {
        background-color: #ECFDF5;
        color: #047857;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 14px;
        display: inline-block;
        margin-top: 6px;
        border: 1px solid #A7F3D0;
    }
    .badge-target {
        background-color: #FFF0F4;
        color: #FF3F6C;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 14px;
        display: inline-block;
        margin-top: 6px;
        border: 1px solid #FFCDD2;
    }

    /* Lookbook Card */
    .lookbook-column-card {
        background: #FAFAFB;
        border: 1px solid #EAEAEC;
        border-radius: 14px;
        padding: 14px;
        display: flex;
        flex-direction: column;
        height: 100%;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
    }
    .lookbook-title {
        font-size: 0.95rem;
        font-weight: 800;
        color: #282C3F;
        margin-bottom: 3px;
    }
    .lookbook-subtitle {
        font-size: 0.75rem;
        color: #7E818C;
        margin-bottom: 10px;
    }
    .lookbook-item-block {
        margin-bottom: 10px;
        background: #FFFFFF;
        border-radius: 10px;
        padding: 8px;
        border: 1px solid #EEEEF0;
        display: flex;
        flex-direction: column;
    }
    .lookbook-img {
        width: 100%;
        height: 160px;
        object-fit: cover;
        border-radius: 8px;
    }
    .lookbook-item-title {
        font-size: 0.78rem;
        font-weight: 700;
        color: #282C3F;
        margin-top: 6px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    /* Primary CTA Button Override (Myntra Pink Gradient) */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #FF3F6C 0%, #FF527B 100%) !important;
        color: #FFFFFF !important;
        font-size: 0.92rem !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.7rem 1.2rem !important;
        box-shadow: 0 4px 14px rgba(255, 63, 108, 0.28) !important;
        width: 100% !important;
        transition: all 0.15s ease-in-out !important;
    }
    div.stButton > button[kind="primary"]:hover {
        box-shadow: 0 6px 18px rgba(255, 63, 108, 0.42) !important;
        transform: translateY(-1px) !important;
    }

    /* Secondary CTA Button Override (WhatsApp Green) */
    div.stButton > button[kind="secondary"] {
        background-color: #25D366 !important;
        color: #FFFFFF !important;
        font-size: 0.92rem !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.7rem 1.2rem !important;
        box-shadow: 0 4px 14px rgba(37, 211, 102, 0.28) !important;
        width: 100% !important;
        transition: all 0.15s ease-in-out !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        box-shadow: 0 6px 18px rgba(37, 211, 102, 0.42) !important;
        transform: translateY(-1px) !important;
    }

    /* iOS WhatsApp Chat Frame */
    .whatsapp-bubble-wrapper {
        background-color: #EFEAE2;
        background-image: radial-gradient(#D8D2C9 0.8px, transparent 0.8px);
        background-size: 10px 10px;
        border-radius: 14px;
        padding: 14px;
        border: 1px solid #D6CEC5;
        margin-top: 12px;
    }
    .whatsapp-bubble-box {
        background-color: #DCF8C6;
        border-radius: 10px 10px 2px 10px;
        padding: 14px 16px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
        color: #111B21;
        font-size: 0.86rem;
        position: relative;
    }
    .whatsapp-header-tag {
        font-size: 0.78rem;
        font-weight: 800;
        color: #075E54;
        display: flex;
        align-items: center;
        gap: 6px;
        margin-bottom: 8px;
    }
    .whatsapp-poll-option {
        background: rgba(255, 255, 255, 0.88);
        border: 1px solid #C4E2B2;
        border-radius: 6px;
        padding: 8px 10px;
        margin-top: 6px;
        font-size: 0.80rem;
    }
    .whatsapp-meta-time {
        font-size: 0.68rem;
        color: #667781;
        text-align: right;
        margin-top: 6px;
    }

    /* Banners */
    .custom-success-banner {
        background: #E8F8F5;
        border-left: 4px solid #03A685;
        border-radius: 8px;
        padding: 10px 14px;
        margin: 10px 0;
        font-size: 0.84rem;
        color: #03A685;
        font-weight: 600;
    }
    .custom-feedback-banner {
        background: #F4F6F8;
        border: 1px solid #E0E4E8;
        border-radius: 8px;
        padding: 10px 12px;
        margin-top: 8px;
        font-size: 0.80rem;
        color: #282C3F;
        font-weight: 600;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ==============================================================================
# 2. DATA ARCHITECTURE & HIGH-RESOLUTION ASSETS
# ==============================================================================

class TargetItem(TypedDict):
    id: str
    name: str
    brand: str
    price: str
    original_price: str
    discount: str
    status: str
    rating: str
    color: str
    material: str
    image_url: str

class WardrobeItem(TypedDict):
    name: str
    badge: str
    badge_class: str
    image_url: str

class OutfitItem(TypedDict):
    role: str
    name: str
    badge: str
    badge_class: str
    image_url: str

class OutfitLook(TypedDict):
    id: str
    title: str
    subtitle: str
    badge_summary: str
    items: List[OutfitItem]

# Target Wishlisted Item (Mango Man Rust Linen Blazer)
TARGET_ITEM: TargetItem = {
    "id": "ITEM-9081",
    "name": "Rust Linen Relaxed-Fit Blazer",
    "brand": "MANGO MAN",
    "price": "₹3,499",
    "original_price": "₹4,999",
    "discount": "30% OFF",
    "status": "In Wishlist 5d",
    "rating": "4.4 ★ (1.2k Ratings)",
    "color": "Rust Terracotta",
    "material": "100% Organic Linen",
    "image_url": "https://images.unsplash.com/photo-1598808503746-f34c53b9323e?w=800&auto=format&fit=crop&q=80"
}

# Rule-of-3 Modular Looks
OUTFIT_LOOKS: List[OutfitLook] = [
    {
        "id": "look_1",
        "title": "Look 1: Smart Casual",
        "subtitle": "Work & City Ready",
        "badge_summary": "✨ 2 Owned Pieces in Closet",
        "items": [
            {
                "role": "Top",
                "name": "Olive Linen Shirt",
                "badge": "📸 Offline Closet",
                "badge_class": "badge-offline",
                "image_url": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=400&auto=format&fit=crop&q=80"
            },
            {
                "role": "Bottoms",
                "name": "Black Trousers",
                "badge": "✅ In Closet (Myntra)",
                "badge_class": "badge-owned",
                "image_url": "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=400&auto=format&fit=crop&q=80"
            }
        ]
    },
    {
        "id": "look_2",
        "title": "Look 2: Weekend Brunch",
        "subtitle": "Relaxed Chic",
        "badge_summary": "🔥 High Social Match",
        "items": [
            {
                "role": "Top",
                "name": "White Ribbed Tank",
                "badge": "💡 Suggested Pair",
                "badge_class": "badge-fit",
                "image_url": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=400&auto=format&fit=crop&q=80"
            },
            {
                "role": "Accessory",
                "name": "Minimalist Watch",
                "badge": "💛 From Wishlist",
                "badge_class": "badge-wishlist",
                "image_url": "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=400&auto=format&fit=crop&q=80"
            }
        ]
    }
]


# ==============================================================================
# 3. ROUTER & STATE MANAGEMENT
# ==============================================================================

def init_session_state() -> None:
    """Initializes session state defaults."""
    if "current_view" not in st.session_state:
        # Default view is Product Display Page (PDP)
        st.session_state["current_view"] = "pdp"
    if "is_styled" not in st.session_state:
        st.session_state["is_styled"] = False
    if "poll_sent" not in st.session_state:
        st.session_state["poll_sent"] = False
    if "vote_feedback" not in st.session_state:
        st.session_state["vote_feedback"] = None

def navigate_to(view_name: str) -> None:
    """Safely transitions between router screens."""
    st.session_state["current_view"] = view_name
    st.rerun()

# Run initialization immediately
init_session_state()


# ==============================================================================
# 4. SHARED COMPONENTS
# ==============================================================================

def render_brand_header(show_back_button: bool = False) -> None:
    """Renders authentic Myntra brand lockup with optional back navigation."""
    nav_left_html = """
    <div class="brand-lockup-left">
        <!-- Authentic Myntra Vector SVG Ribbon Logo -->
        <svg width="42" height="34" viewBox="0 0 108 84" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M14.5 73.2C8.2 63.8 7.5 45.3 17.8 28.2C27.5 12.1 40.1 6.5 43.7 13.2C47.4 20 38.3 38.8 28.5 54.8C19.8 69.1 18.2 78.7 14.5 73.2Z" fill="url(#myntra_pink)"/>
            <path d="M43.7 13.2C40.1 6.5 27.5 12.1 17.8 28.2C27.2 43.8 45.4 69.8 54.2 72.8C63 75.8 56.4 51.2 43.7 13.2Z" fill="url(#myntra_orange)" opacity="0.95"/>
            <path d="M64.3 13.2C67.9 6.5 80.5 12.1 90.2 28.2C80.8 43.8 62.6 69.8 53.8 72.8C45 75.8 51.6 51.2 64.3 13.2Z" fill="url(#myntra_orange)" opacity="0.95"/>
            <path d="M93.5 73.2C99.8 63.8 100.5 45.3 90.2 28.2C80.5 12.1 67.9 6.5 64.3 13.2C60.6 20 69.7 38.8 79.5 54.8C88.2 69.1 89.8 78.7 93.5 73.2Z" fill="url(#myntra_pink)"/>
            <defs>
                <linearGradient id="myntra_pink" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#FF3F6C" />
                    <stop offset="100%" stop-color="#EA1D76" />
                </linearGradient>
                <linearGradient id="myntra_orange" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#FF7A00" />
                    <stop offset="100%" stop-color="#FF527B" />
                </linearGradient>
            </defs>
        </svg>
        <div class="brand-title-group">
            <div class="brand-main-title">
                <span class="brand-wordmark">myntra</span>
                <span class="brand-stylesync-tag">StyleSync</span>
                <span class="brand-ai-badge">✦ AI</span>
            </div>
            <div class="brand-subtext">Smart Wardrobe Matcher & Lookbook</div>
        </div>
    </div>
    """
    
    st.markdown(
        f"""
        <div class="brand-header-wrap">
            {nav_left_html}
            <div class="wishlist-pill">
                💛 Wishlist (24)
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_footer() -> None:
    """Authentic Clean E-commerce Trust Footer."""
    st.markdown(
        """
        <div style="text-align: center; color: #94969F; font-size: 0.72rem; margin-top: 2.5rem; padding-top: 1.2rem; border-top: 1px solid #EEEEF0;">
            🔒 <strong>100% Original Products</strong> &nbsp;•&nbsp; 🚚 <strong>Free Express Delivery</strong> &nbsp;•&nbsp; 🔄 <strong>Easy 14 Days Returns</strong>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==============================================================================
# 5. SCREEN 1: PRODUCT DISPLAY PAGE (PDP)
# ==============================================================================

def render_pdp_screen() -> None:
    """Renders high-fidelity Myntra Product Page (PDP) for the Rust Linen Blazer."""
    render_brand_header(show_back_button=False)

    st.markdown(
        f"""
        <div class="pdp-hero-container">
            <div>
                <img src="{TARGET_ITEM['image_url']}" class="pdp-hero-img" alt="{TARGET_ITEM['name']}"/>
            </div>
            <div>
                <div class="pdp-brand-tag">{TARGET_ITEM['brand']}</div>
                <div class="pdp-product-title">{TARGET_ITEM['name']}</div>
                <div class="pdp-rating-chip">
                    ⭐ <strong>4.4</strong> | 1.2k Verified Ratings
                </div>
                <div class="pdp-price-wrap">
                    <span class="pdp-price-current">{TARGET_ITEM['price']}</span>
                    <span class="pdp-price-mrp">{TARGET_ITEM['original_price']}</span>
                    <span class="pdp-discount-badge">{TARGET_ITEM['discount']}</span>
                </div>
                <div style="font-size: 0.76rem; color: #03A685; font-weight: 700; margin-bottom: 12px;">
                    inclusive of all taxes
                </div>
                <div class="pdp-size-picker">
                    <div class="pdp-size-title">Select Size</div>
                    <div class="pdp-size-options">
                        <div class="pdp-size-circle">S</div>
                        <div class="pdp-size-circle pdp-size-selected">M</div>
                        <div class="pdp-size-circle">L</div>
                        <div class="pdp-size-circle">XL</div>
                    </div>
                </div>
                <div class="pdp-perks-box">
                    <strong>⚡ StyleSync Wardrobe Check Available:</strong><br/>
                    Save this item to your Wishlist to see instant Rule-of-3 outfit pairings matched with your past Myntra orders and camera-roll closet.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Action Buttons Container
    pdp_col1, pdp_col2 = st.columns([1, 1])
    with pdp_col1:
        if st.button(
            "❤️ Save to Wishlist",
            type="primary",
            use_container_width=True,
            help="Adds blazer to Wishlist and opens StyleSync AI Matcher"
        ):
            navigate_to("wishlist")

    with pdp_col2:
        if st.button(
            "🛍️ Add to Bag",
            type="secondary",
            use_container_width=True
        ):
            st.toast("🛍️ Added Mango Man Rust Linen Blazer to your Bag!")


# ==============================================================================
# 6. SCREEN 2: THE STYLESYNC WISHLIST
# ==============================================================================

def render_wishlist_screen() -> None:
    """Renders the complete StyleSync Wishlist with AI Closet Matching and WhatsApp Loop."""
    # Top Navigation with Back to PDP button
    back_col, _ = st.columns([1, 4])
    with back_col:
        if st.button("← Back to Product", use_container_width=True):
            navigate_to("pdp")

    render_brand_header(show_back_button=True)

    # Wishlist Anchor Card
    st.markdown(
        f"""
        <div class="product-card">
            <div class="anchor-grid">
                <img src="{TARGET_ITEM['image_url']}" class="anchor-img" alt="{TARGET_ITEM['name']}"/>
                <div class="anchor-details">
                    <div class="anchor-brand">{TARGET_ITEM['brand']}</div>
                    <div class="anchor-title">{TARGET_ITEM['name']}</div>
                    <div class="anchor-price-row">
                        <span class="anchor-price-now">{TARGET_ITEM['price']}</span>
                        <span class="anchor-price-orig">{TARGET_ITEM['original_price']}</span>
                        <span class="anchor-discount">{TARGET_ITEM['discount']}</span>
                    </div>
                    <div>
                        <span class="badge-target">🎯 Wishlist Anchor</span>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Primary Action Trigger to Style
    if not st.session_state.get("is_styled", False):
        st.caption("Unsure how to style this blazer? StyleSync matches your closet in 1-tap.")
        if st.button(
            "✨ Style with My Closet & Wishlist",
            type="primary",
            use_container_width=True
        ):
            simulate_ai_matching()

    # Lookbook and Social Loop Renderings
    if st.session_state.get("is_styled", False):
        render_lookbook()
        render_social_loop()


def simulate_ai_matching() -> None:
    """Simulates multi-stage neural wardrobe matching with 2.0s delay."""
    status_placeholder = st.empty()
    with status_placeholder.container():
        with st.spinner("🔍 Scanning purchase history & camera roll closet..."):
            time.sleep(1.0)
        with st.spinner("✨ Composing Rule-of-3 modular outfits..."):
            time.sleep(1.0)
    status_placeholder.empty()
    st.session_state["is_styled"] = True
    st.rerun()


def render_lookbook() -> None:
    """Renders Rule-of-3 Outfits in 2 Columns with Vertical Stacks and Custom Badges."""
    st.markdown(
        """
        <div class="custom-success-banner">
            🎉 <strong>Wardrobe Compatibility: 96% Match</strong><br/>
            <span style="font-size: 0.74rem; font-weight: normal; color: #282C3F;">
                Paired with items already in your closet!
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    # Look 1 Column
    with col1:
        look1 = OUTFIT_LOOKS[0]
        st.markdown(
            f"""
            <div class="lookbook-column-card">
                <div class="lookbook-title">{look1['title']}</div>
                <div class="lookbook-subtitle">{look1['subtitle']}</div>
            """,
            unsafe_allow_html=True
        )
        for item in look1["items"]:
            st.markdown(
                f"""
                <div class="lookbook-item-block">
                    <img src="{item['image_url']}" class="lookbook-img" alt="{item['name']}"/>
                    <div class="lookbook-item-title">{item['name']}</div>
                    <span class="{item['badge_class']}">{item['badge']}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
        st.markdown(
            f"""
                <div style="font-size: 0.68rem; color: #03A685; font-weight: 700; text-align: center; margin-top: 4px;">
                    {look1['badge_summary']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Look 2 Column
    with col2:
        look2 = OUTFIT_LOOKS[1]
        st.markdown(
            f"""
            <div class="lookbook-column-card">
                <div class="lookbook-title">{look2['title']}</div>
                <div class="lookbook-subtitle">{look2['subtitle']}</div>
            """,
            unsafe_allow_html=True
        )
        for item in look2["items"]:
            st.markdown(
                f"""
                <div class="lookbook-item-block">
                    <img src="{item['image_url']}" class="lookbook-img" alt="{item['name']}"/>
                    <div class="lookbook-item-title">{item['name']}</div>
                    <span class="{item['badge_class']}">{item['badge']}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
        st.markdown(
            f"""
                <div style="font-size: 0.68rem; color: #FF3F6C; font-weight: 700; text-align: center; margin-top: 4px;">
                    {look2['badge_summary']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


def render_social_loop() -> None:
    """Renders WhatsApp iOS Mockup with #DCF8C6 Chat Bubble & Interactive Poll Buttons."""
    st.markdown("<div style='margin-top: 1.2rem;'></div>", unsafe_allow_html=True)
    st.markdown("##### 💬 Can't decide? Ask your friends.")
    st.caption("Send a 1-tap poll to your WhatsApp group before buying.")

    # WhatsApp Dispatch Button
    if not st.session_state.get("poll_sent", False):
        if st.button(
            "💬 Send Poll to WhatsApp",
            type="secondary",
            use_container_width=True
        ):
            st.balloons()
            st.session_state["poll_sent"] = True
            st.rerun()

    # iOS WhatsApp Chat Bubble
    if st.session_state.get("poll_sent", False):
        st.markdown(
            """
            <div class="whatsapp-bubble-wrapper">
                <div class="whatsapp-bubble-box">
                    <div class="whatsapp-header-tag">
                        <span>📱</span> WhatsApp Group Poll Preview
                    </div>
                    <strong>"Help me choose! Getting this Rust Linen Blazer:"</strong>
                    <div class="whatsapp-poll-option">
                        <strong>1️⃣ Look 1: Smart Casual</strong><br/>
                        <span style="color: #555; font-size: 0.72rem;">Blazer + Olive Shirt + Black Trousers</span>
                    </div>
                    <div class="whatsapp-poll-option">
                        <strong>2️⃣ Look 2: Weekend Brunch</strong><br/>
                        <span style="color: #555; font-size: 0.72rem;">Blazer + Ribbed Tank + Gold Watch</span>
                    </div>
                    <div class="whatsapp-poll-option">
                        <strong>❌ Drop It</strong> <span style="color: #888; font-size: 0.72rem;">(Skip this)</span>
                    </div>
                    <div class="whatsapp-meta-time">Just now &nbsp;✓✓</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
        st.caption("Simulate friend votes:")
        b_col1, b_col2, b_col3 = st.columns(3)
        with b_col1:
            if st.button("🔥 Vote Look 1", use_container_width=True):
                st.session_state["vote_feedback"] = "🎉 **Vote Received!** Priya voted for **Look 1: Smart Casual**."
        with b_col2:
            if st.button("✨ Vote Look 2", use_container_width=True):
                st.session_state["vote_feedback"] = "🎉 **Vote Received!** Rahul voted for **Look 2: Weekend Brunch**."
        with b_col3:
            if st.button("🛑 Drop It", use_container_width=True):
                st.session_state["vote_feedback"] = "💡 **Feedback Logged!** Tanya suggested skipping."

        if st.session_state.get("vote_feedback"):
            st.markdown(
                f"""
                <div class="custom-feedback-banner">
                    {st.session_state['vote_feedback']}
                </div>
                """,
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
        render_pdp_screen()
    else:
        render_wishlist_screen()

    render_footer()


if __name__ == "__main__":
    main()
