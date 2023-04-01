from reviews_with_evidence import fact_checker
import streamlit as st
from PIL import Image
import pandas as pd


st.set_page_config(page_title="Circles", layout="wide")

# Set page title
logo = Image.open('circles.png')
col1, col2, col3 = st.columns(3)
with col2:
    st.image(logo,use_column_width=True)

   
query = st.sidebar.text_area("Describe your condition")
num_results = st.sidebar.number_input("Number of Results", 1, 2000, 2)
ignore_unreliable_results = st.sidebar.checkbox("Show only reliable results")
search = st.sidebar.button('Search')




if search:
    res = fact_checker(query)
    df = pd.DataFrame.from_dict({'Experiences': [r["review"] for r in res], "Treatments": [t["prompts"] for t in res],  "links": [l["links"] for l in res]})

    st.dataframe(df,use_container_width=True)
    st.header("Diabetes Circle")
    photo_bar = Image.open('photo_bar.jpeg')
    st.image(photo_bar,use_column_width=True)
    
    treatments = Image.open('treatments.png')
    st.image(treatments,width=700)