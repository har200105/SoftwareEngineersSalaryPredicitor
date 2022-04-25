import streamlit as st
import pickle
import numpy as np
from forex_python.converter import CurrencyRates, CurrencyCodes


def load_model():
    with open("saved_steps.pkl", "rb") as f:
        data = pickle.load(f)
    return data


data = load_model()

regressor = data["model"]
lbl_enc_country = data["lbl_enc_country"]
lbl_enc_education = data["lbl_enc_education"]
lbl_enc_language = data["lbl_enc_language"]


def show_predict_page():
    st.title("Developer's Salary Prediction")

    st.write(""" We require some details to predict the salary""")

    COUNTRIES = (
        "United States",
        "India",
        "United Kingdom",
        "Germany",
        "Canada",
        "Brazil",
        "France",
        "Spain",
        "Australia",
        "Netherlands",
        "Poland",
        "Italy",
        "Russian Federation",
        "Sweden",
        "Other",
    )

    EDUCATION = (
        "Bachelor’s degree",
        "Master’s degree",
        "Post grad",
    )

    LANGUAGES = (
        "JavaScript",
        "HTML/CSS",
        "Go",
        "Python",
        "C#",
        "Bash/Shell/PowerShell",
        "C++",
        "C",
        "Dart",
        "Java",
        "Rust",
        "Assembly",
        "R",
        "Haskell",
        "Julia",
        "TypeScript",
        "Kotlin",
        "Swift",
        "PHP",
        "Scala",
        "SQL",
        "Objective-C",
        "VBA",
        "Ruby",
        "Perl",
    )

    country = st.selectbox("Country", COUNTRIES)
    education = st.selectbox("Education Level", EDUCATION)
    language = st.selectbox("Programming Language/Tech Stack", LANGUAGES)

    experience = st.slider("Years of Experience", 0, 50, 3)

    m = st.markdown(
        """
        <style>
        div.stButton > button:first-child {
            background-color: purple;
            color:white;
            font-family: "Lucida Grande", sans-serif;
            font-size:20px;
            height:3em;
            width:10em;
            border-radius:10px 10px 10px 10px;
        }
        </style>""",
        unsafe_allow_html=True,
    )

    ok = st.button("Predict Salary")

    if ok:
        X = np.array([[country, education, experience, language]])
        X[:, 0] = lbl_enc_country.transform(X[:, 0])
        X[:, 1] = lbl_enc_education.transform(X[:, 1])
        X[:, 3] = lbl_enc_language.transform(X[:, 3])
        X = X.astype(float)

        salary = regressor.predict(X)

        currency = {
            "USD",
            "INR",
            "GBP",
            "EUR",
            "CAD",
            "BRL",
            "AUD",
            "PLN",
            "RUB",
            "SEK",
        }

        def currency_switch(cnt_with_curr):
            switch = {
                "United States": "USD",
                "India": "INR",
                "United Kingdom": "GBP",
                "Germany": "EUR",
                "Canada": "CAD",
                "Brazil": "BRL",
                "France": "EUR",
                "Spain": "EUR",
                "Australia": "AUD",
                "Netherlands": "EUR",
                "Poland": "PLN",
                "Italy": "EUR",
                "Russian Federation": "RUB",
                "Sweden": "SEK",
            }

            return switch.get(cnt_with_curr, "USD")

        country_with_currency = currency_switch(country)

        currency_value = CurrencyRates()
        converted_salary = currency_value.convert(
            "USD", country_with_currency, salary[0]
        )

        currency_symbol = CurrencyCodes()
        curr_symbol = currency_symbol.get_symbol(country_with_currency)

        st.subheader(
            f"The estimated salary is {curr_symbol}{converted_salary:.2f} per year.")
