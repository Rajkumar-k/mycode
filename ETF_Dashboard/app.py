import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="ETF Dashboard", layout="wide")  # ✅ Must be first

st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    h1, h2, h3 {
        color: #00D4AA;
        font-family: 'Segoe UI', sans-serif;
        text-align: center;
    }
    [data-testid="stMetric"] {
        background-color: #1C2333;
        border: 1px solid #2E3B55;
        padding: 12px;
        border-radius: 12px;
        text-align: center;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        min-height: 140px;
        height: 140px;
        width: 100%;
        box-sizing: border-box;
    }
    /* custom KPI box for HTML-rendered metrics */
    .kpi-box {
        background-color: #1C2333;
        border: 1px solid #2E3B55;
        padding: 12px;
        border-radius: 12px;
        text-align: center;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        min-height: 140px;
        height: 140px;
        width: 100%;
        box-sizing: border-box;
    }
    .kpi-label { color: #A0AEC0; font-size: 14px; font-weight: 600; }
    .kpi-value { color: #FFFFFF; font-size: 28px; font-weight: bold; }
    .kpi-delta { font-size: 14px; font-weight: 600; }
    [data-testid="stMetricLabel"] {
        color: #A0AEC0;
        font-size: 14px;
        font-weight: 600;
    }
    [data-testid="stMetricValue"] {
        color: #FFFFFF;
        font-size: 28px;
        font-weight: bold;
    }
    .stDataFrame {
        border-radius: 12px;
    }
    /* make dataframe/table headers dark and readable */
    .stDataFrame table thead th,
    .stDataFrame thead th,
    table.dataframe thead th,
    .dataframe thead th {
        background-color: #0B1220 !important;
        color: #E6F7F0 !important;
        font-weight: 700;
        border-bottom: 1px solid #2E3B55 !important;
    }
</style>
""", unsafe_allow_html=True)

stocks = ["MON100.NS", "MASPTOP50.NS", "MAFANG.NS"]
my_avg = [259, 81, 208]


df = yf.download(stocks, period="60d", progress=False)
close_df = df["Close"].round(2)

# ✅ Latest and previous values from the full close_df (needs at least 2 rows)
latest = close_df.iloc[-1]
prev = close_df.iloc[-2]

mafang,    mafang_prev    = latest["MAFANG.NS"],   prev["MAFANG.NS"]
masptop50, masptop50_prev = latest["MASPTOP50.NS"], prev["MASPTOP50.NS"]
mon100,    mon100_prev    = latest["MON100.NS"],    prev["MON100.NS"]


curr_row = close_df.iloc[-1]
prev_row = close_df.iloc[-2]

# Create YearWeek
close_df['YearWeek'] = (
    close_df.index.isocalendar().year.astype(str)
    + '-'
    + close_df.index.isocalendar().week.astype(str).str.zfill(2)
)

latest_week = close_df['YearWeek'].max()

previous_week = close_df.loc[
    close_df['YearWeek'] < latest_week,
    'YearWeek'
].max()

# Previous week data
prev_week_df = close_df[close_df['YearWeek'] == previous_week]

# Average of previous week
prev_week_avg = prev_week_df[stocks].mean()

result = pd.DataFrame({
    'Ticker': stocks,
    'My Avg': my_avg,
    'Curr Value': [curr_row[s] for s in stocks],
    'Prev Value': [prev_row[s] for s in stocks],
    'Prev Week Avg': [prev_week_avg[s] for s in stocks]
})

result['Avg %'] = ((result['Curr Value'] - result['My Avg'])
                   / result['My Avg'] * 100).round(2)

result['Day %'] = ((result['Curr Value'] - result['Prev Value'])
                   / result['Prev Value'] * 100).round(2)

result['Week %'] = ((result['Curr Value'] - result['Prev Week Avg'])
                    / result['Prev Week Avg'] * 100).round(2)


# Chart 3: 52-week high/low

high_52w = close_df.max()
low_52w = close_df.min()

result3 = pd.DataFrame({
    "Ticker": stocks,
    'My Avg': my_avg,
    "52W High": [high_52w[s] for s in stocks],
    "52W Low": [low_52w[s] for s in stocks]
})

#Chart4 : Weekly average close vs my average

# Group by YearWeek and compute mean close for each ticker
weekly_group_avg = (
    close_df
    .groupby('YearWeek')[stocks]
    .mean()
    .reset_index()
)

# Optionally rename columns to indicate these are weekly averages
weekly_group_avg = weekly_group_avg.rename(columns={
    stocks[0]: f"{stocks[0]}",
    stocks[1]: f"{stocks[1]}",
    stocks[2]: f"{stocks[2]}",
})

print('\nWeekly grouped averages (last 10 rows):')
print(close_df)


weekly_group_avg['MON100_MyAvg'] = my_avg[0]
weekly_group_avg['MASPTOP50_MyAvg'] = my_avg[1]
weekly_group_avg['MAFANG_MyAvg'] = my_avg[2]

weekly_group_avg['MON100_%'] = (
    (weekly_group_avg['MON100.NS'] - weekly_group_avg['MON100_MyAvg'])
    / weekly_group_avg['MON100_MyAvg'] * 100
).round(2)

weekly_group_avg['MASPTOP50_%'] = (
    (weekly_group_avg['MASPTOP50.NS'] - weekly_group_avg['MASPTOP50_MyAvg'])
    / weekly_group_avg['MASPTOP50_MyAvg'] * 100
).round(2)

weekly_group_avg['MAFANG_%'] = (
    (weekly_group_avg['MAFANG.NS'] - weekly_group_avg['MAFANG_MyAvg'])
    / weekly_group_avg['MAFANG_MyAvg'] * 100
).round(2)

weekly_group_avg = weekly_group_avg[[ 'YearWeek', 'MON100.NS','MON100_MyAvg', 'MON100_%','MASPTOP50.NS', 'MASPTOP50_MyAvg','MASPTOP50_%','MAFANG.NS',   'MAFANG_MyAvg',  'MAFANG_%']]
weekly_group_avg = weekly_group_avg.tail(10).reset_index(drop=True)  # show only last 10 weeks for brevity


st.title("ETF Dashboard")

# Single-column layout: show key metrics across the page, then the table below
st.header("Key Metrics")
# four KPI boxes: three price metrics + latest available date
km1, km2, km3, km4 = st.columns(4)

# helper to render KPI HTML with colored delta
def kpi_html(label, value, delta):
    # delta is a float (could be negative)
    color = '#22c55e' if delta >= 0 else '#ef4444'  # green for positive, red for negative
    delta_text = f"₹{delta:,.2f}"
    return f"""
    <div class='kpi-box'>
      <div class='kpi-label'>{label}</div>
      <div class='kpi-value'>₹{value:,.2f}</div>
      <div class='kpi-delta' style='color:{color};'>{delta_text}</div>
    </div>
    """

# Latest available data date
latest_date = close_df.index.max()
try:
    latest_date_str = pd.to_datetime(latest_date).strftime("%Y-%m-%d")
except Exception:
    latest_date_str = str(latest_date)

with km1:
    st.markdown(kpi_html('MON100 ETF', mon100, mon100 - mon100_prev), unsafe_allow_html=True)
with km2:
    st.markdown(kpi_html('MASPTOP50 ETF', masptop50, masptop50 - masptop50_prev), unsafe_allow_html=True)
with km3:
    st.markdown(kpi_html('MAFANG ETF', mafang, mafang - mafang_prev), unsafe_allow_html=True)
with km4:
    # render latest date as a simple KPI without delta
    st.markdown(f"""
    <div class='kpi-box'>
      <div class='kpi-label'>Latest Available Data</div>
      <div class='kpi-value'>{latest_date_str}</div>
    </div>
    """, unsafe_allow_html=True)



st.subheader("Analysis - Buying Opportunity")

# highlight negative numeric cells green for easier scanning
def highlight_minus(val):
    try:
        if pd.isna(val):
            return ""
        v = float(val)
    except Exception:
        return ""
    if v < 0:
        return 'background-color: #22c55e; color: white;'
    return ""

numeric_cols = result.select_dtypes(include=["number"]).columns.tolist()

# Build a Plotly Table so it can occupy the full container width/height reliably
try:
    header_vals = [f"<b>{c}</b>" for c in result.columns.tolist()]
    cell_values = []
    cell_fill_colors = []
    cell_font_colors = []

    for c in result.columns.tolist():
        col_vals = result[c].tolist()
        if c in numeric_cols:
            formatted = [f"{v:,.2f}" if pd.notna(v) else "" for v in col_vals]
            colors = [('#22c55e' if (pd.notna(v) and float(v) < 0) else '#071019') for v in col_vals]
            fcolors = [('#ffffff' if (pd.notna(v) and float(v) < 0) else '#E6F7F0') for v in col_vals]
        else:
            formatted = [str(v) for v in col_vals]
            colors = ['#071019'] * len(col_vals)
            fcolors = ['#E6F7F0'] * len(col_vals)

        cell_values.append(formatted)
        cell_fill_colors.append(colors)
        cell_font_colors.append(fcolors)

    fig_table = go.Figure(data=[go.Table(
        header=dict(values=header_vals,
                    fill_color='#0B1220',
                    align='left',
                    font=dict(color='#E6F7F0', size=14)),
        cells=dict(values=cell_values,
                   fill_color=cell_fill_colors,
                   align='left',
                   font=dict(color=cell_font_colors, size=13)))
    ])

    # adjust height to fit rows: header + row_height * rows (capped)
    row_count = result.shape[0]
    header_h = 36
    row_h = 30
    max_h = 900
    calc_h = header_h + row_h * row_count + 24
    fig_table.update_layout(
        margin=dict(t=8, b=8, l=8, r=8),
        height=min(calc_h, max_h),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_table, use_container_width=True)
except Exception:
    # Fallback: simple full-width dataframe without styling
    st.dataframe(result, use_container_width=True, height=420)


# --- Stacked layout: show charts/tables vertically
st.subheader("52-Week High / Low")
try:
    m = result3.melt(id_vars='Ticker', value_vars=['52W High', '52W Low','My Avg'],
                     var_name='Measure', value_name='Price')
    # vertical grouped bar chart (Ticker on x-axis, Price on y-axis)
    fig = px.bar(
        m,
        x='Ticker',
        y='Price',
        color='Measure',
        barmode='group',
        text='Price',
        title='52-Week High vs Low by Ticker',
        labels={'Price': 'Price (₹)'}
    )
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside', textfont=dict(size=10), marker_line_width=0.6)
    fig.update_layout(
        showlegend=True,
        legend=dict(title='Measure', orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        margin=dict(t=30, b=12),
        xaxis=dict(tickangle=-45),
        height=380,
        bargap=0.26,
        bargroupgap=0.08
    )
    st.plotly_chart(fig, use_container_width=True)
except Exception as e:
    st.write("Could not render 52-week chart:", e)

st.subheader("Weekly grouped averages")
try:
    wg = weekly_group_avg.tail(10).reset_index(drop=True)

    header_vals = [f"<b>{c}</b>" for c in wg.columns.tolist()]
    cell_values = []
    cell_fill_colors = []
    cell_font_colors = []

    for c in wg.columns.tolist():
        col_vals = wg[c].tolist()
        if pd.api.types.is_numeric_dtype(wg[c]):
            # format numeric values to 2 decimals (with thousands separator)
            formatted = [f"{v:,.2f}" if pd.notna(v) else "" for v in col_vals]
            # use uniform background and font colors (no conditional coloring)
            colors = ['#071019'] * len(col_vals)
            fcolors = ['#E6F7F0'] * len(col_vals)
        else:
            formatted = [str(v) for v in col_vals]
            colors = ['#071019'] * len(col_vals)
            fcolors = ['#E6F7F0'] * len(col_vals)

        cell_values.append(formatted)
        cell_fill_colors.append(colors)
        cell_font_colors.append(fcolors)

    fig_wg = go.Figure(data=[go.Table(
        header=dict(values=header_vals,
                    fill_color='#0B1220',
                    align='left',
                    font=dict(color='#E6F7F0', size=14)),
        cells=dict(values=cell_values,
                   fill_color=cell_fill_colors,
                   align='left',
                   font=dict(color=cell_font_colors, size=14)))
    ])

    # dynamic height for weekly table
    row_count_w = wg.shape[0]
    header_h_w = 36
    row_h_w = 30
    max_h_w = 900
    calc_h_w = header_h_w + row_h_w * row_count_w + 24
    fig_wg.update_layout(
        margin=dict(t=8, b=8, l=8, r=8),
        height=min(calc_h_w, max_h_w),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_wg, use_container_width=True)
except Exception:
    st.write(weekly_group_avg.tail(20))
