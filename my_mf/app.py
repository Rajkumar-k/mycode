# ============================================================
# MUTUAL FUND WEEKLY NAV DASHBOARD
# ============================================================
#
# Install:
# pip install streamlit mftool pandas plotly
#
# ============================================================

import streamlit as st
from mftool import Mftool
import pandas as pd
import plotly.express as px


# ============================================================
# STREAMLIT PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Mutual Fund NAV Dashboard",
    layout="wide"
)


# ============================================================
# TAB LOOK & FEEL
# ============================================================

st.markdown(
    """
    <style>

    /* Main tab container */
    div[data-baseweb="tab-list"] {
        gap: 8px;
        background: #0F172A;
        padding: 6px;
        border-radius: 12px;
        border: 1px solid #334155;
        margin-bottom: 18px;
    }

    /* Individual tabs */
    button[data-baseweb="tab"] {
        height: 46px;
        border-radius: 9px;
        padding: 0 24px;
        font-size: 16px;
        font-weight: 700;
        color: #CBD5E1;
        background: transparent;
        border: 1px solid transparent;
    }

    /* Selected tab */
    button[data-baseweb="tab"][aria-selected="true"] {
        color: white;
        background: #0F766E;
        border: 1px solid #14B8A6;
        box-shadow: 0 3px 10px rgba(20, 184, 166, 0.20);
    }

    /* Tab hover */
    button[data-baseweb="tab"]:hover {
        color: white;
        background: #1E293B;
    }

    /* Remove Streamlit default underline */
    div[data-baseweb="tab-highlight"] {
        display: none;
    }

    /* Tab content spacing */
    div[data-baseweb="tab-panel"] {
        padding-top: 4px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    """
    <div style="
        background: linear-gradient(135deg, #0F172A, #1E293B);
        padding: 14px 20px;
        border-radius: 12px;
        border: 1px solid #475569;
        box-shadow: 0 4px 14px rgba(0,0,0,0.18);
        text-align: center;
        margin-bottom: 20px;
    ">
        <h2 style="
            color: white;
            margin: 0;
            font-size: 26px;
        ">
            📊 Mutual Fund Weekly NAV
        </h2>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# INITIALIZE MF TOOL
# ============================================================

mf = Mftool()


# ============================================================
# MUTUAL FUND SCHEME CODES
#
# fund_type = Dashboard tab
# type      = Fund category inside the tab
# code      = AMFI scheme code
# ============================================================

scheme_codes = {

    # --------------------------------------------------------
    # INDIA
    # --------------------------------------------------------

    "Motilal Oswal Midcap Fund Direct Growth": {
        "fund_type": "India",
        "code": "127042",
        "type": "Mid Cap"
    },

    "Canara Robeco Small Cap Fund Direct": {
        "fund_type": "India",
        "code": "146130",
        "type": "Small Cap"
    },

    "Bandhan Small Cap Fund": {
        "fund_type": "India",
        "code": "147946",
        "type": "Small Cap"
    },

    "Motilal Oswal Infra Fund": {
        "fund_type": "India",
        "code": "153484",
        "type": "Sectorial"
    },

    "Invesco Healthcare & Pharma Fund": {
        "fund_type": "India",
        "code": "154547",
        "type": "Sectorial"
    },

    # --------------------------------------------------------
    # GLOBAL
    # --------------------------------------------------------

    "ICICI Prudential NASDAQ 100 Index Fund": {
        "fund_type": "Global",
        "code": "149219",
        "type": "Equity"
    },

    # --------------------------------------------------------
    # FLEXI ANALYSIS
    # --------------------------------------------------------

    "HDFC Flexi Cap Fund": {
        "fund_type": "Flexi Analysis",
        "code": "118955",
        "type": "Flexi Cap"
    },

    "Bank of India Flexi Cap": {
        "fund_type": "Flexi Analysis",
        "code": "148404",
        "type": "Flexi Cap"
    }
}


# ============================================================
# TAB FUND MAPPING
# ============================================================

india_funds = [
    fund_name
    for fund_name, fund_info in scheme_codes.items()
    if fund_info["fund_type"] == "India"
]

global_funds = [
    fund_name
    for fund_name, fund_info in scheme_codes.items()
    if fund_info["fund_type"] == "Global"
]

flexi_funds = [
    fund_name
    for fund_name, fund_info in scheme_codes.items()
    if fund_info["fund_type"] == "Flexi Analysis"
]


# ============================================================
# DEFAULT MY AVG VALUES
# ============================================================

default_my_avg = {

    "Motilal Oswal Midcap Fund Direct Growth": 105,

    "Canara Robeco Small Cap Fund Direct": 43,

    "Nippon India Small Cap Fund": 206,

    "Bandhan Small Cap Fund": 54,

    "Nippon India ELSS Cap Fund": 138,

    "ICICI Prudential NASDAQ 100 Index Fund": 21.5,

    "HDFC Flexi Cap Fund": 100,

    "Bank of India Flexi Cap": 100
}


# ============================================================
# CREATE SESSION STATE FOR MY AVG
# ============================================================

if "my_avg_values" not in st.session_state:

    st.session_state.my_avg_values = {}

    for fund_name in scheme_codes:

        st.session_state.my_avg_values[fund_name] = (
            default_my_avg.get(
                fund_name,
                0.0
            )
        )


# ============================================================
# MY AVG REPORT SETTINGS
# ============================================================

st.markdown(
    """
    <div style="
        background-color: #1E293B;
        padding: 10px 15px;
        border-radius: 8px;
        border: 1px solid #475569;
        margin-top: 20px;
        margin-bottom: 10px;
    ">
        <h3 style="
            color: white;
            margin: 0;
        ">
            🎯 My Average Reference Values
        </h3>
    </div>
    """,
    unsafe_allow_html=True
)


st.caption(
    "Change the My Avg value for each fund. "
    "The selected value is used as the reference line "
    "in that fund's chart."
)


# ============================================================
# MY AVG INPUTS
# ============================================================

avg_cols = st.columns(3)

for i, fund_name in enumerate(scheme_codes):

    with avg_cols[i % 3]:

        current_value = (
            st.session_state.my_avg_values.get(
                fund_name,
                default_my_avg.get(
                    fund_name,
                    0.0
                )
            )
        )

        new_value = st.number_input(
            fund_name,
            min_value=0.0,
            value=float(current_value),
            step=1.0,
            format="%.2f",
            key=f"my_avg_{fund_name}"
        )

        st.session_state.my_avg_values[
            fund_name
        ] = new_value


# ============================================================
# DATE RANGE
# ============================================================

start_date = "01-01-2026"

end_date = pd.Timestamp.today().strftime(
    "%d-%m-%Y"
)


# ============================================================
# DOWNLOAD NAV HISTORY
# ============================================================

nav_data = {}


with st.spinner(
    "Downloading mutual fund NAV data..."
):

    for fund_name, fund_info in scheme_codes.items():

        scheme_code = fund_info["code"]
        fund_type = fund_info["type"]

        try:

            data = mf.get_scheme_historical_nav_for_dates(
                scheme_code,
                start_date,
                end_date
            )

            # ------------------------------------------------
            # Convert API response to DataFrame
            # ------------------------------------------------

            df = pd.DataFrame(
                data["data"]
            )


            # ------------------------------------------------
            # Check empty data
            # ------------------------------------------------

            if df.empty:

                st.warning(
                    f"No data found for {fund_name}"
                )

                continue


            # ------------------------------------------------
            # Convert NAV to numeric
            # ------------------------------------------------

            df["nav"] = pd.to_numeric(
                df["nav"],
                errors="coerce"
            )


            # ------------------------------------------------
            # Convert date
            # ------------------------------------------------

            df["date"] = pd.to_datetime(
                df["date"],
                format="%d-%m-%Y",
                errors="coerce"
            )


            # ------------------------------------------------
            # Remove invalid records
            # ------------------------------------------------

            df = df.dropna(
                subset=[
                    "date",
                    "nav"
                ]
            )


            # ------------------------------------------------
            # Sort
            # ------------------------------------------------

            df = df.sort_values(
                "date"
            )


            # ------------------------------------------------
            # Set date as index
            # ------------------------------------------------

            df = df.set_index(
                "date"
            )


            # ------------------------------------------------
            # Store NAV + Fund Type
            # ------------------------------------------------

            temp_df = pd.DataFrame({
                "NAV": df["nav"],
                "Fund Name": fund_name,
                "Fund Type": fund_type
            })


            nav_data[fund_name] = temp_df


        except Exception as e:

            st.error(
                f"Error downloading "
                f"{fund_name}: {e}"
            )


# ============================================================
# CHECK DATA
# ============================================================

if not nav_data:

    st.error(
        "No mutual fund NAV data available."
    )

    st.stop()


# ============================================================
# COMBINE ALL FUNDS
# ============================================================

nav_history = pd.concat(
    nav_data.values()
)


# ============================================================
# RESET INDEX
# ============================================================

nav_history = (
    nav_history
    .reset_index()
    .rename(
        columns={
            "index": "date"
        }
    )
)


# ============================================================
# REMOVE MISSING NAV
# ============================================================

nav_history = nav_history.dropna(
    subset=["NAV"]
)


# ============================================================
# SORT NAV HISTORY
# ============================================================

nav_history = (
    nav_history
    .sort_values(
        [
            "date",
            "Fund Type",
            "Fund Name"
        ]
    )
    .reset_index(
        drop=True
    )
)


# ============================================================
# ROUND DAILY NAV
# ============================================================

nav_history["NAV"] = (
    nav_history["NAV"]
    .round(4)
)


# ============================================================
# CREATE WEEKLY AVERAGE NAV
# ============================================================

weekly_nav = (
    nav_history
    .assign(
        week_date=(
            nav_history["date"]
            .dt.to_period("W")
            .dt.start_time
        )
    )
    .groupby(
        [
            "week_date",
            "Fund Type",
            "Fund Name"
        ],
        as_index=False
    )["NAV"]
    .mean()
    .rename(
        columns={
            "NAV": "avg_nav"
        }
    )
)


# ============================================================
# ROUND WEEKLY AVERAGE
# ============================================================

weekly_nav["avg_nav"] = (
    weekly_nav["avg_nav"]
    .round(2)
)


# ============================================================
# SORT WEEKLY DATA
# ============================================================

weekly_nav = (
    weekly_nav
    .sort_values(
        [
            "week_date",
            "Fund Type",
            "Fund Name"
        ]
    )
    .reset_index(
        drop=True
    )
)


# ============================================================
# WEEK RANK
#
# Latest week = 1
# Previous week = 2
# etc.
# ============================================================

unique_weeks = (
    weekly_nav["week_date"]
    .drop_duplicates()
    .sort_values(
        ascending=False
    )
    .reset_index(
        drop=True
    )
)


week_rank = pd.DataFrame(
    {
        "week_date": unique_weeks,
        "week_rank": range(
            1,
            len(unique_weeks) + 1
        )
    }
)


# ============================================================
# MERGE WEEK RANK
# ============================================================

weekly_nav = weekly_nav.merge(
    week_rank,
    on="week_date",
    how="left"
)


# ============================================================
# SORT LATEST WEEK FIRST
# ============================================================

weekly_nav = (
    weekly_nav
    .sort_values(
        [
            "week_rank",
            "Fund Type",
            "Fund Name"
        ]
    )
    .reset_index(
        drop=True
    )
)


# ============================================================
# LATEST NAV FOR EACH FUND
# ============================================================

latest_nav_df = (
    weekly_nav[
        weekly_nav["week_rank"] == 1
    ]
    [
        [
            "Fund Name",
            "avg_nav"
        ]
    ]
    .rename(
        columns={
            "avg_nav": "Latest NAV"
        }
    )
)


# ============================================================
# CREATE TABS
# ============================================================

tab_india, tab_global, tab_flexi, tab_weekly = st.tabs(
    [
        "🇮🇳 India",
        "🌎 Global",
        "📊 Flexi Analysis",
        "📅 Weekly Comparison"
    ]
)


# ============================================================
# FUNCTION FOR NORMAL FUND TABS
# ============================================================

def render_fund_tab(
    tab,
    fund_list,
    tab_key
):

    with tab:

        # ====================================================
        # FILTER BY FUND NAME
        # ====================================================

        tab_nav = weekly_nav[
            weekly_nav["Fund Name"].isin(
                fund_list
            )
        ].copy()


        if tab_nav.empty:

            st.info(
                "No mutual fund data available for this tab."
            )

            return


        # ====================================================
        # WEEK FILTER HEADER
        # ====================================================

        st.markdown(
            """
            <div style="
                background-color: #1E293B;
                padding: 10px 15px;
                border-radius: 8px;
                border: 1px solid #475569;
                margin-top: 20px;
                margin-bottom: 10px;
            ">
                <h3 style="
                    color: white;
                    margin: 0;
                ">
                    📅 Week Filter
                </h3>
            </div>
            """,
            unsafe_allow_html=True
        )


        # ====================================================
        # WEEK FILTER
        # ====================================================

        filter_options = [
            10,
            20,
            50,
            "ALL"
        ]


        selected_weeks = st.selectbox(
            "Show weeks",
            options=filter_options,
            index=1,
            format_func=lambda x: (
                "All Weeks"
                if x == "ALL"
                else f"Last {x} Weeks"
            ),
            key=f"show_weeks_{tab_key}"
        )


        # ====================================================
        # APPLY FILTER FOR CHARTS
        # ====================================================

        if selected_weeks == "ALL":

            filtered_nav = tab_nav.copy()

        else:

            filtered_nav = (
                tab_nav[
                    tab_nav["week_rank"]
                    <= selected_weeks
                ].copy()
            )


        # ====================================================
        # SORT FILTERED DATA
        # ====================================================

        filtered_nav = (
            filtered_nav
            .sort_values(
                [
                    "week_rank",
                    "Fund Type",
                    "Fund Name"
                ]
            )
            .reset_index(
                drop=True
            )
        )


        # ====================================================
        # FUND TYPES
        # ====================================================

        fund_types = (
            tab_nav["Fund Type"]
            .drop_duplicates()
            .tolist()
        )


        # ====================================================
        # TOP 5 MINIMUM NAV SECTION
        # ====================================================

        st.markdown(
            """
            <div style="
                background-color: #1E293B;
                padding: 10px 15px;
                border-radius: 8px;
                border: 1px solid #475569;
                margin-top: 25px;
                margin-bottom: 15px;
            ">
                <h3 style="
                    color: white;
                    margin: 0;
                    text-align: center;
                ">
                    🔻 Top 5 Minimum NAV
                </h3>
            </div>
            """,
            unsafe_allow_html=True
        )


        # ====================================================
        # CREATE SECTION FOR EACH FUND TYPE
        # ====================================================

        for fund_type in fund_types:

            # ------------------------------------------------
            # FUND TYPE HEADER
            # ------------------------------------------------

            st.markdown(
                f"""
                <div style="
                    background-color: #0F766E;
                    padding: 9px 15px;
                    border-radius: 7px;
                    margin-top: 15px;
                    margin-bottom: 10px;
                ">
                    <h3 style="
                        color: white;
                        margin: 0;
                        text-align: center;
                    ">
                        📂 {fund_type}
                    </h3>
                </div>
                """,
                unsafe_allow_html=True
            )


            # ------------------------------------------------
            # FUNDS IN THIS TYPE
            # ------------------------------------------------

            type_funds = (
                tab_nav[
                    tab_nav["Fund Type"]
                    == fund_type
                ]
                ["Fund Name"]
                .drop_duplicates()
                .tolist()
            )


            # ------------------------------------------------
            # TABLE COLUMNS
            # ------------------------------------------------

            table_cols = st.columns(
                len(type_funds)
            )


            # =================================================
            # CREATE TABLE FOR EACH FUND
            # =================================================

            for col, fund_name in zip(
                table_cols,
                type_funds
            ):

                with col:

                    # -----------------------------------------
                    # FUND NAME HEADER
                    # -----------------------------------------

                    st.markdown(
                        f"""
                        <div style="
                            background-color: #334155;
                            padding: 8px 10px;
                            border-radius: 6px;
                            margin-bottom: 8px;
                            text-align: center;
                        ">
                            <h4 style="
                                color: white;
                                margin: 0;
                                font-size: 15px;
                            ">
                                {fund_name}
                            </h4>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                    # =========================================
                    # FULL FUND DATA
                    # =========================================

                    fund_min_df = (
                        tab_nav[
                            tab_nav["Fund Name"]
                            == fund_name
                        ].copy()
                    )


                    # =========================================
                    # GET LATEST NAV
                    # =========================================

                    latest_nav = (
                        fund_min_df
                        .loc[
                            fund_min_df["week_rank"] == 1,
                            "avg_nav"
                        ]
                        .iloc[0]
                    )


                    # =========================================
                    # TOP 5 MINIMUM NAV
                    # =========================================

                    min_nav = (
                        fund_min_df
                        .nsmallest(
                            5,
                            "avg_nav"
                        )
                        [
                            [
                                "week_date",
                                "avg_nav"
                            ]
                        ]
                        .copy()
                    )


                    # =========================================
                    # LATEST NAV COLUMN
                    # =========================================

                    min_nav["Latest NAV"] = (
                        latest_nav
                    )


                    # =========================================
                    # % DIFFERENCE
                    # =========================================

                    min_nav["% Diff"] = (
                        (
                            (
                                latest_nav
                                - min_nav["avg_nav"]
                            )
                            / min_nav["avg_nav"]
                        )
                        * 100
                    )


                    # =========================================
                    # FORMAT DATE
                    # =========================================

                    min_nav["week_date"] = (
                        min_nav["week_date"]
                        .dt.strftime(
                            "%d-%b-%Y"
                        )
                    )


                    # =========================================
                    # RENAME
                    # =========================================

                    min_nav = (
                        min_nav
                        .rename(
                            columns={
                                "week_date": "Week",
                                "avg_nav": "NAV"
                            }
                        )
                    )


                    # =========================================
                    # COLUMN ORDER
                    # =========================================

                    min_nav = min_nav[
                        [
                            "Week",
                            "NAV",
                            "Latest NAV",
                            "% Diff"
                        ]
                    ]


                    # =========================================
                    # ROUND VALUES
                    # =========================================

                    min_nav["NAV"] = (
                        min_nav["NAV"]
                        .round(2)
                    )

                    min_nav["Latest NAV"] = (
                        min_nav["Latest NAV"]
                        .round(2)
                    )

                    min_nav["% Diff"] = (
                        min_nav["% Diff"]
                        .round(2)
                    )


                    # =========================================
                    # COLOR FUNCTION
                    # =========================================

                    def color_diff(value):

                        if value > 0:

                            return (
                                "color: green; "
                                "font-weight: bold;"
                            )

                        elif value < 0:

                            return (
                                "color: red; "
                                "font-weight: bold;"
                            )

                        else:

                            return (
                                "font-weight: bold;"
                            )


                    # =========================================
                    # STYLE TABLE
                    # =========================================

                    styled_table = (
                        min_nav.style
                        .map(
                            color_diff,
                            subset=[
                                "% Diff"
                            ]
                        )
                        .format(
                            {
                                "NAV": "{:.2f}",
                                "Latest NAV": "{:.2f}",
                                "% Diff": "{:+.2f}%"
                            }
                        )
                    )


                    # =========================================
                    # DISPLAY TABLE
                    # =========================================

                    st.dataframe(
                        styled_table,
                        use_container_width=True,
                        hide_index=True
                    )


        # ====================================================
        # WEEKLY NAV CHART SECTION
        # ====================================================

        st.markdown(
            """
            <div style="
                background-color: #1E293B;
                padding: 10px 15px;
                border-radius: 8px;
                border: 1px solid #475569;
                margin-top: 30px;
                margin-bottom: 15px;
            ">
                <h3 style="
                    color: white;
                    margin: 0;
                    text-align: center;
                ">
                    📈 Weekly NAV Charts
                </h3>
            </div>
            """,
            unsafe_allow_html=True
        )


        # ====================================================
        # CHARTS GROUPED BY FUND TYPE
        # ====================================================

        for fund_type in fund_types:

            # ------------------------------------------------
            # FUND TYPE HEADER
            # ------------------------------------------------

            st.markdown(
                f"""
                <div style="
                    background-color: #0F766E;
                    padding: 9px 15px;
                    border-radius: 7px;
                    margin-top: 20px;
                    margin-bottom: 10px;
                ">
                    <h3 style="
                        color: white;
                        margin: 0;
                        text-align: center;
                    ">
                        📂 {fund_type}
                    </h3>
                </div>
                """,
                unsafe_allow_html=True
            )


            # ------------------------------------------------
            # FUNDS IN THIS TYPE
            # ------------------------------------------------

            type_funds = (
                tab_nav[
                    tab_nav["Fund Type"]
                    == fund_type
                ]
                ["Fund Name"]
                .drop_duplicates()
                .tolist()
            )


            # =================================================
            # ONE CHART BELOW ANOTHER
            # =================================================

            for fund_name in type_funds:

                # =============================================
                # FILTER CHART DATA
                # =============================================

                fund_chart_df = (
                    filtered_nav[
                        filtered_nav["Fund Name"]
                        == fund_name
                    ]
                    .copy()
                )


                # =============================================
                # SORT OLDEST → LATEST
                # =============================================

                fund_chart_df = (
                    fund_chart_df
                    .sort_values(
                        "week_date"
                    )
                )


                # =============================================
                # FUND NAME HEADER
                # =============================================

                st.markdown(
                    f"""
                    <div style="
                        background-color: #334155;
                        padding: 8px 15px;
                        border-radius: 6px;
                        margin-top: 15px;
                        margin-bottom: 5px;
                    ">
                        <h4 style="
                            color: white;
                            margin: 0;
                            font-size: 17px;
                        ">
                            {fund_name}
                        </h4>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


                # =============================================
                # GET MY AVG
                # =============================================

                my_avg = (
                    st.session_state.my_avg_values.get(
                        fund_name,
                        default_my_avg.get(
                            fund_name,
                            0.0
                        )
                    )
                )


                # =============================================
                # PLOTLY LINE CHART
                # =============================================

                fig = px.line(
                    fund_chart_df,
                    x="week_date",
                    y="avg_nav",
                    markers=True
                )


                # =============================================
                # NAV VALUE ON EVERY POINT
                # =============================================

                fig.update_traces(

                    text=(
                        fund_chart_df[
                            "avg_nav"
                        ]
                        .round(2)
                    ),

                    textposition="top center",

                    mode=(
                        "lines+markers+text"
                    ),

                    hovertemplate=(
                        "<b>Week:</b> "
                        "%{x|%d-%b-%Y}"
                        "<br>"
                        "<b>Rank:</b> "
                        "%{customdata}"
                        "<br>"
                        "<b>Average NAV:</b> "
                        "%{y:.2f}"
                        "<br>"
                        f"<b>My Avg:</b> {my_avg:.2f}"
                        "<extra></extra>"
                    ),

                    customdata=(
                        fund_chart_df[
                            "week_rank"
                        ]
                    )
                )


                # =============================================
                # MY AVG REFERENCE LINE
                # =============================================

                fig.add_hline(

                    y=my_avg,

                    line_dash="dash",

                    annotation_text=(
                        f"My Avg: {my_avg:.2f}"
                    ),

                    annotation_position="top left"
                )


                # =============================================
                # CHART LAYOUT
                # =============================================

                fig.update_layout(

                    xaxis_title="Week",

                    yaxis_title="Average NAV",

                    height=400,

                    margin=dict(
                        l=20,
                        r=20,
                        t=40,
                        b=20
                    ),

                    showlegend=False
                )


                # =============================================
                # DISPLAY CHART
                # =============================================

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    key=f"chart_{tab_key}_{fund_name}"
                )


                # =============================================
                # SEPARATOR
                # =============================================

                st.markdown(
                    """
                    <hr style="
                        border: 0;
                        border-top: 1px solid #475569;
                        margin-top: 25px;
                        margin-bottom: 25px;
                    ">
                    """,
                    unsafe_allow_html=True
                )


# ============================================================
# RENDER INDIA TAB
# ============================================================

render_fund_tab(
    tab_india,
    india_funds,
    "india"
)


# ============================================================
# RENDER GLOBAL TAB
# ============================================================

render_fund_tab(
    tab_global,
    global_funds,
    "global"
)


# ============================================================
# RENDER FLEXI ANALYSIS TAB
# ============================================================

render_fund_tab(
    tab_flexi,
    flexi_funds,
    "flexi"
)


# ============================================================
# WEEKLY COMPARISON TAB
# ============================================================

with tab_weekly:

    # ========================================================
    # HEADER
    # ========================================================

    st.markdown(
        """
        <div style="
            background-color: #1E293B;
            padding: 10px 15px;
            border-radius: 8px;
            border: 1px solid #475569;
            margin-top: 20px;
            margin-bottom: 15px;
        ">
            <h3 style="
                color: white;
                margin: 0;
                text-align: center;
            ">
                📅 Weekly Comparison
            </h3>
        </div>
        """,
        unsafe_allow_html=True
    )


    st.caption(
        "W1 = latest week. "
        "Positive values mean the latest NAV is higher "
        "than the comparison NAV."
    )


    # ========================================================
    # COMPARISON WEEKS
    # ========================================================

    comparison_weeks = [
        3,
        5,
        7,
        10,
        12,
        15,
        20,
        25,
        30
    ]


    # ========================================================
    # CREATE COMPARISON DATA
    # ========================================================

    comparison_rows = []


    for fund_name in scheme_codes:

        # ----------------------------------------------------
        # GET FUND DATA
        # ----------------------------------------------------

        fund_data = (
            weekly_nav[
                weekly_nav["Fund Name"]
                == fund_name
            ]
            .copy()
        )


        # ----------------------------------------------------
        # GET W1
        # ----------------------------------------------------

        w1_data = fund_data[
            fund_data["week_rank"] == 1
        ]


        if w1_data.empty:

            continue


        w1_nav = float(
            w1_data[
                "avg_nav"
            ].iloc[0]
        )


        # ----------------------------------------------------
        # GET MY AVG
        # ----------------------------------------------------

        my_avg = float(
            st.session_state.my_avg_values.get(
                fund_name,
                default_my_avg.get(
                    fund_name,
                    0.0
                )
            )
        )


        # ----------------------------------------------------
        # START ROW
        # ----------------------------------------------------

        row = {
            "Fund Name": fund_name
        }


        # ====================================================
        # W1 VS MY AVG
        # ====================================================

        if my_avg != 0:

            row["W1 vs My Avg"] = (
                (
                    w1_nav
                    - my_avg
                )
                / my_avg
                * 100
            )

        else:

            row["W1 vs My Avg"] = None


        # ====================================================
        # W1 VS HISTORICAL WEEKS
        # ====================================================

        for week in comparison_weeks:

            column_name = (
                f"W1 vs W{week}"
            )


            historical_data = fund_data[
                fund_data["week_rank"] == week
            ]


            # ------------------------------------------------
            # If week does not exist
            # ------------------------------------------------

            if historical_data.empty:

                row[column_name] = None

                continue


            historical_nav = float(
                historical_data[
                    "avg_nav"
                ].iloc[0]
            )


            # ------------------------------------------------
            # Avoid division by zero
            # ------------------------------------------------

            if historical_nav == 0:

                row[column_name] = None

            else:

                row[column_name] = (
                    (
                        w1_nav
                        - historical_nav
                    )
                    / historical_nav
                    * 100
                )


        comparison_rows.append(
            row
        )


    # ========================================================
    # CREATE DATAFRAME
    # ========================================================

    comparison_df = pd.DataFrame(
        comparison_rows
    )


    # ========================================================
    # COLUMN ORDER
    # ========================================================

    comparison_columns = [
        "Fund Name",
        "W1 vs My Avg",
        "W1 vs W3",
        "W1 vs W5",
        "W1 vs W7",
        "W1 vs W10",
        "W1 vs W12",
        "W1 vs W15",
        "W1 vs W20",
        "W1 vs W25",
        "W1 vs W30"
    ]


    comparison_df = comparison_df[
        comparison_columns
    ]


    # ========================================================
    # ROUND VALUES
    # ========================================================

    percentage_columns = (
        comparison_columns[1:]
    )


    for column in percentage_columns:

        comparison_df[column] = (
            comparison_df[column]
            .round(2)
        )


    # ========================================================
    # COLOR FUNCTION
    # ========================================================

    def comparison_color(value):

        if pd.isna(value):

            return ""

        if value > 0:

            return (
                "color: green; "
                "font-weight: bold;"
            )

        elif value < 0:

            return (
                "color: red; "
                "font-weight: bold;"
            )

        else:

            return (
                "font-weight: bold;"
            )


    # ========================================================
    # STYLE COMPARISON TABLE
    # ========================================================

    styled_comparison = (
        comparison_df.style
        .map(
            comparison_color,
            subset=percentage_columns
        )
        .format(
            {
                column: "{:+.2f}%"
                for column in percentage_columns
            }
        )
    )


    # ========================================================
    # DISPLAY TABLE
    # ========================================================

    st.dataframe(
        styled_comparison,
        use_container_width=True,
        hide_index=True,
        height=500
    )
