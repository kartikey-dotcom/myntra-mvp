"""
Automated Verification Suite for Myntra StyleSync MVP & Master Micro-Catalog
============================================================================
Validates:
1. Master Micro-Catalog structure, segments, and is_stylesync_eligible uniqueness.
2. Target wishlisted garment data model and high-res image URLs.
3. Rule-of-3 modular look configurations and defensive moats.
4. Streamlit session state lifecycle integrity.
"""

import unittest
from app import (
    MICRO_CATALOG,
    TARGET_ITEM,
    WISHLIST_PRODUCTS,
    init_session_state,
)


class TestStyleSyncDataAndState(unittest.TestCase):

    def test_micro_catalog_segments(self):
        """Verify the 30+ items master catalog and segmentation across 5 categories."""
        self.assertGreaterEqual(len(MICRO_CATALOG), 30)
        
        # Verify master categories present
        categories = {item["master_category"] for item in MICRO_CATALOG}
        self.assertTrue({"Apparel", "Footwear", "Beauty", "Accessories", "Home"}.issubset(categories))

        # Verify hero_1 is the ONLY is_stylesync_eligible == True item
        stylesync_eligible_items = [item for item in MICRO_CATALOG if item.get("is_stylesync_eligible")]
        self.assertEqual(len(stylesync_eligible_items), 1)
        self.assertEqual(stylesync_eligible_items[0]["id"], "hero_1")
        self.assertEqual(stylesync_eligible_items[0]["name"], "Rust Linen Relaxed-Fit Blazer")
        self.assertEqual(stylesync_eligible_items[0]["brand"], "MANGO MAN")
        self.assertEqual(stylesync_eligible_items[0]["price"], "₹3,499")
        self.assertEqual(stylesync_eligible_items[0]["mrp"], "₹4,999")
        self.assertEqual(stylesync_eligible_items[0]["discount"], "(30% OFF)")
        self.assertEqual(stylesync_eligible_items[0]["rating"], "4.4 ★")

        # Verify all image URLs are valid
        for item in MICRO_CATALOG:
            self.assertTrue(item["img"].startswith("https://images.unsplash.com/"))
            self.assertTrue(item["price"].startswith("₹"))
            self.assertTrue(item["mrp"].startswith("₹"))

    def test_target_item_schema(self):
        """Verify target wishlisted item structure, pricing, and image asset."""
        self.assertEqual(TARGET_ITEM["id"], "ITEM-9081")
        self.assertIn("Rust Linen", TARGET_ITEM["name"])
        self.assertEqual(TARGET_ITEM["price"], "₹3,499")
        self.assertEqual(TARGET_ITEM["original_price"], "₹4,999")
        self.assertEqual(TARGET_ITEM["discount"], "30% OFF")
        self.assertTrue(TARGET_ITEM["image_url"].startswith("https://images.unsplash.com/"))

    def test_wishlist_products_schema(self):
        """Verify wishlist products list and image assets."""
        self.assertGreaterEqual(len(WISHLIST_PRODUCTS), 6)
        for prod in WISHLIST_PRODUCTS:
            self.assertTrue(prod["image_url"].startswith("https://images.unsplash.com/"))
            self.assertTrue(prod["price"].startswith("₹"))
            self.assertTrue(len(prod["name"]) > 0)

    def test_session_state_helpers(self):
        """Verify session state defaults and router state."""
        import streamlit as st
        init_session_state()
        self.assertIn("current_view", st.session_state)
        self.assertIn(st.session_state["current_view"], ["catalog", "homepage", "pdp"])
        self.assertIn("selected_item", st.session_state)
        self.assertIn("search_query", st.session_state)
        self.assertIn("selected_category_filter", st.session_state)
        self.assertIn("poll_sent", st.session_state)

    def test_dynamic_stylesync_looks(self):
        """Verify dynamic Rule-of-3 outfit generation for various anchor garment types."""
        from app import get_stylesync_looks_for_anchor
        
        # 1. Shirt / Top anchor
        shirt_anchor = {
            "id": "W-102",
            "brand": "H&M",
            "name": "Relaxed Fit Olive Linen Shirt",
            "price": "₹1,999",
            "image_url": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf"
        }
        shirt_looks = get_stylesync_looks_for_anchor(shirt_anchor)
        self.assertEqual(len(shirt_looks), 3)
        self.assertIn("H&M Relaxed Fit Olive Linen Shirt", shirt_looks[0]["anchor_label"])
        self.assertIn("Zara Pants", shirt_looks[0]["sub1_name"])
        self.assertIn("Fossil Watch", shirt_looks[0]["sub2_name"])

        # 2. Footwear anchor
        foot_anchor = {
            "id": "foot_1",
            "brand": "Nike",
            "name": "Air Max SC Leather Retro Sneakers",
            "price": "₹5,995",
            "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff"
        }
        foot_looks = get_stylesync_looks_for_anchor(foot_anchor)
        self.assertEqual(len(foot_looks), 3)
        self.assertIn("Nike Air Max SC Leather Retro Sneakers", foot_looks[0]["anchor_label"])
        self.assertIn("Levi's 511", foot_looks[0]["sub1_name"])

        # 3. Blazer anchor
        blazer_looks = get_stylesync_looks_for_anchor(TARGET_ITEM)
        self.assertEqual(len(blazer_looks), 3)
        self.assertIn("MANGO MAN", blazer_looks[0]["anchor_label"])


    def test_dynamic_shopping_bag_and_order_accuracy(self):
        """Verify dynamic bag items, add/remove functions, and order confirmation accuracy."""
        import streamlit as st
        from app import add_to_bag, remove_from_bag
        
        init_session_state()
        initial_count = len(st.session_state["bag_items"])
        self.assertGreaterEqual(initial_count, 1)

        # Add a custom sneaker item from catalog
        sneaker_item = {
            "id": "foot_1",
            "name": "Air Max SC Leather Retro Sneakers",
            "brand": "Nike",
            "price": "₹5,995",
            "mrp": "₹7,995",
            "discount": "25% OFF",
            "img": "https://images.unsplash.com/photo-1542291026-7eec264c27ff"
        }
        add_to_bag(sneaker_item, size="9")
        self.assertEqual(len(st.session_state["bag_items"]), initial_count + 1)
        self.assertEqual(st.session_state["bag_count"], initial_count + 1)
        self.assertEqual(st.session_state["bag_items"][-1]["name"], "Air Max SC Leather Retro Sneakers")
        self.assertEqual(st.session_state["bag_items"][-1]["img"], "https://images.unsplash.com/photo-1542291026-7eec264c27ff")

        # Test single item checkout preserves actual item image and details
        single_item = st.session_state["bag_items"][-1]
        st.session_state["ordered_item"] = {
            "id": single_item["id"],
            "name": single_item["name"],
            "brand": single_item["brand"],
            "price": single_item["price"],
            "mrp": single_item["mrp"],
            "discount": single_item["discount"],
            "img": single_item["img"]
        }
        self.assertEqual(st.session_state["ordered_item"]["img"], "https://images.unsplash.com/photo-1542291026-7eec264c27ff")
        self.assertEqual(st.session_state["ordered_item"]["brand"], "Nike")
        self.assertEqual(st.session_state["ordered_item"]["name"], "Air Max SC Leather Retro Sneakers")

        # Test removal
        remove_from_bag(len(st.session_state["bag_items"]) - 1)
        self.assertEqual(len(st.session_state["bag_items"]), initial_count)

    def test_dynamic_wishlist_add_and_remove(self):
        """Verify dynamic wishlist items, add/remove functions, and count synchronization."""
        import streamlit as st
        from app import add_to_wishlist, remove_from_wishlist, clear_wishlist
        
        init_session_state()
        initial_wl_count = len(st.session_state["wishlist_items"])
        self.assertGreaterEqual(initial_wl_count, 1)

        # Add a test product to wishlist
        test_prod = {
            "id": "W-TEST-99",
            "name": "Luxury Silk Floral Saree",
            "brand": "KALKI",
            "price": "₹7,999",
            "mrp": "₹11,999",
            "discount": "33% OFF",
            "img": "https://images.unsplash.com/photo-1610030469983-98e550d6193c"
        }
        add_to_wishlist(test_prod)
        self.assertEqual(len(st.session_state["wishlist_items"]), initial_wl_count + 1)
        self.assertEqual(st.session_state["wishlist_count"], initial_wl_count + 1)
        self.assertEqual(st.session_state["wishlist_items"][0]["name"], "Luxury Silk Floral Saree")
        self.assertEqual(st.session_state["anchor_item"]["name"], "Luxury Silk Floral Saree")

        # Test item removal by ID
        remove_from_wishlist("W-TEST-99")
        self.assertEqual(len(st.session_state["wishlist_items"]), initial_wl_count)
        self.assertEqual(st.session_state["wishlist_count"], initial_wl_count)

        # Test clear wishlist
        clear_wishlist()
        self.assertEqual(len(st.session_state["wishlist_items"]), 0)
        self.assertEqual(st.session_state["wishlist_count"], 0)


if __name__ == "__main__":
    unittest.main()
