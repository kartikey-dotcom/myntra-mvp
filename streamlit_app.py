"""
Myntra "StyleSync" MVP - Production-Grade Mobile-First iOS Experience
====================================================================
High-Fidelity AI-Powered Smart Closet & Social Validation System.

Visual System:
- Mobile Viewport: 480px max-width container with iOS app navigation.
- Typography: Inter / SF Pro Display font hierarchy.
- Myntra Signature Aesthetic: #FF3F6C gradient buttons, curated drop shadows, pill badges.
- High-Res Visual Assets: Real clothing photography replacing text/emojis.
- iOS WhatsApp Bubble: Authentic chat bubble & interactive peer voting matrix.
"""

import time
from typing import TypedDict, List, Dict
import streamlit as st

# ==============================================================================
# 1. PAGE CONFIGURATION & MOBILE-FIRST CSS INJECTION
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

    /* Global reset & typography */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        color: #282C3F;
        background-color: #F4F4F6;
    }

    /* Hide or minimize Streamlit default top header bar */
    header[data-testid="stHeader"] {
        background: transparent !important;
        height: 2.5rem !important;
        z-index: 1 !important;
    }

    /* Mobile Viewport Simulation (iOS App Container) */
    .block-container {
        max-width: 480px !important;
        padding-top: 3.8rem !important;
        padding-bottom: 2.5rem !important;
        padding-left: 1.1rem !important;
        padding-right: 1.1rem !important;
        background-color: #FFFFFF;
        min-height: 100vh;
        box-shadow: 0 0 25px rgba(0, 0, 0, 0.06);
    }

    /* Header Bar */
    .mobile-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.6rem 0 1rem 0;
        border-bottom: 1px solid #F0F0F2;
        margin-bottom: 1.2rem;
    }
    .header-logo {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 1.25rem;
        font-weight: 900;
        letter-spacing: -0.4px;
        color: #282C3F;
    }
    .header-logo span {
        color: #FF3F6C;
    }
    .wishlist-pill {
        background: #FFF0F4;
        color: #FF3F6C;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 5px 10px;
        border-radius: 20px;
        border: 1px solid #FFD8E4;
        display: flex;
        align-items: center;
        gap: 4px;
    }

    /* Product Card */
    .product-card {
        background: #FFFFFF;
        border-radius: 12px;
        border: 1px solid #EAEAEC;
        padding: 12px;
        box-shadow: 0 2px 10px rgba(40, 44, 63, 0.06);
        margin-bottom: 1rem;
    }

    /* Split layout for Anchor Item */
    .anchor-grid {
        display: grid;
        grid-template-columns: 100px 1fr;
        gap: 12px;
        align-items: center;
    }
    .anchor-img {
        width: 100px;
        height: 133px;
        object-fit: cover;
        border-radius: 8px;
        background-color: #F5F5F6;
    }
    .anchor-details {
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .anchor-brand {
        font-size: 0.72rem;
        font-weight: 700;
        color: #94969F;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .anchor-title {
        font-size: 0.95rem;
        font-weight: 800;
        color: #282C3F;
        margin: 2px 0 4px 0;
        line-height: 1.2;
    }
    .anchor-price-row {
        display: flex;
        align-items: baseline;
        gap: 6px;
        margin: 2px 0 6px 0;
    }
    .anchor-price-now {
        font-size: 1.15rem;
        font-weight: 800;
        color: #282C3F;
    }
    .anchor-price-orig {
        font-size: 0.82rem;
        color: #94969F;
        text-decoration: line-through;
    }
    .anchor-discount {
        font-size: 0.75rem;
        font-weight: 700;
        color: #FF3F6C;
        background: #FFF0F4;
        padding: 2px 5px;
        border-radius: 4px;
    }

    /* Custom Badges (Pill-shaped) */
    .badge-owned {
        background-color: #E8F8F5;
        color: #03A685;
        font-size: 0.68rem;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 12px;
        display: inline-block;
        margin-top: 4px;
        border: 1px solid #B8EADF;
    }
    .badge-offline {
        background-color: #F3E8FF;
        color: #7E22CE;
        font-size: 0.68rem;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 12px;
        display: inline-block;
        margin-top: 4px;
        border: 1px solid #E4CDFC;
    }
    .badge-wishlist {
        background-color: #FFF4EE;
        color: #FF905A;
        font-size: 0.68rem;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 12px;
        display: inline-block;
        margin-top: 4px;
        border: 1px solid #FFE0D0;
    }
    .badge-fit {
        background-color: #ECFDF5;
        color: #047857;
        font-size: 0.68rem;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 12px;
        display: inline-block;
        margin-top: 4px;
        border: 1px solid #A7F3D0;
    }
    .badge-target {
        background-color: #FFF0F4;
        color: #FF3F6C;
        font-size: 0.68rem;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 12px;
        display: inline-block;
        margin-top: 4px;
        border: 1px solid #FFCDD2;
    }

    /* Lookbook Card */
    .lookbook-column-card {
        background: #FAFAFB;
        border: 1px solid #EAEAEC;
        border-radius: 12px;
        padding: 10px;
        display: flex;
        flex-direction: column;
        height: 100%;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
    }
    .lookbook-title {
        font-size: 0.85rem;
        font-weight: 800;
        color: #282C3F;
        margin-bottom: 2px;
    }
    .lookbook-subtitle {
        font-size: 0.7rem;
        color: #7E818C;
        margin-bottom: 8px;
    }
    .lookbook-item-block {
        margin-bottom: 8px;
        background: #FFFFFF;
        border-radius: 8px;
        padding: 6px;
        border: 1px solid #EEEEF0;
        display: flex;
        flex-direction: column;
    }
    .lookbook-img {
        width: 100%;
        height: 110px;
        object-fit: cover;
        border-radius: 6px;
    }
    .lookbook-item-title {
        font-size: 0.72rem;
        font-weight: 700;
        color: #282C3F;
        margin-top: 4px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    /* Primary CTA Button Override (Myntra Pink Gradient) */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #FF3F6C 0%, #FF527B 100%) !important;
        color: #FFFFFF !important;
        font-size: 0.88rem !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.65rem 1rem !important;
        box-shadow: 0 4px 12px rgba(255, 63, 108, 0.28) !important;
        width: 100% !important;
        transition: all 0.15s ease-in-out !important;
    }
    div.stButton > button[kind="primary"]:hover {
        box-shadow: 0 6px 16px rgba(255, 63, 108, 0.40) !important;
        transform: translateY(-1px) !important;
    }

    /* Secondary CTA Button Override (WhatsApp Green) */
    div.stButton > button[kind="secondary"] {
        background-color: #25D366 !important;
        color: #FFFFFF !important;
        font-size: 0.88rem !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.65rem 1rem !important;
        box-shadow: 0 4px 12px rgba(37, 211, 102, 0.28) !important;
        width: 100% !important;
        transition: all 0.15s ease-in-out !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        box-shadow: 0 6px 16px rgba(37, 211, 102, 0.40) !important;
        transform: translateY(-1px) !important;
    }

    /* iOS WhatsApp Chat Frame */
    .whatsapp-bubble-wrapper {
        background-color: #EFEAE2;
        background-image: radial-gradient(#D8D2C9 0.8px, transparent 0.8px);
        background-size: 10px 10px;
        border-radius: 14px;
        padding: 12px;
        border: 1px solid #D6CEC5;
        margin-top: 10px;
    }
    .whatsapp-bubble-box {
        background-color: #DCF8C6;
        border-radius: 10px 10px 2px 10px;
        padding: 12px 14px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
        color: #111B21;
        font-size: 0.84rem;
        position: relative;
    }
    .whatsapp-header-tag {
        font-size: 0.75rem;
        font-weight: 800;
        color: #075E54;
        display: flex;
        align-items: center;
        gap: 5px;
        margin-bottom: 6px;
    }
    .whatsapp-poll-option {
        background: rgba(255, 255, 255, 0.85);
        border: 1px solid #C4E2B2;
        border-radius: 6px;
        padding: 6px 8px;
        margin-top: 5px;
        font-size: 0.78rem;
    }
    .whatsapp-meta-time {
        font-size: 0.66rem;
        color: #667781;
        text-align: right;
        margin-top: 5px;
    }

    /* Custom Trust Banner */
    .custom-success-banner {
        background: #E8F8F5;
        border-left: 4px solid #03A685;
        border-radius: 8px;
        padding: 10px 12px;
        margin: 10px 0;
        font-size: 0.82rem;
        color: #03A685;
        font-weight: 600;
    }
    .custom-feedback-banner {
        background: #F4F6F8;
        border: 1px solid #E0E4E8;
        border-radius: 8px;
        padding: 8px 10px;
        margin-top: 6px;
        font-size: 0.78rem;
        color: #282C3F;
        font-weight: 600;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ==============================================================================
# 2. PHASE 1: DATA ARCHITECTURE & HIGH-RESOLUTION ASSET CATALOG
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

# Target Wishlisted Item (Rust Blazer - 3:4 Portrait Asset)
TARGET_ITEM: TargetItem = {
    "id": "ITEM-9081",
    "name": "Rust Linen Relaxed Blazer",
    "brand": "Roadster Signature",
    "price": "₹3,499",
    "original_price": "₹4,999",
    "discount": "30% OFF",
    "status": "In Wishlist 5d",
    "rating": "4.4 ★ (1.2k)",
    "color": "Rust Terracotta",
    "material": "100% Organic Linen",
    "image_url": "https://images.unsplash.com/photo-1598808503746-f34c53b9323e?w=500&auto=format&fit=crop&q=80"
}

# Pre-assembled Rule-of-3 Modular Looks with High-Resolution Photography
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
# 3. PHASE 2: STATE MANAGEMENT ENGINE
# ==============================================================================

def init_session_state() -> None:
    """Initializes session state defaults."""
    if "is_styled" not in st.session_state:
        st.session_state["is_styled"] = False
    if "poll_sent" not in st.session_state:
        st.session_state["poll_sent"] = False
    if "vote_feedback" not in st.session_state:
        st.session_state["vote_feedback"] = None

def set_styled(status: bool = True) -> None:
    st.session_state["is_styled"] = status

def set_poll_sent(status: bool = True) -> None:
    st.session_state["poll_sent"] = status

# Run initialization immediately
init_session_state()


# ==============================================================================
# 4. PRESENTATION LAYER (Mobile-First HTML / CSS Layouts)
# ==============================================================================

def render_header() -> None:
    """Renders iOS App Header with Wishlist Counter."""
    st.markdown(
        """
        <div class="mobile-header">
            <div class="header-logo">
                🛍️ myntra <span>StyleSync</span>
            </div>
            <div class="wishlist-pill">
                💛 Wishlist (24)
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_anchor_card() -> None:
    """Renders the Target Item with Horizontal Split Layout & High-Res Image."""
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

    # Primary Action Trigger
    if not st.session_state.get("is_styled", False):
        st.caption("Unsure how to style this blazer? StyleSync matches your closet in 1-tap.")
        if st.button(
            "✨ Style with My Closet & Wishlist",
            type="primary",
            use_container_width=True
        ):
            simulate_ai_matching()


def simulate_ai_matching() -> None:
    """Simulates multi-stage neural wardrobe matching with 2.0s delay."""
    status_placeholder = st.empty()
    with status_placeholder.container():
        with st.spinner("🔍 Scanning purchase history & camera roll closet..."):
            time.sleep(1.0)
        with st.spinner("✨ Composing Rule-of-3 modular outfits..."):
            time.sleep(1.0)
    status_placeholder.empty()
    set_styled(True)
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
            set_poll_sent(True)
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


def render_footer() -> None:
    """Authentic Clean E-commerce Trust Footer."""
    st.markdown(
        """
        <div style="text-align: center; color: #94969F; font-size: 0.72rem; margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #EEEEF0;">
            🔒 <strong>100% Original Products</strong> &nbsp;•&nbsp; 🚚 <strong>Free Delivery</strong> &nbsp;•&nbsp; 🔄 <strong>Easy 14 Days Returns</strong>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==============================================================================
# 5. APPLICATION ENTRYPOINT
# ==============================================================================
def main() -> None:
    """Main execution sequence."""
    init_session_state()
    render_header()
    render_anchor_card()

    if st.session_state.get("is_styled", False):
        render_lookbook()
        render_social_loop()

    render_footer()


if __name__ == "__main__":
    main()
