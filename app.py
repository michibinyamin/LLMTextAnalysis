import streamlit as st
from PyPDF2 import PdfReader
from llm_utils import summarize_text, extract_topics, classify_intent
import json

def load_samples():
    """Load sample texts from the JSON file."""
    try:
        with open("samples.JSON", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {} # Return empty if file is missing

# Load the data once when app starts
SAMPLES = load_samples()

# --- Page Config ---
st.set_page_config(
    page_title="Text Analysis Tool",
    page_icon="🤖",
    layout="wide"
)

# --- Sidebar: Configuration ---
with st.sidebar:
    st.header("Settings")
    # Best practice: Allow user to input key or load from env
    api_key = st.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API key here.")
    
    st.markdown("---")
    st.markdown("### Analysis Type")
    # Requirement: User must be able to select analysis type
    analysis_type = st.radio(
        "Choose a task:",
        ("Summarize Text", "Extract Key Topics", "Classify Intent")
    )

# --- Main Page ---
st.title("🤖 LLM-Powered Text Analysis")

if not api_key:
    st.warning("⚠️ Please enter your OpenAI API key in the sidebar to proceed.")
else:
    # --- USE CASE 1: SUMMARIZE TEXT ---
    if analysis_type == "Summarize Text":
        st.subheader("📝 Summarize Long Text")
        st.markdown("*Goal: Create a clear, concise summary of long text.*")
        
        # Sample texts from public sources (e.g., Wikipedia, NASA)
        SAMPLE_TEXTS = {
            "None": "",
            "Space Exploration (NASA)": """NASA's Artemis program is the first step in the next era of human exploration. Together with commercial and international partners, NASA will establish a sustainable presence on the Moon to prepare for missions to Mars. Through Artemis, NASA will land the first woman and the first person of color on the Moon... [You would paste the full 500 words here]""",
            "History of Computing": """The history of computing is longer than the history of computing hardware and modern computing technology and includes the history of methods intended for pen and paper or for chalk and slate... [Paste full text here]"""
        }

        # Feature: Select from Public Dataset
        selected_sample = st.selectbox("Load a sample text:", options=list(SAMPLES["summarize"].keys()))

        # Logic: If a sample is picked, use it. Otherwise, leave blank.
        if selected_sample != "None":
            default_text = SAMPLES["summarize"][selected_sample]
        else:
            default_text = ""

        # The text area pre-fills with the sample if selected
        input_text = st.text_area("Enter text or edit sample:", value=default_text, height=300)
        
        # Requirement: Option to load from file
        uploaded_file = st.file_uploader("upload a text / pdf file (.txt / .pdf):", type=["txt", "pdf"])
        if uploaded_file is not None:
            if uploaded_file.type == "application/pdf":
                reader = PdfReader(uploaded_file)
                input_text = ""
                for page in reader.pages:
                    input_text += page.extract_text() + "\n"
            else:   # assume txt file
                input_text = uploaded_file.read().decode("utf-8")
            st.info("File loaded successfully!")

        if st.button("Generate Summary"):
            if input_text:
                with st.spinner("Summarizing..."):
                    # Call the function from llm_utils
                    result = summarize_text(input_text, api_key)
                    st.success("Summary:")
                    st.markdown(result)
            else:
                st.error("Please enter some text to summarize.")

    # --- USE CASE 2: EXTRACT KEY TOPICS ---
    elif analysis_type == "Extract Key Topics":
        st.subheader("🏷️ Extract Key Topics")
        st.markdown("*Goal: Identify 3-7 main themes from the text.*")

        # Requirement: Medium to long text input
        input_text = st.text_area("Enter text to analyze:", height=300)

        if st.button("Extract Topics"):
            if input_text:
                with st.spinner("Extracting topics..."):
                    result = extract_topics(input_text, api_key)
                    st.success("Key Topics Found:")
                    # Display as neat tags or list
                    st.write(result)
            else:
                st.error("Please enter text to extract topics from.")

    # --- USE CASE 3: CLASSIFY INTENT ---
    elif analysis_type == "Classify Intent":
        st.subheader("🎯 Classify User Intent")
        st.markdown("*Goal: Categorize short user messages.*")
        st.markdown("categories: 'Technical issue', 'Billing question', 'Feature request', 'Complaint', 'General inquiry'")

        # Feature: Select from Dataset
        selected_sample = st.selectbox("Load a sample text:", options=list(SAMPLES["intent"].keys()))
        
        # Logic: If a sample is picked, use it. Otherwise, leave blank.
        if selected_sample != "None":
            default_text = SAMPLES["intent"][selected_sample]
        else:
            default_text = ""

        # The text area pre-fills with the sample if selected
        #input_text = st.text_area("Enter text or edit sample:", value=default_text, height=300)

        # Requirement: Short messages (1-3 sentences)
        input_text = st.text_area("Enter a user message:", placeholder="e.g., 'I want to cancel my subscription.'",value=default_text, height=20)

        if st.button("Classify"):
            if input_text:
                with st.spinner("Classifying..."):
                    result = classify_intent(input_text, api_key)
                    st.metric(label="Predicted Intent", value=result)
            else:
                st.error("Please enter a message to classify.")

# --- Footer ---
st.markdown("---")
st.caption("ML Junior Home Assignment | Streamlit & OpenAI")