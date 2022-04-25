import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = "Other"
    return categorical_map


def clean_experience(x):
    if x == "More than 50 years":
        return 50
    if x == "Less than 1 year":
        return 0.5
    return float(x)


def clean_education(x):
    if "Bachelor’s degree" in x:
        return "Bachelor’s degree"
    if "Master’s degree" in x:
        return "Master’s degree"
    if "Professional degree" or "Other doctoral degree":
        return "Post grad"
    return "Less than a Bachelors"


def clean_languages(df):

    arr = list(df["LanguageDesireNextYear"])

    lst = [x.split(";")[0] for x in arr]
    df["LanguageDesireNextYear"] = lst

    return df


@st.cache
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    df = df[
        [
            "Country",
            "EdLevel",
            "YearsCodePro",
            "Employment",
            "LanguageDesireNextYear",
            "ConvertedComp",
        ]
    ]
    df = df[df["ConvertedComp"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed full-time"]
    df = df.drop("Employment", axis=1)

    country_map = shorten_categories(df.Country.value_counts(), 400)
    df["Country"] = df["Country"].map(country_map)
    df = df[df["ConvertedComp"] <= 250000]

    df["YearsCodePro"] = df["YearsCodePro"].apply(clean_experience)
    df["EdLevel"] = df["EdLevel"].apply(clean_education)
    df = clean_languages(df)
    df = df.rename({"ConvertedComp": "Salary"}, axis=1)
    return df


df = load_data()


def show_explore_page():
    st.title("Explore Software Engineer Salaries")

    st.write(
        """
     Stack Overflow Developer Survey 2020
    """
    )

    data = df["Country"].value_counts()

    fig1, ax1 = plt.subplots()
    inner_circle = plt.Circle((0, 0), 0.7, color="white")

    plt.rcParams["axes.labelsize"] = 20
    sns.set(font_scale=0.5)
    plt.rcParams["text.color"] = "black"
    plt.rcParams["font.size"] = 5

    color_pallete = [
        "#a50026",
        "#d73027",
        "#f46d43",
        "#fdae61",
        "#fee090",
        "#ffffbf",
        "#e0f3f8",
        "#abd9e9",
        "#74add1",
        "#4575b4",
        "#313695",
    ]
    ax1.pie(
        data,
        labels=data.index,
        colors=color_pallete,
        wedgeprops={"linewidth": 5, "edgecolor": "white"},
        autopct="%1.1f%%",
        startangle=90,
    )

    p = plt.gcf()
    p.gca().add_artist(inner_circle)
    ax1.axis("equal")

    st.write("""#### Number of Data from different countries""")
    st.pyplot(fig1)

    st.write(
        """
        #### Mean Salary Based On Country
        """
    )

    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)

    st.bar_chart(data)

    st.write(
        """
        #### Mean Salary Based On Experience
        """
    )

    data = df.groupby(["YearsCodePro"])[
        "Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)

    st.write(
        """
        #### Mean Salary Based On Language
        """
    )

    data = (
        df.groupby(["LanguageDesireNextYear"])["Salary"]
        .mean()
        .sort_values(ascending=True)
    )
    st.line_chart(data)
