import math
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
            max_tokens=max_tokens,
            logprobs=True,      # Request the confidence scores
            top_logprobs=2      # See the top 2 choices for each token
        )
        content = response.choices[0].message.content
    
        # Extract logprobs from the response
        token_logprobs = response.choices[0].logprobs.content
        
        # Calculate an average confidence score for the whole sentence
        # We convert log(probability) back to a % (0-100)
        all_probs = [math.exp(t.logprob) for t in token_logprobs]
        avg_confidence = sum(all_probs) / len(all_probs) * 100
        
        return content, round(avg_confidence, 2)
        #return response.choices[0].message.content
    except Exception as e:
        print(f"API Error: {e}")
        return None, 0.0  # Return None so the caller knows it failed

# --- Use Case 1 Logic ---
def summarize_text(text, api_key):
    system_instruction = f"""
    ### Role
    You are an expert executive editor. Your goal is to synthesize the provided text into a clear, high-level summary.

    ### Content Guidelines
    - **Directness:** Use active voice. Avoid meta-talk like "The article discusses..." or "The author says...". Just state the facts.
    - **Substance:** Prioritize conclusions, data points, and decisions over general descriptions.

    ### Constraints
    1. **Quantity:** Output strictly between 3 and 6 bullet points.
    2. **Format:** Use standard bullet characters (-, *, or •).
    3. **Length:** Each bullet must be 1 concise sentence (maximum 2).
    4. **No Fluff:** Do not output any introductory text (e.g., "Here is the summary:") or closing remarks.

    ### Input Text
    """
    pattern = r'^([\-\*\•] .+\n){2,5}[\-\*\•] .+$'  # Regex to check for 3 to 6 bullet points!

    response = get_completion(text, system_instruction, api_key, temperature=0.3, max_tokens=300)
    content = response[0]

    if not re.match(pattern, content):
        if content is None:
            return "Error: API failure."
        for _ in range(2):  # Retry up to 2 times
            print("Fixing bullet format... attempt", _ + 1)

            # Include both original text and previous summary for context
            fix_prompt = f"""
            The original text is:

            {text}

            Your previous summary was:

            {content}

            It did not follow the bullet format correctly. 
            Please rewrite it so it has between 3 and 6 bullet points, 
            each starting with -, *, or • while capturing the main ideas and key conclusions.
            """
            response = get_completion(fix_prompt, system_instruction, api_key, temperature=0.3, max_tokens=300)
            content = response[0]
            if re.match(pattern, content):
                print ("Successful response.")
                return content
        print("Failed to get correct bulleted format after retries.")
        return "Error: Unable to generate summary in the required bulleted format."
    else:
        print ("Successful response.")
        return content


# --- Use Case 2 Logic ---
def extract_topics(text, api_key):
    system_instruction = f"""
    ### Role
    You are an expert content analyzer. Your task is to extract the main topics from the text provided.

    ### Definition of a Topic
    A Topic is a concise **noun phrase** (1-3 words) that categorizes a significant theme in the text. 
    It must be specific (e.g., use "Network Latency" instead of just "Issues").

    ### Constraints
    1. **Quantity:** Return between 3 and 7 topics.
    2. **Length:** Strictly 1-3 words per topic.
    3. **Uniqueness:** Compare topics before outputting. Merge semantically similar concepts (e.g., 'Cost' and 'Price' -> 'Pricing Strategy').
    4. **Format:** Output ONLY a bulleted list (using -, *, or •). 
    5. **No Fluff:** Do not include introductory text (e.g., "Here are the topics") or closing remarks.

    ### Input Text
    """

    # Initial Call
    response = get_completion(text, system_instruction, api_key, temperature=0.2, max_tokens=150)
    
    # We allow 4 checks total: 1 for initial, 3 for retries
    max_retries = 3

    # Retry Loop (Max 3 attempts)
    for attempt in range(max_retries + 1):
        content = response[0]
        
        # 1. API Error Check
        if content is None:
            return "Error: API failure."
        
        # 2. Clean and parse Lines (More robust than splitlines)
        # Only keep lines that start with a bullet point
        lines = [line.strip() for line in content.splitlines() if re.match(r'^[-*•]', line.strip())]
        
        # 3. validation Checks
        errors = []
        
        # Check A: Bullet Count (3 to 7 items)
        if not (3 <= len(lines) <= 7):
            errors.append(f"Output had {len(lines)} topics, but required between 3 and 7.")

        # Check B: Word Count (1-3 words per topic)
        # We assume a topic looks like "- Topic Name", so we split and ignore the first char if it's a bullet
        long_topics = []
        for line in lines:
            # Remove common bullet markers to count actual words
            clean_line = re.sub(r'^[-*•]\s*', '', line)
            word_count = len(clean_line.split())
            if word_count > 3:
                long_topics.append(line)
        
        if long_topics:
            errors.append(f"These topics were too long (limit is 3 words): {', '.join(long_topics)}")

        # Check C: Exact Duplicates
        # Normalize to lowercase for better dupe checking
        normalized_lines = [l.lower() for l in lines]
        if len(normalized_lines) != len(set(normalized_lines)):
            errors.append("Output contained duplicate topics.")

        # 4. If no errors, we are done!
        if not errors:
            print("Successful response.")
            return content
        
        # 5. If errors exist, construct a fix prompt
        if attempt < max_retries:
            print(f"Attempt {attempt+1} failed. Errors: {errors}")
            
            fix_prompt = f"""
            The original text is:
            {text}

            Your previous extraction was:
            {content}

            It failed the following constraints:
            { " ".join(errors) }

            Please rewrite the list to fix these errors specifically.
            """
            
            # Generate new response based on the critique
            response = get_completion(fix_prompt, system_instruction, api_key, temperature=0.2, max_tokens=150)

    print("Failed to get correct format after retries.")
    return "Error: Unable to generate summary in the required format."


# --- Use Case 3 Logic ---
def classify_intent(text, api_key):
    categories = ["Technical issue", "Billing question", "Feature request", "Complaint", "General inquiry"]
    system_instruction = f"""
    Classify the intent of the following user message into exactly one of these categories:
    {', '.join(categories)}
    
    If the message is ambiguous or does not fit, reply with "Unclassified".
    
    Return ONLY the category name.
    """
    #return get_completion(prompt, api_key)
    response = get_completion(text, system_instruction, api_key, temperature=0.2, max_tokens=50)
    content = response[0]
    confidence = response[1]
    # Clean the output (remove extra whitespace or periods)
    if content is None:
            return "Error: API failure."
    cleaned_response = content.strip().strip(".")
    print ("Cleaned Response:", cleaned_response)

    # Enforce allowed categories
    if cleaned_response not in categories or confidence < 85.0:  # If the response is not accurate or confidence is low, mark as Unclassified
        return "Unclassified"

    return cleaned_response + f" (Confidence: {confidence}%)"