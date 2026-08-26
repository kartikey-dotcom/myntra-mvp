"""
Myntra "StyleSync" MVP - Desktop Web Application
================================================
High-Fidelity Desktop E-Commerce Experience with 3-Step User Journey Router:
1. Screen 1: Discovery (Desktop Product Display Page - PDP)
2. Screen 2: The Wishlist Anchor (Saved Blazer & Smart Wishlist Grid)
3. Screen 3: StyleSync AI Results & Social Loop (Rule-of-3 Collages & WhatsApp Peer Poll)
"""

import time
from typing import TypedDict, List, Dict
import streamlit as st

# ==============================================================================
# 1. PAGE CONFIGURATION & DESKTOP WEB DESIGN SYSTEM
# ==============================================================================

st.set_page_config(
    page_title="Myntra StyleSync - AI Wardrobe Matcher",
    page_icon="🛍️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    /* Global reset & typography */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        color: #282C3F;
        background-color: #F5F5F6;
    }

    /* Streamlit top header adjustment */
    header[data-testid="stHeader"] {
        background: transparent !important;
        height: 2rem !important;
        z-index: 1 !important;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Desktop Viewport Container (960px Standard) */
    .block-container {
        max-width: 960px !important;
        padding-top: 2.2rem !important;
        padding-bottom: 3.5rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        background-color: #FFFFFF;
        min-height: 100vh;
        box-shadow: 0 4px 25px rgba(0, 0, 0, 0.06);
        border-radius: 16px;
        margin: auto;
    }

    /* Desktop Brand Header Bar */
    .desktop-header-wrap {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.2rem 0 1.2rem 0;
        border-bottom: 1.5px solid #F0F0F2;
        margin-bottom: 1.2rem;
    }
    .desktop-brand-left {
        display: flex;
        align-items: center;
        gap: 14px;
    }
    .desktop-brand-titles {
        display: flex;
        flex-direction: column;
    }
    .brand-main-title {
        display: flex;
        align-items: center;
        gap: 8px;
        line-height: 1.1;
    }
    .brand-wordmark {
        font-size: 1.5rem;
        font-weight: 900;
        letter-spacing: -0.5px;
        color: #282C3F;
    }
    .brand-stylesync-tag {
        font-size: 1.3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FF3F6C 0%, #FF7A00 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.3px;
    }
    .brand-ai-pill {
        font-size: 0.68rem;
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
        font-size: 0.74rem;
        color: #878B94;
        font-weight: 500;
        margin-top: 2px;
    }
    .desktop-header-right {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .wishlist-counter-badge {
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
    }

    /* Breadcrumbs */
    .breadcrumb-bar {
        font-size: 0.76rem;
        color: #94969F;
        margin-bottom: 1.2rem;
    }
    .breadcrumb-bar span {
        color: #282C3F;
        font-weight: 600;
    }

    /* Screen 1: Desktop PDP 2-Column Grid */
    .desktop-pdp-layout {
        display: grid;
        grid-template-columns: 440px 1fr;
        gap: 36px;
        align-items: start;
        margin-bottom: 2rem;
    }
    .pdp-gallery-box {
        display: flex;
        flex-direction: column;
        gap: 12px;
    }
    .pdp-main-hero-img {
        width: 100%;
        height: 520px;
        object-fit: cover;
        border-radius: 12px;
        background-color: #F8F3EE;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
    }
    .pdp-thumb-row {
        display: flex;
        gap: 10px;
    }
    .pdp-thumb-img {
        width: 70px;
        height: 85px;
        object-fit: cover;
        border-radius: 6px;
        border: 1.5px solid #EAEAEC;
        cursor: pointer;
    }
    .pdp-thumb-active {
        border-color: #FF3F6C !important;
    }

    /* PDP Details */
    .pdp-brand-heading {
        font-size: 1.35rem;
        font-weight: 900;
        color: #282C3F;
        letter-spacing: -0.3px;
        margin-bottom: 2px;
    }
    .pdp-title-heading {
        font-size: 1.1rem;
        color: #535766;
        font-weight: 500;
        margin-bottom: 12px;
    }
    .pdp-rating-strip {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        border: 1px solid #EAEAEC;
        border-radius: 6px;
        padding: 5px 10px;
        font-size: 0.82rem;
        font-weight: 700;
        color: #282C3F;
        background: #FAFAFA;
        margin-bottom: 14px;
    }
    .pdp-price-container {
        display: flex;
        align-items: baseline;
        gap: 12px;
        margin: 6px 0 2px 0;
    }
    .pdp-price-highlight {
        font-size: 1.7rem;
        font-weight: 900;
        color: #282C3F;
    }
    .pdp-price-strikethrough {
        font-size: 1.1rem;
        color: #94969F;
        text-decoration: line-through;
    }
    .pdp-discount-pill {
        font-size: 0.9rem;
        font-weight: 800;
        color: #FF3F6C;
        background: #FFF0F4;
        padding: 3px 8px;
        border-radius: 6px;
    }
    .pdp-tax-caption {
        font-size: 0.74rem;
        font-weight: 700;
        color: #03A685;
        margin-bottom: 18px;
    }

    /* Size Selector Desktop */
    .pdp-size-title-row {
        display: flex;
        justify-content: space-between;
        font-size: 0.84rem;
        font-weight: 800;
        color: #282C3F;
        margin-bottom: 10px;
    }
    .pdp-size-chart-btn {
        color: #FF3F6C;
        font-size: 0.78rem;
        cursor: pointer;
    }
    .pdp-sizes-flex {
        display: flex;
        gap: 12px;
        margin-bottom: 20px;
    }
    .desktop-size-bubble {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        border: 1.5px solid #D4D5D9;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-size: 0.86rem;
        font-weight: 800;
        color: #282C3F;
        background: #FFFFFF;
        position: relative;
    }
    .desktop-size-active {
        border-color: #FF3F6C !important;
        color: #FF3F6C !important;
        background: #FFF0F4 !important;
    }
    .desktop-few-left {
        position: absolute;
        top: -9px;
        font-size: 0.55rem;
        font-weight: 800;
        color: #E24444;
        background: #FFF0F0;
        padding: 1px 4px;
        border-radius: 4px;
        white-space: nowrap;
    }

    /* Delivery & StyleSync Perk Box */
    .pdp-perk-card {
        background: #F8F9FA;
        border: 1px solid #ECEEF0;
        border-radius: 10px;
        padding: 14px;
        margin-top: 14px;
        margin-bottom: 20px;
        font-size: 0.80rem;
        color: #535766;
        line-height: 1.5;
    }

    /* Screen 2: Desktop Wishlist Anchor Card */
    .wishlist-desktop-card {
        background: #FAFAFB;
        border: 1px solid #EAEAEC;
        border-radius: 14px;
        padding: 20px;
        display: grid;
        grid-template-columns: 240px 1fr;
        gap: 24px;
        align-items: center;
        margin-bottom: 24px;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
        position: relative;
    }
    .wishlist-anchor-img {
        width: 240px;
        height: 320px;
        object-fit: cover;
        border-radius: 10px;
    }
    .wishlist-anchor-info {
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .wishlist-anchor-brand {
        font-size: 0.85rem;
        font-weight: 800;
        color: #94969F;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    .wishlist-anchor-title {
        font-size: 1.35rem;
        font-weight: 900;
        color: #282C3F;
        margin: 4px 0 8px 0;
    }
    .wishlist-anchor-price {
        font-size: 1.45rem;
        font-weight: 900;
        color: #282C3F;
        margin-bottom: 16px;
    }

    /* Screen 2: "More from your Wishlist" Desktop Grid */
    .more-wishlist-heading {
        font-size: 1.1rem;
        font-weight: 900;
        color: #282C3F;
        margin-bottom: 14px;
    }
    .more-grid-card {
        background: #FFFFFF;
        border: 1px solid #ECEEF0;
        border-radius: 10px;
        padding: 12px;
        height: 100%;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
    }
    .more-grid-img {
        width: 100%;
        height: 180px;
        object-fit: cover;
        border-radius: 8px;
        margin-bottom: 8px;
    }

    /* Screen 3: Desktop AI Results & Collages */
    .ai-results-banner {
        background: #E8F8F5;
        border-left: 4px solid #03A685;
        border-radius: 8px;
        padding: 12px 18px;
        margin-bottom: 20px;
        font-size: 0.88rem;
        color: #03A685;
        font-weight: 700;
    }
    .desktop-look-card {
        background: #FAFAFB;
        border: 1px solid #EAEAEC;
        border-radius: 14px;
        padding: 18px;
        display: flex;
        flex-direction: column;
        height: 100%;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
    }
    .desktop-look-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }
    .desktop-look-title {
        font-size: 1.1rem;
        font-weight: 900;
        color: #282C3F;
    }
    .desktop-badges-group {
        display: flex;
        gap: 8px;
        margin-bottom: 12px;
    }
    .badge-dark-owned {
        background: #282C3F;
        color: #FFFFFF;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 6px;
    }
    .badge-offline {
        background: #F3E8FF;
        color: #7E22CE;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 6px;
        border: 1px solid #E4CDFC;
    }
    .badge-fit-match {
        background: #E8F8F5;
        color: #03A685;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 6px;
        border: 1px solid #B8EADF;
    }
    .badge-suggested-green {
        background: #ECFDF5;
        color: #047857;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 6px;
    }

    /* Desktop Collage Box */
    .desktop-collage-container {
        position: relative;
        height: 280px;
        background: #F3EFE9;
        border-radius: 12px;
        overflow: hidden;
        margin-bottom: 14px;
    }
    .desktop-collage-base {
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 240px;
        height: 240px;
        object-fit: cover;
        border-radius: 8px;
        opacity: 0.95;
    }
    .desktop-collage-left {
        position: absolute;
        top: 16px;
        left: 16px;
        width: 170px;
        height: 170px;
        object-fit: cover;
        border-radius: 8px;
        border: 2.5px solid #FFFFFF;
        box-shadow: 0 6px 14px rgba(0, 0, 0, 0.12);
        z-index: 2;
    }
    .desktop-collage-right {
        position: absolute;
        top: 45px;
        right: 16px;
        width: 185px;
        height: 185px;
        object-fit: cover;
        border-radius: 8px;
        border: 2.5px solid #FFFFFF;
        box-shadow: 0 8px 18px rgba(0, 0, 0, 0.14);
        z-index: 3;
    }
    .desktop-look-caption {
        font-size: 0.82rem;
        color: #535766;
        line-height: 1.45;
    }

    /* Screen 3: Desktop WhatsApp Social Loop */
    .desktop-whatsapp-card {
        border: 2px dashed #25D366;
        background-color: #F4FAF5;
        border-radius: 14px;
        padding: 20px;
        margin-top: 24px;
        margin-bottom: 20px;
    }
    .desktop-whatsapp-title {
        font-size: 1.05rem;
        font-weight: 900;
        color: #0E7569;
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 4px;
    }
    .desktop-whatsapp-sub {
        font-size: 0.82rem;
        color: #535766;
        margin-bottom: 14px;
    }
    .desktop-whatsapp-bubble {
        background: #DCF8C6;
        border-radius: 12px 12px 2px 12px;
        padding: 16px 20px;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.12);
        font-size: 0.88rem;
        color: #111B21;
        margin-top: 14px;
    }
    .whatsapp-option-item {
        background: rgba(255, 255, 255, 0.90);
        border: 1px solid #C4E2B2;
        border-radius: 8px;
        padding: 8px 12px;
        margin-top: 8px;
        font-size: 0.82rem;
    }

    /* Primary Streamlit Button (Myntra Pink Gradient) */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #FF3F6C 0%, #FF527B 100%) !important;
        color: #FFFFFF !important;
        font-size: 0.94rem !important;
        font-weight: 800 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.4rem !important;
        box-shadow: 0 4px 14px rgba(255, 63, 108, 0.28) !important;
        width: 100% !important;
        transition: all 0.15s ease-in-out !important;
    }
    div.stButton > button[kind="primary"]:hover {
        box-shadow: 0 6px 18px rgba(255, 63, 108, 0.42) !important;
        transform: translateY(-1px) !important;
    }

    /* Secondary Streamlit Button (WhatsApp Green) */
    div.stButton > button[kind="secondary"] {
        background-color: #25D366 !important;
        color: #FFFFFF !important;
        font-size: 0.94rem !important;
        font-weight: 800 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.4rem !important;
        box-shadow: 0 4px 14px rgba(37, 211, 102, 0.28) !important;
        width: 100% !important;
        transition: all 0.15s ease-in-out !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        box-shadow: 0 6px 18px rgba(37, 211, 102, 0.42) !important;
        transform: translateY(-1px) !important;
    }

    /* Top Header Bar Clickable Wishlist Pill Button */
    .st-key-nav_wishlist_btn_pdp button,
    .st-key-nav_wishlist_btn_wishlist_anchor button,
    .st-key-nav_wishlist_btn_stylesync_results button {
        background-color: #FFF0F4 !important;
        color: #FF3F6C !important;
        border: 1.5px solid #FFD8E4 !important;
        border-radius: 20px !important;
        font-size: 0.84rem !important;
        font-weight: 800 !important;
        padding: 0.45rem 1.1rem !important;
        box-shadow: 0 2px 6px rgba(255, 63, 108, 0.08) !important;
        transition: all 0.15s ease !important;
        margin-top: 4px !important;
    }
    .st-key-nav_wishlist_btn_pdp button:hover,
    .st-key-nav_wishlist_btn_wishlist_anchor button:hover,
    .st-key-nav_wishlist_btn_stylesync_results button:hover {
        background-color: #FFE2EB !important;
        border-color: #FF3F6C !important;
        color: #FF3F6C !important;
        transform: translateY(-1px) !important;
    }

    /* Back / Outline Buttons */
    div.stButton > button:not([kind="primary"]):not([kind="secondary"]) {
        background-color: #FFFFFF !important;
        color: #282C3F !important;
        border: 1.5px solid #D4D5D9 !important;
        border-radius: 8px !important;
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        padding: 0.5rem 1rem !important;
    }
    div.stButton > button:not([kind="primary"]):not([kind="secondary"]):hover {
        border-color: #282C3F !important;
        background-color: #F8F8F9 !important;
    }

    /* Footer Trust */
    .desktop-trust-footer {
        text-align: center;
        color: #94969F;
        font-size: 0.78rem;
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid #EEEEF0;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ==============================================================================
# 2. DATA SCHEMAS & HIGH-RESOLUTION ASSETS
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
    "reviews": "124 Verified Customer Ratings",
    "image_url": "https://images.unsplash.com/photo-1598808503746-f34c53b9323e?w=800&auto=format&fit=crop&q=80"
}

# Image Assets for Collages & Wishlist recommendations
IMAGE_OLIVE_SHIRT = "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=400&auto=format&fit=crop&q=80"
IMAGE_BLACK_TROUSERS = "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=400&auto=format&fit=crop&q=80"
IMAGE_WHITE_TANK = "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=400&auto=format&fit=crop&q=80"
IMAGE_LIGHT_DENIM = "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=400&auto=format&fit=crop&q=80"
IMAGE_FOSSIL_WATCH = "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=400&auto=format&fit=crop&q=80"
IMAGE_PUMA_SNEAKERS = "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400&auto=format&fit=crop&q=80"

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
        "name": "The Minimalist 3H Black Dial Leather Watch",
        "price": "₹8,495",
        "original_price": "₹10,495",
        "discount": "19% OFF",
        "rating": "4.8 ★ (890)",
        "image_url": "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=500&auto=format&fit=crop&q=80",
        "tag": "Accessory Match"
    },
    {
        "id": "W-102",
        "brand": "PUMA",
        "name": "RS-X Efekt Retro Chunky Unisex Sneakers",
        "price": "₹5,999",
        "original_price": "₹9,999",
        "discount": "40% OFF",
        "rating": "4.5 ★ (1.4k)",
        "image_url": "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=500&auto=format&fit=crop&q=80",
        "tag": "Footwear Match"
    },
    {
        "id": "W-103",
        "brand": "ZARA MAN",
        "name": "Slim-Fit Textured Cotton Knit Polo Shirt",
        "price": "₹2,290",
        "original_price": "₹2,990",
        "discount": "23% OFF",
        "rating": "4.6 ★ (620)",
        "image_url": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=500&auto=format&fit=crop&q=80",
        "tag": "Closet Sync"
    },
    {
        "id": "W-104",
        "brand": "LEVI'S",
        "name": "511 Slim Fit Light Wash Selvedge Jeans",
        "price": "₹3,799",
        "original_price": "₹4,999",
        "discount": "24% OFF",
        "rating": "4.7 ★ (2.1k)",
        "image_url": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=500&auto=format&fit=crop&q=80",
        "tag": "Weekend Pair"
    },
    {
        "id": "W-105",
        "brand": "H&M EDITION",
        "name": "Premium Suede Chelsea Ankle Boots",
        "price": "₹4,499",
        "original_price": "₹5,999",
        "discount": "25% OFF",
        "rating": "4.4 ★ (410)",
        "image_url": "https://images.unsplash.com/photo-1608256246200-53e635b5b65f?w=500&auto=format&fit=crop&q=80",
        "tag": "Trending"
    },
    {
        "id": "W-106",
        "brand": "RAY-BAN",
        "name": "Hexagonal Flat Lenses Gold-Tone Sunglasses",
        "price": "₹7,190",
        "original_price": "₹8,990",
        "discount": "20% OFF",
        "rating": "4.9 ★ (1.8k)",
        "image_url": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=500&auto=format&fit=crop&q=80",
        "tag": "Summer Essential"
    }
]


# ==============================================================================
# 3. ROUTER & STATE MACHINE
# ==============================================================================

def init_session_state() -> None:
    """Initializes router state defaults."""
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
# 4. SHARED DESKTOP HEADER & FOOTER
# ==============================================================================

def render_desktop_header() -> None:
    """Renders the authentic Myntra Desktop Header with Vector Ribbon Logo & Clickable Wishlist."""
    h_col1, h_col2 = st.columns([3.8, 1.2])
    with h_col1:
        st.markdown(
            """<div class="desktop-header-wrap" style="border-bottom: none; margin-bottom: 0; padding-bottom: 0;">
<div class="desktop-brand-left">
<svg width="44" height="35" viewBox="0 0 108 84" fill="none" xmlns="http://www.w3.org/2000/svg">
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
<div class="desktop-brand-titles">
<div class="brand-main-title">
<span class="brand-wordmark">myntra</span>
<span class="brand-stylesync-tag">StyleSync</span>
<span class="brand-ai-pill">✦ AI</span>
</div>
<div class="brand-subtext">Smart Wardrobe Matcher & Lookbook</div>
</div>
</div>
</div>""",
            unsafe_allow_html=True
        )
    with h_col2:
        current_view = st.session_state.get("current_view", "pdp")
        # Clickable Wishlist Pill Button
        if st.button("💛 Wishlist (24)", key=f"nav_wishlist_btn_{current_view}", use_container_width=True, help="Open your saved Wishlist"):
            navigate_to("wishlist_anchor")

    st.markdown("<div style='border-bottom: 1.5px solid #F0F0F2; margin-bottom: 1.2rem; margin-top: 4px;'></div>", unsafe_allow_html=True)


def render_desktop_footer() -> None:
    """Renders authentic e-commerce trust footer."""
    st.markdown(
        """<div class="desktop-trust-footer">
🔒 <strong>100% Original Products</strong> &nbsp;•&nbsp; 🚚 <strong>Free Express Delivery</strong> &nbsp;•&nbsp; 🔄 <strong>Easy 14 Days Returns & Exchanges</strong>
</div>""",
        unsafe_allow_html=True
    )


# ==============================================================================
# 5. SCREEN 1: DISCOVERY (DESKTOP PRODUCT DISPLAY PAGE - PDP)
# ==============================================================================

def render_screen_pdp() -> None:
    """Renders Screen 1: Desktop PDP Layout."""
    render_desktop_header()

    st.markdown(
        """<div class="breadcrumb-bar">
Home / Men / Western Wear / Blazers / <span>MANGO MAN Rust Linen Relaxed-Fit Blazer</span>
</div>""",
        unsafe_allow_html=True
    )

    st.markdown(
        f"""<div class="desktop-pdp-layout">
<div class="pdp-gallery-box">
<img src="{TARGET_ITEM['image_url']}" class="pdp-main-hero-img" alt="{TARGET_ITEM['name']}"/>
<div class="pdp-thumb-row">
<img src="{TARGET_ITEM['image_url']}" class="pdp-thumb-img pdp-thumb-active"/>
<img src="{IMAGE_OLIVE_SHIRT}" class="pdp-thumb-img"/>
<img src="{IMAGE_BLACK_TROUSERS}" class="pdp-thumb-img"/>
</div>
</div>

<div>
<div class="pdp-brand-heading">{TARGET_ITEM['brand']}</div>
<div class="pdp-title-heading">{TARGET_ITEM['name']}</div>
<div class="pdp-rating-strip">
⭐ <strong>{TARGET_ITEM['rating']}</strong> &nbsp;|&nbsp; {TARGET_ITEM['reviews']}
</div>

<div class="pdp-price-container">
<span class="pdp-price-highlight">{TARGET_ITEM['price']}</span>
<span class="pdp-price-strikethrough">{TARGET_ITEM['original_price']}</span>
<span class="pdp-discount-pill">{TARGET_ITEM['discount']}</span>
</div>
<div class="pdp-tax-caption">inclusive of all taxes</div>

<div class="pdp-size-title-row">
<span>SELECT SIZE</span>
<span class="pdp-size-chart-btn">SIZE CHART & FIT GUIDE</span>
</div>
<div class="pdp-sizes-flex">
<div class="desktop-size-bubble">
<span class="desktop-few-left">Few Left</span>
38
</div>
<div class="desktop-size-bubble desktop-size-active">40</div>
<div class="desktop-size-bubble">42</div>
<div class="desktop-size-bubble">44</div>
</div>

<div class="pdp-perk-card">
<strong>⚡ StyleSync AI Wardrobe Check Available:</strong><br/>
Save this blazer to your Wishlist to see instant <strong>Rule-of-3 outfit pairings</strong> matched with your past Myntra orders and camera-roll closet.
</div>
</div>
</div>""",
        unsafe_allow_html=True
    )

    # Action Buttons (Side by Side in Desktop PDP)
    col_empty, col_wish, col_bag = st.columns([1.1, 1, 1])
    with col_wish:
        if st.button("🤍 SAVE TO WISHLIST", use_container_width=True):
            navigate_to("wishlist_anchor")
    with col_bag:
        if st.button("🛍️ ADD TO BAG", type="primary", use_container_width=True):
            st.toast("🛍️ Added Mango Man Rust Linen Blazer to your Bag!")


# ==============================================================================
# 6. SCREEN 2: THE WISHLIST ANCHOR (DESKTOP WEB VIEW)
# ==============================================================================

def render_screen_wishlist_anchor() -> None:
    """Renders Screen 2: The Wishlist Anchor Desktop Web View."""
    # Top Navigation Row with Back to Product button
    nav_col1, nav_col2 = st.columns([1, 4])
    with nav_col1:
        if st.button("← Back to Product", use_container_width=True):
            navigate_to("pdp")

    render_desktop_header()

    st.markdown(
        f"""<div class="wishlist-desktop-card">
<img src="{TARGET_ITEM['image_url']}" class="wishlist-anchor-img" alt="{TARGET_ITEM['name']}"/>
<div class="wishlist-anchor-info">
<div class="wishlist-anchor-brand">{TARGET_ITEM['brand']}</div>
<div class="wishlist-anchor-title">{TARGET_ITEM['name']}</div>
<div class="wishlist-anchor-price">{TARGET_ITEM['price']} <span style="font-size: 0.95rem; color: #94969F; text-decoration: line-through;">{TARGET_ITEM['original_price']}</span> <span style="font-size: 0.85rem; color: #FF3F6C; background: #FFF0F4; padding: 2px 6px; border-radius: 4px;">{TARGET_ITEM['discount']}</span></div>
<div style="font-size: 0.82rem; color: #535766; margin-bottom: 16px;">
✨ <em>Unsure how to style this blazer? StyleSync analyzes your existing closet in 1-tap.</em>
</div>
</div>
</div>""",
        unsafe_allow_html=True
    )

    # The StyleSync Trigger CTA Button
    if st.button("✨ Style with My Closet & Wishlist", type="primary", use_container_width=True):
        with st.spinner("Analyzing closet & past purchases..."):
            time.sleep(1.5)
        navigate_to("stylesync_results")

    # "More from your Wishlist" Section (Desktop 3-Column Grid)
    st.markdown("<div class='more-wishlist-heading' style='margin-top: 28px;'>Saved Items in Your Wishlist (6 Pieces)</div>", unsafe_allow_html=True)
    
    # 3-Column Desktop Grid for Wishlist items
    grid_cols = st.columns(3)
    for idx, prod in enumerate(WISHLIST_PRODUCTS):
        with grid_cols[idx % 3]:
            st.markdown(
                f"""<div class="more-grid-card" style="margin-bottom: 16px;">
<div style="position: relative;">
<img src="{prod['image_url']}" class="more-grid-img" alt="{prod['name']}"/>
<div style="position: absolute; top: 8px; right: 8px; background: #FFF; width: 26px; height: 26px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.75rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">❤️</div>
</div>
<div style="font-size: 0.68rem; color: #03A685; font-weight: 700; background: #E8F8F5; padding: 2px 6px; border-radius: 4px; display: inline-block; margin-bottom: 4px;">{prod['tag']}</div>
<div style="font-size: 0.70rem; color: #282C3F; font-weight: 700;">{prod['rating']}</div>
<div style="font-size: 0.84rem; font-weight: 800; color: #282C3F; margin-top: 2px;">{prod['brand']}</div>
<div style="font-size: 0.76rem; color: #535766; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{prod['name']}</div>
<div style="font-size: 0.90rem; font-weight: 800; color: #282C3F; margin-top: 4px;">{prod['price']} <span style="font-size: 0.74rem; color: #94969F; text-decoration: line-through;">{prod['original_price']}</span> <span style="font-size: 0.72rem; color: #FF3F6C; background: #FFF0F4; padding: 1px 4px; border-radius: 3px;">{prod['discount']}</span></div>
</div>""",
                unsafe_allow_html=True
            )
            if st.button("🛍️ Move to Bag", key=f"move_to_bag_{prod['id']}", use_container_width=True):
                st.toast(f"🛍️ Moved {prod['brand']} {prod['name'][:20]}... to your Bag!")


# ==============================================================================
# 7. SCREEN 3: STYLESYNC AI RESULTS & SOCIAL LOOP (DESKTOP WEB VIEW)
# ==============================================================================

def render_screen_stylesync_results() -> None:
    """Renders Screen 3: StyleSync AI Results & Social Loop Desktop Web View."""
    nav_col1, nav_col2 = st.columns([1, 4])
    with nav_col1:
        if st.button("← Back to Wishlist", use_container_width=True):
            navigate_to("wishlist_anchor")

    render_desktop_header()

    st.markdown(
        """<div class="ai-results-banner">
🎉 <strong>Wardrobe Compatibility: 98% Match</strong> &nbsp;•&nbsp; Paired with 2 pieces already in your wardrobe!
</div>""",
        unsafe_allow_html=True
    )

    # 2-Column Desktop Lookbook Grid
    l_col1, l_col2 = st.columns(2)

    # Look 1: Smart Casual
    with l_col1:
        st.markdown(
            f"""<div class="desktop-look-card">
<div class="desktop-look-header">
<span class="desktop-look-title">Look 1: Smart Casual</span>
<span style="font-size: 1.1rem;">🤍</span>
</div>
<div class="desktop-badges-group">
<span class="badge-dark-owned">✔ 2 of 3 pieces owned</span>
<span class="badge-offline">📸 Offline Closet</span>
</div>
<div class="desktop-collage-container">
<img src="{TARGET_ITEM['image_url']}" class="desktop-collage-base" alt="Blazer"/>
<img src="{IMAGE_OLIVE_SHIRT}" class="desktop-collage-left" alt="Olive Shirt"/>
<img src="{IMAGE_BLACK_TROUSERS}" class="desktop-collage-right" alt="Black Trousers"/>
</div>
<div class="desktop-look-caption">
The rust linen blazer pairs seamlessly with your <strong>Olive Linen Shirt</strong> (from camera-roll closet) and <strong>Black Tailored Trousers</strong> for an effortless office-to-dinner transition.
</div>
</div>""",
            unsafe_allow_html=True
        )

    # Look 2: Weekend Brunch
    with l_col2:
        st.markdown(
            f"""<div class="desktop-look-card">
<div class="desktop-look-header">
<span class="desktop-look-title">Look 2: Weekend Brunch</span>
<span style="font-size: 1.1rem;">🤍</span>
</div>
<div class="desktop-badges-group">
<span class="badge-suggested-green">Suggested Pairings</span>
<span class="badge-fit-match">🎯 98% Fit Match</span>
</div>
<div class="desktop-collage-container">
<img src="{TARGET_ITEM['image_url']}" class="desktop-collage-base" alt="Blazer"/>
<img src="{IMAGE_WHITE_TANK}" class="desktop-collage-left" alt="White Tank"/>
<img src="{IMAGE_LIGHT_DENIM}" class="desktop-collage-right" alt="Wide Leg Denim"/>
</div>
<div class="desktop-look-caption">
Dress down the rust blazer with a crisp <strong>White Ribbed Tank</strong> and <strong>Light Wash Wide-Leg Denim</strong> for a breezy, contemporary weekend aesthetic.
</div>
</div>""",
            unsafe_allow_html=True
        )

    # WhatsApp Social Loop Card (Wide Desktop Layout)
    st.markdown(
        """<div class="desktop-whatsapp-card">
<div class="desktop-whatsapp-title">
<span>💬</span> Can't decide? Ask your crew on WhatsApp.
</div>
<div class="desktop-whatsapp-sub">
Generate an interactive poll and send it directly to your friends before making the purchase.
</div>
</div>""",
        unsafe_allow_html=True
    )

    # WhatsApp Trigger Button
    if not st.session_state.get("poll_sent", False):
        if st.button("💬 Send Buy or Drop Poll to WhatsApp", type="secondary", use_container_width=True):
            st.balloons()
            st.session_state["poll_sent"] = True
            st.rerun()

    # Interactive WhatsApp Chat Mockup
    if st.session_state.get("poll_sent", False):
        st.markdown(
            """<div class="desktop-whatsapp-bubble">
<div style="font-size: 0.82rem; font-weight: 800; color: #075E54; margin-bottom: 6px;">
📱 WhatsApp Group Poll (Live Friend Preview)
</div>
<strong>"Help me choose! Thinking of buying this Mango Man Rust Linen Blazer:"</strong>
<div class="whatsapp-option-item">
<strong>1️⃣ Look 1: Smart Casual</strong><br/>
<span style="color: #555; font-size: 0.76rem;">Blazer + Olive Linen Shirt + Black Tailored Trousers</span>
</div>
<div class="whatsapp-option-item">
<strong>2️⃣ Look 2: Weekend Brunch</strong><br/>
<span style="color: #555; font-size: 0.76rem;">Blazer + White Ribbed Tank + Wide-Leg Denim</span>
</div>
<div class="whatsapp-option-item">
<strong>❌ Drop It</strong> <span style="color: #888; font-size: 0.76rem;">(Skip this purchase)</span>
</div>
<div style="font-size: 0.70rem; color: #667781; text-align: right; margin-top: 6px;">Just now &nbsp;✓✓</div>
</div>""",
            unsafe_allow_html=True
        )

        st.caption("Simulate friend votes:")
        s_col1, s_col2, s_col3 = st.columns(3)
        with s_col1:
            if st.button("🔥 Vote Look 1", use_container_width=True):
                st.session_state["vote_feedback"] = "🎉 **Priya voted for Look 1: Smart Casual**."
        with s_col2:
            if st.button("✨ Vote Look 2", use_container_width=True):
                st.session_state["vote_feedback"] = "🎉 **Rahul voted for Look 2: Weekend Brunch**."
        with s_col3:
            if st.button("🛑 Drop It", use_container_width=True):
                st.session_state["vote_feedback"] = "💡 **Tanya suggested dropping this purchase.**"

        if st.session_state.get("vote_feedback"):
            st.info(st.session_state["vote_feedback"])


# ==============================================================================
# 8. MAIN EXECUTION ROUTER
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

    render_desktop_footer()


if __name__ == "__main__":
    main()
