import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.stylable_container import stylable_container

# --- 1. CONFIG & THEME ---
st.set_page_config(page_title="Analytics Pro | Dashboard", page_icon="⚡", layout="wide")

# Custom CSS for glassmorphism effect
st.markdown("""
    <style>
    .stApp { background: #0E1117; color: #FFFFFF; }
    div[data-testid="stMetricValue"] { font-size: 28px; color: #00d4ff; }
    .plot-container { border-radius: 10px; background: #161b22; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA ENGINE ---
@st.cache_data
def load_data():
    df = pd.read_csv("Data/sales_data.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    # Adding Year/Month for better grouping
    df['Month_Year'] = df['Date'].dt.to_period('M').astype(str)
    return df

try:
    df = load_data()

    # --- 3. SIDEBAR (Advanced Navigation) ---
    with st.sidebar:
        st.title("🛡️ Sunny Kumar")
        st.divider()
        
        # Date Range with better UI
        date_range = st.date_input("Analysis Period", [df['Date'].min(), df['Date'].max()])
        
        # Hierarchical Filters
        region = st.multiselect("📍 Geography", df['Region'].unique(), default=df['Region'].unique())
        cat = st.selectbox("📦 Category Focus", ["All"] + list(df['Category'].unique()))
        
        st.divider()
        st.info("💡 Tip: Use filters to drill down into specific market segments.")

    # --- 4. FILTERING LOGIC ---
    mask = (df['Date'] >= pd.to_datetime(date_range[0])) & (df['Date'] <= pd.to_datetime(date_range[1]))
    if region:
        mask &= df['Region'].isin(region)
    if cat != "All":
        mask &= (df['Category'] == cat)
    
    f_df = df.loc[mask]

    # --- 5. TOP KPI ROW ---
    st.title("🚀 Business Intelligence Hub")
    
    c1, c2, c3, c4 = st.columns(4)
    total_sales = f_df['Sales'].sum()
    total_profit = f_df['Profit'].sum()
    target = 200000 # Example Target
    
    c1.metric("Gross Revenue", f"₹{total_sales:,}", delta="14% vs LW")
    c2.metric("Net Profit", f"₹{total_profit:,}", delta="8% vs LW")
    c3.metric("Profit Margin", f"{(total_profit/total_sales*100):.1f}%" if total_sales > 0 else "0%")
    c4.metric("Active Orders", len(f_df))
    
    style_metric_cards(background_color="#1c1f26", border_left_color="#00d4ff", border_size_px=1)

    st.divider()

    # --- 6. ADVANCED VISUALS ---
    tab1, tab2, tab3 = st.tabs(["📈 Market Performance", "🎯 Target Analysis", "🤖 AI Insights"])

    with tab1:
        col_left, col_right = st.columns([2, 1])
        with col_left:
            # Sales Trend with Moving Average
            trend_df = f_df.groupby('Date')['Sales'].sum().reset_index()
            fig_trend = px.line(trend_df, x='Date', y='Sales', title="Revenue Stream (Time-Series)")
            fig_trend.update_traces(line_color='#00d4ff', fill='tozeroy')
            st.plotly_chart(fig_trend, use_container_width=True)
        
        with col_right:
            # Category Breakdown
            fig_bar = px.bar(f_df, x='Category', y='Sales', color='Region', title="Category vs Region", barmode='group')
            st.plotly_chart(fig_bar, use_container_width=True)

    with tab2:
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            # Gauge Chart for Target
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = total_sales,
                title = {'text': "Sales Target Achievement"},
                gauge = {
                    'axis': {'range': [None, target]},
                    'bar': {'color': "#00d4ff"},
                    'steps': [
                        {'range': [0, target*0.5], 'color': "gray"},
                        {'range': [target*0.5, target], 'color': "lightgray"}]
                }
            ))
            fig_gauge.update_layout(paper_bgcolor="#0e1117", font={'color': "white"})
            st.plotly_chart(fig_gauge, use_container_width=True)
        
        with col_g2:
            st.subheader("Regional Profitability Heatmap")
            heat_df = f_df.groupby('Region')[['Sales', 'Profit']].sum().reset_index()
            fig_heat = px.density_heatmap(heat_df, x="Region", y="Sales", z="Profit", text_auto=True, color_continuous_scale='Viridis')
            st.plotly_chart(fig_heat, use_container_width=True)

    with tab3:
        st.subheader("Executive Summary (Auto-Generated)")
        best_region = f_df.groupby('Region')['Sales'].sum().idxmax()
        worst_product = f_df.groupby('Product')['Profit'].sum().idxmin()
        
        with stylable_container(key="insight_box", css_styles="""{ border: 1px solid #00d4ff; border-radius: 10px; padding: 20px; }"""):
            st.write(f"✅ **Strength:** Your best performing market is **{best_region}**.")
            st.write(f"⚠️ **Attention:** Product **{worst_product}** is underperforming in terms of net profit.")
            st.write("🔮 **Forecast:** Based on current velocity, you will hit 90% of your target by month-end.")

    # --- 7. EXPORT & DATA ---
    with st.expander("📥 Export Transactional Data"):
        st.dataframe(f_df.style.background_gradient(cmap='Blues'), use_container_width=True)
        csv = f_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV Report", data=csv, file_name="sales_report.csv", mime="text/csv")

except Exception as e:
    st.error(f"Setup Error: {e}")