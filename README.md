# 🛍️ Myntra "StyleSync" MVP
### AI-Powered Smart Closet & Social Validation System

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 Executive Overview

**StyleSync** is a high-fidelity "Wizard of Oz" prototype designed to eliminate the two largest drop-off points in modern fashion e-commerce:
1. **"Styling Paralysis"**: Users hesitate to buy wishlisted items because they don't know how to style them with their existing clothes.
2. **"Off-Platform Leakage"**: Users exit the shopping app to ask friends on WhatsApp, causing cart abandonment and lost conversion.

---

## 🛡️ Strategic Moats Implemented

1. **"Universal Closet"**:
   - Merges verified on-platform purchase history (`✅ In your closet (Purchased on Myntra)`) with external wardrobe uploads (`📸 Offline Closet (Uploaded from Camera Roll)`).
   - Creates a durable cross-platform lock-in effect that competitors cannot easily replicate.
2. **"Buy or Drop" Social Loop**:
   - Native WhatsApp interactive card preview allowing 1-tap peer voting directly without breaking purchasing momentum.
3. **Resilient Session State Machine**:
   - Built on robust `st.session_state` persistence to prevent UI resets on secondary button clicks.

---

## 🚀 Quickstart & Local Execution

### 1. Prerequisites
- Python 3.9+ installed on your machine.

### 2. Clone the Repository
```bash
git clone https://github.com/kartikey-dotcom/myntra-mvp.git
cd myntra-mvp
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables (Optional for LLM integration)
Copy `env.example` to `.env` and insert your Google AI Studio API key:
```bash
cp .env.example .env
```

### 5. Launch the Application
```bash
streamlit run app.py
```
The prototype will open in your browser at `http://localhost:8501`.

---

## ☁️ 1-Click Streamlit Community Cloud Deployment

To deploy this live on the cloud for your portfolio:
1. Go to [share.streamlit.io](https://share.streamlit.io).
2. Sign in with GitHub and click **"New app"**.
3. Select your repository: `kartikey-dotcom/myntra-mvp`.
4. Branch: `main` | Main file path: `app.py`.
5. Click **"Deploy!"**.

---

## 🧪 Automated Verification Suite

Run the built-in unit tests to verify data schemas, the Universal Closet moat, and state lifecycle:
```bash
python -m unittest test_app.py
```

---

## 📁 Repository Structure

```
myntra-mvp/
├── app.py                      # Complete single-file Streamlit application
├── test_app.py                 # Automated verification test suite
├── requirements.txt            # Streamlit Cloud deployment dependencies
├── .env.example                # Sample environment configuration template
├── .gitignore                  # Secrets and cache exclusion rules
├── README.md                   # Project documentation & presentation guide
├── problemstatement.md         # Problem & requirements specification
├── architecture.md             # System technical architecture document
├── implementationplan.md       # Phase-wise implementation plan (Phases 0-8)
├── edgecase.md                 # Edge case analysis & mitigation matrix
└── docs/                       # Synced reference documentation
    ├── problemstatement.md
    ├── architecture.md
    ├── implementationplan.md
    └── edgecase.md
```
