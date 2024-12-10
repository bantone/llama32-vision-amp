import streamlit as st
import requests
import base64
import mimetypes
import json

# Define the Llama-3.2 API endpoints
llm_options = {
    "Llama-3.2-11b": {
        "invoke_url": "https://ai.api.nvidia.com/v1/gr/meta/llama-3.2-11b-vision-instruct/chat/completions",
        "model": "meta/llama-3.2-11b-vision-instruct"
    }
    "Llama-3.2-90b": {
        "invoke_url": "https://ai.api.nvidia.com/v1/gr/meta/llama-3.2-90b-vision-instruct/chat/completions",
        "model": "meta/llama-3.2-90b-vision-instruct"
    },
}

stream = False  # Set to True if you want to stream the response

# Streamlit UI
st.title("Llama 3.2 Vision AMP")
st.write("Upload an image and ask questions!")

# Initialize session state for storing image data
if "image_b64" not in st.session_state:
    st.session_state["image_b64"] = None
    st.session_state["mime_type"] = None

# Select the LLM option
selected_llm = st.selectbox("Select the LLM Model:", options=list(llm_options.keys()))
invoke_url = llm_options[selected_llm]["invoke_url"]
model = llm_options[selected_llm]["model"]

# Image upload section
if not st.session_state["image_b64"]:
    uploaded_file = st.file_uploader("Upload an image (.png or .jpg)", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        # Validate MIME type
        mime_type = mimetypes.guess_type(uploaded_file.name)[0]
        if mime_type not in ["image/png", "image/jpeg"]:
            st.error("Unsupported file type. Please upload a PNG or JPG image.")
        else:
            # Read and encode the image
            try:
                image_b64 = base64.b64encode(uploaded_file.read()).decode()
                assert len(image_b64) < 360_000, "Image is too large. Please upload a smaller image."

                # Store image data in session state
                st.session_state["image_b64"] = image_b64
                st.session_state["mime_type"] = mime_type

                # Display the uploaded image
                st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
                st.success("Image uploaded successfully! You can now ask questions.")

            except Exception as e:
                st.error(f"Error processing the image: {e}")

else:
    # Display the previously uploaded image
    st.image(f"data:{st.session_state['mime_type']};base64,{st.session_state['image_b64']}",
             caption="Uploaded Image", use_container_width=True)

# Prompt for questions
if st.session_state["image_b64"]:
    prompt = st.text_input("Ask a question about the image:")

    if prompt:
        # Prepare the API payload
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": f'{prompt} <img src="data:{st.session_state["mime_type"]};base64,{st.session_state["image_b64"]}" />',
                    "image": {
                        "data": st.session_state["image_b64"],
                        "mime": st.session_state["mime_type"],
                    },
                }
            ],
            "max_tokens": 1024,
            "temperature": 1.00,
            "top_p": 1.00,
            "stream": stream,
        }

        # Headers for the API request
        headers = {
            "Authorization": "Bearer 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",  # Add your API key here
            "Accept": "application/json" if not stream else "text/event-stream",
        }

        # Make the API request
        with st.spinner("Processing your question..."):
            try:
                response = requests.post(invoke_url, headers=headers, json=payload)

                if response.status_code == 200:
                    result = response.json()
                    st.success("AI Response:")
                    st.json(result)
                else:
                    st.error(f"Error: API call failed with status code {response.status_code}")
                    st.text(response.text)

            except Exception as e:
                st.error(f"Error during API request: {e}")

