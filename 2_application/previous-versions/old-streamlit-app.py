import streamlit as st
import requests
import base64
import mimetypes
import json
import os

# Define the Llama-3.2 API endpoint
invoke_url = "https://ai.api.nvidia.com/v1/gr/meta/llama-3.2-90b-vision-instruct/chat/completions"
stream = False  # Set to True if you want to stream the response

# Streamlit UI
st.title("Vision-Based AI Assistant")
st.write("Upload an image and ask the AI a question about it!")

# Image upload section
uploaded_file = st.file_uploader("Upload an image (.png or .jpg)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Validate MIME type
    mime_type = mimetypes.guess_type(uploaded_file.name)[0]
    if mime_type not in ["image/png", "image/jpeg"]:
        st.error("Unsupported file type. Please upload a PNG or JPG image.")
    else:
        # Display the uploaded image
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

        # Ask the user for a prompt
        prompt = st.text_input("What would you like to know about this image?")

        if prompt:
            # Read and encode the image
            try:
                image_b64 = base64.b64encode(uploaded_file.read()).decode()
                assert len(image_b64) < 360_000, "Image is too large. Please upload a smaller image."

                # Prepare the API payload
                payload = {
                    "model": "meta/llama-3.2-90b-vision-instruct",
                    "messages": [
                        {
                            "role": "user",
                            "content": f'{prompt} <img src="data:{mime_type};base64,{image_b64}" />',
                            "image": {
                                "data": image_b64,
                                "mime": mime_type,
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
                with st.spinner("Processing..."):
                    response = requests.post(invoke_url, headers=headers, json=payload)

                # Handle the response
                if response.status_code == 200:
                    result = response.json()
                    st.success("API call successful! Response:")
                    st.json(result)
                else:
                    st.error(f"Error: API call failed with status code {response.status_code}")
                    st.text(response.text)

            except Exception as e:
                st.error(f"Error processing the image or making the API call: {e}")

