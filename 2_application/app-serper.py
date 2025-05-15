import streamlit as st
import requests
import base64
import mimetypes
import hashlib
import uuid
import json
import os

# LLM Environment
NVIDIA_APIKEY = os.getenv("NVIDIA_APIKEY", "YOUR_NVIDIA_API_KEY")

# SERPER (Web Scraping) Environment
# 👉 Place your Serper API key here or set SERPER_API_KEY in your env vars
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "YOUR_SERPER_API_KEY")

from serper import SerperClient
serper = SerperClient(api_key=SERPER_API_KEY)

# Llama-3.2 API endpoints
tt = "https://ai.api.nvidia.com/v1/gr/meta/llama-3.2-11b-vision-instruct/chat/completions"
llm_options = {
    "Llama-3.2-11b": {"invoke_url": tt, "model": "meta/llama-3.2-11b-vision-instruct"},
}

# Sidebar: Model Parameters
st.sidebar.header("Model Parameters")
max_tokens = st.sidebar.slider("Max Tokens", 1024, 10240, 1024, 1024)
temperature = st.sidebar.slider("Temperature", 0.0, 2.0, 1.0, 0.1)
top_p = st.sidebar.slider("Top P", 0.0, 1.0, 1.0, 0.1)

# Utility: compute file hash
def compute_hash(file_data):
    return hashlib.md5(file_data).hexdigest()

# Function: fetch weather updates via Serper
def fetch_weather_with_serper(query: str):
    results = serper.search(query)
    alerts = []
    for item in results.get("organic", []):
        alerts.append({
            "title": item.get("title"),
            "snippet": item.get("snippet"),
            "link": item.get("link")
        })
    return alerts

# Function: call Llama Vision LLM
def llama_vision(invoke_url, model, messages, max_tokens, temperature, top_p):
    headers = {"Authorization": f"Bearer {NVIDIA_APIKEY}", "Content-Type": "application/json"}
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": top_p,
    }
    resp = requests.post(invoke_url, headers=headers, json=payload)
    resp.raise_for_status()
    return resp.json().get("choices", [{}])[0].get("message", {}).get("content", "")

# Streamlit app
st.title("Disaster‐Aware Map with Serper Weather Enrichment")

tab1, tab2 = st.tabs(["Upload & Analyze", "Uploaded Images"])

# Session state init
if "uploaded_images" not in st.session_state:
    st.session_state["uploaded_images"] = {}

with tab1:
    st.header("Upload Satellite/Map Image")
    selected_llm = st.selectbox("Select LLM:", list(llm_options.keys()))
    invoke_url = llm_options[selected_llm]["invoke_url"]
    model = llm_options[selected_llm]["model"]

    uploaded_files = st.file_uploader("Upload images (.png, .jpg)", type=["png","jpg","jpeg"], accept_multiple_files=True)
    if uploaded_files:
        for uf in uploaded_files:
            data = uf.read()
            h = compute_hash(data)
            if h not in st.session_state["uploaded_images"]:
                st.session_state["uploaded_images"][h] = {
                    "name": uf.name,
                    "mime": mimetypes.guess_type(uf.name)[0],
                    "data": base64.b64encode(data).decode()
                }
                st.success(f"Uploaded {uf.name}")

    # Select image to analyze
    hashes = list(st.session_state["uploaded_images"].keys())
    sel = st.selectbox("Select image:", hashes, format_func=lambda x: st.session_state["uploaded_images"][x]["name"]) if hashes else None
    if sel:
        img = st.session_state["uploaded_images"][sel]
        st.image(f"data:{img['mime']};base64,{img['data']}")
        prompt = st.text_input("Enter analysis prompt (e.g., detect flooding):")

        if prompt:
            # First-pass: LLM vision analysis
            initial_msg = {"role": "user", "content": f"{prompt} <img src='data:{img['mime']};base64,{img['data']}'/>"}
            st.subheader("Initial LLM Analysis")
            with st.spinner("Analyzing image..."):
                ai_text = llama_vision(invoke_url, model, [initial_msg], max_tokens, temperature, top_p)
            st.write(ai_text)

            # Parse events JSON
            try:
                events = json.loads(ai_text)
            except:
                events = []
                st.warning("Could not parse JSON from LLM response.")

            # Fetch weather alerts and build summaries
            summaries = []
            for evt in events:
                loc = evt.get("location", "unknown location")
                query = f"current weather alerts in {loc}"
                alerts = fetch_weather_with_serper(query)
                if alerts:
                    text = "; ".join([f"{a['title']}: {a['snippet']}" for a in alerts])
                else:
                    text = "No alerts found"
                summaries.append(f"{loc}: {text}")

            # Second-pass: Enrichment prompt
            enrichment_content = (
                "Based on the map shown and the following weather-alert summaries, "
                "please refine your assessment of disaster severity and impacted areas:\n\n"
                + "\n".join(summaries)
                + f"\n\nMap: <img src='data:{img['mime']};base64,{img['data']}'/>"
            )
            enrichment_msg = {"role": "user", "content": enrichment_content}

            st.subheader("Enriched LLM Analysis")
            with st.spinner("Enriching analysis with weather data..."):
                enriched_text = llama_vision(invoke_url, model, [enrichment_msg], max_tokens, temperature, top_p)
            st.write(enriched_text)

with tab2:
    st.header("Previously Uploaded Images")
    if st.session_state["uploaded_images"]:
        for h, d in st.session_state["uploaded_images"].items():
            st.image(f"data:{d['mime']};base64,{d['data']}", caption=d['name'])
    else:
        st.info("No images yet.")

