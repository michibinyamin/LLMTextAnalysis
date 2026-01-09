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

    if not re.match(pattern, response[0]):
        for _ in range(2):  # Retry up to 2 times
            print("Fixing bullet format... attempt", _ + 1)

            # Include both original text and previous summary for context
            fix_prompt = f"""
            The original text is:

            {text}

            Your previous summary was:

            {response[0]}

            It did not follow the bullet format correctly. 
            Please rewrite it so it has between 3 and 6 bullet points, 
            each starting with -, *, or • while capturing the main ideas and key conclusions.
            """
            response = get_completion(fix_prompt, system_instruction, api_key, temperature=0.3, max_tokens=300)
            if re.match(pattern, response[0]):
                print ("Successful response.")
                return response
        print("Failed to get correct bulleted format after retries.")
        return "Error: Unable to generate summary in the required bulleted format."
    else:
        print ("Successful response.")
        return response[0]


# --- Use Case 2 Logic ---
import re

def extract_topics(text, api_key):
    system_instruction = f"""
    Analyze the text below and extract the main topics.
    
    Constraints:
    - Return a list of 3 to 7 topics.
    - Each topic must be very short (1-3 words maximum).
    - Ensure topics are meaningful and not duplicated.
    - Output format: Bullet points (start with -, *, or •).
    - Compare each topic against the others before finalizing your list. 
    If two topics are semantically similar (e.g., 'Green Energy' and 'Renewable Power'), 
    merge them into a single topic.
    """

    # Initial Call
    response = get_completion(text, system_instruction, api_key, temperature=0.2, max_tokens=150)
    
    # Retry Loop (Max 3 attempts)
    for attempt in range(3):
        
        # 1. Clean and parse lines
        lines = [line.strip() for line in response[0].splitlines() if line.strip()]
        
        # 2. validation Checks
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
        if len(lines) != len(set(lines)):
            errors.append(" The output contained duplicate topics.")

        # 3. If no errors, we are done!
        if not errors:
            print("Successful response.")
            return response[0]
        
        # 4. If errors exist, construct a fix prompt
        print(f"Attempt {attempt+1} failed. Errors: {errors}")
        
        fix_prompt = f"""
        The original text is:
        {text}

        Your previous summary was:
        {response[0]}

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
    # Clean the output (remove extra whitespace or periods)
    cleaned_response = response[0].strip().strip(".")
    print ("Cleaned Response:", cleaned_response)

    # Enforce allowed categories
    if cleaned_response not in categories or response[1] < 85.0:  # If the response is not accurate or confidence is low, mark as Unclassified
        return "Unclassified"

    return cleaned_response + f" (Confidence: {response[1]}%)"
    