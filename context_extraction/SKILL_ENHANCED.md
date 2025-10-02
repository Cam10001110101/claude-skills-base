# Enhanced Context Extraction & Analysis Skill
## Version 2.0 - With Comprehensive Table Generation

---

## 1) Overview

**Goal**  
Reliably **extract, synthesize, and analyze context** from a set of files, producing:

- A concise TL;DR
- A normalized outline of topics (deduplicated)
- **A comprehensive analysis table with 20+ analytical dimensions**
- An inventory of processed files with statuses
- Reusable artifacts (markdown summaries, JSON/CSV inventories)

**Scope**  
Local files and containerized workspaces with multi-dimensional business analysis.

**Key Enhancement**  
**Structured table analysis** with columns for business impact, technical dependencies, timelines, metrics, and actionable insights.

---

## 2) Required Output Artifacts

### PRIMARY OUTPUTS (MANDATORY)

1. **`analysis_table.md`** - Comprehensive markdown table with these columns:
   - File (topic)
   - Why it matters
   - Unique points
   - Impacted parties
   - Hype vs breakthrough
   - Business opportunities
   - Technical dependencies
   - Cost structure
   - Risks & limitations
   - Implementation timeline
   - Key metrics for success
   - Actionable recommendations
   - Expert questions
   - Action items
   - Relevant dates
   - Relevant people
   - Relevant orgs
   - Relevant products
   - Relevant interests
   - Unanswered questions
   - Common questions

2. **`tldr.md`** - Executive summary with:
   - 5-10 key takeaways
   - Business opportunities section
   - Immediate action items
   - Critical trends analysis

3. **`topics.md`** - Hierarchical outline with source citations

4. **`inventory.csv`** and **`inventory.json`** - File processing metadata

5. **`process_log.jsonl`** - Detailed processing log

---

## 3) Table Generation Rules

### Column Definitions & Analysis Guidelines

| Column | Purpose | Analysis Approach |
|--------|---------|------------------|
| **File (topic)** | Primary subject with date | Extract main theme + timestamp |
| **Why it matters** | Business/strategic significance | Focus on ROI, market impact, competitive advantage |
| **Unique points** | Differentiating features | List 3-5 key innovations or distinctions |
| **Impacted parties** | Stakeholders affected | Identify users, teams, departments, customers |
| **Hype vs breakthrough** | Reality assessment | Classify as: Hype, Incremental, or **Breakthrough** |
| **Business opportunities** | Revenue/efficiency potential | Specific monetization strategies, cost savings |
| **Technical dependencies** | Required infrastructure | List tools, frameworks, platforms, APIs |
| **Cost structure** | Financial model | Pricing tiers, licensing, TCO estimates |
| **Risks & limitations** | Challenges and constraints | Technical, regulatory, market, adoption risks |
| **Implementation timeline** | Deployment schedule | Phases with specific quarters/dates |
| **Key metrics for success** | KPIs to track | Quantifiable measurements (%, $, time) |
| **Actionable recommendations** | Next steps | Specific, executable tasks |
| **Expert questions** | Critical unknowns | Questions requiring specialist input |
| **Action items** | Immediate tasks | Bullet list of concrete steps |
| **Relevant dates** | Timeline markers | Release dates, deadlines, milestones |
| **Relevant people** | Key individuals | Authors, maintainers, stakeholders |
| **Relevant orgs** | Organizations involved | Companies, teams, departments |
| **Relevant products** | Tools/services mentioned | Software, platforms, frameworks |
| **Relevant interests** | Domain areas | Tags for categorization |
| **Unanswered questions** | Knowledge gaps | Open issues requiring research |
| **Common questions** | FAQ items | Anticipated user questions |

### Analysis Depth Requirements

- **Quantify when possible**: Use specific numbers, percentages, dollar amounts
- **Be prescriptive**: Provide specific recommendations, not generic advice
- **Identify breakthrough vs hype**: Use bold for **Breakthrough** items
- **Connect dots**: Link related items across different files
- **Business focus**: Always include revenue/cost/efficiency angles

---

## 4) Processing Pipeline

### Phase 1: Discovery & Extraction
1. Scan source_path with filters
2. Extract content per file type
3. Identify metadata (dates, authors, versions)

### Phase 2: Analysis & Synthesis
1. **Deep content analysis** for each file:
   - Extract technical specifications
   - Identify business implications
   - Map dependencies and requirements
   - Assess maturity and readiness
   
2. **Cross-file synthesis**:
   - Find common themes
   - Identify contradictions
   - Build dependency graphs
   - Create timeline overlays

### Phase 3: Table Generation
1. **Row creation** - One row per major topic/file
2. **Column population** - Fill all 21 columns with specific analysis
3. **Quality checks**:
   - No empty cells (use "—" if not applicable)
   - Consistent formatting
   - Actionable content in recommendation columns
   - Dates in ISO format where applicable

### Phase 4: Summary Generation
1. **TL;DR with business focus**:
   ```markdown
   ### TL;DR – Key Trends & Actionable Business Ideas
   - **Trend 1** with specific opportunity
   - **Trend 2** with ROI estimate
   - ...
   
   **Immediate actions for a business:**
   1. Specific integration step
   2. Pilot program definition
   3. Metric tracking setup
   ```

2. **Topics outline** with source traceability

---

## 5) Quality Standards

### Table Quality Checklist
- [ ] Every row has all 21 columns filled
- [ ] Business opportunities include specific revenue/cost figures where possible
- [ ] Technical dependencies list actual tools/versions
- [ ] Timelines use specific quarters/dates (Q4 2025, not "soon")
- [ ] Action items are executable (start with verbs)
- [ ] Hype vs breakthrough assessment is justified
- [ ] Risks are specific, not generic
- [ ] Metrics are quantifiable

### Content Quality Rules
- **Specificity over generality**: "Deploy Prometheus + Grafana for metrics" not "Set up monitoring"
- **Business value focus**: Always connect technical details to business impact
- **Actionability**: Every recommendation must be implementable
- **Traceability**: Link assertions to specific source files

---

## 6) Configuration Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `source_path` | string | — | Root directory to scan |
| `output_comprehensive_table` | boolean | `true` | Generate full 21-column analysis table |
| `business_analysis_depth` | string | `deep` | Level of business analysis (basic/deep/expert) |
| `include_roi_estimates` | boolean | `true` | Calculate ROI where data available |
| `cross_reference_topics` | boolean | `true` | Link related items across files |
| `generate_exec_summary` | boolean | `true` | Create executive-level TL;DR |
| `max_rows_per_table` | integer | `50` | Maximum table rows before splitting |

---

## 7) Example Output Structure

```
./out/
  analysis_table.md         # Primary comprehensive table
  analysis_table.csv        # CSV version for spreadsheet import
  tldr.md                   # Executive summary with business focus
  topics.md                 # Hierarchical topic outline
  inventory.csv             # File processing metadata
  inventory.json            # JSON metadata
  process_log.jsonl         # Detailed processing log
  errors.md                 # Issues and resolutions
  samples/                  # Reference excerpts
```

---

## 8) Table Formatting Example

```markdown
| File (topic) | Why it matters | Unique points | ... | Action items |
|--------------|----------------|---------------|-----|--------------|
| **Ollama Turbo FAQ (2025-09-01)** | Shows how Ollama is adding datacenter-grade acceleration to open-source models, a key step for enterprise-scale LLM use. | "Turbo" mode, US-hosted hardware, preview models (gpt-oss 20B/120B) | ... | Enable `OLLAMA_HOST=ollama.com`; create API-key; test with target models |
```

---

## 9) Error Handling for Table Generation

| Error Type | Handling | Table Cell Value |
|------------|----------|------------------|
| Missing data | Note in cell | "Not specified" |
| Parsing failure | Log and continue | "Parse error - see log" |
| Contradictory info | Note both versions | "Conflicting: A vs B" |
| Future dates | Validate and flag | "Future: YYYY-MM-DD" |
| Large content | Summarize | "See appendix for details" |

---

## 10) Research Integration Rules

When `allow_research=true`:
- Fill knowledge gaps in table cells
- Verify technical specifications
- Add market size/growth estimates
- Include competitive landscape info
- Cite all external sources

---

## 11) Validation Requirements

### Table Validation
- [ ] All cells populated (no blanks)
- [ ] Dates properly formatted
- [ ] Dollar amounts include currency
- [ ] Percentages clearly marked
- [ ] All acronyms defined on first use
- [ ] Cross-references use consistent naming

### Business Analysis Validation
- [ ] Every item has clear business impact
- [ ] ROI estimates are justified
- [ ] Timelines are realistic
- [ ] Dependencies are complete
- [ ] Risks have mitigation strategies

---

## 12) Performance Optimizations

- **Parallel processing** for multi-file analysis
- **Incremental table building** to avoid memory issues
- **Column width optimization** for readability
- **Smart truncation** for long content with appendix references
- **Caching** for repeated analysis runs

---

## 13) Key Differentiator

This enhanced skill **ALWAYS generates the comprehensive analysis table** as its primary output. The table is not optional—it's the core value proposition that transforms raw context extraction into actionable business intelligence.

**Critical Success Factor**: The analysis table must provide immediate business value by answering:
- What should we build/buy/integrate?
- What's the ROI and timeline?
- What are the technical requirements?
- What are the risks and how do we mitigate them?
- What specific actions should we take today?

---

## END OF SKILL DEFINITION