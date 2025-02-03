import streamlit as st
import requests

# Set the API base URL (assumes the FastAPI server is running on localhost:8000)
API_URL = "http://localhost:8000"

st.title("Bitmap Index Management")

# Insert Value
st.header("Insert Value")
value_to_insert = st.number_input("Enter a value to insert:", min_value=0)  # Allowing 0 and positive integers
if st.button("Insert"):
    response = requests.post(f"{API_URL}/insert", json={"value": value_to_insert})
    st.success(response.json()["message"])

# Delete Value
st.header("Delete Value")
value_to_delete = st.number_input("Enter a value to delete:", min_value=0)
if st.button("Delete"):
    response = requests.post(f"{API_URL}/delete", json={"value": value_to_delete})
    if response.status_code == 200:
        st.success(response.json()["message"])
    else:
        st.error(response.json()["detail"])

# Search Value
st.header("Search Value")
value_to_search = st.number_input("Enter a value to search:", min_value=0)
if st.button("Search"):
    response = requests.post(f"{API_URL}/search", json={"value": value_to_search})
    if response.status_code == 200:
        indices = response.json()["indices"]
        if indices:
            st.success(f"Value found at indexes: {indices}")
        else:
            st.warning("Value found but no indexes are available.")
    else:
        st.error(response.json()["detail"])

# Display Index
if st.button("Display Index"):
    response = requests.get(f"{API_URL}/display")
    if response.status_code == 200:
        result = response.json()
        if isinstance(result, list):  # If the response is a list of attributes
            for line in result:
                st.write(line)  # Display each line of formatted result
        else:
            st.warning(result["message"])  # Display message if the index is empty
    else:
        st.error(response.json()["detail"])
