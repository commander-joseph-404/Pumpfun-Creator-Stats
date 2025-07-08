# 🚀 Pump.fun Creator Stats

A powerful Streamlit app that analyzes token creation activity on [Pump.fun](https://pump.fun), giving you detailed insights into tokens created by a specific creator or tied to a specific token address.

---

## 🔍 What It Does

- Accepts either:
  - A **Token Address** (to fetch the creator), or  
  - A **Creator Address** (to fetch all tokens they've created)
- Fetches up to **1,000 tokens** created by that user
- Analyzes:
  - Which tokens were **migrated** (to Raydium or Pumpswap)
  - **Time it took to migrate**
  - **Average and max market cap**
  - **Creator wallet balance (USD)**
  - **Total creator rewards (in SOL)**

---

## 📊 Features

- ✅ Analyze any token or creator on Pump.fun  
- 📈 Shows percentage of tokens migrated  
- ⏱️ Tracks migration time per token  
- 💰 Calculates wallet balance and creator rewards  
- 📦 View top 10 tokens by market cap  
- 🧾 Full token table with migration status  
- 📉 Interactive Plotly charts: Pie, Histogram, Bar

---

## 🧪 How It Works

1. **Choose Input Type** – Token or Creator address
2. **Fetch Creator Tokens** – Retrieves all tokens created by the address via Pump.fun API
3. **Analyze**:
    - Migration timestamp
    - Market cap stats
    - Wallet balance (via `swap-api.pump.fun`)
    - Creator rewards (via `fees` endpoint)
4. **Display**:
    - Metrics
    - Charts
    - Interactive data table

---

## 🧰 How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/your-username/pumpfun-creator-stats.git
cd pumpfun-creator-stats
---

### 2. Install Dependencies
Make sure you have Python 3.10 or higher installed. Then run:

```bash
pip install -r requirements.txt

---
### 3. Run the App Locally
To launch the Streamlit app in your browser:

```bash
streamlit run main.py

---
## 🧑‍💻 Author

Built with 🦁 by [@Comm_Joseph](https://x.com/Comm_Joseph)

🚀 2. Install Dependencies
Make sure you have Python 3.10+ installed. Then run:

bash
Copy
Edit
pip install -r requirements.txt
If you're using poetry:

bash
Copy
Edit
poetry install
🧪 3. Run the App
To start the Streamlit app locally:

bash
Copy
Edit
streamlit run app.py
🧑‍💻 Author







