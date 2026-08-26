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
    OUTFIT_LOOKS,
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

    def test_outfit_looks_and_moats(self):
        """Verify presence of Rule-of-3 outfits and defensive moats."""
        self.assertEqual(len(OUTFIT_LOOKS), 2, "Must generate exactly 2 modular looks")
        
        # Check Look 1 contains offline camera roll moat item
        look_1_badges = [item["badge_class"] for item in OUTFIT_LOOKS[0]["items"]]
        self.assertIn("badge-offline", look_1_badges, "Look 1 must contain offline camera roll moat piece")
        self.assertIn("badge-owned", look_1_badges, "Look 1 must contain owned closet piece")

        # Check Look 2 contains suggested pairing and wishlist accessory
        look_2_badges = [item["badge_class"] for item in OUTFIT_LOOKS[1]["items"]]
        self.assertIn("badge-fit", look_2_badges, "Look 2 must contain suggested fit piece")
        self.assertIn("badge-wishlist", look_2_badges, "Look 2 must contain wishlist piece")

    def test_session_state_helpers(self):
        """Verify session state defaults."""
        import streamlit as st
        init_session_state()
        self.assertIn("is_styled", st.session_state)
        self.assertIn("poll_sent", st.session_state)


if __name__ == "__main__":
    unittest.main()
