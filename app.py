"""
Myntra E-Commerce Platform & StyleSync™ Smart Wardrobe MVP
==========================================================
Master Micro-Catalog & Search Architecture + StyleSync AI Engine:
1. Master Micro-Catalog (31 items across Apparel, Footwear, Beauty, Accessories, Home)
2. Interactive Search & Filter Engine (Free-text search + Category Chips)
3. Dynamic PDP with StyleSync AI Interceptor (Rust Linen Blazer triggers StyleSync Wardrobe Match)
4. Wishlist Anchor & Smart Closet Matcher
5. StyleSync AI Studio & WhatsApp Social Validation Loop ("Buy or Drop" Peer Poll)
"""

import time
import re
from typing import TypedDict, List, Dict, Optional
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
        margin: 1.5rem 0 1rem 0;
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

    /* Product Grid Card & Uniform Image Sizing */
    [data-testid="stImage"] > img {
        height: 220px !important;
        max-height: 220px !important;
        min-height: 220px !important;
        width: 100% !important;
        object-fit: cover !important;
        object-position: center !important;
        border-radius: 10px !important;
        display: block !important;
    }

    .pdp-gallery-wrap [data-testid="stImage"] > img {
        height: 480px !important;
        max-height: 480px !important;
        min-height: 480px !important;
    }
    .look-card-container [data-testid="stImage"] > img {
        height: 160px !important;
        max-height: 160px !important;
        min-height: 160px !important;
    }
    .thumb-wrap [data-testid="stImage"] > img {
        height: 90px !important;
        max-height: 90px !important;
        min-height: 90px !important;
    }

    .catalog-item-card {
        background: #FFFFFF;
        border: 1px solid #ECEEF0;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
        height: 100%;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .catalog-item-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
    }
    .catalog-item-info {
        padding: 10px 12px;
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
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
        font-size: 0.8rem !important;
        height: 38px !important;
        min-height: 38px !important;
        max-height: 38px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 0 8px !important;
    }
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
# 2. MASTER MICRO-CATALOG (31 Realistic Items Across 5 Master Categories)
# ==============================================================================

class CatalogItem(TypedDict):
    id: str
    name: str
    brand: str
    master_category: str
    sub_category: str
    price: str
    mrp: str
    discount: str
    rating: str
    is_stylesync_eligible: bool
    tags: str
    img: str

MICRO_CATALOG: List[CatalogItem] = [
    # 1. Apparel - Men (hero_1 is the ONLY is_stylesync_eligible == True)
    {
        "id": "hero_1",
        "name": "Rust Linen Relaxed-Fit Blazer",
        "brand": "MANGO MAN",
        "master_category": "Apparel",
        "sub_category": "Men",
        "price": "₹3,499",
        "mrp": "₹4,999",
        "discount": "(30% OFF)",
        "rating": "4.4 ★",
        "is_stylesync_eligible": True,
        "tags": "blazer jacket linen formal coat rust mango men apparel outfit",
        "img": "https://images.unsplash.com/photo-1598808503746-f34c53b9323e?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "men_2",
        "name": "Classic Pure Linen White Shirt",
        "brand": "H&M",
        "master_category": "Shirts",
        "sub_category": "Casual Shirts",
        "price": "₹1,999",
        "mrp": "₹2,499",
        "discount": "(20% OFF)",
        "rating": "4.3 ★",
        "is_stylesync_eligible": False,
        "tags": "shirt shirts linen casual tops white hm h&m men apparel",
        "img": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "men_3",
        "name": "Tailored Pleated Formal Trousers",
        "brand": "ZARA",
        "master_category": "Apparel",
        "sub_category": "Men",
        "price": "₹2,990",
        "mrp": "₹3,990",
        "discount": "(25% OFF)",
        "rating": "4.5 ★",
        "is_stylesync_eligible": False,
        "tags": "trousers pants formal tailored pleated black zara bottomwear men apparel chinos",
        "img": "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "men_4",
        "name": "511 Slim Fit Raw Indigo Denim Jeans",
        "brand": "LEVIS",
        "master_category": "Apparel",
        "sub_category": "Men",
        "price": "₹3,199",
        "mrp": "₹4,599",
        "discount": "(30% OFF)",
        "rating": "4.6 ★",
        "is_stylesync_eligible": False,
        "tags": "jeans denim pants slim fit 511 levis levi's indigo bottomwear men apparel",
        "img": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "men_5",
        "name": "Olive Mandarin Collar Casual Shirt",
        "brand": "Roadster",
        "master_category": "Shirts",
        "sub_category": "Casual Shirts",
        "price": "₹1,299",
        "mrp": "₹1,999",
        "discount": "(35% OFF)",
        "rating": "4.1 ★",
        "is_stylesync_eligible": False,
        "tags": "shirt shirts casual mandarin collar olive roadster top men apparel",
        "img": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=800&auto=format&fit=crop&q=80"
    },

    # Dedicated Shirts Category Products
    {
        "id": "shirt_1",
        "name": "Slim Fit Oxford Cotton Formal Shirt",
        "brand": "Tommy Hilfiger",
        "master_category": "Shirts",
        "sub_category": "Formal Shirts",
        "price": "₹3,999",
        "mrp": "₹5,999",
        "discount": "(33% OFF)",
        "rating": "4.7 ★",
        "is_stylesync_eligible": False,
        "tags": "shirt shirts oxford formal button down tommy hilfiger men apparel",
        "img": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "shirt_2",
        "name": "Checkered Cotton Twill Casual Shirt",
        "brand": "Levi's",
        "master_category": "Shirts",
        "sub_category": "Casual Shirts",
        "price": "₹2,299",
        "mrp": "₹3,499",
        "discount": "(34% OFF)",
        "rating": "4.6 ★",
        "is_stylesync_eligible": False,
        "tags": "shirt shirts checkered plaid flannel levis levi's men apparel casual",
        "img": "https://images.unsplash.com/photo-1603252109303-2751441dd157?w=800&auto=format&fit=crop&q=80"
    },

    # Dedicated T-Shirts Category Products (Pure T-Shirts Only)
    {
        "id": "tshirt_1",
        "name": "Nike Sportswear Club Crewneck Graphic T-Shirt",
        "brand": "Nike",
        "master_category": "T-Shirts",
        "sub_category": "Graphic Tees",
        "price": "₹1,495",
        "mrp": "₹1,995",
        "discount": "(25% OFF)",
        "rating": "4.8 ★",
        "is_stylesync_eligible": False,
        "tags": "tshirt t-shirt tee graphic nike sportswear white",
        "img": "https://images.unsplash.com/photo-1581655353564-df123a1eb820?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "tshirt_2",
        "name": "Heavyweight Oversized Streetwear Graphic T-Shirt",
        "brand": "Jack & Jones",
        "master_category": "T-Shirts",
        "sub_category": "Oversized Tees",
        "price": "₹1,299",
        "mrp": "₹2,199",
        "discount": "(41% OFF)",
        "rating": "4.5 ★",
        "is_stylesync_eligible": False,
        "tags": "tshirt t-shirt tee oversized streetwear jack & jones black",
        "img": "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "tshirt_3",
        "name": "Pure Cotton Crewneck Slim-Fit T-Shirt",
        "brand": "Puma",
        "master_category": "T-Shirts",
        "sub_category": "Crewneck Tees",
        "price": "₹999",
        "mrp": "₹1,799",
        "discount": "(44% OFF)",
        "rating": "4.4 ★",
        "is_stylesync_eligible": False,
        "tags": "tshirt t-shirt tee crewneck solid basic pima cotton puma",
        "img": "https://images.unsplash.com/photo-1562157873-818bc0726f68?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "tshirt_4",
        "name": "Trefoil Essentials Heritage Graphic T-Shirt",
        "brand": "Adidas Originals",
        "master_category": "T-Shirts",
        "sub_category": "Graphic Tees",
        "price": "₹1,799",
        "mrp": "₹2,499",
        "discount": "(28% OFF)",
        "rating": "4.7 ★",
        "is_stylesync_eligible": False,
        "tags": "tshirt t-shirt tee graphic trefoil adidas sportswear",
        "img": "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "tshirt_5",
        "name": "Vintage Mineral Wash Relaxed Fit T-Shirt",
        "brand": "H&M",
        "master_category": "T-Shirts",
        "sub_category": "Relaxed Tees",
        "price": "₹1,199",
        "mrp": "₹1,999",
        "discount": "(40% OFF)",
        "rating": "4.6 ★",
        "is_stylesync_eligible": False,
        "tags": "tshirt t-shirt tee vintage mineral wash h&m hm relaxed",
        "img": "https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "tshirt_6",
        "name": "Signature Embroidered Crest Crewneck T-Shirt",
        "brand": "Tommy Hilfiger",
        "master_category": "T-Shirts",
        "sub_category": "Crewneck Tees",
        "price": "₹2,299",
        "mrp": "₹3,499",
        "discount": "(34% OFF)",
        "rating": "4.8 ★",
        "is_stylesync_eligible": False,
        "tags": "tshirt t-shirt tee embroidered tommy hilfiger black crewneck",
        "img": "https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=800&auto=format&fit=crop&q=80"
    },

    # 2. Apparel - Women
    {
        "id": "women_1",
        "name": "Embroidered Anarkali Kurta Set",
        "brand": "Biba",
        "master_category": "Apparel",
        "sub_category": "Women",
        "price": "₹3,299",
        "mrp": "₹5,499",
        "discount": "(40% OFF)",
        "rating": "4.6 ★",
        "is_stylesync_eligible": False,
        "tags": "kurti kurta ethnic anarkali biba dress embroidery traditional women apparel salwar_suit",
        "img": "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "women_2",
        "name": "Floral Printed Maxi Wrap Dress",
        "brand": "H&M",
        "master_category": "Apparel",
        "sub_category": "Women",
        "price": "₹2,499",
        "mrp": "₹3,499",
        "discount": "(28% OFF)",
        "rating": "4.4 ★",
        "is_stylesync_eligible": False,
        "tags": "dress maxi floral wrap h&m hm summer gown western women apparel",
        "img": "https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "women_3",
        "name": "Pure Chanderi Silk Festive Kurti",
        "brand": "Libas",
        "master_category": "Apparel",
        "sub_category": "Women",
        "price": "₹1,899",
        "mrp": "₹3,199",
        "discount": "(40% OFF)",
        "rating": "4.5 ★",
        "is_stylesync_eligible": False,
        "tags": "kurti kurta silk ethnic festive libas traditional party women apparel",
        "img": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "women_4",
        "name": "Ribbed Cotton Lounge Co-ord Set",
        "brand": "Marks & Spencer",
        "master_category": "Apparel",
        "sub_category": "Women",
        "price": "₹2,799",
        "mrp": "₹3,999",
        "discount": "(30% OFF)",
        "rating": "4.3 ★",
        "is_stylesync_eligible": False,
        "tags": "lounge loungewear co-ord coord set sleepwear marks & spencer m&s women apparel",
        "img": "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "women_5",
        "name": "High-Rise Wide Leg Washed Denim Jeans",
        "brand": "MANGO",
        "master_category": "Apparel",
        "sub_category": "Women",
        "price": "₹3,590",
        "mrp": "₹4,990",
        "discount": "(28% OFF)",
        "rating": "4.7 ★",
        "is_stylesync_eligible": False,
        "tags": "jeans denim high rise wide leg washed pants mango bottomwear women apparel",
        "img": "https://images.unsplash.com/photo-1582552938357-32b906df40cb?w=800&auto=format&fit=crop&q=80"
    },

    # 3. Apparel - Kids & Infants
    {
        "id": "kids_1",
        "name": "Organic Cotton Infant Onesie (3-Pack)",
        "brand": "Mothercare",
        "master_category": "Apparel",
        "sub_category": "Kids",
        "price": "₹1,499",
        "mrp": "₹2,199",
        "discount": "(31% OFF)",
        "rating": "4.8 ★",
        "is_stylesync_eligible": False,
        "tags": "onesie infant baby romper organic cotton mothercare newborn kids clothes",
        "img": "https://images.unsplash.com/photo-1522771930-78848d9293e8?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "kids_2",
        "name": "Boys Graphic Crewneck Cotton Top",
        "brand": "Gini & Jony",
        "master_category": "Apparel",
        "sub_category": "Kids",
        "price": "₹699",
        "mrp": "₹1,199",
        "discount": "(41% OFF)",
        "rating": "4.2 ★",
        "is_stylesync_eligible": False,
        "tags": "graphic crewneck cotton gini & jony boys kids apparel boys_top",
        "img": "https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "kids_3",
        "name": "Girls Tiered Tulle Party Frock",
        "brand": "Cutecumber",
        "master_category": "Apparel",
        "sub_category": "Kids",
        "price": "₹1,799",
        "mrp": "₹2,999",
        "discount": "(40% OFF)",
        "rating": "4.5 ★",
        "is_stylesync_eligible": False,
        "tags": "frock dress party wear tulle tiered cutecumber girls kids birthday gown",
        "img": "https://images.unsplash.com/photo-1622290291468-a28f7a7dc6a8?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "kids_4",
        "name": "Infant Knit Dungaree Set",
        "brand": "Carter's",
        "master_category": "Apparel",
        "sub_category": "Kids",
        "price": "₹1,899",
        "mrp": "₹2,499",
        "discount": "(24% OFF)",
        "rating": "4.7 ★",
        "is_stylesync_eligible": False,
        "tags": "dungaree set knit carters carter's infant kids baby toddler apparel romper",
        "img": "https://images.unsplash.com/photo-1519689680058-324335c77eba?w=800&auto=format&fit=crop&q=80"
    },

    # 4. Footwear
    {
        "id": "foot_1",
        "name": "Air Max SC Leather Retro Sneakers",
        "brand": "Nike",
        "master_category": "Footwear",
        "sub_category": "Men",
        "price": "₹5,995",
        "mrp": "₹7,495",
        "discount": "(20% OFF)",
        "rating": "4.7 ★",
        "is_stylesync_eligible": False,
        "tags": "sneakers shoes running retro leather air max nike men sports footwear shoes trainers",
        "img": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "foot_2",
        "name": "Caven 2.0 Court Low-Top Sneakers",
        "brand": "Puma",
        "master_category": "Footwear",
        "sub_category": "Men",
        "price": "₹2,749",
        "mrp": "₹4,999",
        "discount": "(45% OFF)",
        "rating": "4.3 ★",
        "is_stylesync_eligible": False,
        "tags": "sneakers shoes court low top caven puma men casual footwear white shoes trainers",
        "img": "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "foot_3",
        "name": "Strappy Block Heeled Evening Sandals",
        "brand": "Carlton London",
        "master_category": "Footwear",
        "sub_category": "Women",
        "price": "₹1,899",
        "mrp": "₹3,499",
        "discount": "(45% OFF)",
        "rating": "4.4 ★",
        "is_stylesync_eligible": False,
        "tags": "heels sandals block heeled strappy evening carlton london women footwear party shoes",
        "img": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "foot_4",
        "name": "Ultraboost Light Running Shoes",
        "brand": "Adidas",
        "master_category": "Footwear",
        "sub_category": "Men",
        "price": "₹8,999",
        "mrp": "₹14,999",
        "discount": "(40% OFF)",
        "rating": "4.8 ★",
        "is_stylesync_eligible": False,
        "tags": "running shoes sneakers sports ultraboost adidas men footwear gym trainers",
        "img": "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "foot_5",
        "name": "Suede Chelsea High-Top Boots",
        "brand": "Roadster",
        "master_category": "Footwear",
        "sub_category": "Men",
        "price": "₹2,499",
        "mrp": "₹4,299",
        "discount": "(41% OFF)",
        "rating": "4.2 ★",
        "is_stylesync_eligible": False,
        "tags": "boots chelsea high top suede roadster men shoes footwear winter brown",
        "img": "https://images.unsplash.com/photo-1608256246200-53e635b5b65f?w=800&auto=format&fit=crop&q=80"
    },

    # 5. Beauty & Personal Care
    {
        "id": "beauty_1",
        "name": "10% Niacinamide Clarifying Face Serum",
        "brand": "Minimalist",
        "master_category": "Beauty",
        "sub_category": "Skincare",
        "price": "₹599",
        "mrp": "₹699",
        "discount": "(14% OFF)",
        "rating": "4.6 ★",
        "is_stylesync_eligible": False,
        "tags": "serum niacinamide skincare face clarifying minimalist beauty skin glow acne",
        "img": "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "beauty_2",
        "name": "Retro Matte Longwear Lipstick - Ruby Woo",
        "brand": "MAC",
        "master_category": "Beauty",
        "sub_category": "Makeup",
        "price": "₹1,950",
        "mrp": "₹2,300",
        "discount": "(15% OFF)",
        "rating": "4.8 ★",
        "is_stylesync_eligible": False,
        "tags": "lipstick ruby woo matte red longwear mac cosmetics makeup beauty lips",
        "img": "https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "beauty_3",
        "name": "Club De Nuit Intense Man Luxury EDP",
        "brand": "Armaf",
        "master_category": "Beauty",
        "sub_category": "Fragrance",
        "price": "₹3,450",
        "mrp": "₹4,900",
        "discount": "(29% OFF)",
        "rating": "4.7 ★",
        "is_stylesync_eligible": False,
        "tags": "perfume fragrance edp scent luxury armaf beauty club de nuit cologne scent spray",
        "img": "https://images.unsplash.com/photo-1523293182086-7651a899d37f?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "beauty_4",
        "name": "Revitalift Hyaluronic Acid Plumping Serum",
        "brand": "L'Oreal Paris",
        "master_category": "Beauty",
        "sub_category": "Skincare",
        "price": "₹899",
        "mrp": "₹1,199",
        "discount": "(25% OFF)",
        "rating": "4.4 ★",
        "is_stylesync_eligible": False,
        "tags": "serum hyaluronic acid plumping skincare l'oreal loreal paris beauty anti aging hydration",
        "img": "https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?w=800&auto=format&fit=crop&q=80"
    },

    # 6. Accessories & Jewelry
    {
        "id": "acc_1",
        "name": "Grant Chronograph Blue Dial Watch",
        "brand": "Fossil",
        "master_category": "Accessories",
        "sub_category": "Watches",
        "price": "₹7,995",
        "mrp": "₹12,495",
        "discount": "(36% OFF)",
        "rating": "4.6 ★",
        "is_stylesync_eligible": False,
        "tags": "watch watches chronograph leather blue dial fossil accessories wrist watch analog",
        "img": "https://images.unsplash.com/photo-1524805444758-089113d48a6d?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "acc_2",
        "name": "Classic Aviator Polarized Sunglasses",
        "brand": "Ray-Ban",
        "master_category": "Accessories",
        "sub_category": "Eyewear",
        "price": "₹6,890",
        "mrp": "₹8,590",
        "discount": "(20% OFF)",
        "rating": "4.8 ★",
        "is_stylesync_eligible": False,
        "tags": "sunglasses aviator polarized green ray-ban rayban accessories eyewear shades glasses",
        "img": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "acc_3",
        "name": "Faux Leather Structured Satchel Handbag",
        "brand": "Caprese",
        "master_category": "Accessories",
        "sub_category": "Bags",
        "price": "₹2,499",
        "mrp": "₹4,999",
        "discount": "(50% OFF)",
        "rating": "4.3 ★",
        "is_stylesync_eligible": False,
        "tags": "handbag satchel faux leather structured caprese accessories bag purse tote women",
        "img": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "acc_4",
        "name": "Reversible Genuine Leather Belt",
        "brand": "Tommy Hilfiger",
        "master_category": "Accessories",
        "sub_category": "Belts",
        "price": "₹1,899",
        "mrp": "₹2,999",
        "discount": "(36% OFF)",
        "rating": "4.5 ★",
        "is_stylesync_eligible": False,
        "tags": "belt leather belt reversible tommy hilfiger accessories formal brown black buckle",
        "img": "https://images.unsplash.com/photo-1624222247344-550fb60583dc?w=800&auto=format&fit=crop&q=80"
    },

    # 7. Home & Lifestyle
    {
        "id": "home_1",
        "name": "100% Cotton 300TC King Size Bed Sheet",
        "brand": "Bombay Dyeing",
        "master_category": "Home",
        "sub_category": "Bedding",
        "price": "₹1,999",
        "mrp": "₹3,499",
        "discount": "(42% OFF)",
        "rating": "4.5 ★",
        "is_stylesync_eligible": False,
        "tags": "bedsheet bed sheet king size cotton 300tc floral bombay dyeing home bedding linen mattress cover",
        "img": "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "home_2",
        "name": "Nordic Ceramic Fluted Flower Vase",
        "brand": "Home Centre",
        "master_category": "Home",
        "sub_category": "Decor",
        "price": "₹899",
        "mrp": "₹1,499",
        "discount": "(40% OFF)",
        "rating": "4.6 ★",
        "is_stylesync_eligible": False,
        "tags": "vase fluted flower vase ceramic nordic home centre home decor aesthetic pottery plant",
        "img": "https://images.unsplash.com/photo-1581783342308-f792dbdd27c5?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "home_3",
        "name": "Textured Velvet Cushion Covers (Set of 5)",
        "brand": "D'Decor",
        "master_category": "Home",
        "sub_category": "Furnishing",
        "price": "₹1,199",
        "mrp": "₹2,199",
        "discount": "(45% OFF)",
        "rating": "4.4 ★",
        "is_stylesync_eligible": False,
        "tags": "cushion cushion covers velvet textured set of 5 d'decor ddecor home furnishing sofa pillow",
        "img": "https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=800&auto=format&fit=crop&q=80"
    },
    {
        "id": "home_4",
        "name": "Aroma Diffuser with Essential Oil",
        "brand": "PureSource",
        "master_category": "Home",
        "sub_category": "Living",
        "price": "₹1,299",
        "mrp": "₹1,999",
        "discount": "(35% OFF)",
        "rating": "4.7 ★",
        "is_stylesync_eligible": False,
        "tags": "diffuser aroma essential oil lavender puresource home living fragrance air freshener",
        "img": "https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=800&auto=format&fit=crop&q=80"
    }
]

# Legacy Compatibility for test_app.py
TARGET_ITEM = {
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

WISHLIST_PRODUCTS = [
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
# 3. STATE MANAGEMENT & ROUTING
# ==============================================================================

def init_session_state() -> None:
    """Initializes router state defaults ensuring compliance with prompt specifications."""
    if "current_view" not in st.session_state:
        st.session_state["current_view"] = "catalog"
    if "selected_item" not in st.session_state or st.session_state["selected_item"] is None:
        st.session_state["selected_item"] = MICRO_CATALOG[0]
    if "search_query" not in st.session_state:
        st.session_state["search_query"] = ""
    if "selected_category_filter" not in st.session_state:
        st.session_state["selected_category_filter"] = "All"
    if "bag_count" not in st.session_state:
        st.session_state["bag_count"] = 2
    if "wishlist_count" not in st.session_state:
        st.session_state["wishlist_count"] = 1
    if "selected_size" not in st.session_state:
        st.session_state["selected_size"] = "40"
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
    if "show_order_modal" not in st.session_state:
        st.session_state["show_order_modal"] = False
    if "ordered_item" not in st.session_state:
        st.session_state["ordered_item"] = None

init_session_state()

def set_view(view_name: str) -> None:
    st.session_state["current_view"] = view_name
    st.session_state["show_bag_drawer"] = False
    st.session_state["show_profile_modal"] = False
    st.session_state["show_size_chart"] = False
    st.rerun()

def view_product_pdp(item: CatalogItem) -> None:
    st.session_state["selected_item"] = item
    st.session_state["current_view"] = "pdp"
    st.rerun()

# ==============================================================================
# 4. TOP BRAND NAVIGATION BAR
# ==============================================================================

# Synonym & Keyword Matcher for High-Precision Search across ALL categories
SYNONYMS = {
    "jeans": ["jeans", "denim", "511", "501"],
    "jean": ["jeans", "denim"],
    "denim": ["denim", "jeans"],
    "shirt": ["shirt", "mandarin collar", "formal shirt", "casual shirt"],
    "tshirt": ["t-shirt", "tee", "graphic tee", "crewneck"],
    "tee": ["t-shirt", "tee", "graphic tee"],
    "blazer": ["blazer", "blazers", "coat", "mango man"],
    "jacket": ["jacket", "blazer", "coat", "trucker"],
    "trousers": ["trousers", "pleated trousers", "formal trousers", "chinos"],
    "pants": ["trousers", "pants", "chinos"],
    "shoes": ["shoes", "sneakers", "sneaker", "heels", "boots", "footwear", "running"],
    "sneaker": ["sneakers", "sneaker", "air max", "caven", "court", "ultraboost"],
    "sneakers": ["sneakers", "sneaker", "air max", "caven", "court", "ultraboost"],
    "running": ["running shoes", "ultraboost", "air max"],
    "heels": ["heels", "sandals", "block heeled", "carlton london"],
    "sandals": ["heels", "sandals", "block heeled"],
    "boots": ["boots", "chelsea", "high-top"],
    "watch": ["watch", "watches", "chronograph", "fossil", "dial"],
    "watches": ["watch", "watches", "chronograph", "fossil"],
    "sunglasses": ["sunglasses", "aviator", "ray-ban", "rayban", "eyewear", "shades"],
    "shades": ["sunglasses", "aviator", "ray-ban", "eyewear", "shades"],
    "perfume": ["perfume", "fragrance", "edp", "scent", "armaf", "cologne"],
    "fragrance": ["fragrance", "perfume", "edp", "scent", "armaf", "cologne"],
    "serum": ["serum", "niacinamide", "hyaluronic", "skincare", "clarifying"],
    "skincare": ["serum", "niacinamide", "hyaluronic", "skincare"],
    "lipstick": ["lipstick", "ruby woo", "matte lipstick", "lip color"],
    "makeup": ["lipstick", "ruby woo", "makeup"],
    "dress": ["dress", "frock", "maxi dress", "wrap dress", "gown"],
    "kurti": ["kurti", "kurta", "anarkali", "ethnic", "biba", "libas"],
    "kurta": ["kurti", "kurta", "anarkali", "ethnic", "biba", "libas"],
    "onesie": ["onesie", "infant onesie", "baby romper", "mothercare"],
    "baby": ["onesie", "infant", "baby romper", "mothercare", "carter's"],
    "kids": ["kids", "boys", "girls", "infant", "onesie", "dungaree", "frock"],
    "bedsheet": ["bed sheet", "bedsheet", "bedding", "bed cover", "bombay dyeing", "mattress cover"],
    "sheet": ["bed sheet", "bedsheet", "bedding"],
    "bedding": ["bed sheet", "bedsheet", "bedding"],
    "vase": ["vase", "flower vase", "fluted vase", "ceramic vase", "home centre"],
    "decor": ["vase", "decor", "cushion", "diffuser", "home centre", "d'decor"],
    "cushion": ["cushion", "cushion covers", "pillow cover", "d'decor"],
    "diffuser": ["diffuser", "aroma diffuser", "essential oil", "puresource"],
    "bag": ["bag", "handbag", "satchel", "purse", "tote", "caprese"],
    "handbag": ["bag", "handbag", "satchel", "purse", "tote", "caprese"],
    "belt": ["belt", "leather belt", "reversible belt", "tommy hilfiger"]
}

def render_top_navbar() -> None:
    curr = st.session_state.get("current_view", "catalog")
    bag_num = st.session_state.get("bag_count", 2)
    wl_num = st.session_state.get("wishlist_count", 1)

    nav_col1, nav_col2, nav_col3, nav_col4 = st.columns([2.2, 4.2, 3.4, 2.2])
    
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
        b1, b2, b3, b4, b5 = st.columns(5)
        with b1:
            if st.button("CATALOG", key="nav_cat_tab", use_container_width=True):
                set_view("catalog")
        with b2:
            if st.button("HOME", key="nav_home", use_container_width=True):
                set_view("homepage")
        with b3:
            if st.button("STUDIO ✨", key="nav_studio", use_container_width=True):
                set_view("stylesync")
        with b4:
            if st.button("WISHLIST", key="nav_wl_tab", use_container_width=True):
                set_view("wishlist")
        with b5:
            if st.button("BAG", key="nav_bag_tab", use_container_width=True):
                st.session_state["show_bag_drawer"] = not st.session_state["show_bag_drawer"]
                st.rerun()

    with nav_col3:
        with st.form("top_navbar_search_form", clear_on_submit=False):
            sc1, sc2 = st.columns([3.5, 1])
            with sc1:
                quick_search = st.text_input(
                    "Quick Search",
                    value=st.session_state.get("search_query", ""),
                    placeholder="🔍 Search jeans, shoes, kurti...",
                    label_visibility="collapsed",
                    key="top_nav_search_text"
                )
            with sc2:
                top_searched = st.form_submit_button("Search", type="primary", use_container_width=True)
            if top_searched:
                st.session_state["search_query"] = quick_search
                st.session_state["selected_category_filter"] = "All"
                st.session_state["current_view"] = "catalog"
                st.rerun()

    with nav_col4:
        ic1, ic2, ic3 = st.columns(3)
        with ic1:
            if st.button("👤 Profile", key="top_prof_btn", use_container_width=True):
                st.session_state["show_profile_modal"] = not st.session_state["show_profile_modal"]
                st.rerun()
        with ic2:
            if st.button(f"❤️ ({wl_num})", key="top_wl_btn", use_container_width=True):
                set_view("wishlist")
        with ic3:
            if st.button(f"🛍️ ({bag_num})", key="top_bag_btn", use_container_width=True):
                st.session_state["show_bag_drawer"] = not st.session_state["show_bag_drawer"]
                st.rerun()

    # Journey Stepper Quick Navigator Bar
    st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
    step1, step2, step3, step4, step5 = st.columns(5)
    with step1:
        if st.button("🔍 1. Master Catalog & Search", use_container_width=True, type="primary" if curr == "catalog" else "secondary"):
            set_view("catalog")
    with step2:
        if st.button("🏠 Storefront Hero", use_container_width=True, type="primary" if curr == "homepage" else "secondary"):
            set_view("homepage")
    with step3:
        if st.button("🛍️ 2. Product Display (PDP)", use_container_width=True, type="primary" if curr == "pdp" else "secondary"):
            set_view("pdp")
    with step4:
        if st.button("❤️ 3. Wishlist & Closet", use_container_width=True, type="primary" if curr == "wishlist" else "secondary"):
            set_view("wishlist")
    with step5:
        if st.button("✨ 4. StyleSync Studio", use_container_width=True, type="primary" if curr == "stylesync" else "secondary"):
            set_view("stylesync")
    
    st.markdown("<hr style='margin: 0.8rem 0 1.2rem 0; border: none; border-top: 1px solid #ECEEF0;'>", unsafe_allow_html=True)

    render_drawers_and_modals()


# ==============================================================================
# 5. DRAWERS & MODALS
# ==============================================================================

def render_drawers_and_modals() -> None:
    # 1-Click Order Placed Celebration Modal
    if st.session_state.get("show_order_modal", False) and st.session_state.get("ordered_item"):
        ord_item = st.session_state["ordered_item"]
        st.markdown(
            f"""
            <div class="modal-banner" style="border: 2px solid #03A685; box-shadow: 0 10px 30px rgba(3, 166, 133, 0.15); animation: fadeIn 0.3s ease-in-out;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <div style="font-size: 1.3rem; font-weight: 900; color: #282C3F;">
                        🎉 ORDER CONFIRMED & READY TO DISPATCH!
                    </div>
                    <span style="font-size: 0.8rem; font-weight: 800; color: #03A685; background: #E8F8F5; padding: 4px 10px; border-radius: 6px;">
                        Order #MYN-{int(time.time()) % 1000000}
                    </span>
                </div>
                <div style="display: flex; gap: 1.2rem; align-items: center; background: #F9FAFB; padding: 14px; border-radius: 10px; margin-bottom: 1rem; border: 1px solid #ECEEF0;">
                    <img src="{ord_item['img']}" style="width: 80px; height: 100px; object-fit: cover; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
                    <div style="flex: 1;">
                        <span style="font-size: 0.75rem; font-weight: 800; color: #FF3F6C; text-transform: uppercase;">{ord_item['brand']}</span>
                        <h4 style="font-size: 1.05rem; font-weight: 900; color: #282C3F; margin: 2px 0;">{ord_item['name']}</h4>
                        <div style="display: flex; align-items: baseline; gap: 8px; margin: 4px 0;">
                            <span style="font-size: 1.1rem; font-weight: 900; color: #282C3F;">{ord_item['price']}</span>
                            <span style="font-size: 0.85rem; color: #94969F; text-decoration: line-through;">{ord_item['mrp']}</span>
                            <span style="font-size: 0.75rem; font-weight: 800; color: #FF3F6C;">{ord_item['discount']}</span>
                        </div>
                        <div style="font-size: 0.8rem; color: #03A685; font-weight: 700;">
                            ⚡ Fast Express Delivery: <b>Tomorrow by 5:00 PM</b> • 100% Genuine • Free Returns
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        oc1, oc2 = st.columns(2)
        with oc1:
            if st.button("🛍️ View in Shopping Bag", key="order_view_bag_btn", type="primary", use_container_width=True):
                st.session_state["show_order_modal"] = False
                st.session_state["show_bag_drawer"] = True
                st.rerun()
        with oc2:
            if st.button("✖️ Continue Shopping", key="order_close_modal_btn", use_container_width=True):
                st.session_state["show_order_modal"] = False
                st.session_state["ordered_item"] = None
                st.rerun()

    # Shopping Bag Drawer
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
                    <div><b>Total Payable:</b> <span style="font-size: 1.2rem; font-weight: 900; color: #282C3F;">₹6,289</span> (Coupon: <code>MYNTRASAVE</code> applied -₹200)</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        b_c1, b_c2 = st.columns(2)
        with b_c1:
            if st.button("💳 Proceed to Checkout Now", key="drawer_checkout_btn", type="primary", use_container_width=True):
                st.balloons()
                st.toast("🎉 Order placed successfully! Delivery scheduled by tomorrow.")
                st.session_state["show_bag_drawer"] = False
                st.rerun()
        with b_c2:
            if st.button("✖️ Close Bag", key="close_bag_btn", use_container_width=True):
                st.session_state["show_bag_drawer"] = False
                st.rerun()

    # User Profile Modal
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
        if st.button("✖️ Close Profile", key="close_prof_btn", use_container_width=True):
            st.session_state["show_profile_modal"] = False
            st.rerun()


# ==============================================================================
# 6. SCREEN 1: THE MASTER SEARCH & DISCOVERY UI (`current_view == "catalog"`)
# ==============================================================================

def render_catalog_view() -> None:
    st.markdown(
        """
        <div class="section-header-wrap" style="margin-top: 0;">
            <div>
                <div class="section-title">🔍 MYNTRA MASTER CATALOG & SEARCH</div>
                <div class="section-subtitle">Browse all 5 Master Categories • Apparel, Footwear, Beauty, Accessories & Home</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 1. Top Wide Free-Text Search Bar Form
    with st.form("catalog_main_search_form", clear_on_submit=False):
        sb_col1, sb_col2, sb_col3 = st.columns([5, 1.2, 1])
        with sb_col1:
            search_input = st.text_input(
                "Free-Text Catalog Search",
                value=st.session_state.get("search_query", ""),
                placeholder="🔍 Search across fashion, beauty, home (e.g. jeans, linen blazer, sneakers, kurti, watch)...",
                label_visibility="collapsed",
                key="catalog_search_box_input"
            )
        with sb_col2:
            search_submitted = st.form_submit_button("🔍 Search", type="primary", use_container_width=True)
        with sb_col3:
            clear_submitted = st.form_submit_button("✖ Clear", use_container_width=True)
        
        if search_submitted:
            st.session_state["search_query"] = search_input
            st.session_state["selected_category_filter"] = "All"
            st.rerun()
        elif clear_submitted:
            st.session_state["search_query"] = ""
            st.session_state["selected_category_filter"] = "All"
            st.rerun()

    # Trending Search Keywords Chips
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 8px; font-size: 0.78rem; font-weight: 700; color: #7E818C; margin: 4px 0 8px 0;">
            <span>🔥 Trending Searches:</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    t_cols = st.columns(9)
    trend_list = [
        ("👖 Jeans", "jeans"),
        ("👔 Shirts", "shirt"),
        ("👕 T-Shirts", "tshirt"),
        ("🧥 Blazer", "blazer"),
        ("👟 Sneakers", "sneakers"),
        ("👗 Kurti", "kurti"),
        ("⌚ Watch", "watch"),
        ("🌸 Fragrance", "fragrance"),
        ("🛏️ Bedsheet", "bedsheet"),
    ]
    for idx, (label, val) in enumerate(trend_list):
        with t_cols[idx]:
            if st.button(label, key=f"trend_chip_{val}", use_container_width=True):
                st.session_state["search_query"] = val
                st.session_state["selected_category_filter"] = "All"
                st.rerun()

    # 2. Horizontal Category Filter Chips
    st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)
    categories = ["All", "Apparel", "Shirts", "T-Shirts", "Footwear", "Beauty", "Accessories", "Home"]
    current_cat = st.session_state.get("selected_category_filter", "All")
    
    chip_cols = st.columns(len(categories))
    for idx, cat_name in enumerate(categories):
        with chip_cols[idx]:
            is_active = (current_cat == cat_name)
            if st.button(
                f"{'⭐ ' if cat_name == 'All' else ''}{cat_name}",
                key=f"chip_{cat_name}",
                type="primary" if is_active else "secondary",
                use_container_width=True
            ):
                st.session_state["selected_category_filter"] = cat_name
                st.session_state["search_query"] = ""
                st.rerun()

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # 3. High-Precision Tokenized Filtering Engine with Synonym Expansion
    query = st.session_state.get("search_query", "").strip().lower()
    selected_filter = st.session_state.get("selected_category_filter", "All")

    query_tokens = [q for q in query.split() if len(q) > 0]
    search_tokens = set(query_tokens)
    for q_tok in query_tokens:
        for syn_key, syn_vals in SYNONYMS.items():
            if syn_key in q_tok or q_tok in syn_key:
                search_tokens.update(syn_vals)

    def filter_catalog(target_filter: str) -> List[CatalogItem]:
        results = []
        for item in MICRO_CATALOG:
            # 1. Category filter check
            if target_filter == "All":
                pass
            elif target_filter == "Apparel":
                if item["master_category"] not in ["Apparel", "Shirts", "T-Shirts"]:
                    continue
            elif target_filter == "Shirts":
                if item["master_category"] != "Shirts":
                    continue
            elif target_filter == "T-Shirts":
                if item["master_category"] != "T-Shirts":
                    continue
            elif item["master_category"] != target_filter:
                continue

            # 2. Search query check
            if query:
                item_name = item["name"].lower()
                item_brand = item["brand"].lower()
                item_cat = item["master_category"].lower()
                item_sub = item["sub_category"].lower()
                item_tags = item.get("tags", "").lower()
                item_text = f"{item_name} {item_brand} {item_cat} {item_sub} {item_tags}"

                matched = False
                if query in ["shirt", "shirts"]:
                    if item["master_category"] == "Shirts" or ("shirt" in item_name and "t-shirt" not in item_name and "tshirt" not in item_name):
                        matched = True
                elif query in ["tshirt", "t-shirt", "tshirts", "t-shirts", "tee", "tees"]:
                    if item["master_category"] == "T-Shirts" or "t-shirt" in item_name or "tshirt" in item_name or "tee" in item_tags:
                        matched = True
                else:
                    if query in item_text or any(token in item_text for token in search_tokens):
                        matched = True

                if not matched:
                    continue

            results.append(item)
        return results

    filtered_items = filter_catalog(selected_filter)

    # Results Header
    st.markdown(
        f"""
        <div style="font-size: 0.85rem; font-weight: 700; color: #535766; margin-bottom: 1rem;">
            Showing <b>{len(filtered_items)} items</b> in <i>{selected_filter}</i> {f'matching "{query}"' if query else ''}
        </div>
        """,
        unsafe_allow_html=True
    )

    if not filtered_items:
        st.warning(f"No products found matching '{query}' in '{selected_filter}'. Try searching for 'jeans', 'linen blazer', 'sneakers', 'watch', or 'serum'.")
        if st.button("Reset Search Filters", key="reset_filters_btn"):
            st.session_state["search_query"] = ""
            st.session_state["selected_category_filter"] = "All"
            st.rerun()
        return

    # 4. Grid Display (4-Column Layout with Direct Action Buttons)
    num_cols = 4
    rows = [filtered_items[i:i + num_cols] for i in range(0, len(filtered_items), num_cols)]

    for row_items in rows:
        cols = st.columns(num_cols)
        for idx, item in enumerate(row_items):
            with cols[idx]:
                # StyleSync / SubCategory Badge in fixed-height row
                if item["is_stylesync_eligible"]:
                    badge_html = '<span style="font-size: 0.68rem; font-weight: 900; background: #FFF0F4; color: #FF3F6C; border: 1px solid #FFD8E4; padding: 2px 6px; border-radius: 4px; text-transform: uppercase;">✨ StyleSync Eligible</span>'
                else:
                    badge_html = f'<span style="font-size: 0.68rem; font-weight: 700; background: #F5F5F6; color: #7E818C; padding: 2px 6px; border-radius: 4px; text-transform: uppercase;">{item["sub_category"]}</span>'

                img_html = f'<img src="{item["img"]}" style="width: 100%; height: 220px; max-height: 220px; min-height: 220px; object-fit: cover; object-position: center; border-radius: 10px; display: block;" />'

                card_html = (
                    f'<div>'
                    f'{img_html}'
                    f'<div style="margin-top: 6px;">'
                    f'<div style="height: 24px; display: flex; align-items: center;">{badge_html}</div>'
                    f'<div style="font-weight: 900; font-size: 0.82rem; color: #282C3F; text-transform: uppercase; height: 18px; line-height: 18px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; margin-top: 2px;">{item["brand"]}</div>'
                    f'<div style="font-size: 0.8rem; color: #535766; font-weight: 500; height: 36px; line-height: 1.25; overflow: hidden; text-overflow: ellipsis; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; margin-top: 2px;">{item["name"]}</div>'
                    f'<div style="display: flex; align-items: baseline; gap: 6px; height: 22px; margin: 4px 0 8px 0;">'
                    f'<span style="font-weight: 900; font-size: 0.92rem; color: #282C3F;">{item["price"]}</span>'
                    f'<span style="font-size: 0.75rem; color: #94969F; text-decoration: line-through;">{item["mrp"]}</span>'
                    f'<span style="font-size: 0.72rem; font-weight: 800; color: #FF3F6C;">{item["discount"]}</span>'
                    f'</div></div></div>'
                )
                st.markdown(card_html, unsafe_allow_html=True)
                
                # Direct Action Buttons for Every Product Card
                if st.button("👉 View Details", key=f"view_prod_{item['id']}", use_container_width=True):
                    view_product_pdp(item)

                qb1, qb2 = st.columns(2)
                with qb1:
                    if st.button("🛍️ +Bag", key=f"quick_bag_{item['id']}", use_container_width=True):
                        st.session_state["bag_count"] += 1
                        st.toast(f"✅ Added {item['brand']} {item['name']} to Bag!")
                        st.rerun()
                with qb2:
                    if st.button("❤️ Save", key=f"quick_wl_{item['id']}", use_container_width=True):
                        st.session_state["wishlist_count"] += 1
                        st.toast(f"❤️ Added {item['name']} to Wishlist!")
                        st.rerun()

                if st.button("⚡ 1-Click Order", key=f"quick_order_{item['id']}", type="primary", use_container_width=True):
                    st.session_state["ordered_item"] = item
                    st.session_state["show_order_modal"] = True
                    st.toast(f"🎉 Order placed for {item['brand']} {item['name']}!")
                    st.rerun()

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)


# ==============================================================================
# 7. SCREEN 2: HOMEPAGE STOREFRONT
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
        if st.button("📋 Copy Code 'MYNTRASAVE'", key="copy_coupon_btn_h", use_container_width=True):
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
            if st.button("🔥 EXPLORE NOW", key="hero_explore_btn_h", type="primary", use_container_width=True):
                view_product_pdp(MICRO_CATALOG[0])
        with c_btn2:
            if st.button("✨ Style with Closet", key="hero_stylesync_btn_h", use_container_width=True):
                set_view("stylesync")
        with c_btn3:
            if st.button("🔍 Search Catalog", key="hero_catalog_btn", use_container_width=True):
                set_view("catalog")

    # 3. Shop by Category Grid
    st.markdown(
        """
        <div class="section-header-wrap">
            <div>
                <div class="section-title">SHOP BY CATEGORY</div>
                <div class="section-subtitle">Curated trends across 5 master categories</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    cat1, cat2, cat3, cat4 = st.columns(4)
    with cat1:
        st.image(IMAGE_MEN_CAT, use_container_width=True)
        st.markdown("<h4 style='margin: 6px 0 2px 0; font-weight: 800;'>MEN'S CASUALS</h4><p style='color: #7E818C; font-size: 0.8rem;'>Linens, Polos & Trousers</p>", unsafe_allow_html=True)
        if st.button("Browse Apparel →", key="cat_men_btn_h", use_container_width=True):
            st.session_state["selected_category_filter"] = "Apparel"
            set_view("catalog")

    with cat2:
        st.image(IMAGE_WOMEN_CAT, use_container_width=True)
        st.markdown("<h4 style='margin: 6px 0 2px 0; font-weight: 800;'>WOMEN'S WEAR</h4><p style='color: #7E818C; font-size: 0.8rem;'>Dresses, Tops & Coordinates</p>", unsafe_allow_html=True)
        if st.button("Browse Women's →", key="cat_women_btn_h", use_container_width=True):
            st.session_state["selected_category_filter"] = "Apparel"
            set_view("catalog")

    with cat3:
        st.image(IMAGE_BEAUTY_CAT, use_container_width=True)
        st.markdown("<h4 style='margin: 6px 0 2px 0; font-weight: 800;'>BEAUTY & GROOMING</h4><p style='color: #7E818C; font-size: 0.8rem;'>Fragrance, Skincare & Grooming</p>", unsafe_allow_html=True)
        if st.button("Browse Beauty →", key="cat_beauty_btn_h", use_container_width=True):
            st.session_state["selected_category_filter"] = "Beauty"
            set_view("catalog")

    with cat4:
        st.image(IMAGE_HOME_CAT, use_container_width=True)
        st.markdown("<h4 style='margin: 6px 0 2px 0; font-weight: 800;'>HOME LIVING</h4><p style='color: #7E818C; font-size: 0.8rem;'>Modern Decor & Bedroom Accents</p>", unsafe_allow_html=True)
        if st.button("Browse Home →", key="cat_home_btn_h", use_container_width=True):
            st.session_state["selected_category_filter"] = "Home"
            set_view("catalog")


# ==============================================================================
# 8. SCREEN 3: DYNAMIC PRODUCT DISPLAY PAGE (`current_view == "pdp"`)
# ==============================================================================

def render_pdp_view() -> None:
    item: CatalogItem = st.session_state.get("selected_item", MICRO_CATALOG[0])

    # Header Back Button
    b_col1, b_col2 = st.columns([1.5, 4])
    with b_col1:
        if st.button("← Back to Catalog", key="pdp_back_catalog_btn", use_container_width=True):
            set_view("catalog")
    with b_col2:
        st.markdown(
            f"""
            <div style="font-size: 0.8rem; font-weight: 600; color: #7E818C; padding-top: 6px;">
                <span>Home</span> / <span>{item.get('master_category', 'Apparel')}</span> / <span>{item.get('sub_category', 'Men')}</span> / 
                <span style="color: #282C3F; font-weight: 800;">{item['brand']} {item['name']}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    col_img, col_details = st.columns([1.1, 1.2], gap="large")

    with col_img:
        st.image(item["img"], use_container_width=True)
        # Thumbnails
        t1, t2, t3 = st.columns(3)
        with t1:
            st.image(item["img"], use_container_width=True)
        with t2:
            st.image(IMAGE_OLIVE_SHIRT if item["is_stylesync_eligible"] else item["img"], use_container_width=True)
        with t3:
            st.image(IMAGE_BLACK_TROUSERS if item["is_stylesync_eligible"] else item["img"], use_container_width=True)

    with col_details:
        st.markdown(f"<span style='font-size: 0.85rem; font-weight: 900; color: #FF3F6C; letter-spacing: 1px;'>{item['brand']}</span>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='font-size: 1.8rem; font-weight: 900; color: #282C3F; margin: 4px 0 10px 0;'>{item['name']}</h1>", unsafe_allow_html=True)
        
        # Rating
        st.markdown(
            f"""
            <div style="display: inline-flex; align-items: center; gap: 6px; background: #FAFAFA; border: 1px solid #EAEAEC; border-radius: 6px; padding: 4px 10px; font-size: 0.82rem; font-weight: 800; margin-bottom: 1rem;">
                <span style="color: #03A685;">{item['rating']}</span>
                <span style="color: #94969F;">|</span>
                <span style="color: #535766;">Verified Customer Ratings</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Price
        st.markdown(
            f"""
            <div style="display: flex; align-items: baseline; gap: 12px; margin-bottom: 4px;">
                <span style="font-size: 1.8rem; font-weight: 900; color: #282C3F;">{item['price']}</span>
                <span style="font-size: 1.1rem; color: #94969F; text-decoration: line-through;">{item['mrp']}</span>
                <span style="font-size: 0.95rem; font-weight: 800; color: #FF5722; background: #FFF5F0; padding: 3px 8px; border-radius: 6px;">{item['discount']}</span>
            </div>
            <div style="font-size: 0.76rem; font-weight: 800; color: #03A685; margin-bottom: 1.2rem;">inclusive of all taxes • Free Shipping & 14-Day Returns</div>
            """,
            unsafe_allow_html=True
        )

        # ======================================================================
        # THE STYLESYNC INTERCEPTOR (If is_stylesync_eligible == True)
        # ======================================================================
        if item.get("is_stylesync_eligible", False):
            st.markdown(
                """
                <div style="background: linear-gradient(135deg, #FFF0F4 0%, #F5F0FF 100%); border: 2px solid #FF3F6C; border-radius: 14px; padding: 1.2rem; margin-bottom: 1.5rem; box-shadow: 0 4px 16px rgba(255, 63, 108, 0.08);">
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
                        <span style="font-size: 1.4rem;">✨</span>
                        <span style="font-size: 1rem; font-weight: 900; color: #FF3F6C;">StyleSync™ Smart Match Found!</span>
                    </div>
                    <p style="font-size: 0.85rem; color: #282C3F; font-weight: 600; margin-bottom: 0.8rem; line-height: 1.4;">
                        We detected <b>3 items in your purchase history</b> (Zara Trousers, Olive Linen Shirt, Fossil Watch) that create full modular outfits with this item.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button("✨ Launch StyleSync™ AI Studio & WhatsApp Poll →", key="pdp_stylesync_cta_btn", type="primary", use_container_width=True):
                st.toast("Opening StyleSync Wardrobe Matcher...")
                set_view("stylesync")

            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

        # Size Selector (Apparel/Footwear)
        if item["master_category"] in ["Apparel", "Footwear"]:
            st.markdown("<div style='font-size: 0.84rem; font-weight: 900; color: #282C3F; margin-bottom: 6px;'>SELECT SIZE</div>", unsafe_allow_html=True)
            s1, s2, s3, s4 = st.columns(4)
            curr_size = st.session_state.get("selected_size", "40")
            with s1:
                if st.button("38 / S", key="p_sz_38", type="primary" if curr_size == "38" else "secondary", use_container_width=True):
                    st.session_state["selected_size"] = "38"
                    st.rerun()
            with s2:
                if st.button("40 / M ⭐", key="p_sz_40", type="primary" if curr_size == "40" else "secondary", use_container_width=True):
                    st.session_state["selected_size"] = "40"
                    st.rerun()
            with s3:
                if st.button("42 / L", key="p_sz_42", type="primary" if curr_size == "42" else "secondary", use_container_width=True):
                    st.session_state["selected_size"] = "42"
                    st.rerun()
            with s4:
                if st.button("44 / XL", key="p_sz_44", type="primary" if curr_size == "44" else "secondary", use_container_width=True):
                    st.session_state["selected_size"] = "44"
                    st.rerun()

        # Standard Action Buttons
        btn_bag, btn_wish, btn_order = st.columns([1, 1, 1.2])
        with btn_bag:
            if st.button("🛍️ ADD TO BAG", key="pdp_add_bag_standard", type="secondary", use_container_width=True):
                st.session_state["bag_count"] += 1
                st.toast(f"✅ {item['brand']} {item['name']} added to shopping bag!")
                st.rerun()
        with btn_wish:
            if st.button("❤️ WISHLIST", key="pdp_add_wl_standard", use_container_width=True):
                st.session_state["wishlist_count"] += 1
                st.toast(f"❤️ Added {item['name']} to Wishlist!")
                st.rerun()
        with btn_order:
            if st.button("⚡ BUY NOW (1-CLICK)", key="pdp_buy_now_btn", type="primary", use_container_width=True):
                st.session_state["ordered_item"] = item
                st.session_state["show_order_modal"] = True
                st.balloons()
                st.toast(f"🎉 Order placed for {item['brand']} {item['name']}!")
                st.rerun()


# ==============================================================================
# 9. SCREEN 4: WISHLIST & SMART CLOSET ANCHOR
# ==============================================================================

def render_wishlist_view() -> None:
    st.markdown(
        """
        <div class="section-header-wrap" style="margin-top: 0;">
            <div>
                <div class="section-title">MY WISHLIST & SAVED WARDROBE</div>
                <div class="section-subtitle">1 Target Anchor Garment • 6 Paired Wardrobe Pieces</div>
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
        if st.button("✨ Style with My Closet (Run StyleSync AI) →", key="wl_run_ai_btn", type="primary", use_container_width=True):
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
            if st.button(f"🛍️ Move to Bag", key=f"wl_bag_{item['id']}", use_container_width=True):
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
            if st.button(f"🛍️ Move to Bag", key=f"wl_bag_{item['id']}", use_container_width=True):
                st.session_state["bag_count"] += 1
                st.toast(f"Added {item['name']} to Bag!")
                st.rerun()


# ==============================================================================
# 10. SCREEN 5: STYLESYNC AI STUDIO & WHATSAPP SOCIAL POLL
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
            if st.button("💬 Poll Look 1", key="poll_look_1_btn", type="primary", use_container_width=True):
                st.session_state["poll_sent"] = True
                st.session_state["poll_look_title"] = "Look 1: Sunset Linen"
                st.toast("💬 Look 1 shared to WhatsApp Poll!")
                st.rerun()
        with b_p2:
            if st.button("🛍️ Add Look 1", key="add_l1_btn", use_container_width=True):
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
            if st.button("💬 Poll Look 2", key="poll_look_2_btn", use_container_width=True):
                st.session_state["poll_sent"] = True
                st.session_state["poll_look_title"] = "Look 2: Urban Brunch"
                st.toast("💬 Look 2 shared to WhatsApp Poll!")
                st.rerun()
        with b_p4:
            if st.button("🛍️ Add Look 2", key="add_l2_btn", use_container_width=True):
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
            if st.button("💬 Poll Look 3", key="poll_look_3_btn", use_container_width=True):
                st.session_state["poll_sent"] = True
                st.session_state["poll_look_title"] = "Look 3: Smart Business"
                st.toast("💬 Look 3 shared to WhatsApp Poll!")
                st.rerun()
        with b_p6:
            if st.button("🛍️ Add Look 3", key="add_l3_btn", use_container_width=True):
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
# 11. FOOTER COMPONENT
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
# 12. MAIN ROUTER
# ==============================================================================

def main() -> None:
    render_top_navbar()

    current_view = st.session_state.get("current_view", "catalog")

    if current_view == "catalog":
        render_catalog_view()
    elif current_view == "homepage":
        render_homepage_view()
    elif current_view == "pdp":
        render_pdp_view()
    elif current_view == "wishlist":
        render_wishlist_view()
    elif current_view == "stylesync":
        render_stylesync_view()
    else:
        render_catalog_view()

    render_footer()


if __name__ == "__main__":
    main()
