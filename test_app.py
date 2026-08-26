"""
Automated Verification Suite for Myntra StyleSync MVP (Phase 8)
==============================================================
Validates:
1. In-memory data structures and TypedDict compliance.
2. Presence of the Universal Closet defensive moat.
3. Rule-of-3 modular look configurations.
4. Session state lifecycle integrity.
"""

import sys
import unittest
from app import (
    TARGET_ITEM,
    PAST_PURCHASES,
    WISHLIST_INVENTORY,
    OUTFIT_LOOKS,
    init_session_state,
    reset_session_state,
    get_session_debug_state,
)


class TestStyleSyncDataAndState(unittest.TestCase):

    def test_target_item_schema(self):
        """Verify target wishlisted item structure and pricing."""
        self.assertEqual(TARGET_ITEM["id"], "ITEM-9081")
        self.assertIn("Rust Linen", TARGET_ITEM["name"])
        self.assertEqual(TARGET_ITEM["price"], "₹3,499")
        self.assertEqual(TARGET_ITEM["original_price"], "₹4,999")
        self.assertEqual(TARGET_ITEM["discount"], "30% OFF")
        self.assertEqual(TARGET_ITEM["icon"], "🧥")

    def test_universal_closet_moat(self):
        """Verify presence of on-platform and off-platform closet items."""
        badges = [item["badge"] for item in PAST_PURCHASES]
        
        # Verify on-platform Myntra item
        has_myntra_item = any("Purchased on Myntra" in b for b in badges)
        self.assertTrue(has_myntra_item, "Must contain an on-platform Myntra purchase")
        
        # Verify Universal Closet moat (camera-roll upload)
        has_offline_item = any("Offline Closet" in b for b in badges)
        self.assertTrue(has_offline_item, "Must contain an offline camera-roll upload item")

    def test_outfit_looks_composition(self):
        """Verify Rule-of-3 modular looks."""
        self.assertEqual(len(OUTFIT_LOOKS), 2, "Must generate exactly 2 modular looks")
        
        # Look 1: Smart Casual Office
        look_1 = OUTFIT_LOOKS[0]
        self.assertEqual(look_1["id"], "look_1")
        self.assertIn("Smart Casual", look_1["title"])
        self.assertEqual(len(look_1["items"]), 3, "Look 1 must have 3 modular pieces")
        
        # Look 2: Weekend Brunch
        look_2 = OUTFIT_LOOKS[1]
        self.assertEqual(look_2["id"], "look_2")
        self.assertIn("Weekend", look_2["title"])
        self.assertEqual(len(look_2["items"]), 4, "Look 2 must have 4 modular pieces (including accessory)")

    def test_session_state_helpers(self):
        """Verify session state default registry."""
        import streamlit as st
        init_session_state()
        state = get_session_debug_state()
        self.assertIn("is_styled", state)
        self.assertIn("poll_sent", state)
        self.assertIn("active_look", state)


if __name__ == "__main__":
    unittest.main()
