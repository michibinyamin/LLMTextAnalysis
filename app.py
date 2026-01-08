import streamlit as st
from llm_utils import summarize_text, extract_topics, classify_intent

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
        
        # Requirement: Input text provided by user
        input_text = st.text_area("Enter text (min 500 words recommended):", height=300)
        
        # Requirement: Option to load from file
        uploaded_file = st.file_uploader("Or upload a text file (.txt):", type=["txt"])
        if uploaded_file is not None:
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

        # Requirement: Short messages (1-3 sentences)
        input_text = st.text_input("Enter a user message:", placeholder="e.g., 'I want to cancel my subscription.'")

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