# Streamlit/Gradio UI for testing
import streamlit as st
import requests
import uuid

# Configuration
API_URL = "http://localhost:8000/generate"

# Initialize Streamlit session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Router Controls")
    st.markdown("---")
    
    # Force Route Selection
    force_route = st.selectbox(
        "Force Routing Decision", 
        ["Auto (Let Router Decide)", "LOCAL (Ollama)", "CLOUD (Groq)"]
    )
    
    st.markdown("---")
    
    # Session Management
    st.caption(f"**Active Session ID:**")
    st.code(st.session_state.session_id, language=None)
    
    if st.button("🗑️ Clear Chat & Reset Session", use_container_width=True):
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()

# --- MAIN CHAT UI ---
st.title("🧠 SLM Smart Router Demo")
st.caption("Testing dynamic routing between Local SLMs and Cloud LLMs.")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        # Show metadata for assistant messages
        if msg["role"] == "assistant" and "metadata" in msg:
            meta = msg["metadata"]
            route_emoji = "🏠" if meta["route"] == "LOCAL" else "☁️" if meta["route"] == "CLOUD" else "💾"
            st.caption(
                f"{route_emoji} **Route:** {meta['route']} | "
                f"⏱️ **Latency:** {meta['latency']}ms | "
                f"💾 **Cached:** {meta['cached']}"
            )

# Chat input
if prompt := st.chat_input("Ask a simple or complex question..."):
    # Add user message to state and display
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare API payload
    payload = {
        "prompt": prompt,
        "session_id": st.session_state.session_id,
        "stream": False
    }
    
    # Map UI dropdown to API enum
    if force_route == "LOCAL (Ollama)":
        payload["force_route"] = "LOCAL"
    elif force_route == "CLOUD (Groq)":
        payload["force_route"] = "CLOUD"

    # Call the FastAPI backend
    with st.chat_message("assistant"):
        with st.spinner("Routing request..."):
            try:
                response = requests.post(API_URL, json=payload)
                response.raise_for_status()
                data = response.json()
                
                assistant_text = data["response"]
                metadata = {
                    "route": data["route_used"],
                    "latency": round(data["latency_ms"], 2),
                    "cached": data["cached"]
                }
                
                # Display response
                st.markdown(assistant_text)
                
                # Display metadata beautifully
                route_emoji = "🏠" if metadata["route"] == "LOCAL" else "☁️" if metadata["route"] == "CLOUD" else "💾"
                st.caption(
                    f"{route_emoji} **Route:** {metadata['route']} | "
                    f"⏱️ **Latency:** {metadata['latency']}ms | "
                    f"💾 **Cached:** {metadata['cached']}"
                )
                
                # Save to state
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": assistant_text,
                    "metadata": metadata
                })
                
            except requests.exceptions.ConnectionError:
                st.error("❌ Could not connect to the FastAPI backend. Is `main.py` running on port 8000?")
            except requests.exceptions.HTTPError as e:
                # Show the backend's detailed error message
                try:
                    detail = e.response.json().get("detail", str(e))
                except Exception:
                    detail = str(e)
                st.error(f"❌ Backend Error ({e.response.status_code}): {detail}")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ API Error: {e}")