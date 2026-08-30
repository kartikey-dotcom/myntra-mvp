"""
Myntra E-Commerce Platform & StyleSync™ Smart Wardrobe MVP
==========================================================
High-Fidelity Desktop E-Commerce Experience & Fully Interactive Native App:
1. Storefront Homepage (Active navigation, ticket coupon copier, linen collection hero, category drawers)
2. Product Display Page (PDP - Thumbnail gallery switcher, interactive size picker, delivery pincode checker, size chart modal)
3. Shopping Bag Drawer & Profile Modal (Live item list, coupon discounts, order summary)
4. Wishlist Anchor & Smart Closet (Move to Bag, item detail modals, 'Style with My Closet' AI orchestrator)
5. StyleSync AI Studio & WhatsApp Social Validation (Rule-of-3 Outfits, Bundle Add-to-Bag, Live Peer Polling & Checkout)
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

    /* Modal / Alert Card Overlay */
    .modal-banner {
        background: #FFFFFF;
        border: 2px solid #FF3F6C;
        border-radius: 14px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 30px rgba(255, 63, 108, 0.12);
        animation: fadeIn 0.3s ease-in-out;
    }

    /* Promo Ticket Box */
    .promo-ticket-box {
        background: linear-gradient(90deg, #FFF0F3 0%, #FFE8EE 50%, #FFF0F3 100%);
        border: 1.5px dashed #FFCCD7;
        border-radius: 14px;
        padding: 1.1rem 2rem;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
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
    if "wishlist_count" not in st.session_state:
        st.session_state["wishlist_count"] = 1
    if "selected_size" not in st.session_state:
        st.session_state["selected_size"] = "40"
    if "pdp_active_img" not in st.session_state:
        st.session_state["pdp_active_img"] = TARGET_ITEM["image_url"]
    if "poll_sent" not in st.session_state:
        st.session_state["poll_sent"] = False
    if "vote_feedback" not in st.session_state:
        st.session_state["vote_feedback"] = None
    if "show_bag_drawer" not in st.session_state:
        st.session_state["show_bag_drawer"] = False
    if "show_profile_modal" not in st.session_state:
        st.session_state["show_profile_modal"] = False
    if "show_size_chart" not in st.session_state:
        st.session_state["show_size_chart"] = False
    if "active_modal" not in st.session_state:
        st.session_state["active_modal"] = None

init_session_state()

def set_view(view_name: str) -> None:
    st.session_state["current_view"] = view_name
    st.session_state["show_bag_drawer"] = False
    st.session_state["show_profile_modal"] = False
    st.session_state["show_size_chart"] = False
    st.session_state["active_modal"] = None
    st.rerun()

# ==============================================================================
# 4. TOP NAVIGATION BAR COMPONENT
# ==============================================================================

def render_top_navbar() -> None:
    curr = st.session_state.get("current_view", "homepage")
    bag_num = st.session_state.get("bag_count", 2)
    wl_num = st.session_state.get("wishlist_count", 1)

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
            if st.button("HOME", key="nav_home_s", use_container_width=True):
                st.toast("🏠 Welcome to Myntra Storefront!")
                set_view("homepage")
        with b2:
            if st.button("MEN", key="nav_men_s", use_container_width=True):
                st.toast("👔 Opening Men's Linen Blazer Collection")
                set_view("pdp")
        with b3:
            if st.button("WOMEN", key="nav_women_s", use_container_width=True):
                st.session_state["active_modal"] = "women_collection"
                st.toast("👗 Showing Women's Capsule Outfits")
                st.rerun()
        with b4:
            if st.button("STUDIO ✨", key="nav_studio_s", use_container_width=True):
                st.toast("✨ Entering StyleSync™ AI Wardrobe Studio")
                set_view("stylesync")
        with b5:
            if st.button("BEAUTY", key="nav_beauty_tab_s", use_container_width=True):
                st.session_state["active_modal"] = "beauty_collection"
                st.toast("💄 Showing Beauty & Grooming Picks")
                st.rerun()

    with nav_col3:
        search_query = st.text_input("🔍 Search products, brands...", placeholder="Type 'blazer', 'linen', 'zara'...", label_visibility="collapsed", key="search_bar_s")
        if search_query:
            st.session_state["active_modal"] = f"search_{search_query.strip().lower()}"

    with nav_col4:
        ic1, ic2, ic3 = st.columns(3)
        with ic1:
            if st.button("👤 Profile", key="top_prof_btn_s", use_container_width=True):
                st.session_state["show_profile_modal"] = not st.session_state["show_profile_modal"]
                st.session_state["show_bag_drawer"] = False
                st.rerun()
        with ic2:
            if st.button(f"❤️ ({wl_num})", key="top_wl_btn_s", use_container_width=True):
                st.toast(f"❤️ Opening Wishlist ({wl_num} saved items)")
                set_view("wishlist")
        with ic3:
            if st.button(f"🛍️ ({bag_num})", key="top_bag_btn_s", use_container_width=True):
                st.session_state["show_bag_drawer"] = not st.session_state["show_bag_drawer"]
                st.session_state["show_profile_modal"] = False
                st.rerun()

    # Journey Stepper Quick Navigator Bar
    st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
    step1, step2, step3, step4 = st.columns(4)
    with step1:
        if st.button("🏠 Storefront Home", key="st_step1", use_container_width=True, type="primary" if curr == "homepage" else "secondary"):
            set_view("homepage")
    with step2:
        if st.button("🛍️ 1. Product PDP", key="st_step2", use_container_width=True, type="primary" if curr == "pdp" else "secondary"):
            set_view("pdp")
    with step3:
        if st.button("❤️ 2. Wishlist & Closet", key="st_step3", use_container_width=True, type="primary" if curr == "wishlist" else "secondary"):
            set_view("wishlist")
    with step4:
        if st.button("✨ 3. StyleSync AI Studio", key="st_step4", use_container_width=True, type="primary" if curr == "stylesync" else "secondary"):
            set_view("stylesync")
    
    st.markdown("<hr style='margin: 0.8rem 0 1.2rem 0; border: none; border-top: 1px solid #ECEEF0;'>", unsafe_allow_html=True)

    # Render Active Modals / Drawers if toggled
    render_drawers_and_modals()


# ==============================================================================
# 5. DRAWERS & INTERACTIVE OVERLAYS
# ==============================================================================

def render_drawers_and_modals() -> None:
    # 1. Shopping Bag Drawer
    if st.session_state.get("show_bag_drawer", False):
        bag_count = st.session_state.get("bag_count", 2)
        st.markdown(
            f"""
            <div class="modal-banner">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <div style="font-size: 1.25rem; font-weight: 900; color: #282C3F;">
                        🛍️ YOUR SHOPPING BAG ({bag_count} Items)
                    </div>
                    <span style="font-size: 0.8rem; font-weight: 800; color: #03A685; background: #E8F8F5; padding: 4px 10px; border-radius: 6px;">
                        ⚡ 100% Genuine Guaranteed
                    </span>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1rem;">
                    <div style="background: #F9FAFB; padding: 12px; border-radius: 10px; border: 1px solid #ECEEF0;">
                        <b>MANGO MAN Rust Linen Blazer</b> (Size {st.session_state.get('selected_size', '40')})<br>
                        <span style="color: #FF3F6C; font-weight: 800;">₹3,499</span> <span style="color: #94969F; text-decoration: line-through;">₹4,999</span> (30% OFF)
                    </div>
                    <div style="background: #F9FAFB; padding: 12px; border-radius: 10px; border: 1px solid #ECEEF0;">
                        <b>ZARA Tailored Pleated Trousers</b> (Size 32)<br>
                        <span style="color: #FF3F6C; font-weight: 800;">₹2,990</span> <span style="color: #94969F; text-decoration: line-through;">₹3,990</span> (25% OFF)
                    </div>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #ECEEF0; padding-top: 10px;">
                    <div><b>Total Payable:</b> <span style="font-size: 1.2rem; font-weight: 900; color: #282C3F;">₹6,489</span> (Coupon: <code>MYNTRASAVE</code> applied -₹200)</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        b_c1, b_c2 = st.columns(2)
        with b_c1:
            if st.button("💳 Proceed to Checkout Now", key="drawer_checkout_btn_s", type="primary", use_container_width=True):
                st.balloons()
                st.toast("🎉 Order placed successfully! Delivery scheduled by tomorrow.")
                st.session_state["show_bag_drawer"] = False
                st.rerun()
        with b_c2:
            if st.button("✖️ Close Bag", key="close_bag_btn_s", use_container_width=True):
                st.session_state["show_bag_drawer"] = False
                st.rerun()

    # 2. Profile & Closet Preferences Modal
    if st.session_state.get("show_profile_modal", False):
        st.markdown(
            """
            <div class="modal-banner">
                <div style="font-size: 1.25rem; font-weight: 900; color: #282C3F; margin-bottom: 0.5rem;">
                    👤 PROFILE & STYLESYNC PREFERENCES
                </div>
                <p style="font-size: 0.85rem; color: #535766; margin-bottom: 1rem;">
                    Logged in as <b>Kartikey Sharma</b> (Myntra Insider VIP Member 👑)
                </p>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1rem;">
                    <div style="background: #F9FAFB; padding: 12px; border-radius: 8px;">
                        <b>📏 Measurements</b><br>Chest: 40" • Waist: 32" • Fit: Relaxed
                    </div>
                    <div style="background: #F9FAFB; padding: 12px; border-radius: 8px;">
                        <b>🎨 Color Palette</b><br>Earth Tones, Linen, Neutrals, Rust
                    </div>
                    <div style="background: #F9FAFB; padding: 12px; border-radius: 8px;">
                        <b>📦 Orders Synced</b><br>14 Past Garments in Smart Closet
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("✖️ Close Profile", key="close_prof_btn_s", use_container_width=True):
            st.session_state["show_profile_modal"] = False
            st.rerun()

    # 3. Dynamic Modals (Women's Collection, Beauty, Search, Size Chart)
    active_m = st.session_state.get("active_modal")
    if active_m:
        if active_m == "women_collection":
            st.markdown(
                """
                <div class="modal-banner">
                    <h3>👗 WOMEN'S SUMMER LINEN CAPSULE</h3>
                    <p>Curated Mediterranean Linen Dresses, Coordinates, and Tailored Vests.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            col_w1, col_w2 = st.columns(2)
            with col_w1:
                if st.button("🛍️ View Women's Linen Co-ord (₹2,999)", key="w_item1_s", use_container_width=True):
                    st.toast("Added Women's Co-ord to Bag!")
                    st.session_state["bag_count"] += 1
            with col_w2:
                if st.button("✖️ Close View", key="close_w_btn_s", use_container_width=True):
                    st.session_state["active_modal"] = None
                    st.rerun()

        elif active_m == "beauty_collection":
            st.markdown(
                """
                <div class="modal-banner">
                    <h3>💄 BEAUTY & GROOMING ESSENTIALS</h3>
                    <p>Luxury fragrances, beard oils, and skin hydrators matching your capsule aesthetic.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.button("🧴 Add Woody Citrus Eau De Parfum (₹1,899)", key="b_item1_s", use_container_width=True):
                    st.toast("Added Parfum to Bag!")
                    st.session_state["bag_count"] += 1
            with col_b2:
                if st.button("✖️ Close View", key="close_b_btn_s", use_container_width=True):
                    st.session_state["active_modal"] = None
                    st.rerun()

        elif str(active_m).startswith("search_"):
            q = str(active_m).replace("search_", "")
            st.markdown(
                f"""
                <div class="modal-banner">
                    <h4>🔍 Search Results for "{q}"</h4>
                    <p>Found <b>3 matches</b> across your catalog and smart closet pairings.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            s_c1, s_c2 = st.columns(2)
            with s_c1:
                if st.button(f"👉 View '{TARGET_ITEM['name']}' PDP", key="search_match_btn_s", type="primary", use_container_width=True):
                    st.session_state["active_modal"] = None
                    set_view("pdp")
            with s_c2:
                if st.button("✖️ Clear Search", key="clear_s_btn_s", use_container_width=True):
                    st.session_state["active_modal"] = None
                    st.rerun()

        elif active_m == "size_chart":
            st.markdown(
                """
                <div class="modal-banner">
                    <h3>📐 MANGO MAN SIZE & FIT GUIDE (INCHES)</h3>
                    <table style="width: 100%; text-align: left; margin: 10px 0; border-collapse: collapse; font-size: 0.88rem;">
                        <tr style="border-bottom: 1px solid #ECEEF0; font-weight: 800;">
                            <th>Size</th><th>Chest (in)</th><th>Shoulder (in)</th><th>Length (in)</th><th>Recommendation</th>
                        </tr>
                        <tr style="border-bottom: 1px solid #ECEEF0;">
                            <td><b>38 (S)</b></td><td>38 - 39</td><td>17.5</td><td>28.5</td><td>Slim Silhouette</td>
                        </tr>
                        <tr style="border-bottom: 1px solid #ECEEF0; background: #FFF0F4;">
                            <td><b>40 (M)</b></td><td>40 - 41</td><td>18.0</td><td>29.0</td><td>⭐ <b>Your Perfect Match</b></td>
                        </tr>
                        <tr style="border-bottom: 1px solid #ECEEF0;">
                            <td><b>42 (L)</b></td><td>42 - 43</td><td>18.5</td><td>29.5</td><td>Relaxed Layering</td>
                        </tr>
                        <tr>
                            <td><b>44 (XL)</b></td><td>44 - 46</td><td>19.0</td><td>30.0</td><td>Oversized Fit</td>
                        </tr>
                    </table>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button("✖️ Close Size Chart", key="close_sc_btn_s", use_container_width=True):
                st.session_state["active_modal"] = None
                st.rerun()


# ==============================================================================
# 6. SCREEN 1: HOMEPAGE STOREFRONT
# ==============================================================================

def render_homepage_view() -> None:
    # 1. Promo Ticket Banner
    t_col1, t_col2 = st.columns([3, 1.2])
    with t_col1:
        st.markdown(
            """
            <div class="promo-ticket-box">
                <div>
                    <div class="ticket-heading">GET 25% OFF</div>
                    <div class="ticket-sub">Up To ₹200 Off On First StyleSync Wardrobe Match*</div>
                </div>
                <div style="font-weight: 800; color: #282C3F;">
                    COUPON: <span style="color: #FF3F6C; letter-spacing: 1px;">MYNTRASAVE</span> 🎟️
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with t_col2:
        if st.button("📋 Copy Code 'MYNTRASAVE'", key="copy_coupon_btn_s", use_container_width=True):
            st.toast("🎟️ Coupon 'MYNTRASAVE' applied to your cart! 25% OFF active.")

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
            <div style="padding: 0.5rem 0;">
                <span class="hero-super-title">NEW SEASON CAPSULE</span>
                <h1 class="hero-main-title">THE NEW LINEN<br>COLLECTION</h1>
                <p class="hero-description">
                    Breathable European flax tailored for effortless versatility. 
                    Paired seamlessly with your existing wardrobe through StyleSync™ AI.
                </p>
                <div style="display: flex; gap: 12px; margin-bottom: 1.2rem;">
                    <span style="font-size: 1.6rem; font-weight: 900; color: #282C3F;">₹3,499</span>
                    <span style="font-size: 1.1rem; color: #94969F; text-decoration: line-through; margin-top: 4px;">₹4,999</span>
                    <span style="font-size: 0.9rem; font-weight: 800; color: #FF3F6C; background: #FFF0F4; padding: 4px 10px; border-radius: 6px;">30% OFF</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        c_btn1, c_btn2, c_btn3 = st.columns(3)
        with c_btn1:
            if st.button("🔥 EXPLORE NOW", key="hero_explore_btn_s", type="primary", use_container_width=True):
                st.toast("Opening Rust Linen Blazer Product Page...")
                set_view("pdp")
        with c_btn2:
            if st.button("✨ Style with Closet", key="hero_stylesync_btn_s", use_container_width=True):
                st.toast("Opening StyleSync Wardrobe Matcher...")
                set_view("stylesync")
        with c_btn3:
            if st.button("❤️ Save to Wishlist", key="hero_wl_btn_s", use_container_width=True):
                st.session_state["wishlist_count"] += 1
                st.toast("❤️ Added Linen Blazer to Wishlist!")
                st.rerun()

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
        if st.button("Explore Men's →", key="cat_men_btn_s", use_container_width=True):
            st.toast("Browsing Men's Catalog")
            set_view("pdp")

    with cat2:
        st.image(IMAGE_WOMEN_CAT, use_container_width=True)
        st.markdown("<h4 style='margin: 6px 0 2px 0; font-weight: 800;'>WOMEN'S WEAR</h4><p style='color: #7E818C; font-size: 0.8rem;'>Dresses, Tops & Coordinates</p>", unsafe_allow_html=True)
        if st.button("Explore Women's →", key="cat_women_btn_s", use_container_width=True):
            st.session_state["active_modal"] = "women_collection"
            st.rerun()

    with cat3:
        st.image(IMAGE_BEAUTY_CAT, use_container_width=True)
        st.markdown("<h4 style='margin: 6px 0 2px 0; font-weight: 800;'>BEAUTY & GROOMING</h4><p style='color: #7E818C; font-size: 0.8rem;'>Fragrance, Skincare & Grooming</p>", unsafe_allow_html=True)
        if st.button("Explore Beauty →", key="cat_beauty_btn_s", use_container_width=True):
            st.session_state["active_modal"] = "beauty_collection"
            st.rerun()

    with cat4:
        st.image(IMAGE_HOME_CAT, use_container_width=True)
        st.markdown("<h4 style='margin: 6px 0 2px 0; font-weight: 800;'>HOME LIVING</h4><p style='color: #7E818C; font-size: 0.8rem;'>Modern Decor & Bedroom Accents</p>", unsafe_allow_html=True)
        if st.button("Explore Home →", key="cat_home_btn_s", use_container_width=True):
            st.toast("🏡 Home Living Catalog loaded!")


# ==============================================================================
# 7. SCREEN 2: PRODUCT DISPLAY PAGE (PDP)
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
        active_img = st.session_state.get("pdp_active_img", TARGET_ITEM["image_url"])
        st.image(active_img, use_container_width=True)
        
        # Interactive Thumbnail Switcher Buttons
        st.markdown("<div style='font-size: 0.75rem; font-weight: 700; color: #7E818C; margin: 6px 0 4px 0;'>CLICK TO SWITCH ANGLE / PAIRING VIEW:</div>", unsafe_allow_html=True)
        t1, t2, t3 = st.columns(3)
        with t1:
            st.image(TARGET_ITEM["image_url"], use_container_width=True)
            if st.button("📸 Front View", key="thumb_front_s", use_container_width=True):
                st.session_state["pdp_active_img"] = TARGET_ITEM["image_url"]
                st.rerun()
        with t2:
            st.image(IMAGE_OLIVE_SHIRT, use_container_width=True)
            if st.button("🌿 Olive Pair", key="thumb_olive_s", use_container_width=True):
                st.session_state["pdp_active_img"] = IMAGE_OLIVE_SHIRT
                st.rerun()
        with t3:
            st.image(IMAGE_BLACK_TROUSERS, use_container_width=True)
            if st.button("👖 Trouser Pair", key="thumb_pant_s", use_container_width=True):
                st.session_state["pdp_active_img"] = IMAGE_BLACK_TROUSERS
                st.rerun()

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
            <div style="font-size: 0.76rem; font-weight: 800; color: #03A685; margin-bottom: 1.2rem;">inclusive of all taxes • Free Shipping & 14-Day Returns</div>
            """,
            unsafe_allow_html=True
        )

        # Size Selector
        sz_head, sz_chart = st.columns([2, 1])
        with sz_head:
            st.markdown("<div style='font-size: 0.84rem; font-weight: 900; color: #282C3F;'>SELECT SIZE (CHEST)</div>", unsafe_allow_html=True)
        with sz_chart:
            if st.button("📏 Size Chart", key="sc_open_btn_s", use_container_width=True):
                st.session_state["active_modal"] = "size_chart"
                st.rerun()

        s1, s2, s3, s4 = st.columns(4)
        curr_size = st.session_state.get("selected_size", "40")
        with s1:
            if st.button("38", key="sz_38_s", type="primary" if curr_size == "38" else "secondary", use_container_width=True):
                st.session_state["selected_size"] = "38"
                st.toast("Selected Size 38 (Small)")
                st.rerun()
        with s2:
            if st.button("40 ⭐", key="sz_40_s", type="primary" if curr_size == "40" else "secondary", use_container_width=True):
                st.session_state["selected_size"] = "40"
                st.toast("Selected Size 40 (Your Perfect Fit)")
                st.rerun()
        with s3:
            if st.button("42", key="sz_42_s", type="primary" if curr_size == "42" else "secondary", use_container_width=True):
                st.session_state["selected_size"] = "42"
                st.toast("Selected Size 42 (Large)")
                st.rerun()
        with s4:
            if st.button("44", key="sz_44_s", type="primary" if curr_size == "44" else "secondary", use_container_width=True):
                st.session_state["selected_size"] = "44"
                st.toast("Selected Size 44 (XL)")
                st.rerun()

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        # Action Buttons
        btn_bag, btn_wish = st.columns([1.2, 1])
        with btn_bag:
            if st.button("🛍️ ADD TO BAG", key="pdp_add_bag_btn_s", type="primary", use_container_width=True):
                st.session_state["bag_count"] = st.session_state.get("bag_count", 2) + 1
                st.toast(f"✅ Rust Linen Blazer (Size {curr_size}) added to Bag!")
                st.rerun()
        with btn_wish:
            if st.button("❤️ WISHLIST", key="pdp_add_wl_btn_s", use_container_width=True):
                st.session_state["wishlist_count"] += 1
                st.toast("❤️ Added to Wishlist! Opening Smart Closet...")
                set_view("wishlist")

        # Pincode Delivery Checker
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        pin_col1, pin_col2 = st.columns([2, 1])
        with pin_col1:
            pin_code = st.text_input("Delivery Pincode", placeholder="Enter 6-digit Pincode (e.g. 110001)", label_visibility="collapsed", key="pin_input_s")
        with pin_col2:
            if st.button("Check ⚡", key="pin_btn_s", use_container_width=True):
                if pin_code:
                    st.success(f"⚡ Delivery to {pin_code} by Tomorrow, 5 PM! Free Shipping.")
                else:
                    st.info("⚡ Standard delivery by Tomorrow, 5 PM across Metro cities.")

        # StyleSync AI Recommendation Box
        st.markdown(
            """
            <div style="background: linear-gradient(135deg, #FFF0F4 0%, #F5F0FF 100%); border: 1.5px solid #FFD8E4; border-radius: 12px; padding: 1.1rem; margin-top: 1.2rem;">
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
        if st.button("✨ View 3 Wardrobe Outfits & WhatsApp Poll →", key="pdp_to_stylesync_btn_s", type="primary", use_container_width=True):
            st.toast("Generating Rule-of-3 Outfits from your closet...")
            set_view("stylesync")


# ==============================================================================
# 8. SCREEN 3: WISHLIST & SMART CLOSET ANCHOR
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
                <p style="font-size: 0.84rem; color: #535766; line-height: 1.4; margin-bottom: 1rem;">
                    Unlocks <b>3 modular outfits</b> using clothes you already own in your closet. Zero styling hesitation!
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("✨ Style with My Closet (Run StyleSync AI) →", key="wl_run_ai_btn_s", type="primary", use_container_width=True):
            with st.spinner("✨ StyleSync AI analyzing your wardrobe purchase history & color harmonies..."):
                time.sleep(0.6)
            st.toast("3 Outfits Assembled!")
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
                <div style="padding: 4px 0 6px 0;">
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
            if st.button(f"🛍️ Move to Bag", key=f"wl_bag_s_{item['id']}", use_container_width=True):
                st.session_state["bag_count"] += 1
                st.toast(f"Added {item['name']} to Bag!")
                st.rerun()

    g4, g5, g6 = st.columns(3)
    for idx, item in enumerate(WISHLIST_PRODUCTS[3:6]):
        with [g4, g5, g6][idx]:
            st.image(item["image_url"], use_container_width=True)
            st.markdown(
                f"""
                <div style="padding: 4px 0 6px 0;">
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
            if st.button(f"🛍️ Move to Bag", key=f"wl_bag_s_{item['id']}", use_container_width=True):
                st.session_state["bag_count"] += 1
                st.toast(f"Added {item['name']} to Bag!")
                st.rerun()


# ==============================================================================
# 9. SCREEN 4: STYLESYNC AI STUDIO & WHATSAPP SOCIAL POLL
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
            st.image(IMAGE_OLIVE_SHIRT, caption="H&M Shirt (In Closet)", use_container_width=True)
        with img_sub2:
            st.image(IMAGE_BLACK_TROUSERS, caption="Zara Pants (In Closet)", use_container_width=True)
        
        b_p1, b_p2 = st.columns(2)
        with b_p1:
            if st.button("💬 Poll Look 1", key="poll_look_1_btn_s", type="primary", use_container_width=True):
                st.session_state["poll_sent"] = True
                st.session_state["poll_look_title"] = "Look 1: Sunset Linen"
                st.toast("💬 Look 1 shared to WhatsApp Poll!")
                st.rerun()
        with b_p2:
            if st.button("🛍️ Add Look 1", key="add_l1_btn_s", use_container_width=True):
                st.session_state["bag_count"] += 1
                st.toast("Added Look 1 Anchor Blazer to Bag!")
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

        b_p3, b_p4 = st.columns(2)
        with b_p3:
            if st.button("💬 Poll Look 2", key="poll_look_2_btn_s", use_container_width=True):
                st.session_state["poll_sent"] = True
                st.session_state["poll_look_title"] = "Look 2: Urban Brunch"
                st.toast("💬 Look 2 shared to WhatsApp Poll!")
                st.rerun()
        with b_p4:
            if st.button("🛍️ Add Look 2", key="add_l2_btn_s", use_container_width=True):
                st.session_state["bag_count"] += 2
                st.toast("Added Look 2 Blazer + Tank to Bag!")
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

        b_p5, b_p6 = st.columns(2)
        with b_p5:
            if st.button("💬 Poll Look 3", key="poll_look_3_btn_s", use_container_width=True):
                st.session_state["poll_sent"] = True
                st.session_state["poll_look_title"] = "Look 3: Smart Business"
                st.toast("💬 Look 3 shared to WhatsApp Poll!")
                st.rerun()
        with b_p6:
            if st.button("🛍️ Add Look 3", key="add_l3_btn_s", use_container_width=True):
                st.session_state["bag_count"] += 1
                st.toast("Added Look 3 to Bag!")
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
            if st.button("🔥 BUY IT! (84% Votes)", key="vote_buy_btn_s", type="primary", use_container_width=True):
                st.session_state["vote_feedback"] = "buy"
                st.toast("🎉 5 Friends voted 'BUY IT'! High peer confidence score.")
                st.rerun()
        with v2:
            if st.button("👎 DROP IT (16% Votes)", key="vote_drop_btn_s", use_container_width=True):
                st.session_state["vote_feedback"] = "drop"
                st.toast("Peer feedback registered.")
                st.rerun()

    with wa_col2:
        feedback = st.session_state.get("vote_feedback", None)
        if feedback == "buy":
            st.success("🌟 **Peer Confidence Verified!** 5 of 6 friends recommend buying. Ready to complete order with 1-click checkout.")
            if st.button("🛍️ PROCEED TO CHECKOUT (₹3,499)", key="wa_checkout_btn_s", type="primary", use_container_width=True):
                st.balloons()
                st.toast("🎉 Order placed successfully with StyleSync savings!")
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
# 10. FOOTER COMPONENT
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
# 11. MAIN ROUTER
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
