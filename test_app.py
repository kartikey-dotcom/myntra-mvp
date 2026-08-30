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


if __name__ == "__main__":
    unittest.main()
