import streamlit as st
import requests
import base64
import mimetypes
import hashlib
import uuid
import json
import os

# Define the Llama-3.2 API endpoints
llm_options = {
    "Llama-3.2-11b": {
        "invoke_url": "https://ai.api.nvidia.com/v1/gr/meta/llama-3.2-11b-vision-instruct/chat/completions",
        "model": "meta/llama-3.2-11b-vision-instruct"
    },
    "Llama-3.2-90b": {
        "invoke_url": "https://ai.api.nvidia.com/v1/gr/meta/llama-3.2-90b-vision-instruct/chat/completions",
        "model": "meta/llama-3.2-90b-vision-instruct"
    },
}

stream = False  # Set to True if you want to stream the response

# Initialize session states
if "uploaded_images" not in st.session_state:
    st.session_state["uploaded_images"] = {}
if "selected_image" not in st.session_state:
    st.session_state["selected_image"] = None

# Helper function to compute file hash
def compute_hash(file_data):
    return hashlib.md5(file_data).hexdigest()

# Tabs
st.title("Llama 3.2 Vision AMP")
tab1, tab2 = st.tabs(["Upload and Ask Questions", "Upload and View Images"])

# Tab 1: Upload and Ask Questions
with tab1:
    st.header("Upload an Image and Ask Questions")

    # LLM Selection
    selected_llm = st.selectbox("Select the LLM Model:", options=list(llm_options.keys()))
    invoke_url = llm_options[selected_llm]["invoke_url"]
    model = llm_options[selected_llm]["model"]

    # File Uploader
    uploaded_file = st.file_uploader("Upload an image (.png or .jpg)", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        # Read file data and compute hash
        file_data = uploaded_file.read()
        file_hash = compute_hash(file_data)

        # Check for duplicates
        if file_hash not in st.session_state["uploaded_images"]:
            unique_id = str(uuid.uuid4())
            mime_type = mimetypes.guess_type(uploaded_file.name)[0]
            image_data = {
                "id": unique_id,
                "name": uploaded_file.name,
                "mime_type": mime_type,
                "data": base64.b64encode(file_data).decode(),
            }
            st.session_state["uploaded_images"][file_hash] = image_data
            st.session_state["selected_image"] = image_data
            st.success("Image uploaded successfully!")
        else:
            st.warning("This image has already been uploaded.")

    # Display selected image
    if st.session_state["selected_image"]:
        st.image(
            f"data:{st.session_state['selected_image']['mime_type']};base64,{st.session_state['selected_image']['data']}",
            caption="Selected Image",
        )

    # Prompt for questions
    prompt = st.text_input("Ask a question about the image:")
    payload = None  # Ensure payload is always defined

    if prompt:
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": f'{prompt} <img src="data:{st.session_state["selected_image"]["mime_type"]};base64,{st.session_state["selected_image"]["data"]}" />',
                }
            ],
            "max_tokens": 1024,
            "temperature": 1.0,
            "top_p": 1.0,
            "stream": stream,
        }

    # API Request (only if payload is not None)
    if payload is not None:
        api_key = os.getenv("NVIDIA_APIKEY")

        if not api_key:
            raise ValueError("NVIDIA_APIKEY environment variable is not set!")

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json" if not stream else "text/event-stream",
            "Content-Type": "application/json",  # Ensure correct content type
        }

        with st.spinner("Processing your question..."):
            try:
                response = requests.post(invoke_url, headers=headers, json=payload)
                if response.status_code == 200:
                    result = response.json()
                    st.success("AI Response:")
                    st.json(result)
                else:
                    st.error(f"Error: {response.status_code}")
                    st.text(response.text)
            except Exception as e:
                st.error(f"Error during API request: {e}")

