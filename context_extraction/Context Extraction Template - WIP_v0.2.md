

## Overview

- **Goal:** Extract and summarize topics from files located at specified location.
    
- **Allowed Tools:** Filesystem (read-only for local), Container tools (processing & artifact creation: `.docx`, `.xlsx`, `.pptx`, `.pdf`).
    
- **Disallowed:** Any network I/O unless explicitly required by “Research” (see Research Rules).
    

## Operating Constraints

1. **Filesystem scope**
    
    - **Local:** Use 'Filesystem' tools
	    - 
        
    - **Container:** All read/write must happen under `/app`.
        
        - **Outputs directory:** `/app/out` (create if missing). Never access `/Users` from inside the container.
            
2. **Session model**
    
    - Perform work **synchronously** within the current session.
        
    - **Batching is allowed** (chunk files into groups to fit context limits) but **no background/async jobs after the response**.
        
3. **Time & locale**
    
    - Timezone: **America/Chicago**.
        
    - Dates in output: **YYYY-MM-DD**.
        
4. **Size limits & fallbacks**
    
    - Max file size to parse: **25 MB** each. If larger, record the filename and reason in a “Skipped Files” note and continue.
        
    - Non-text binaries without parsers should be listed with `Status=Unparsed`.
        

## Inputs & Outputs

- **Input directory (required):** `@/Users/cam/VAULT01/Clippings/2025/09-Sep`
    
- **Output artifacts (write to `/app/out`):**
    
    1. `summary_table.md` — Markdown table (one row per topic) followed by a TL;DR bullet list.
        
    2. `summary_table.json` — Array of `{ "Aspect": "...", "Details": "..." }` objects per topic, matching the schema below.
        
    3. `process_log.jsonl` — One JSON line per file processed (`{timestamp, file, status, bytes, parser, errors[]}`).
        
    4. `skipped_files.csv` — Filename and reason.
        

## File Handling

- **Allowed extensions (case-insensitive):** `.txt, .md, .rtf, .html, .pdf, .docx, .pptx, .xlsx, .csv, .json, .yaml, .yml`
    
- **Parsing priority (per file):** text → markdown → HTML → PDF → Office formats → CSV/JSON/YAML.
    
- **Encoding:** Try UTF-8; if decode fails, attempt BOM detection; else mark as `Unparsed`.
    

## Workflow

1. **Plan**
    
    - Read the user request and confirm input/output paths as specified above. If the input path is missing, **stop** and report.
        
2. **Inventory**
    
    - Recursively list files under the input directory; sort deterministically by `relative_path, then filename`.
        
3. **Batching**
    
    - Process files in batches sized to fit context; complete the full extract→summarize→append cycle per batch before moving on.
        
4. **Extraction**
    
    - Derive **topics** from headings, titles, filenames, and salient terms. Normalize topic names (lowercase, trim, collapse whitespace).
        
    - Generate a **stable Topic ID**: `sha1(relative_path + first_200_chars_of_text)`; reuse it across re-runs to avoid duplicates.
        
5. **Per-topic synthesis**
    
    - Populate every required **Aspect** below with short, factual sentences. If unknown, use `N/A` (do **not** hallucinate).
        
    - When a source URL is explicitly present in the file, include it; otherwise don’t invent links.
        
6. **Consistency checks**
    
    - Ensure **every detected topic** appears **exactly once** in the table.
        
    - Verify column headers match **exactly** (see Formatting).
        
    - Cross-check counts: `#topics == #unique Topic IDs`.
        
7. **Finalize**
    
    - Write all artifacts to `/app/out`.
        
    - In the chat response: provide a brief summary of counts (files scanned, parsed, skipped; topics found) and list the artifact paths.
        

## Research Rules (optional)

- Default: **No external browsing**.
    
- If a topic **requires external context**, explicitly mark a “Research used” flag for that topic and include a citation; otherwise leave aspects as `N/A`. Never leak private file contents to external tools.
    

## Formatting

- **Markdown Table (per-topic row):** Columns **exactly** in this order:  
    `Aspect | Details`
    
- **Rows (exactly these, in this order):**
    
    1. Why it matters
        
    2. Unique points
        
    3. Impacted parties
        
    4. Hype vs. breakthrough
        
    5. Business opportunities
        
    6. Technical dependencies
        
    7. Cost Structure
        
    8. Risks & Limitations
        
    9. Implementation Timeline
        
    10. Key Metrics for Success
        
    11. Actionable Recommendations
        
    12. Questions an Expert Would Ask
        
    13. Action Items
        
    14. Relevant Dates
        
    15. Relevant People
        
    16. Relevant Organizations
        
    17. Relevant Products
        
    18. Relevant Interests
        
    19. Unanswered Questions
        
    20. Common Questions
        
    21. References and Links
        
- **TL;DR:** End with a **plain-text** bullet list summarizing overall trends and the most actionable business ideas.
    

## JSON Schema (lock this)

Each topic exports a JSON array **in this exact order**:

```json
[
  {"Aspect":"Why it matters","Details":""},
  {"Aspect":"Unique points","Details":""},
  {"Aspect":"Impacted parties","Details":""},
  {"Aspect":"Hype vs. breakthrough","Details":""},
  {"Aspect":"Business opportunities","Details":""},
  {"Aspect":"Technical dependencies","Details":""},
  {"Aspect":"Cost Structure","Details":""},
  {"Aspect":"Risks & Limitations","Details":""},
  {"Aspect":"Implementation Timeline","Details":""},
  {"Aspect":"Key Metrics for Success","Details":""},
  {"Aspect":"Actionable Recommendations","Details":""},
  {"Aspect":"Questions an Expert Would Ask","Details":""},
  {"Aspect":"Action Items","Details":""},
  {"Aspect":"Relevant Dates","Details":""},
  {"Aspect":"Relevant People","Details":""},
  {"Aspect":"Relevant Organizations","Details":""},
  {"Aspect":"Relevant Products","Details":""},
  {"Aspect":"Relevant Interests","Details":""},
  {"Aspect":"Unanswered Questions","Details":""},
  {"Aspect":"Common Questions","Details":""},
  {"Aspect":"References and Links","Details":""}
]
```

## Quality & Safety

- **No hallucination:** If the file doesn’t support a detail, use `N/A`.
    
- **PII & secrets:** Never include passwords, API keys, or private emails in outputs.
    
- **Determinism:** Stable sort, stable Topic IDs, idempotent re-runs (no duplicate rows).
    
- **Logging:** Record errors and skips; do not fail the entire run due to one file.
    

## Success Criteria

- All artifacts created in the desired location.
    
- Every topic represented once; headers match exactly.
    
- TL;DR is concise, actionable, and grounded in the extracted topics.
    
- `process_log.jsonl` shows each file with `status ∈ {parsed, skipped, unparsed}`.
---
