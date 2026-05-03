# Predictive Inventory Optimization: The Impact of Demand Sensing on Stockout Prevention

## 📌 Project Overview
This project focuses on the prototyping and validation of a predictive Demand Sensing system for DataCo. The core objective is to demonstrate that integrating digital intent signals (web traffic and navigation) with transactional history allows the transition from a reactive inventory management to a highly proactive system.

## ⚠️ The Business Problem & The ERP Gap
The company suffered from an inertia-based management (relying strictly on past sales history). Because the native ERP system had severe analytical blockages regarding physical stock identification (the *Product Status* variable had zero variance), a "Stockout Proxy" and a "Viability Score" were engineered to statistically isolate the Top 5 most critical products. In the baseline scenario, this reactive operational management resulted in a critical volume of 161 stockout units in a single week.

## 🧠 The Solution & Tech Stack
A predictive engine (Random Forest Regressor) was developed to act as an advanced purchase intent radar, structurally enriched through Feature Engineering (using click lags and moving averages).
*   **Language:** Python
*   **Machine Learning:** Scikit-Learn (Random Forest Regressor configured with `max_depth=5` for mathematical stability)
*   **Logistics Simulation:** Interactive executive Dashboard built with Streamlit

## 📊 Key Results (7-Day Stress-Test)
*   **Statistical Accuracy:** The model achieved an $R^2$ of **72.2%** on unseen test data, vastly outperforming the simple Baseline heuristic (which only explained 37.7% of market volatility).
*   **Operational Efficiency:** In a scenario forced with a strict 6-day Lead Time, the model reduced critical logistical incidents by **74.5%** (dropping from 161 to just 41 failures compared to historical reality).
*   **Financial Return (ROI):** The intelligent anticipation of demand effectively prevented delivery disruptions and generated **$18,128.69** in Protected Revenue.

## 🚀 How to Run Locally
1. Clone this repository.
2. Install required dependencies: `pip install -r requirements.txt`
3. Run the application prototype: `streamlit run app/app.py` *(adjust path if necessary)*

> **Data Note:** Due to GitHub file size limits and code versioning best practices, the original large `.csv` datasets are not included in this repository. The complete data folder is provided in the Cloud directory shared with the evaluation committee.
