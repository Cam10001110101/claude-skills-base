
# Examples

```
Extract the context from the files in @/Users/cam/VAULT01/Clippings/2025/09-Sep
```

# Overview
- Goals: Extract the context from the files in specified location
- Allowed Tools: All
- Restricted Tools: N/A
- Expected Tool Use: 
	- Filesystem Tools
	- Web Search
	- Deepagents and subagents

# Rules
1. While working with container tools, only allow access to the container filesystem (/app), restrict local (/Users)
2.  As long as you're not actively working with container tools, only allow access to the local filesystem, restrict local filesystem

# Tips
- Perform work in batches to optimize context windows and asyncronous workflows and jobs

# Workflow
1. **Read the user’s request to determine the best next steps**
2. Confirm desired locations of input and output files
3. **Gather the source material**
    - List the files in the specified directories
    - Perform your work in batches, completing the full process for each file in sequence
    - Perform research if topics need additional context or references

4. **For each topic/document create a table‑style summary** (one row per topic).
    - The wording should be short, factual sentences, no fluff.
    - Keep the “TL;DR” section at the end that synthesizes the overall trend and highlights the most actionable business ideas.

5. **Formatting**
    - Use Markdown tables for the per‑topic details.
    - End with a plain‑text “TL;DR” bullet list.
    - Do **not** add extra sections, personal commentary, or unrelated content.
    - Include hyperlinks to sources when they're known

6. **Consistency checks**
    - Verify every topic from the directory appears once in the table.
    - Ensure the column headings match exactly


# Output, Deliverables, and Artifacts

| Aspect                         | Details |
| ------------------------------ | ------- |
| **Why it matters**             |         |
| **Unique points**              |         |
| **Impacted parties**           |         |
| **Hype vs. breakthrough**      |         |
| **Business opportunities**     |         |
| **Technical dependencies**     |         |
| **Cost Structure**             |         |
| **Risks & Limitations**        |         |
| **Implementation Timeline**    |         |
| **Key Metrics for Success**    |         |
| **Actionable Recommendations** |         |
| Questions an Expert Would Ask  |         |
| Action Items                   |         |
| Relevant Dates                 |         |
| Relevant People                |         |
| Relevant Organizations         |         |
| Relevant Products              |         |
| Relevant Interests             |         |
| Unanswered Questions           |         |
| Common Questions               |         |
| References and Links           |         |

```json
[  
	{ "Aspect": "Why it matters", "Details": "" },  
	{ "Aspect": "Unique points", "Details": "" },  
	{ "Aspect": "Impacted parties", "Details": "" },  
	{ "Aspect": "Hype vs. breakthrough", "Details": "" },  
	{ "Aspect": "Business opportunities", "Details": "" },  
	{ "Aspect": "Technical dependencies", "Details": "" },  
	{ "Aspect": "Cost Structure", "Details": "" },  
	{ "Aspect": "Risks & Limitations", "Details": "" },  
	{ "Aspect": "Implementation Timeline", "Details": "" },  
	{ "Aspect": "Key Metrics for Success", "Details": "" },  
	{ "Aspect": "Actionable Recommendations", "Details": "" },  
	{ "Aspect": "Questions an Expert Would Ask", "Details": "" },  
	{ "Aspect": "Action Items", "Details": "" },  
	{ "Aspect": "Relevant Dates", "Details": "" },  
	{ "Aspect": "Relevant People", "Details": "" },  
	{ "Aspect": "Relevant Organizations", "Details": "" },  
	{ "Aspect": "Relevant Products", "Details": "" },  
	{ "Aspect": "Relevant Interests", "Details": "" },  
	{ "Aspect": "Unanswered Questions", "Details": "" },  
	{ "Aspect": "Common Questions", "Details": "" }  
]
```