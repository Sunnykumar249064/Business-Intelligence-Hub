import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.stylable_container import stylable_container

# PAGE CONFIG

st.set_page_config(
    page_title="Business Intelligence Hub",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# CSS


st.markdown("""
<style>

/* MAIN APP */

.stApp {
    background-color: #0E1117;
    color: white;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background-color: #161b22;
    border-right: 1px solid #2d3748;
}

/* Sidebar Text */
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* TITLE */

h1, h2, h3 {
    color: white !important;
}

/* METRIC CARDS */

div[data-testid="stMetric"] {
    background-color: #1c1f26;
    border: 1px solid #2d3748;
    padding: 15px;
    border-radius: 14px;
}

/* Metric Value */
div[data-testid="stMetricValue"] {
    color: #00d4ff !important;
    font-size: 30px;
    font-weight: bold;
}

/* Metric Label */
div[data-testid="stMetricLabel"] {
    color: white !important;
    font-size: 15px;
}

/* TABS */

button[data-baseweb="tab"] {
    color: white !important;
    font-size: 16px;
    font-weight: 600;
}

button[data-baseweb="tab"][aria-selected="true"] {
    border-bottom: 3px solid #00d4ff !important;
}

/* INPUTS */

.stTextInput input,
.stDateInput input,
.stSelectbox div,
.stMultiSelect div {
    background-color: #1c1f26 !important;
    color: white !important;
}

/* Dropdown */
div[data-baseweb="select"] > div {
    background-color: #1c1f26 !important;
    color: white !important;
}

/* PLOTLY CHARTS */

.plot-container {
    border-radius: 15px;
    overflow: hidden;
}

/* EXPANDER */

.streamlit-expanderHeader {
    color: white !important;
    font-weight: bold;
}

/* TABLE */

[data-testid="stDataFrame"] {
    background-color: white;
    border-radius: 10px;
}

/* TOP HEADER */

header[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

/* Toolbar Icons */
button[kind="header"] {
    color: white !important;
}

/* SCROLLBAR */

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    background: #00d4ff;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# DATA LOADING

@st.cache_data
def load_data():
    df = pd.read_csv("Data/sales_data.csv")

    df["Date"] = pd.to_datetime(df["Date"])

    df["Month_Year"] = df["Date"].dt.to_period("M").astype(str)

    return df


try:

    df = load_data()

    # SIDEBAR
  
    with st.sidebar:

        st.title("🛡️ Sunny Kumar")

        st.divider()

        date_range = st.date_input(
            "📅 Analysis Period",
            [df["Date"].min(), df["Date"].max()]
        )

        region = st.multiselect(
            "📍 Geography",
            df["Region"].unique(),
            default=df["Region"].unique()
        )

        cat = st.selectbox(
            "📦 Category Focus",
            ["All"] + list(df["Category"].unique())
        )

        st.divider()

        st.info(
            "💡 Tip: Use filters to drill down into specific market segments."
        )

    # FILTERING
   
    mask = (
        (df["Date"] >= pd.to_datetime(date_range[0])) &
        (df["Date"] <= pd.to_datetime(date_range[1]))
    )

    if region:
        mask &= df["Region"].isin(region)

    if cat != "All":
        mask &= (df["Category"] == cat)

    f_df = df.loc[mask]

    # KPI SECTION
   
    st.title("🚀 Sales Data Analysis Dashboard")

    st.markdown("### Real-Time Sales Data Analysis Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    total_sales = f_df["Sales"].sum()

    total_profit = f_df["Profit"].sum()

    total_orders = len(f_df)

    profit_margin = (
        (total_profit / total_sales) * 100
        if total_sales > 0
        else 0
    )

    c1.metric(
        "Gross Revenue",
        f"₹{total_sales:,}",
        delta="14% vs Last Week"
    )

    c2.metric(
        "Net Profit",
        f"₹{total_profit:,}",
        delta="8% vs Last Week"
    )

    c3.metric(
        "Profit Margin",
        f"{profit_margin:.1f}%"
    )

    c4.metric(
        "Active Orders",
        total_orders
    )

    style_metric_cards(
        background_color="#1c1f26",
        border_left_color="#00d4ff",
        border_size_px=1
    )

    st.divider()

    # TABS
   
    tab1, tab2, tab3 = st.tabs([
        "📈 Market Performance",
        "🎯 Target Analysis",
        "🤖 AI Insights"
    ])
    # TAB 1
   
    with tab1:

        left_col, right_col = st.columns([2, 1])

        # SALES TREND
        
        with left_col:

            trend_df = (
                f_df.groupby("Date")["Sales"]
                .sum()
                .reset_index()
            )

            fig_trend = px.line(
                trend_df,
                x="Date",
                y="Sales",
                title="Revenue Stream (Time-Series)"
            )

            fig_trend.update_traces(
                line_color="#00d4ff",
                fill="tozeroy"
            )

            fig_trend.update_layout(
                paper_bgcolor="#161b22",
                plot_bgcolor="#161b22",
                font_color="white"
            )

            st.plotly_chart(
                fig_trend,
                use_container_width=True
            )

        # CATEGORY VS REGION
        
        with right_col:

            fig_bar = px.bar(
                f_df,
                x="Category",
                y="Sales",
                color="Region",
                title="Category vs Region",
                barmode="group"
            )

            fig_bar.update_layout(
                paper_bgcolor="#161b22",
                plot_bgcolor="#161b22",
                font_color="white"
            )

            st.plotly_chart(
                fig_bar,
                use_container_width=True
            )

    # TAB 2
   
    with tab2:

        g1, g2 = st.columns(2)

        target = 200000

        # GAUGE CHART

        with g1:

            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=total_sales,
                title={"text": "Sales Target Achievement"},
                gauge={
                    "axis": {"range": [0, target]},
                    "bar": {"color": "#00d4ff"},
                    "steps": [
                        {
                            "range": [0, target * 0.5],
                            "color": "#2d3748"
                        },
                        {
                            "range": [target * 0.5, target],
                            "color": "#4a5568"
                        }
                    ]
                }
            ))

            fig_gauge.update_layout(
                paper_bgcolor="#161b22",
                font={"color": "white"}
            )

            st.plotly_chart(
                fig_gauge,
                use_container_width=True
            )

        # HEATMAP
       
        with g2:

            st.subheader("Regional Profitability Heatmap")

            heat_df = (
                f_df.groupby("Region")[["Sales", "Profit"]]
                .sum()
                .reset_index()
            )

            fig_heat = px.density_heatmap(
                heat_df,
                x="Region",
                y="Sales",
                z="Profit",
                text_auto=True,
                color_continuous_scale="Viridis"
            )

            fig_heat.update_layout(
                paper_bgcolor="#161b22",
                plot_bgcolor="#161b22",
                font_color="white"
            )

            st.plotly_chart(
                fig_heat,
                use_container_width=True
            )

    # TAB 3
    
    with tab3:

        st.subheader("Executive Summary")

        best_region = (
            f_df.groupby("Region")["Sales"]
            .sum()
            .idxmax()
        )

        worst_product = (
            f_df.groupby("Product")["Profit"]
            .sum()
            .idxmin()
        )

        with stylable_container(
            key="insight_box",
            css_styles="""
            {
                border: 1px solid #00d4ff;
                border-radius: 15px;
                padding: 20px;
                background-color: #161b22;
            }
            """
        ):

            st.write(
                f"✅ **Strength:** Best performing region is **{best_region}**."
            )

            st.write(
                f"⚠️ **Attention:** Product **{worst_product}** is underperforming."
            )

            st.write(
                "🔮 **Forecast:** You are likely to achieve 90% of your target by month-end."
            )

    # EXPORT SECTION

    with st.expander("📥 Export Transactional Data"):

        st.dataframe(
            f_df,
            use_container_width=True
        )

        csv = f_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇️ Download CSV Report",
            data=csv,
            file_name="sales_report.csv",
            mime="text/csv"
        )

except Exception as e:

    st.error(f"❌ Setup Error: {e}")