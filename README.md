# LLMTextAnalysis

### Use Case 1 - Summarize Long Text

**parameters**:  
*temperature=0.3,  
*max_tokens*=300*

**system prompt**:

        ## Role
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

**How was the prompt designed:**  
The summarize_text function uses a system prompt to instruct the LLM as an expert editor:  
It tells the model to produce a clear and concise bulleted summary.
Constraints explicitly specify 3 to 6 bullets to control summary size.  
It emphasizes capturing main ideas, key conclusions, and important facts, guiding content selection.  
This ensures the LLM focuses on relevant points rather than writing a free-form summary.

**How Length and Verbosity Are Controlled:**  
_Bullet Count:_  
A regex checks that the summary has 3–6 bullets.  
If the output has too few or too many bullets, the function retries by sending the previous summary  
plus the original text back to the model with instructions to fix it.

_Token Limit:_  
max_tokens=300 - sets a hard upper bound on the response length.
This helps keep the output manageable, but it may cut the text mid-sentence, so it is not a quality guarantee, only a strict safety limit.

_Temperature_:  
temperature=0.3 keeps the output deterministic and concise, avoiding overly verbose or creative responses.

_Context Feedback Loop:_  
By including the original text and previous attempt when retrying, the model can adjust its summary while respecting the bullet and length constraints.

This combination of prompt constraints, regex validation,  
token limit, and low temperature effectively controls both length and verbosity  
while maintaining clarity.

## Before:

#### Text input:

        Gabriel de Clieu brought coffee seedlings to Martinique in the Caribbean in 1720.
        Those sprouts flourished and 50 years later there were 18,680 coffee trees in Martinique enabling the spread of coffee cultivation to Saint-Domingue (Haiti), Mexico and other islands of the Caribbean.
        The French territory of Saint-Domingue saw coffee cultivated starting in 1734, and by 1788 supplied half the world's coffee.
        Coffee had a major influence on the geography of Latin America.[97] The French colonial plantations relied heavily on African slave laborers.
        However, the dreadful conditions that the slaves worked in on coffee plantations were a factor in the soon-to-follow Haitian
        Revolution. The coffee industry never fully recovered there.
        Coffee also found its way to the Isle of Bourbon, now known as
        Réunion, in the Indian Ocean. The plant produced smaller beans and was deemed a different variety of arabica known as var.Bourbon.
        The Santos coffee of Brazil and the Oaxaca coffee of Mexico are the progeny of that Bourbon tree. Circa 1727, the King of Portugal sent
        Francisco de Melo Palheta to French Guiana to obtain coffee seeds to become a part of the coffee market.
        Francisco initially had difficulty obtaining these seeds, but he captivated the French Governor's wife, and she sent him enough seeds and shoots to commence the coffee industry of Brazil.
        However, cultivation did not gather momentum until independence in 1822,[8]: 19  leading to the clearing of massive tracts of the Atlantic Forest, first from the vicinity of Rio and later São Paulo for coffee plantations.
        In 1893, the coffee from Brazil was introduced into Kenya and Tanzania (Tanganyika), not far from its place of origin in Ethiopia, 600 years prior, ending its transcontinental journey.
        After the Boston Tea Party of 1773, large numbers of Americans switched to drinking coffee during the American Revolution because drinking tea had become unpatriotic.
        Cultivation was taken up by many countries in the latter half of the 19th century, and in almost all of them it involved the large-scale displacement and exploitation of indigenous people. Harsh conditions led to many uprisings, coups and bloody suppressions of peasants
        For example, Guatemala started producing coffee in the 1500s but lacked the manpower to harvest the coffee beans.
        As a result, the Guatemalan government forced indigenous people to work on the fields.
        This led to a strain in the indigenous and Guatemalan people's relationship that still exists today.
        A notable exception is Costa Rica where a lack of ready labor prevented the formation of large farms. Smaller farms and more egalitarian conditions ameliorated unrest over the 19th and 20th centuries. In the 20th century, Latin American countries faced a possible economic collapse.
        Before World War II, Europe was consuming large amounts of coffee.
        Once the war started, Latin America lost 40% of its market and was on the verge of economic collapse. Coffee was and is a Latin American commodity. The United States saw this and talked with the Latin American countries and as a result the producers agreed on an equitable division of the U.S. market. The U.S. government monitored this agreement.
        For the period that this plan was followed the value of coffee doubled, which greatly benefited coffee producers and the Latin American countries.
        Brazil became the largest producer of coffee in the world by 1852 and it has held that status ever since. It dominated world production, exporting more coffee than the rest of the world combined, from 1850 to 1950.
        The period since 1950 saw the widening of the playing field due to the emergence of several other major producers, notably Colombia,
        Ivory Coast, Ethiopia, and, most recently, Vietnam, which overtook Colombia and became the second-largest producer in 1999 and reached
        15% market share by 2011.
        Recent additions to the coffee market are lattes, Frappuccinos and other sugary coffee drinks. This has caused coffee houses to be able to use cheaper coffee beans in their coffee.

## After:

- Gabriel de Clieu introduced coffee seedlings to Martinique in 1720, leading to the establishment of coffee cultivation in the Caribbean and significant production in Saint-Domingue by 1788.
- The French colonial coffee plantations relied on African slave labor, contributing to harsh conditions that fueled the Haitian Revolution and hindered the industry's recovery.
- Coffee cultivation spread to Brazil after Francisco de Melo Palheta acquired seeds in the 1720s, but significant growth did not occur until Brazil's independence in 1822.
- The coffee industry faced challenges during World War II, leading to a U.S.-Latin American agreement that doubled coffee prices and benefited producers.
- Brazil became the world's largest coffee producer by 1852, dominating global production until the emergence of other major producers like Colombia, Vietnam, and Ethiopia in the latter half of the 20th century.
- The rise of sugary coffee drinks has allowed coffee houses to use cheaper beans, impacting the quality and market dynamics of coffee.

## Use Case 2 - Extract Key Topics

**parameters**:  
_temperature=0.2,  
max_tokens=150_

system prompt:

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

**How was the prompt designed:**  
The extract_topics function treats the LLM as a "Content Analyzer." The key to this design is the Definition of a Topic section. By explicitly defining a topic as a "concise noun phrase," we prevent the model from outputting verbs or full sentences.

Specificity: It explicitly asks for specific terms (e.g., "Network Latency") rather than generic ones, ensuring high-quality tagging.

Semantic Merging: The prompt instructs the model to compare topics internally and merge synonyms (Cost vs. Price), reducing redundancy before the text is even generated.

**How Quality and Consistency Are Controlled:**  
_Strict Validation Logic:_  
Unlike simple summarization, topic extraction requires strict formatting.  
The Python code validates the output against three specific rules:

- Bullet Count: Must be between 3 and 7 lines.
- Word Count: Each line must contain only 1–3 words (regex-based check).
- Duplication: A set-based check ensures no exact duplicates exist (case-insensitive).

Automatic Retry Loop:  
If any validation fails, the function enters a retry loop (max 3 attempts).  
It constructs a dynamic fix_prompt that includes:

- The original text.
- The failed output.
- Specific Error Messages: It **explicitly** tells the LLM why it failed (e.g., "Output contained duplicate topics" or "These topics were too long"). This "critique-and-refine" approach forces the model to self-correct based on precise feedback.

Examples:
Example 1: Technical Support Analysis
Input Text:

"We are seeing a significant drop in packet delivery speeds during peak hours. The server logs indicate high latency in the US-East region, specifically interacting with the load balancer. Users are complaining about timeouts and slow page loads. We checked the database, but read/write IOPS are within normal limits. It seems to be purely a network layer issue."

Extracted Topics:

Network Latency

Packet Delivery

Load Balancer

Server Timeouts

US-East Region

Example 2: Health & Nutrition
Input Text:

"Regular cardiovascular exercise is essential for heart health, but nutrition plays an equally large role. Doctors recommend a diet rich in vegetables and low in saturated fats. Combining running with a balanced diet can significantly lower the risk of chronic disease and improve mental health."

Extracted Topics:

Heart Health

Cardiovascular Exercise

Nutrition

Balanced Diet

Chronic Disease

Mental Health

Example 3: Business/Financial
Input Text:

"The quarterly report shows a 15% increase in operational costs due to supply chain disruptions. However, revenue has grown by 10% thanks to the new subscription model. Investors are concerned about the shrinking profit margins, but the CEO assures that logistics will stabilize by Q3."

Extracted Topics:

Operational Costs

Supply Chain

Revenue Growth

Subscription Model

Profit Margins

Investor Concerns
