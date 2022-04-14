from matplotlib.pyplot import title
import streamlit as st
from predict import predictPage
from explore import explorePage

st.set_page_config(
    page_title="Software Developers Salary Prediciton",
    layout="wide"
)

page = st.sidebar.selectbox("Explore Or Predict", ("Predict", "Explore"))


if page == "Predict":
    predictPage()
else:
    explorePage()
