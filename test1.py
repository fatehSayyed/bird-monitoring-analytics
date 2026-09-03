import streamlit as st
import pandas as pd
import plotly.express as px


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Bird Species Analysis",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# DARK THEME + CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

        /* =========================
           MAIN APP BACKGROUND
           ========================= */

        .stApp {
            background-color: #0E1117;
            color: #FAFAFA;
        }

        .block-container {
            padding-top: 1rem;
            padding-bottom: 2rem;
        }


        /* =========================
           REMOVE STREAMLIT TOP STRIP
           ========================= */

        [data-testid="stHeader"] {
            background: transparent;
        }

        [data-testid="stToolbar"] {
            background: transparent;
        }


        /* =========================
           MAIN TITLE
           ========================= */

        .main-title {
            text-align: center;
            font-size: 2.3rem;
            font-weight: 700;
            color: #FFFFFF;
            margin: 0;
            padding: 10px 0 5px 0;
            line-height: 1.2;
            background: transparent;
        }


        /* =========================
           SUBTITLE
           ========================= */

        .dashboard-subtitle {
            text-align: center;
            font-size: 1rem;
            color: #B8C1CC;
            margin: 5px 0 10px 0;
            padding: 0;
            background: transparent;
        }


        /* =========================
           FULL WIDTH TITLE LINE
           ========================= */

        .title-line {
            border: none;
            height: 2px;
            background-color: #30363D;
            margin: 12px 0 25px 0;
            width: 100%;
        }


        /* =========================
           CHART TITLES
           ========================= */

        .chart-title {
            text-align: center;
            font-size: 1.2rem;
            font-weight: 600;
            color: #FFFFFF;
            margin-bottom: 10px;
            line-height: 1.3;
        }


        /* =========================
           CHART CARD
           ========================= */

        div[data-testid="stVerticalBlockBorderWrapper"] {
            border: 1px solid #30363D;
            border-radius: 12px;
            background-color: #161B22;
            padding: 10px;
            margin-bottom: 20px;
        }


        /* =========================
           SIDEBAR
           ========================= */

        section[data-testid="stSidebar"] {
            background-color: #121820;
        }

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            color: #FFFFFF;
        }


        /* =========================
           SIDEBAR METRICS
           ========================= */

        div[data-testid="stMetric"] {
            background-color: #161B22;
            border: 1px solid #30363D;
            border-radius: 10px;
            padding: 10px;
        }


        /* =========================
           DATAFRAME
           ========================= */

        div[data-testid="stDataFrame"] {
            border-radius: 10px;
        }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_csv("result_final.csv")


# =========================================================
# DATE CONVERSION
# =========================================================

df["date_x"] = pd.to_datetime(
    df["date_x"],
    errors="coerce"
)

# Remove rows with missing dates
df = df.dropna(
    subset=["date_x"]
).copy()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🔎 FILTERS")


# =========================================================
# DATE SLICER
# =========================================================

min_date = df["date_x"].min().date()
max_date = df["date_x"].max().date()

selected_dates = st.sidebar.date_input(
    "📅 Observation Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)


# =========================================================
# APPLY DATE FILTER
# =========================================================

if len(selected_dates) == 2:

    start_date, end_date = selected_dates

    filtered_df = df[
        (df["date_x"].dt.date >= start_date) &
        (df["date_x"].dt.date <= end_date)
    ].copy()

else:

    filtered_df = df.copy()


# =========================================================
# SPECIES FILTER
# =========================================================

species_list = sorted(
    filtered_df[
        "scientific_name"
    ]
    .dropna()
    .unique()
)

selected_species = st.sidebar.selectbox(
    "Select Species",
    ["All Species"] + species_list
)


# =========================================================
# APPLY SPECIES FILTER
# =========================================================

if selected_species != "All Species":

    filtered_df = filtered_df[
        filtered_df[
            "scientific_name"
        ] == selected_species
    ].copy()


# =========================================================
# SELECTED DATA SUMMARY
# =========================================================

st.sidebar.markdown("---")

st.sidebar.subheader(
    "📊 SELECTED DATA SUMMARY"
)


# Records
st.sidebar.metric(
    "Records",
    f"{len(filtered_df):,}"
)


# Species
st.sidebar.metric(
    "Species",
    filtered_df[
        "scientific_name"
    ].nunique()
)


# Male
male_count = (
    filtered_df[
        "sex"
    ] == "Male"
).sum()

st.sidebar.metric(
    "Male",
    f"{male_count:,}"
)


# Female
female_count = (
    filtered_df[
        "sex"
    ] == "Female"
).sum()

st.sidebar.metric(
    "Female",
    f"{female_count:,}"
)


# =========================================================
# MAIN TITLE
# =========================================================

st.markdown(
    """
    <div class="main-title">
         Species Diversity, Activity & Sex Ratio Analysis
    </div>

    <div class="dashboard-subtitle">
        Exploring bird species distribution, identification methods,
        observation intervals, and sex patterns
    </div>

    <hr class="title-line">
    """,
    unsafe_allow_html=True
)


# =========================================================
# ROW 1
# TOP 10 SPECIES + IDENTIFICATION METHOD
# =========================================================

col1, col2 = st.columns(2)


# ---------------------------------------------------------
# LEFT SIDE - TOP 10 SPECIES
# ---------------------------------------------------------

with col1:

    with st.container(border=True):

        st.markdown(
            """
            <div class="chart-title">
                Top 10 Most Observed Species
            </div>
            """,
            unsafe_allow_html=True
        )

        top_species = (
            filtered_df[
                "scientific_name"
            ]
            .value_counts()
            .head(10)
            .reset_index()
        )

        top_species.columns = [
            "scientific_name",
            "Observations"
        ]

        fig1 = px.bar(
            top_species,
            x="Observations",
            y="scientific_name",
            orientation="h",
            title="",
            labels={
                "Observations": "Number of Observations",
                "scientific_name": "Species"
            },
            template="plotly_dark"
        )

        fig1.update_layout(
            yaxis={
                "categoryorder": "total ascending"
            },
            height=450,
            margin=dict(
                l=10,
                r=10,
                t=10,
                b=20
            )
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )


# ---------------------------------------------------------
# RIGHT SIDE - IDENTIFICATION METHOD
# ---------------------------------------------------------

with col2:

    with st.container(border=True):

        st.markdown(
            """
            <div class="chart-title">
                Bird Identification Method
            </div>
            """,
            unsafe_allow_html=True
        )

        activity = (
            filtered_df[
                "id_method"
            ]
            .value_counts()
            .reset_index()
        )

        activity.columns = [
            "id_method",
            "Observations"
        ]

        fig2 = px.pie(
            activity,
            names="id_method",
            values="Observations",
            title="",
            hole=0.4,
            template="plotly_dark"
        )

        fig2.update_layout(
            height=450,
            margin=dict(
                l=10,
                r=10,
                t=10,
                b=20
            )
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )


# =========================================================
# ROW 2
# INTERVAL LENGTH + SEX DISTRIBUTION
# =========================================================

col3, col4 = st.columns(2)


# ---------------------------------------------------------
# LEFT SIDE - INTERVAL LENGTH
# ---------------------------------------------------------

with col3:

    with st.container(border=True):

        st.markdown(
            """
            <div class="chart-title">
                Observation Interval Length
            </div>
            """,
            unsafe_allow_html=True
        )

        interval = (
            filtered_df[
                "interval_length"
            ]
            .value_counts()
            .reset_index()
        )

        interval.columns = [
            "interval_length",
            "Observations"
        ]

        fig3 = px.bar(
            interval,
            x="interval_length",
            y="Observations",
            title="",
            labels={
                "interval_length": "Interval Length",
                "Observations": "Number of Observations"
            },
            template="plotly_dark"
        )

        fig3.update_layout(
            height=450,
            margin=dict(
                l=10,
                r=10,
                t=10,
                b=20
            )
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )


# ---------------------------------------------------------
# RIGHT SIDE - SEX DISTRIBUTION
# ---------------------------------------------------------

with col4:

    with st.container(border=True):

        st.markdown(
            """
            <div class="chart-title">
                Overall Sex Distribution
            </div>
            """,
            unsafe_allow_html=True
        )

        sex_distribution = (
            filtered_df[
                "sex"
            ]
            .value_counts()
            .reset_index()
        )

        sex_distribution.columns = [
            "sex",
            "Observations"
        ]

        fig4 = px.pie(
            sex_distribution,
            names="sex",
            values="Observations",
            title="",
            hole=0.5,
            template="plotly_dark"
        )

        fig4.update_layout(
            height=450,
            margin=dict(
                l=10,
                r=10,
                t=10,
                b=20
            )
        )

        st.plotly_chart(
            fig4,
            use_container_width=True
        )


# =========================================================
# ROW 3
# SPECIES-WISE SEX DISTRIBUTION + SEX RATIO
# =========================================================

col5, col6 = st.columns(2)


# ---------------------------------------------------------
# LEFT SIDE - MALE VS FEMALE BY SPECIES
# ---------------------------------------------------------

with col5:

    with st.container(border=True):

        st.markdown(
            """
            <div class="chart-title">
                Species-wise Sex Distribution
            </div>
            """,
            unsafe_allow_html=True
        )

        sex_species = filtered_df[
            filtered_df[
                "sex"
            ].isin(
                ["Male", "Female"]
            )
        ]

        species_sex = (
            sex_species
            .groupby(
                [
                    "scientific_name",
                    "sex"
                ]
            )
            .size()
            .reset_index(
                name="Observations"
            )
        )

        top_10_species = (
            species_sex
            .groupby(
                "scientific_name"
            )["Observations"]
            .sum()
            .nlargest(10)
            .index
        )

        species_sex_top10 = species_sex[
            species_sex[
                "scientific_name"
            ].isin(
                top_10_species
            )
        ]

        fig5 = px.bar(
            species_sex_top10,
            x="Observations",
            y="scientific_name",
            color="sex",
            barmode="group",
            orientation="h",
            title="",
            labels={
                "scientific_name": "Species",
                "Observations": "Number of Observations",
                "sex": "Sex"
            },
            template="plotly_dark"
        )

        fig5.update_layout(
            yaxis={
                "categoryorder": "total ascending"
            },
            height=500,
            margin=dict(
                l=10,
                r=10,
                t=10,
                b=20
            )
        )

        st.plotly_chart(
            fig5,
            use_container_width=True
        )


# ---------------------------------------------------------
# RIGHT SIDE - SPECIES-WISE SEX RATIO
# ---------------------------------------------------------

with col6:

   with st.container(border=True):

    st.markdown(
        """
        <div class="chart-title">
            Top 10 Species-wise Sex Ratio
        </div>
        """,
        unsafe_allow_html=True
    )

    sex_ratio = (
        sex_species
        .groupby(
            [
                "scientific_name",
                "sex"
            ]
        )
        .size()
        .unstack(
            fill_value=0
        )
    )

    if "Male" not in sex_ratio.columns:
        sex_ratio["Male"] = 0

    if "Female" not in sex_ratio.columns:
        sex_ratio["Female"] = 0

    sex_ratio["Male_to_Female_Ratio"] = (
        sex_ratio["Male"] /
        sex_ratio["Female"].replace(
            0,
            float("nan")
        )
    )

    sex_ratio["Total"] = (
        sex_ratio["Male"] +
        sex_ratio["Female"]
    )

    sex_ratio = (
        sex_ratio
        .sort_values(
            "Total",
            ascending=False
        )
        .head(10)
        .reset_index()
    )

    # Create numbering column from 1 to 10
    sex_ratio.insert(
        0,
        "No.",
        range(1, len(sex_ratio) + 1)
    )

    st.dataframe(
        sex_ratio[
            [
                "No.",
                "scientific_name",
                "Male",
                "Female",
                "Male_to_Female_Ratio"
            ]
        ],
        use_container_width=True,
        height=450,
        hide_index=True
    )

# =========================================================
# ROW 4
# SPECIES CONTRIBUTION + TOP SPECIES BY ID METHOD
# =========================================================

col7, col8 = st.columns(2)


# ---------------------------------------------------------
# LEFT SIDE - SPECIES CONTRIBUTION
# ---------------------------------------------------------

with col7:

    with st.container(border=True):

        st.markdown(
            """
            <div class="chart-title">
                Species Contribution to Total Observations
            </div>
            """,
            unsafe_allow_html=True
        )

        species_count = (
            filtered_df[
                "scientific_name"
            ]
            .value_counts()
            .reset_index()
        )

        species_count.columns = [
            "scientific_name",
            "Observations"
        ]

        top_5 = species_count.head(5).copy()

        other_count = (
            species_count
            .iloc[5:]["Observations"]
            .sum()
        )

        other_row = pd.DataFrame(
            {
                "scientific_name": [
                    "Other Species"
                ],
                "Observations": [
                    other_count
                ]
            }
        )

        species_share = pd.concat(
            [
                top_5,
                other_row
            ],
            ignore_index=True
        )

        fig7 = px.pie(
            species_share,
            names="scientific_name",
            values="Observations",
            title="",
            hole=0.45,
            template="plotly_dark"
        )

        fig7.update_layout(
            height=450,
            margin=dict(
                l=10,
                r=10,
                t=10,
                b=20
            )
        )

        st.plotly_chart(
            fig7,
            use_container_width=True
        )


# ---------------------------------------------------------
# RIGHT SIDE - TOP SPECIES BY ID METHOD
# ---------------------------------------------------------

with col8:

    with st.container(border=True):

        st.markdown(
            """
            <div class="chart-title">
                Top Species by Identification Method
            </div>
            """,
            unsafe_allow_html=True
        )

        top_5_species = (
            filtered_df[
                "scientific_name"
            ]
            .value_counts()
            .head(5)
            .index
        )

        species_activity = filtered_df[
            filtered_df[
                "scientific_name"
            ].isin(
                top_5_species
            )
        ]

        species_activity = (
            species_activity
            .groupby(
                [
                    "scientific_name",
                    "id_method"
                ]
            )
            .size()
            .reset_index(
                name="Observations"
            )
        )

        fig8 = px.bar(
            species_activity,
            x="scientific_name",
            y="Observations",
            color="id_method",
            barmode="stack",
            title="",
            labels={
                "scientific_name": "Species",
                "Observations": "Number of Observations",
                "id_method": "Identification Method"
            },
            template="plotly_dark"
        )

        fig8.update_layout(
            height=450,
            margin=dict(
                l=10,
                r=10,
                t=10,
                b=20
            )
        )

        st.plotly_chart(
            fig8,
            use_container_width=True
        )