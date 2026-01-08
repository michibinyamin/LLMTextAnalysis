import openai
import re
    
def get_completion(user_text, system_instruction, api_key, model="gpt-4o-mini", temperature=0.3, max_tokens=500):
    """Sends a System prompt (rules) and User prompt (data) to OpenAI."""
    client = openai.OpenAI(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": system_instruction},
                      {"role": "user", "content": user_text}],
            temperature=temperature,
            max_tokens=max_tokens 
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# --- Use Case 1 Logic ---
def summarize_text(text, api_key):
    system_instruction = f"""
    You are an expert editor. Please provide a clear, concise summary of the following text.
    
    Constraints:
    - The output must be a bulleted list.
    - It must have between 3 and 6 bullet points.
    - Capture the main ideas, key conclusions and Important facts.
    """
    pattern = r'^([\-\*\•] .+\n){2,5}[\-\*\•] .+$'  # Regex to check for 3 to 6 bullet points!

    response = get_completion(text, system_instruction, api_key, temperature=0.3, max_tokens=300)

    if not re.match(pattern, response):
        for _ in range(2):  # Retry up to 2 times
            print("Fixing bullet format... attempt", _ + 1)

            # Include both original text and previous summary for context
            fix_prompt = f"""
            The original text is:

            {text}

            Your previous summary was:

            {response}

            It did not follow the bullet format correctly. 
            Please rewrite it so it has between 3 and 6 bullet points, 
            each starting with -, *, or • while capturing the main ideas and key conclusions.
            """
            response = get_completion(fix_prompt, system_instruction, api_key, temperature=0.3, max_tokens=300)
            if re.match(pattern, response):
                print ("Successful response.")
                return response
        print("Failed to get correct bulleted format after retries.")
        return "Error: Unable to generate summary in the required bulleted format."
    else:
        print ("Successful response.")
        return response


# --- Use Case 2 Logic ---
def extract_topics(text, api_key):
    system_instruction = f"""
    Analyze the text below and extract the main topics.
    
    Constraints:
    - Return a list of 3 to 7 topics.
    - Each topic must be very short (1-3 words maximum).
    - Ensure topics are meaningful and not duplicated.
    - Output format: A simple comma-separated list.
    """
    #return get_completion(prompt, api_key)
    return get_completion(text, system_instruction, api_key, temperature=0.2, max_tokens=150)


# --- Use Case 3 Logic ---
def classify_intent(text, api_key):
    system_instruction = f"""
    Classify the intent of the following user message into exactly one of these categories:
    1. Technical issue
    2. Billing question
    3. Feature request
    4. Complaint
    5. General inquiry
    
    If the message is ambiguous or does not fit, reply with "Unclassified".
    
    Return ONLY the category name.
    """
    #return get_completion(prompt, api_key)
    return get_completion(text, system_instruction, api_key, temperature=0.2, max_tokens=50)

