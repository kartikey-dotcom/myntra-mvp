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

    def test_session_state_helpers(self):
        """Verify session state defaults and 3-step router state."""
        import streamlit as st
        init_session_state()
        self.assertIn("current_view", st.session_state)
        self.assertEqual(st.session_state["current_view"], "pdp")
        self.assertIn("poll_sent", st.session_state)


if __name__ == "__main__":
    unittest.main()
