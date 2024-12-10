import requests
import base64
import json
import mimetypes
import os

# Define the Llama-3.2 API endpoint
invoke_url = "https://ai.api.nvidia.com/v1/gr/meta/llama-3.2-90b-vision-instruct/chat/completions"
stream = False  # Set to True if you want to stream the response

# api_key = os.getenv('NVIDIA_API_KEY') 

# Ask user for image file
image_path = input("Please upload an image file (e.g., image.png, image.jpg): ")

# Validate the MIME type of the file
mime_type, _ = mimetypes.guess_type(image_path)
if mime_type not in ['image/png', 'image/jpeg', 'image/jpg']:
    print("Error: Unsupported file type. Please upload a PNG or JPG image.")
    exit(1)

# Ask the user what they'd like to know about the image
prompt = input("What would you like to know about this image? ")

# Print the current working directory for debugging
print(f"Current working directory: {os.getcwd()}")

# Ensure the image path is absolute
if not os.path.isabs(image_path):
    image_path = os.path.join(os.getcwd(), image_path)

# Check if the file exists
if not os.path.exists(image_path):
    print(f"Error: The file at {image_path} was not found.")
    exit(1)

# Try opening and encoding the image to base64
try:
    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode()
    print(f"Image successfully loaded and encoded. Image length: {len(image_b64)} characters.")
except Exception as e:
    print(f"Error opening or encoding the image: {e}")
    exit(1)

# Check if the image is within the acceptable size limit
assert len(image_b64) < 360_000, "Image is too large. Please upload a smaller image."

# Headers for the API request
headers = {
    "Authorization": "Bearer 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",  # Add your API key here if required
    # "Authorization": "Bearer $NVIDIA_API_KEY",  # Default NVIDIA_API_KEY set in environment.
    "Accept": "application/json" if not stream else "text/event-stream",
}

# Construct the payload for the API call
payload = {
    "model": "meta/llama-3.2-90b-vision-instruct",
    "messages": [
        {
            "role": "user",
           #"content": prompt,  # User's prompt asking about the image
            "content": f'{prompt} <img src="data:image/png;base64,{image_b64}" />',"image": {
                "data": image_b64,  # The base64-encoded image data
                "mime": mime_type,  # MIME type (image/jpeg, image/png)
            }
        }
    ],
    "max_tokens": 1024,  # Maximum number of tokens the model will generate
    "temperature": 1.00,  # Sampling temperature for diversity
    "top_p": 1.00,  # Top-p sampling for controlling output diversity
    "stream": stream,  # Whether to stream the response or not
}

# Make the API request
try:
    response = requests.post(invoke_url, headers=headers, json=payload)

    # Check for streaming response
    if stream:
        for line in response.iter_lines():
            if line:
                print(line.decode("utf-8"))
    else:
        # For non-streaming, simply print the JSON response
        if response.status_code == 200:
            print("API call successful! Response:")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Error: API call failed with status code {response.status_code}")
            print(response.text)

except requests.exceptions.RequestException as e:
    print(f"Error during API request: {e}")
    exit(1)

