import openai

def get_completion(prompt, api_key, model="gpt-3.5-turbo"):
    """Helper function to call OpenAI API."""
    client = openai.OpenAI(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3, # Low temp for more deterministic results [cite: 90]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# --- Use Case 1 Logic ---
def summarize_text(text, api_key):
    # Prompt designed to ensure 3-6 bullet points [cite: 20]
    prompt = f"""
    You are an expert editor. Please provide a clear, concise summary of the following text.
    
    Constraints:
    - The output must be a bulleted list.
    - It must have between 3 and 6 bullet points.
    - Capture the main ideas and key conclusions.
    
    Text:
    {text}
    """
    return get_completion(prompt, api_key)

# --- Use Case 2 Logic ---
def extract_topics(text, api_key):
    # Prompt designed to ensure topics are short (1-3 words) and distinct [cite: 40, 41]
    prompt = f"""
    Analyze the text below and extract the main topics.
    
    Constraints:
    - Return a list of 3 to 7 topics.
    - Each topic must be very short (1-3 words maximum).
    - Ensure topics are meaningful and not duplicated.
    - Output format: A simple comma-separated list.
    
    Text:
    {text}
    """
    return get_completion(prompt, api_key)

# --- Use Case 3 Logic ---
def classify_intent(text, api_key):
    # Requirement: Define labels clearly [cite: 68]
    # Requirement: Handle ambiguous messages [cite: 69]
    prompt = f"""
    Classify the intent of the following user message into exactly one of these categories:
    1. Technical issue
    2. Billing question
    3. Feature request
    4. Complaint
    5. General inquiry
    
    If the message is ambiguous or does not fit, reply with "Unclassified".
    
    Message:
    "{text}"
    
    Return ONLY the category name.
    """
    return get_completion(prompt, api_key)