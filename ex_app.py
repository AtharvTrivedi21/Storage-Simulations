import streamlit as st
import requests

# Base URL of the FastAPI backend
API_URL = "http://127.0.0.1:8000"

# Function to get the current directory from the API
def get_directory():
    response = requests.get(f"{API_URL}/directory")
    return response.json()

# Function to insert a value via the API
def insert_value(value):
    response = requests.post(f"{API_URL}/insert", json={"value": value})
    return response.json()

# Function to delete a value via the API
def delete_value(value):
    response = requests.post(f"{API_URL}/delete", json={"value": value})
    return response.json()

# Function to clear the storage on the server
def clear_storage():
    # Clear stored values in the FastAPI backend (add a clear endpoint in FastAPI)
    response = requests.post(f"{API_URL}/clear")
    return response.json()

# Main page showing global depth first, then the current directory
st.title("Extendible Hashing Simulation with FastAPI")

# Fetch and display the current directory
directory_data = get_directory()

# Displaying Global Depth
st.write(f"### Global Depth: {directory_data['global_depth']}")

# Displaying Current Directory in vertical boxes
st.write("### Current Directory (Buckets)")
directory = directory_data["directory"]

# Displaying each bucket's values and local depth
for bucket, values in directory.items():
    local_depth = len(values)  # Local depth as the count of elements in the bucket
    bucket_html = f"""
        <div style='border: 2px solid #4CAF50; padding: 10px; margin: 10px; border-radius: 10px;'>
            <div style='font-size:20px; font-weight: bold;'>Bucket {bucket}</div>
            <div>Local Depth: {local_depth}</div>
            <div style='font-size:18px; margin-top: 10px;'>Values: {', '.join(map(str, values)) if values else 'None'}</div>
        </div>
    """
    st.markdown(bucket_html, unsafe_allow_html=True)

# Sidebar for Insert and Delete operations
st.sidebar.header("Insert/Delete Values")

# Insert Value
insert_value_input = st.sidebar.text_input("Insert a value:")
if st.sidebar.button("Insert"):
    if insert_value_input.isdigit():
        result = insert_value(int(insert_value_input))  # Convert input to integer
        st.sidebar.success(result['message'])
        st.experimental_rerun()  # Refresh the display
    else:
        st.sidebar.error("Please enter a valid integer.")

# Delete Value
delete_value_input = st.sidebar.text_input("Delete a value:")
if st.sidebar.button("Delete"):
    if delete_value_input.isdigit():
        result = delete_value(int(delete_value_input))  # Convert input to integer
        st.sidebar.success(result['message'])
        st.experimental_rerun()  # Refresh the display
    else:
        st.sidebar.error("Please enter a valid integer.")

# Clear Storage Button
if st.sidebar.button("Clear All"):
    result = clear_storage()
    st.sidebar.success(result['message'])
    st.experimental_rerun()  # Refresh the display

