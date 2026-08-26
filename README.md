# 🛍️ Myntra "StyleSync" MVP
### AI-Powered Smart Closet & Social Validation System

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)

---

## 🎯 Executive Overview

**StyleSync** is a high-fidelity "Wizard of Oz" prototype designed to solve two major friction points in e-commerce:
1. **"Styling Paralysis"**: Users hesitate to buy wishlisted items because they don't know how to style them with their existing clothes.
2. **"Off-Platform Leakage"**: Users exit the shopping app to ask friends on WhatsApp, causing cart abandonment and lost conversion.

---

## 🛡️ Strategic Moats Implemented

1. **"Universal Closet"**:
   - Merges verified on-platform purchase history (`✅ In your closet (Purchased on Myntra)`) with external wardrobe uploads (`📸 Offline Closet (Uploaded from Camera Roll)`).
   - Creates a durable cross-platform lock-in effect.
2. **"Buy or Drop" Social Loop**:
   - Native WhatsApp interactive card preview allowing 1-tap peer voting directly without breaking purchasing momentum.
3. **Resilient Session State Machine**:
   - Built on robust `st.session_state` persistence to prevent UI resets on secondary button clicks.

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Python 3.9+ installed.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Application
```bash
streamlit run app.py
```
The application will launch locally at `http://localhost:8501`.

---

## 📁 Repository Structure

```
myntra-mvp/
├── app.py                      # Complete single-file Streamlit application
├── requirements.txt            # Streamlit deployment dependencies
├── README.md                   # Project documentation & presentation guide
├── problemstatement.md         # Problem & requirements specification
├── architecture.md             # System technical architecture document
├── implementationplan.md       # Phase-wise implementation plan
└── docs/                       # Synced reference documentation
    ├── problemstatement.md
    ├── architecture.md
    └── implementationplan.md
```
