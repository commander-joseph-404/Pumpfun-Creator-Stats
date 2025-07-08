# Pump.fun Creator Stats

A Streamlit web app that analyzes token creation activity by any Pump.fun creator. It reveals token migration data, wallet balances, creator rewards, and key token stats.

## Features

- 🔍 Look up any Pump.fun creator using their wallet address or a token address
- 📊 View detailed stats on:
  - Number of tokens created
  - Number and percentage of tokens migrated to Raydium or Pumpswap
  - Market cap of created vs. migrated tokens
  - Average time to migrate
- 📈 Visualize token performance with charts
- 🔗 Fetch live data from the Pump.fun API

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username//Pumpfun-Creator-Stats.git
cd Pumpfun-Creator-Stats
```

### 2. Install Dependencies

Make sure you have Python 3.10+ installed.

```bash
pip install -r requirements.txt
```

### 3. Run the App

```bash
streamlit run main.py
```

## Project Structure

```
Pumpfun-Creator-Stats/
├── main.py                  # Main Streamlit app
├── requirements.txt        # Python dependencies
└── README.md
```

## Notes

- Sleep intervals are used in API calls to ensure stable data collection.

## Disclaimer

This project is not affiliated with Pump.fun. Use at your own risk.

## Author

Built with 🦁 by [@Comm\_Joseph](https://x.com/Comm_Joseph)

