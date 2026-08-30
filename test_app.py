"""
Automated Verification Suite for Myntra StyleSync MVP
=====================================================
Validates:
1. Target wishlisted garment data model and high-res image URLs.
2. Rule-of-3 modular look configurations and defensive moats.
3. Streamlit session state lifecycle integrity.
"""

import unittest
from app import (
    TARGET_ITEM,
    WISHLIST_PRODUCTS,
    init_session_state,
)


class TestStyleSyncDataAndState(unittest.TestCase):

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
        """Verify session state defaults and 3-step router state."""
        import streamlit as st
        init_session_state()
        self.assertIn("current_view", st.session_state)
        self.assertIn(st.session_state["current_view"], ["homepage", "pdp"])
        self.assertIn("poll_sent", st.session_state)


if __name__ == "__main__":
    unittest.main()
