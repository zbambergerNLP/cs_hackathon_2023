import streamlit as st
from PIL import Image



# Set page title
logo = Image.open('circles.png')
col1, col2, col3 = st.columns(3)
with col2:
    st.image(logo,use_column_width=True)


# Add a title to the page

# Add a text input field to the subsection
diagnose = st.text_area("Give a brief description of your diagnostics")
symptoms = st.text_area("Provide a description of your symptoms")
treatments = st.text_area("Please describe the treatments you have received")

col1, col2, col3 , col4, col5, col6, col7, col8, col9 = st.columns(9)
with col5:
    center_button = st.button('Submmit')

