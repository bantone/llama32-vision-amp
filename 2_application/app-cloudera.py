import streamlit as st
import requests
import base64
import mimetypes
import hashlib
import uuid
import json
import os

# NVIDIA Environment Variables
NVIDIA_APIKEY = os.getenv("NVIDIA_APIKEY")
CDP_TOKEN = os.getenv("CDP_TOKEN")

# Define the Llama-3.2 API endpoints
llm_options = {
    "Llama-3.2-11b-vision-4xa10g": {
        "invoke_url": "https://caii-prod-long-running.eng-ml-l.vnu8-sqze.cloudera.site/namespaces/serving-default/endpoints/llama-32-11b-vision-4xa10g/v1/chat/completions",
        "model": "meta/llama-3.2-11b-vision-instruct"
    },
#    "Llama-3.2-90b": {
#        "invoke_url": "https://ai.api.nvidia.com/v1/gr/meta/llama-3.2-90b-vision-instruct/chat/completions",
#        "model": "meta/llama-3.2-90b-vision-instruct"
#    },
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
tab1, tab2 = st.tabs(["Upload and Ask Questions", "Uploaded Images"])

# Tab 1: Upload and Ask Questions
with tab1:
    st.header("Upload Images and Ask Questions")

    # LLM Selection
    selected_llm = st.selectbox("Select the LLM Model:", options=list(llm_options.keys()))
    invoke_url = llm_options[selected_llm]["invoke_url"]
    model = llm_options[selected_llm]["model"]

    # File Uploader
    uploaded_files = st.file_uploader("Upload images (.png or .jpg)", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_data = uploaded_file.read()
            file_hash = compute_hash(file_data)

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
                st.success(f"Uploaded {uploaded_file.name} successfully!")

    # Allow selection of one image at a time
    selected_image = st.selectbox(
        "Select an image to analyze:",
        options=list(st.session_state["uploaded_images"].keys()),
        format_func=lambda x: st.session_state["uploaded_images"][x]["name"],
    )

    if selected_image:
        st.session_state["selected_image"] = st.session_state["uploaded_images"][selected_image]
        img = st.session_state["selected_image"]
        st.image(f"data:{img['mime_type']};base64,{img['data']}", caption=img['name'])

    # Prompt for questions
    prompt = st.text_input("Ask a question about the selected image:")
    payload = None

    if prompt and st.session_state["selected_image"]:
        img = st.session_state["selected_image"]
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": f'{prompt} <img src="data:{img["mime_type"]};base64,{img["data"]}" />'}
            ],
            "max_tokens": 1024,
            "temperature": 1.0,
            "top_p": 1.0,
            "stream": stream,
        }

    if payload is not None:
        headers = {
#            "Authorization": f"Bearer {NVIDIA_APIKEY}",
            "Authorization": f"Bearer {CDP_TOKEN}",
            "Accept": "application/json" if not stream else "text/event-stream",
            "Content-Type": "application/json",
        }

        with st.spinner("Processing your question..."):
            try:
                response = requests.post(invoke_url, headers=headers, json=payload)
                if response.status_code == 200:
                    result = response.json()
                    content_text = result.get("choices", [{}])[0].get("message", {}).get("content", "No response received.")
                    st.success("AI Response:")
                    st.write(content_text)
                else:
                    st.error(f"Error: {response.status_code}")
                    st.text(response.text)
            except Exception as e:
                st.error(f"Error during API request: {e}")

# Tab 2: Upload and View Images
with tab2:
    st.header("Previously Uploaded Images")

    if st.session_state["uploaded_images"]:
        for img_hash, img_data in st.session_state["uploaded_images"].items():
            st.image(
                f"data:{img_data['mime_type']};base64,{img_data['data']}",
                caption=img_data['name'],
            )
    else:
        st.info("No images uploaded yet.")

