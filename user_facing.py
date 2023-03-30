import streamlit as st

# Set page title
st.set_page_config(page_title="My Streamlit Page")

# Add a title to the page
st.title("Welcome to my Streamlit page!")

# Add some text to the page
st.write("This is a basic page built using the Streamlit API.")

# Add a header to a section
st.header("Section 1")

# Add some text to the section
st.write("This is the first section of the page.")

# Add a subheader to the section
st.subheader("Subsection 1.1")

# Add a text input field to the subsection
user_input = st.text_input("Enter some text")

# Display the input on the page
st.write("You entered:", user_input)

# Add a header to another section
st.header("Section 2")

# Add some text to the section
st.write("This is the second section of the page.")

# Add a subheader to the section
st.subheader("Subsection 2.1")

# Add a slider to the subsection
slider_value = st.slider("Select a value", 0, 100)

# Display the slider value on the page
st.write("You selected:", slider_value)
