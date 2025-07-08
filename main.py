
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import time
# Set headers for requests
headers = {"accept": "application/json",
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

# Streamlit app for Pump.fun Creator Token Stats
st.set_page_config(page_title="Pump.fun Creator Stats", layout="wide")
st.title("🚀 Pump.fun Token Creator Stats")

# Input selection: Token or Creator address
input_type = st.radio("Choose input method:", ["🎯 Token address", "👤 Creator address"])

col1, col2 = st.columns([4, 1])

creator_address = None
token_address = None

with col1:
    if input_type == "🎯 Token address":
        token_address = st.text_input("Enter Token Address")
    else:
        creator_address = st.text_input("Enter Creator Address")

with col2:
    analyze = st.button("🔍 Analyze Tokens", type="primary")

# Handle token address -> get creator
if input_type == "🎯 Token address" and analyze:
    if not token_address:
        st.warning("⚠️ Please enter a valid token address.")
        st.stop()

    url = f"https://frontend-api-v3.pump.fun/coins/{token_address}"
    try:
        resp = requests.get(url, timeout=10, headers=headers)
        if resp.status_code == 200 and resp.text.strip():
            data = resp.json()
            creator_address = data.get("creator")
            if not creator_address:
                st.error("❌ Creator not found in token response.")
                st.stop()
        else:
            st.error("❌ Token not found or invalid address.")
            st.stop()
    except Exception:
        st.error("❌ Error fetching token info.")
        st.stop()

# Stop if no creator address
if not creator_address and analyze:
    st.warning("⚠️ Please enter a valid creator address.")
    st.stop()

# MAIN ANALYSIS BLOCK
if creator_address and analyze:
    limit = 50
    max_pages = 20
    all_tokens = []
    total_balance_usd = 0.0
    creator_rewards_sol = 0.0

    # Show creator address in a copyable format
    st.markdown("### 👤 Creator Address")
    st.code(creator_address, language='none')

    loading_placeholder = st.empty()
    loading_placeholder.markdown("⏳ Loading... Please wait.")

    success = True
    for page in range(max_pages):
        offset = page * limit
        url = (
            f"https://frontend-api-v3.pump.fun/coins/user-created-coins/"
            f"{creator_address}?offset={offset}&limit={limit}&includeNsfw=false"
        )
        try:
            resp = requests.get(url, timeout=10, headers=headers)
            resp.raise_for_status()
            coins = resp.json().get("coins", [])
        except Exception:
            success = False
            break

        if not coins:
            break
        all_tokens.extend(coins)
        # 💤 Sleep to avoid rate limiting
        time.sleep(0.5)  # sleep for 0.5 seconds between requests

    loading_placeholder.empty()

    if not success:
        st.error("❌ Error fetching tokens. Please check the address or try again later.")
        st.stop()

    if not all_tokens:
        st.warning("⚠️ No tokens found for this creator.")
        st.stop()

    # Wallet balance
    try:
        bal_url = (
            f"https://swap-api.pump.fun/v1/wallet/"
            f"{creator_address}/balances?includePnl=true&page=1&limit=10"
        )
        bal_resp = requests.get(bal_url, timeout=10, headers=headers)
        bal_resp.raise_for_status()
        total_balance_usd = float(bal_resp.json().get("totalBalanceUSD", 0) or 0)
    except Exception:
        st.warning("⚠️ Could not fetch wallet balance.")

    # Creator rewards
    try:
        reward_url = (
            f"https://swap-api.pump.fun/v1/creators/"
            f"{creator_address}/fees?interval=1h&limit=336"
        )
        reward_resp = requests.get(reward_url, timeout=10)
        reward_resp.raise_for_status()
        rewards = reward_resp.json()
        if rewards:
            creator_rewards_sol = float(rewards[-1].get("cumulativeCreatorFeeSOL", 0) or 0)
    except Exception:
        st.warning("⚠️ Could not fetch creator rewards.")

    # Data processing
    df = pd.DataFrame(all_tokens)
    df['created_timestamp'] = pd.to_datetime(df['created_timestamp'], unit='ms')
    df['king_of_the_hill_timestamp'] = pd.to_datetime(
        df['king_of_the_hill_timestamp'], unit='ms', errors='coerce'
    )
    df['migrated'] = df['king_of_the_hill_timestamp'].notna()
    df['migration_time_min'] = (
        (df['king_of_the_hill_timestamp'] - df['created_timestamp'])
        / pd.Timedelta(minutes=1)
    ).round(1)

    total = len(df)
    migrated = int(df['migrated'].sum())
    migration_pct = migrated / total * 100 if total else 0.0
    avg_migration = df.loc[df['migrated'], 'migration_time_min'].mean()
    avg_market_cap = df['usd_market_cap'].mean()
    max_market_cap = df['usd_market_cap'].max()

    # Metrics
    st.markdown("### 📊 Key Stats")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📦 Tokens Created", total)
    col1.metric("✅ Migrated", migrated)
    col2.metric("📈 Migration %", f"{migration_pct:.2f}%")
    col2.metric("⏱️ Avg Migration Time", f"{avg_migration:.1f} min" if not pd.isna(avg_migration) else "N/A")
    col3.metric("💰 Avg Market Cap", f"${avg_market_cap:,.0f}")
    col3.metric("🔝 Max Market Cap", f"${max_market_cap:,.0f}")
    col4.metric("💲 Wallet Balance", f"${total_balance_usd:,.2f}")
    col4.metric("💸 Creator Rewards", f"{creator_rewards_sol:.4f} SOL")

    st.markdown("---")

    # Pie chart
    st.subheader("Migration Distribution")
    fig1 = px.pie(
        names=["Migrated", "Not Migrated"],
        values=[migrated, total - migrated],
        color_discrete_sequence=["#00cc96", "#ffa15a"]
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Histogram
    st.subheader("Migration Time Histogram")
    fig2 = px.histogram(
        df[df['migrated']],
        x='migration_time_min',
        nbins=30,
        title="Migration Time (Minutes)",
        labels={"migration_time_min": "Minutes", "count": "Number of Tokens"}
    )
    fig2.update_layout(yaxis_title="Number of Tokens")
    fig2.update_traces(marker_line_color='black', marker_line_width=2)
    st.plotly_chart(fig2, use_container_width=True)

    # Bar chart
    st.subheader("Top 10 Tokens by Market Cap")
    top10 = df.nlargest(10, 'usd_market_cap')
    fig3 = px.bar(
        top10,
        x='symbol',
        y='usd_market_cap',
        text='name',
        color='usd_market_cap',
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig3, use_container_width=True)

    # Data Table
    st.subheader("Token Details")
    display_df = df[[
        'mint', 'name', 'symbol', 'usd_market_cap',
        'created_timestamp', 'king_of_the_hill_timestamp',
        'migrated', 'migration_time_min'
    ]].sort_values(by='created_timestamp', ascending=False)

    display_df['usd_market_cap'] = display_df['usd_market_cap'].map(lambda x: f"${x:,.0f}")
    st.dataframe(display_df, use_container_width=True)

st.caption("Built with ❤️ by [@Comm_Joseph](https://x.com/Comm_Joseph)")
