# LLMTextAnalysis

Use Case 1 - Summarize Long Text  
How the Prompt Was Designed

The summarize_text function uses a system prompt to instruct the LLM as an expert editor:

It tells the model to produce a clear and concise bulleted summary.

Constraints explicitly specify 3 to 6 bullets to control summary size.

It emphasizes capturing main ideas, key conclusions, and important facts, guiding content selection.

For example, the system prompt includes:

You are an expert editor. Please provide a clear, concise summary of the following text.

Constraints:

- The output must be a bulleted list.
- It must have between 3 and 6 bullet points.
- Capture the main ideas, key conclusions and Important facts.

This ensures the LLM focuses on relevant points rather than writing a free-form summary.

How Length and Verbosity Are Controlled

Bullet Count:

A regex checks that the summary has 3–6 bullets.

If the output has too few or too many bullets, the function retries by sending the previous summary plus the original text back to the model with instructions to fix it.

Token Limit:

max_tokens=300 ensures the output does not exceed a manageable length.

Temperature:

temperature=0.3 keeps the output deterministic and concise, avoiding overly verbose or creative responses.

Context Feedback Loop:

By including the original text and previous attempt when retrying, the model can adjust its summary while respecting the bullet and length constraints.

This combination of prompt constraints, regex validation, token limit, and low temperature effectively controls both length and verbosity while maintaining clarity.

## Before:

### System prompt

You are an expert editor. Please provide a clear, concise summary of the following text.

Constraints:

- The output must be a bulleted list.
- It must have between 3 and 6 bullet points.
- Capture the main ideas, key conclusions and Important facts.

### Text input:

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
