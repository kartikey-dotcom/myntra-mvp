"""
Myntra "StyleSync" MVP - AI-Powered Smart Closet & Social Validation System
==========================================================================
High-Fidelity "Wizard of Oz" Interactive UI Prototype.

Key Strategic Objectives:
1. Eliminate "Styling Paralysis" by orchestrating complete outfits pairing target
   wishlist items with past Myntra orders and user-uploaded offline wardrobe pieces.
2. Defend against "Off-Platform Leakage" via an integrated WhatsApp social validation loop.
3. Showcase the "Universal Closet" moat (bridging online Myntra purchases & offline camera roll uploads).

Architectural Notes:
- Wizard of Oz Architecture: Deterministic mock payloads + calibrated latency simulation (2s)
  to ensure zero-downtime, zero-failure stakeholder presentations.
- State Persistence: Explicit `st.session_state` management prevents UI reset on secondary actions.
"""

import time
from typing import TypedDict, List, Dict, Optional
import streamlit as st

# ==============================================================================
# 1. PAGE CONFIGURATION & CUSTOM STYLING (Myntra Brand Aesthetic)
# ==============================================================================

st.set_page_config(
    page_title="Myntra StyleSync | Smart Closet",
    page_icon="🛍️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom CSS for polished, responsive e-commerce look & feel (Myntra Design System)
CUSTOM_CSS = """
<style>
    /* Global Typography & Background adjustments */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #282C3F;
    }
    
    /* Main Streamlit Container */
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3.5rem;
        max-width: 800px;
    }
    
    /* Brand Header Banner */
    .brand-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-bottom: 0.9rem;
        border-bottom: 2px solid #F5F5F6;
        margin-bottom: 1.5rem;
    }
    .brand-logo {
        font-size: 1.65rem;
        font-weight: 900;
        letter-spacing: -0.5px;
        color: #282C3F;
    }
    .brand-logo span {
        color: #FF3F6C; /* Myntra Signature Pink */
    }
    .brand-tagline {
        font-size: 0.8rem;
        color: #FF3F6C;
        font-weight: 700;
        background-color: #FFF0F4;
        padding: 5px 12px;
        border-radius: 20px;
        border: 1px solid #FFD8E4;
        box-shadow: 0 1px 3px rgba(255, 63, 108, 0.08);
    }

    /* Product & Look Cards */
    .product-card {
        background: #FFFFFF;
        border: 1px solid #EAEAEC;
        border-radius: 16px;
        padding: 1.4rem;
        box-shadow: 0 4px 16px rgba(40, 44, 63, 0.06);
        margin-bottom: 1.25rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .product-card:hover {
        box-shadow: 0 6px 20px rgba(40, 44, 63, 0.10);
    }
    
    .look-card {
        background: #FAFAFB;
        border: 1px solid #E2E2E7;
        border-radius: 14px;
        padding: 1.2rem;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
        transition: all 0.25s ease-in-out;
    }
    .look-card:hover {
        border-color: #FF3F6C;
        background: #FFFFFF;
        box-shadow: 0 6px 20px rgba(255, 63, 108, 0.14);
        transform: translateY(-2px);
    }

    /* Badges & Psychological Anchors */
    .badge {
        display: inline-block;
        font-size: 0.76rem;
        font-weight: 700;
        padding: 4px 9px;
        border-radius: 6px;
        margin-top: 4px;
        letter-spacing: 0.1px;
    }
    .badge-owned-myntra {
        background-color: #E8F8F5;
        color: #0E7569;
        border: 1px solid #A3E4D7;
    }
    .badge-owned-offline {
        background-color: #EBF5FB;
        color: #1B4F72;
        border: 1px solid #AED6F1;
    }
    .badge-wishlist {
        background-color: #FEF9E7;
        color: #7D6608;
        border: 1px solid #F9E79F;
    }
    .badge-suggested {
        background-color: #F4ECF7;
        color: #5B2C6F;
        border: 1px solid #D7BDE2;
    }
    .badge-target {
        background-color: #FFF0F4;
        color: #D81B60;
        border: 1px solid #FFCDD2;
    }

    /* Custom Streamlit Button Overrides */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #FF3F6C 0%, #FF527B 100%) !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 1.2rem !important;
        box-shadow: 0 4px 12px rgba(255, 63, 108, 0.28) !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button[kind="primary"]:hover {
        box-shadow: 0 6px 16px rgba(255, 63, 108, 0.42) !important;
        transform: scale(1.01) !important;
    }

    div.stButton > button[kind="secondary"] {
        background-color: #25D366 !important; /* WhatsApp Green */
        color: #FFFFFF !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 1.2rem !important;
        box-shadow: 0 4px 12px rgba(37, 211, 102, 0.28) !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        box-shadow: 0 6px 16px rgba(37, 211, 102, 0.42) !important;
        transform: scale(1.01) !important;
    }

    /* WhatsApp Interactive Mockup */
    .whatsapp-container {
        background-color: #EFEAE2;
        background-image: radial-gradient(#D1D7DB 0.75px, transparent 0.75px);
        background-size: 12px 12px;
        border-radius: 16px;
        padding: 1.4rem;
        border: 1px solid #DAD3CC;
        margin-top: 1rem;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.05);
    }
    .whatsapp-bubble {
        background-color: #FFFFFF;
        border-radius: 12px 12px 12px 2px;
        padding: 16px 18px;
        max-width: 95%;
        box-shadow: 0 2px 4px rgba(0,0,0,0.10);
        font-size: 0.92rem;
        color: #111B21;
    }
    .whatsapp-meta {
        font-size: 0.72rem;
        color: #667781;
        text-align: right;
        margin-top: 6px;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ==============================================================================
# 2. PHASE 1: MOCK DATA ARCHITECTURE & SCHEMAS (Wizard of Oz Data Store)
# ==============================================================================
# NOTE FOR PM / PORTFOLIO REVIEW:
# In this high-fidelity prototype, data is hardcoded to guarantee 100% deterministic
# execution during stakeholder reviews while precisely modeling production schemas.

class TargetItem(TypedDict):
    id: str
    name: str
    brand: str
    price: str
    original_price: str
    discount: str
    status: str
    rating: str
    icon: str
    color: str
    material: str

class WardrobeItem(TypedDict):
    name: str
    badge: str
    badge_class: str
    icon: str

class OutfitItem(TypedDict):
    role: str
    name: str
    badge: str
    badge_class: str
    icon: str

class OutfitLook(TypedDict):
    id: str
    title: str
    subtitle: str
    badge_summary: str
    items: List[OutfitItem]

# 2.1. Target Wishlisted Item (The item triggering 'Styling Paralysis')
TARGET_ITEM: TargetItem = {
    "id": "ITEM-9081",
    "name": "Rust Linen Relaxed-Fit Blazer",
    "brand": "Roadster Signature Collection",
    "price": "₹3,499",
    "original_price": "₹4,999",
    "discount": "30% OFF",
    "status": "Added to Wishlist 5 days ago",
    "rating": "4.4 ★ (1.2k verified reviews)",
    "icon": "🧥",
    "color": "Rust Terracotta",
    "material": "100% Pure Organic Linen"
}

# 2.2. User's Historical Closet Purchases (Including the "Universal Closet" Moat)
# STRATEGIC MOAT: Combines verified on-platform Myntra order history with off-platform
# camera roll uploads, creating a cross-platform lock-in competitors cannot replicate.
PAST_PURCHASES: List[WardrobeItem] = [
    {
        "name": "Classic White Crewneck Tee",
        "badge": "✅ In your closet (Purchased on Myntra)",
        "badge_class": "badge-owned-myntra",
        "icon": "👕"
    },
    {
        "name": "Olive Linen Shirt",
        "badge": "📸 Offline Closet (Uploaded from Camera Roll)",
        "badge_class": "badge-owned-offline",
        "icon": "👔"
    }
]

# 2.3. User's Wishlist & Smart Catalog Recommendations
WISHLIST_INVENTORY: List[WardrobeItem] = [
    {
        "name": "Gold Minimalist Watch",
        "badge": "💛 From your Wishlist",
        "badge_class": "badge-wishlist",
        "icon": "⌚"
    },
    {
        "name": "Light Wash Wide-Leg Denim",
        "badge": "💡 Suggested Pairing - ₹1,899",
        "badge_class": "badge-suggested",
        "icon": "👖"
    },
    {
        "name": "White Ribbed Tank Top",
        "badge": "💡 Suggested Pairing - ₹799",
        "badge_class": "badge-suggested",
        "icon": "🎽"
    },
    {
        "name": "High-Waisted Black Trousers",
        "badge": "✅ In your closet (Purchased on Myntra)",
        "badge_class": "badge-owned-myntra",
        "icon": "👖"
    }
]

# 2.4. Rule-of-3 Pre-assembled Modular Outfits
OUTFIT_LOOKS: List[OutfitLook] = [
    {
        "id": "look_1",
        "title": "Look 1: Smart Casual Office",
        "subtitle": "Sharp, breathable & work-ready",
        "badge_summary": "✨ 2 of 3 Pieces in Your Closet",
        "items": [
            {
                "role": "Layer (Target)",
                "name": "Rust Linen Relaxed-Fit Blazer",
                "badge": "🎯 Target Wishlist Item (₹3,499)",
                "badge_class": "badge-target",
                "icon": "🧥"
            },
            {
                "role": "Base Top",
                "name": "Classic White Crewneck Tee",
                "badge": "✅ In your closet (Purchased on Myntra)",
                "badge_class": "badge-owned-myntra",
                "icon": "👕"
            },
            {
                "role": "Accent Layer",
                "name": "Olive Linen Shirt",
                "badge": "📸 Offline Closet (Uploaded from Camera Roll)",
                "badge_class": "badge-owned-offline",
                "icon": "👔"
            }
        ]
    },
    {
        "id": "look_2",
        "title": "Look 2: Weekend Brunch & Social",
        "subtitle": "Relaxed, warm & effortless chic",
        "badge_summary": "🔥 High Social Compatibility",
        "items": [
            {
                "role": "Layer (Target)",
                "name": "Rust Linen Relaxed-Fit Blazer",
                "badge": "🎯 Target Wishlist Item (₹3,499)",
                "badge_class": "badge-target",
                "icon": "🧥"
            },
            {
                "role": "Base Top",
                "name": "White Ribbed Tank Top",
                "badge": "💡 Suggested Pairing - ₹799",
                "badge_class": "badge-suggested",
                "icon": "🎽"
            },
            {
                "role": "Bottoms",
                "name": "Light Wash Wide-Leg Denim",
                "badge": "💡 Suggested Pairing - ₹1,899",
                "badge_class": "badge-suggested",
                "icon": "👖"
            },
            {
                "role": "Accessory",
                "name": "Gold Minimalist Watch",
                "badge": "💛 From your Wishlist",
                "badge_class": "badge-wishlist",
                "icon": "⌚"
            }
        ]
    }
]


# ==============================================================================
# 3. PHASE 2: STATE MANAGEMENT ENGINE (Streamlit Lifecycle Controller)
# ==============================================================================
# ARCHITECTURAL INSIGHT FOR STAKEHOLDERS:
# Streamlit adheres to an execution model where any user interaction (button click,
# input change) triggers a top-to-bottom re-execution of the entire Python script.
#
# To prevent "Lookbook Collapse" or "UI State Amnesia" when a user clicks secondary
# buttons (such as 'Send Poll to WhatsApp'), all dynamic UI gates MUST be bound to
# persistent keys in `st.session_state`.

def init_session_state() -> None:
    """
    Initializes session state defaults upon first session bootstrap.
    Guarantees idempotency on all subsequent script re-runs.
    """
    if "is_styled" not in st.session_state:
        # Flag: Controls visibility of Lookbook outfits & WhatsApp social loop
        st.session_state.is_styled = False

    if "poll_sent" not in st.session_state:
        # Flag: Controls WhatsApp message card render & confirmation banner
        st.session_state.poll_sent = False

    if "active_look" not in st.session_state:
        # State: Tracks which look is currently selected/highlighted for social polling
        st.session_state.active_look = "look_1"


def set_styled(status: bool = True) -> None:
    """Safely transitions the styling state flag."""
    st.session_state.is_styled = status


def set_poll_sent(status: bool = True) -> None:
    """Safely records that the WhatsApp poll was dispatched."""
    st.session_state.poll_sent = status


def reset_session_state() -> None:
    """
    Resets all interactive flags back to factory defaults.
    Provides a frictionless hook for live product demonstrations.
    """
    st.session_state.is_styled = False
    st.session_state.poll_sent = False
    st.session_state.active_look = "look_1"


def get_session_debug_state() -> Dict[str, any]:
    """Returns a snapshot dictionary of active session flags for debugging."""
    return {
        "is_styled": st.session_state.get("is_styled", False),
        "poll_sent": st.session_state.get("poll_sent", False),
        "active_look": st.session_state.get("active_look", "look_1")
    }


# Execute state initialization immediately on script startup
init_session_state()


# ==============================================================================
# 4. PHASE 3: PRESENTATION LAYER – HEADER & WISHLIST ANCHOR VIEW
# ==============================================================================

def render_header() -> None:
    """
    Renders the top branding header with authentic Myntra e-commerce styling.
    Includes breadcrumbs, live feature badge, and decorative separator.
    """
    st.markdown(
        """
        <div style="font-size: 0.75rem; color: #94969F; font-weight: 500; margin-bottom: 0.5rem;">
            Home / Wishlist / <span style="color: #282C3F; font-weight: 600;">StyleSync Assistant</span>
        </div>
        <div class="brand-header">
            <div>
                <div class="brand-logo">🛍️ myntra <span>StyleSync</span></div>
                <div style="font-size: 0.8rem; color: #696E79; margin-top: 2px;">
                    AI-Powered Wardrobe Companion & Smart Lookbook
                </div>
            </div>
            <div class="brand-tagline">✨ Rule of 3 Styling</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_anchor_card() -> None:
    """
    Renders Section 1: The Wishlist Item Anchor.
    Establishes the user's styling hesitation context with rich product metadata,
    pricing breakdown, discount pill, and primary styling action.
    """
    st.markdown("#### 📌 Target Wishlisted Item")
    
    st.markdown(
        f"""
        <div class="product-card">
            <div style="display: flex; gap: 1.25rem; align-items: center; flex-wrap: wrap;">
                <div style="font-size: 3.5rem; background: #FFF4F7; padding: 14px 20px; border-radius: 14px; border: 1px solid #FFDEE7; text-align: center;">
                    {TARGET_ITEM["icon"]}
                </div>
                <div style="flex-grow: 1; min-width: 240px;">
                    <div style="font-size: 0.78rem; color: #878B94; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">
                        {TARGET_ITEM["brand"]}
                    </div>
                    <div style="font-size: 1.22rem; font-weight: 800; color: #282C3F; margin: 3px 0;">
                        {TARGET_ITEM["name"]}
                    </div>
                    <div style="display: flex; align-items: baseline; gap: 10px; margin: 4px 0;">
                        <span style="font-size: 1.3rem; font-weight: 800; color: #282C3F;">{TARGET_ITEM["price"]}</span>
                        <span style="font-size: 0.95rem; color: #94969F; text-decoration: line-through;">{TARGET_ITEM["original_price"]}</span>
                        <span style="font-size: 0.85rem; color: #FF3F6C; font-weight: 700; background: #FFF0F4; padding: 2px 6px; border-radius: 4px;">{TARGET_ITEM["discount"]}</span>
                    </div>
                    <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-top: 6px;">
                        <span style="font-size: 0.75rem; background: #F5F5F6; color: #535766; padding: 3px 8px; border-radius: 4px; font-weight: 500;">
                            🎨 {TARGET_ITEM["color"]}
                        </span>
                        <span style="font-size: 0.75rem; background: #F5F5F6; color: #535766; padding: 3px 8px; border-radius: 4px; font-weight: 500;">
                            🧵 {TARGET_ITEM["material"]}
                        </span>
                        <span style="font-size: 0.75rem; background: #F5F5F6; color: #535766; padding: 3px 8px; border-radius: 4px; font-weight: 500;">
                            ⭐ {TARGET_ITEM["rating"]}
                        </span>
                    </div>
                    <div style="font-size: 0.76rem; color: #878B94; margin-top: 6px;">
                        ⏱️ {TARGET_ITEM["status"]} &nbsp;•&nbsp; 🚚 Free Express Delivery Available
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Primary Action Trigger to activate AI Closet Matching
    if not st.session_state.is_styled:
        st.caption("Hesitating on how to pair this blazer? Let StyleSync check your wardrobe.")
        if st.button(
            "✨ Style with My Closet & Wishlist",
            type="primary",
            use_container_width=True,
            help="Simulates AI pairing with your past Myntra orders and uploaded offline closet"
        ):
            simulate_ai_matching()

# ==============================================================================
# 5. PHASE 4: SIMULATED AI ORCHESTRATOR & TRANSITION ENGINE
# ==============================================================================
# STRATEGIC DESIGN RATIONALE:
# Rather than returning instant zero-latency results (which reduces perceived AI value)
# or calling an external LLM API (which introduces token costs & network failure risks),
# the prototype simulates a multi-step neural wardrobe matching pipeline with a
# calibrated 2.0-second delay.

def simulate_ai_matching() -> None:
    """
    Simulates the multi-stage neural wardrobe matching algorithm:
    1. Embeds target garment attributes (color palette, fabric, formality).
    2. Clusters user's past Myntra orders and camera-roll uploads.
    3. Solves Rule-of-3 modular look constraints.
    """
    status_placeholder = st.empty()
    with status_placeholder.container():
        with st.spinner("🔍 Step 1/2: Scanning purchase history & camera roll closet..."):
            time.sleep(1.0)
        with st.spinner("✨ Step 2/2: Composing Rule-of-3 modular outfits..."):
            time.sleep(1.0)
    status_placeholder.empty()
    
    # Lock Lookbook into session state and trigger reactive render
    set_styled(True)
    st.rerun()


# ==============================================================================
# 6. PHASE 5: LOOKBOOK PRESENTATION LAYER – RULE OF 3 OUTFIT GRID
# ==============================================================================
# PSYCHOLOGICAL PERSUASION FRAMEWORK:
# By visually demonstrating that the ₹3,499 Rust Linen Blazer instantly pairs with
# items already owned (both on Myntra and offline uploads), we trigger the 'Endowment Effect'
# and eliminate 'Styling Paralysis', turning a hesitant browser into a confident buyer.

def render_lookbook() -> None:
    """
    Renders Section 2: The Multi-Column Lookbook.
    Displays Rule-of-3 modular outfits with explicit psychological confidence tags,
    wardrobe ownership calculations, and catalog upselling cards.
    """
    st.markdown("---")
    st.markdown(
        """
        <div style="background: #E8F8F5; border-left: 4px solid #0E7569; padding: 12px 16px; border-radius: 8px; margin-bottom: 1.5rem; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
            <div>
                <strong style="color: #0E7569; font-size: 0.95rem;">🎉 Wardrobe Compatibility Check: High Match (96%)</strong>
                <div style="color: #282C3F; font-size: 0.85rem; margin-top: 2px;">
                    We created <strong>2 complete Rule-of-3 outfits</strong> using pieces already in your closet!
                </div>
            </div>
            <span style="background: #0E7569; color: #FFFFFF; font-size: 0.72rem; font-weight: 700; padding: 3px 8px; border-radius: 12px;">
                AI VERIFIED
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    # Column 1: Look 1 (Smart Casual Office)
    with col1:
        look = OUTFIT_LOOKS[0]
        st.markdown(
            f"""
            <div class="look-card">
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2px;">
                        <span style="font-size: 1.05rem; font-weight: 800; color: #282C3F;">{look["title"]}</span>
                        <span style="font-size: 0.72rem; font-weight: 700; color: #0E7569; background: #E8F8F5; padding: 2px 6px; border-radius: 4px;">OFFICE / CASUAL</span>
                    </div>
                    <div style="font-size: 0.78rem; color: #696E79; margin-bottom: 0.85rem;">{look["subtitle"]}</div>
                    <div style="border-top: 1px solid #EAEAEC; padding-top: 0.6rem;">
            """,
            unsafe_allow_html=True
        )
        for item in look["items"]:
            st.markdown(
                f"""
                <div style="margin-bottom: 0.7rem; background: #FFFFFF; padding: 7px 10px; border-radius: 8px; border: 1px solid #ECECEC;">
                    <div style="font-size: 0.85rem; font-weight: 700; color: #282C3F;">
                        {item["icon"]} {item["name"]}
                    </div>
                    <span class="badge {item['badge_class']}">{item["badge"]}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
        st.markdown(
            f"""
                    </div>
                </div>
                <div style="margin-top: 0.85rem; border-top: 1px dashed #D0D0D5; padding-top: 0.6rem;">
                    <div style="font-size: 0.75rem; font-weight: 700; color: #0E7569; background: #E8F8F5; padding: 6px 8px; border-radius: 6px; text-align: center;">
                        {look["badge_summary"]} (Saves you ₹2,698)
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Column 2: Look 2 (Weekend Brunch & Social)
    with col2:
        look = OUTFIT_LOOKS[1]
        st.markdown(
            f"""
            <div class="look-card">
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2px;">
                        <span style="font-size: 1.05rem; font-weight: 800; color: #282C3F;">{look["title"]}</span>
                        <span style="font-size: 0.72rem; font-weight: 700; color: #D81B60; background: #FFF0F4; padding: 2px 6px; border-radius: 4px;">WEEKEND / CHIC</span>
                    </div>
                    <div style="font-size: 0.78rem; color: #696E79; margin-bottom: 0.85rem;">{look["subtitle"]}</div>
                    <div style="border-top: 1px solid #EAEAEC; padding-top: 0.6rem;">
            """,
            unsafe_allow_html=True
        )
        for item in look["items"]:
            st.markdown(
                f"""
                <div style="margin-bottom: 0.7rem; background: #FFFFFF; padding: 7px 10px; border-radius: 8px; border: 1px solid #ECECEC;">
                    <div style="font-size: 0.85rem; font-weight: 700; color: #282C3F;">
                        {item["icon"]} {item["name"]}
                    </div>
                    <span class="badge {item['badge_class']}">{item["badge"]}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
        st.markdown(
            f"""
                    </div>
                </div>
                <div style="margin-top: 0.85rem; border-top: 1px dashed #D0D0D5; padding-top: 0.6rem;">
                    <div style="font-size: 0.75rem; font-weight: 700; color: #D81B60; background: #FFF0F4; padding: 6px 8px; border-radius: 6px; text-align: center;">
                        {look["badge_summary"]} (1 Wishlist + 2 New Additions)
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ==============================================================================
# 7. PHASE 6: SOCIAL VALIDATION LOOP – WHATSAPP SHARE & POLL MOCKUP
# ==============================================================================
# STRATEGIC DEFENSIVE MOAT:
# Prevents 'Off-Platform Leakage'. When fashion shoppers hesitate, 68% take screenshots
# to ask friends on WhatsApp and forget to return to the e-commerce cart.
# By generating an interactive WhatsApp Poll directly in-app, Myntra closes the social loop.

def render_social_loop() -> None:
    """
    Renders Section 3: The WhatsApp Social Validation Loop.
    Provides in-app peer polling to prevent off-platform drop-off and maintain cart momentum.
    """
    st.markdown("---")
    st.markdown("### 💬 Can't decide? Ask your friends.")
    st.caption("Send an instant 1-tap poll to your WhatsApp group so your trusted circle can vote before you buy.")

    # WhatsApp Trigger CTA
    if not st.session_state.poll_sent:
        if st.button(
            "💬 Send Poll to WhatsApp",
            use_container_width=True,
            type="secondary",
            help="Generates an interactive voting card for your WhatsApp group chat"
        ):
            st.balloons()
            set_poll_sent(True)
            st.rerun()

    # Social Loop Confirmation & Interactive Mockup Preview
    if st.session_state.poll_sent:
        st.success("✅ **Poll dispatched to WhatsApp!** We'll notify you here the moment your friends vote.")
        
        st.markdown(
            """
            <div class="whatsapp-container">
                <div style="font-size: 0.78rem; font-weight: 700; color: #128C7E; margin-bottom: 6px; display: flex; align-items: center; gap: 5px;">
                    <span>📱</span> WhatsApp Interactive Card (Recipient Group Preview)
                </div>
                <div class="whatsapp-bubble">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                        <span style="font-size: 1.1rem;">🛍️</span>
                        <strong style="color: #128C7E; font-size: 0.85rem;">Myntra StyleSync Poll</strong>
                    </div>
                    <strong>"Help me choose! Thinking of getting this Rust Linen Blazer:"</strong>
                    <div style="margin: 10px 0 8px 0; padding: 10px; background: #F8F9FA; border-radius: 8px; border: 1px solid #ECE5DD; font-size: 0.86rem;">
                        <div style="margin-bottom: 6px;">
                            <strong>1️⃣ Look 1: Smart Casual Office</strong><br/>
                            <span style="color: #54656F; font-size: 0.78rem;">Blazer + White Crewneck Tee + Olive Linen Shirt</span>
                        </div>
                        <div style="margin-bottom: 6px; border-top: 1px dashed #E0E0E0; padding-top: 6px;">
                            <strong>2️⃣ Look 2: Weekend Brunch</strong><br/>
                            <span style="color: #54656F; font-size: 0.78rem;">Blazer + Ribbed Tank + Wide-Leg Denim + Gold Watch</span>
                        </div>
                        <div style="border-top: 1px dashed #E0E0E0; padding-top: 6px;">
                            <strong>❌ Drop It</strong> &nbsp;<span style="color: #878B94; font-size: 0.78rem;">(Skip this purchase)</span>
                        </div>
                    </div>
                    <div style="display: flex; gap: 6px; flex-wrap: wrap; margin-top: 8px;">
                        <span style="background: #E7FCE3; color: #0E7569; font-size: 0.75rem; font-weight: 700; padding: 4px 10px; border-radius: 12px; border: 1px solid #C4F7BE;">
                            🔘 Vote Look 1
                        </span>
                        <span style="background: #E7FCE3; color: #0E7569; font-size: 0.75rem; font-weight: 700; padding: 4px 10px; border-radius: 12px; border: 1px solid #C4F7BE;">
                            🔘 Vote Look 2
                        </span>
                        <span style="background: #FEEBEB; color: #C62828; font-size: 0.75rem; font-weight: 700; padding: 4px 10px; border-radius: 12px; border: 1px solid #FFCDD2;">
                            ❌ Drop It
                        </span>
                    </div>
                    <div class="whatsapp-meta">Just now &nbsp;✓✓</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Interactive Demonstration Tool for Stakeholders
        with st.expander("🗳️ Simulate Friend Voting (Live Demo Feature)"):
            st.caption("Click a simulated response below to see how StyleSync handles social consensus:")
            sim_col1, sim_col2, sim_col3 = st.columns(3)
            with sim_col1:
                if st.button("👍 Friend Votes Look 1", use_container_width=True):
                    st.info("🎉 **Vote Received!** Priya voted for **Look 1: Smart Casual Office**.")
            with sim_col2:
                if st.button("🔥 Friend Votes Look 2", use_container_width=True):
                    st.info("🎉 **Vote Received!** Rahul voted for **Look 2: Weekend Brunch**.")
            with sim_col3:
                if st.button("👎 Friend Votes Drop", use_container_width=True):
                    st.warning("💡 **Feedback Logged!** Tanya suggested skipping. StyleSync queued alternative silhouettes.")


def render_footer() -> None:
    """
    Renders Section 4: PM Walkthrough, Architecture Notes, and Live Demo Controls.
    Provides complete transparency for stakeholder reviews and portfolio presentations.
    """
    st.markdown("<br/><br/>", unsafe_allow_html=True)
    
    with st.expander("📋 Product Manager Walkthrough & Architecture Notes"):
        st.markdown(
            """
            ### 🎯 Product Strategy & Value Hypothesis
            * **Core Friction Solved:**
              1. **Styling Paralysis:** Users wishlist garments but don't complete the purchase because they aren't sure how to style them with clothes they already own.
              2. **Off-Platform Leakage:** Users take screenshots to WhatsApp to ask friends for validation, breaking checkout momentum and abandoning the funnel.
            * **Defensive Moats:**
              * **Universal Closet Moat:** Combines verified on-platform Myntra purchases with camera-roll uploads (`📸 Offline Closet`), establishing durable cross-platform lock-in.
              * **In-App Social Validation Loop:** Eliminates drop-off by bringing the peer voting loop natively into the product.

            ---

            ### 🏗️ Technical Architecture & Lifecycle
            * **Wizard of Oz AI Simulation:**
              * Deterministic mock data structures model the exact production schema.
              * 2.0s calibrated delay builds realistic AI anticipation while guaranteeing zero network failures, zero token costs, and 100% demo reliability.
            * **Streamlit Session State Resilience:**
              * Script re-runs from top-to-bottom on every user click.
              * Gating Lookbook & WhatsApp rendering on `st.session_state.is_styled` prevents UI reset when users interact with secondary poll buttons.
            """
        )

    with st.expander("🛠️ Portfolio Demo Controls & State Registry"):
        st.caption("Inspect live session state or reset the prototype to demonstrate from scratch:")
        st.json(get_session_debug_state())
        if st.button("🔄 Reset Prototype State", help="Reset all state flags to demonstrate from scratch"):
            reset_session_state()
            st.rerun()


# ==============================================================================
# 5. APPLICATION ENTRYPOINT
# ==============================================================================
def main() -> None:
    """Main orchestration sequence."""
    render_header()
    render_anchor_card()

    # Conditional section renders based on resilient session state
    if st.session_state.is_styled:
        render_lookbook()
        render_social_loop()

    render_footer()


if __name__ == "__main__":
    main()
