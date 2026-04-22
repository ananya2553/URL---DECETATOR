# 🛡️ Sentinel Blue | Neural-Sync Engine

**Sentinel Blue** is a high-performance URL Phishing Defense system that leverages a hybrid architecture of traditional Machine Learning and Advanced Generative AI (Gemini) to neutralize malicious threats in real-time.

![Sentinel Blue UI](https://raw.githubusercontent.com/ananya2553/URL---DECETATOR/main/preview.png) *(Placeholder for Preview Image)*

## 🚀 Features

- **Hybrid Intelligence**: Combines a Random Forest ML model for pattern recognition with Google's Gemini AI for deep semantic reasoning.
- **Neural-Sync Visualization**: A premium, MacBook-inspired dashboard built with Streamlit, featuring glassmorphism and real-time scanning animations.
- **Deep Feature Extraction**: Analyzes structure, behavioral patterns, and suspicious keywords from target URLs.
- **Confidence Scoring**: Provides transparency with percentage-based confidence levels for every verdict.

## 🛠️ Technology Stack

- **Frontend**: [Streamlit](https://streamlit.io/) with custom CSS immersion.
- **Machine Learning**: Scikit-Learn (Random Forest) for fast local inference.
- **Generative AI**: Google Gemini Pro via the `google-generativeai` SDK.
- **Data Engineering**: Pandas & Plotly for insights and visualization.

## 📦 Setup & Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ananya2553/URL---DECETATOR.git
   cd url-detector
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Key**:
   Open `app.py` and replace `GEMINI_API_KEY` with your actual Google AI Studio API key.

4. **Launch the Engine**:
   ```bash
   streamlit run app.py
   ```

## 🧠 Behind the Scenes

The engine evaluates URLs based on:
- **Structural Integrity**: Length, dot count, subdomain complexity.
- **Security Protocols**: HTTPS validation and IP-based redirection checks.
- **Semantic Intent**: Suspicious keyword frequency (login, verify, update, etc.).

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
Built with ❤️ by [Ananya](https://github.com/ananya2553)
