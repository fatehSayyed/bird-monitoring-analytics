import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
# reading the data from excel file
df = pd.read_csv("result_final.csv")
st.set_page_config(layout="wide")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
image = Image.open('bird.png')

col1, col2 = st.columns([0.1, 0.9])
with col1:
    st.image(image, width=200)

html_title = """
<style>
.title-test {
    font-weight: bold;
    padding: 5px;
    border-radius: 6px;
}
</style>
"""
html_title = """
<style>
.title-test {
    font-weight: bold;
    padding: 5px;
    border-radius: 6px;
}
</style>

<center>
    <h1 class="title-test">Bird Species Diversity & Population Characteristics </h1>
</center>
"""
# Top 10 most observed species
top_species = (
    df["scientific_name"]
    .value_counts()
    .head(10)
    .reset_index()
)

# Rename columns
top_species.columns = ["scientific_name", "Observations"]

# Create chart
fig = px.bar(
    top_species,
    x="Observations",
    y="scientific_name",
    orientation="h",
    title="Top 10 Most Observed Species",
    labels={
        "Observations": "Number of Observations",
        "scientific_name": "Species"
    }
)

fig.update_layout(
    yaxis={"categoryorder": "total ascending"}
)

st.plotly_chart(fig, use_container_width=True)
col1, col2 = st.columns(2)

# LEFT SIDE
with col1:
    st.subheader("Bird Identification Method")

    activity = (
        df["id_method"]
        .value_counts()
        .reset_index()
    )

    activity.columns = ["id_method", "Observations"]

    fig1 = px.bar(
        activity,
        x="id_method",
        y="Observations",
        title="Identification Method Distribution",
        labels={
            "ID_Method": "Identification Method",
            "Observations": "Number of Observations"
        }
    )

    st.plotly_chart(fig1, use_container_width=True)


# RIGHT SIDE
with col2:
    st.subheader("Observation Interval Length")

    interval = (
        df["interval_length"]
        .value_counts()
        .reset_index()
    )

    interval.columns = ["interval_length", "Observations"]

    fig2 = px.bar(
        interval,
        x="interval_length",
        y="Observations",
        title="Observations by Interval Length",
        labels={
            "Interval_Length": "Interval Length",
            "Observations": "Number of Observations"
        }
    )

    st.plotly_chart(fig2, use_container_width=True)
    col3, col4 = st.columns(2)

# =========================================
# ROW 2 - Sex Distribution + ID Method
# =========================================

col3, col4 = st.columns(2)


# =========================================
# LEFT SIDE - SEX DISTRIBUTION
# =========================================

with col3:

    st.subheader("Overall Sex Distribution of Observed Birds")

    sex_distribution = (
        df["sex"]
        .value_counts()
        .reset_index()
    )

    sex_distribution.columns = ["sex", "Observations"]

    fig4 = px.pie(
        sex_distribution,
        names="sex",
        values="Observations",
        title="Overall Sex Distribution",
        hole=0.5
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )


# =========================================
# RIGHT SIDE - ID METHOD
# =========================================

with col4:

    st.subheader("Bird Identification Method Distribution")

    id_method_count = (
        df["id_method"]
        .value_counts()
        .reset_index()
    )

    id_method_count.columns = ["id_method", "Observations"]

    fig6 = px.pie(
        id_method_count,
        names="id_method",
        values="Observations",
        title="Identification Method Distribution",
        hole=0.4
    )

    st.plotly_chart(
        fig6,
        use_container_width=True
    )
    # ---------------------------------------
# 5. Species-wise Sex Ratio
# ---------------------------------------

col5, col6 = st.columns(2)

# LEFT SIDE
with col5:

    st.subheader("Species-wise Sex Distribution")

    # Keep only Male and Female
    sex_species = df[
        df["sex"].isin(["Male", "Female"])
    ]

    # Count Male/Female for each species
    species_sex = (
        sex_species
        .groupby(["scientific_name", "sex"])
        .size()
        .reset_index(name="Observations")
    )

    # Find top 10 species based on total Male + Female observations
    top_10_species = (
        species_sex
        .groupby("scientific_name")["Observations"]
        .sum()
        .nlargest(10)
        .index
    )

    species_sex_top10 = species_sex[
        species_sex["scientific_name"].isin(top_10_species)
    ]

    # Create grouped horizontal bar chart
    fig5 = px.bar(
        species_sex_top10,
        x="Observations",
        y="scientific_name",
        color="sex",
        barmode="group",
        orientation="h",
        title="Male vs Female by Species",
        labels={
            "Scientific_Name": "Species",
            "Observations": "Number of Observations",
            "Sex": "Sex"
        }
    )

    fig5.update_layout(
        yaxis={"categoryorder": "total ascending"}
    )

    st.plotly_chart(fig5, use_container_width=True)


# RIGHT SIDE
with col6:

    st.subheader("Species-wise Sex Ratio")

    # Calculate Male/Female counts
    sex_ratio = (
        sex_species
        .groupby(["scientific_name", "sex"])
        .size()
        .unstack(fill_value=0)
    )

    # Make sure both columns exist
    if "Male" not in sex_ratio.columns:
        sex_ratio["Male"] = 0

    if "Female" not in sex_ratio.columns:
        sex_ratio["Female"] = 0

    # Calculate ratio
    sex_ratio["Male_to_Female_Ratio"] = (
        sex_ratio["Male"] /
        sex_ratio["Female"].replace(0, float("nan"))
    )

    # Top 10 species
    sex_ratio = (
        sex_ratio
        .sort_values("Male_to_Female_Ratio", ascending=False)
        .head(10)
        .reset_index()
    )

    st.dataframe(
        sex_ratio[
            [
                "scientific_name",
                "Male",
                "Female",
                "Male_to_Female_Ratio"
            ]
        ],
        use_container_width=True
    )