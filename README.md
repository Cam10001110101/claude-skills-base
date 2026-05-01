# Claude's Skills

A comprehensive collection of specialized skills and capabilities for Claude Code, Claude AI, and Claude API. 

## Quick Start (Claude Code)
  
```bash
/plugin marketplace add Cam10001110101/claude-skills-base
```

## 📁 Repository Structure

```
/mnt/skills
├── public/                      # Production-ready core skills
│   │
│   ├── docx/                    # Word document creation & editing
│   │   ├── SKILL.md             # Main documentation
│   │   ├── docx-js.md           # JavaScript library guide
│   │   ├── ooxml.md             # OOXML format reference
│   │   ├── ooxml/               # OOXML specifications
│   │   └── scripts/             # Helper utilities
│   │
│   ├── pdf/                     # PDF manipulation & forms
│   │   ├── SKILL.md             # Main documentation
│   │   ├── FORMS.md             # Form filling guide
│   │   ├── REFERENCE.md         # API reference
│   │   └── scripts/             # Helper utilities
│   │
│   ├── pptx/                    # PowerPoint presentation creation
│   │   ├── SKILL.md             # Main documentation
│   │   ├── html2pptx.md         # HTML to PowerPoint conversion
│   │   ├── css.md               # Styling guide
│   │   ├── ooxml.md             # OOXML format reference
│   │   ├── ooxml/               # OOXML specifications
│   │   └── scripts/             # Helper utilities
│   │
│   └── xlsx/                    # Excel spreadsheet creation
│       ├── SKILL.md             # Main documentation
│       └── recalc.py            # Formula recalculation
│
└── examples/                    # Specialized domain skills
    │
    ├── code-to-music/
    │   ├── SKILL.md
    │   ├── electronic-music-pipeline.md
    │   ├── traditional-music-pipeline.md
    │   └── scripts/             # MIDI rendering & utilities
    │
    └── music-generation/
        ├── SKILL.md
        └── scripts/             # Synthesizers, MIDI tools
            ├── drum_synthesizer.py
            └── melodic_synthesizer.py
```

## 🎯 About Agent Skills

This repository follows Anthropic's [Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) pattern. Agent Skills are modular packages that extend Claude's capabilities by providing domain-specific knowledge, instructions, and executable tools.

### How Skills Work

As Anthropic explains, "Claude is powerful, but real work requires procedural knowledge and organizational context." Skills transform general-purpose agents into specialized ones through **progressive disclosure**:

1. **Metadata Level**: Each skill includes a `SKILL.md` file with name and description, pre-loaded so Claude knows when to use it
2. **Core Content**: If relevant, Claude loads the full `SKILL.md` documentation
3. **Supplementary Files**: Additional references load only when needed

This keeps context efficient while allowing unbounded skill complexity.

## 🚀 Try in Claude Code, Claude.ai, and the API

### Claude Code

You can register this repository as a Claude Code Plugin from the marketplace by running the following command in Claude Code:

```
/plugin marketplace add Cam10001110101/claude-skills-base
```

After installing the plugin, you can use the skills by simply mentioning them. For example:

```
"use the pdf skill to extract the form fields from path/to/some-file.pdf"
"use the xlsx skill to create a financial model with formulas"
"use the pptx skill to create a presentation from this content"
```

### Claude.ai

Skills are available directly in Claude.ai conversations. Simply reference them when working with documents:

- Excel tasks are automatically handled with the xlsx skill
- PowerPoint creation uses the pptx skill
- PDF processing leverages the pdf skill
- Word documents use the docx skill

### Claude Agent SDK

Integrate skills into custom agent workflows using the Claude Agent SDK. Skills are automatically discovered and loaded when available in the agent's environment.

### API Integration

See the [API Integration section](#api-integration) below for details on using skills with the Claude Messages API.

For more information, see the [Agent Skills documentation](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) and [examples](https://github.com/anthropics/claude-cookbooks/tree/main/skills).

## 📊 How Skills Work in Practice

### PowerPoint Generation Flow

When you ask Claude to create a presentation, here's the automated workflow:

#### Step 1: User Input
Receive content request for presentation creation
```
Create a .pptx using this content: [EXAMPLE_CONTENT]
```

#### Step 2: Skill Discovery
Claude scans available PowerPoint skills and templates in the system
```bash
/mnt/skills/public/pptx/
├── SKILL.md              # Main documentation
├── pptxgenjs.md          # PptxGenJS library guide
├── ooxml.md              # OOXML format reference
└── scripts/              # PowerPoint utilities
```

#### Step 3: Documentation Review
Claude reads the PptxGenJS documentation to understand API and formatting options, reviewing:
- PptxGenJS API Reference
- OOXML Schemas
- Layout and styling options

#### Step 4: Code Generation
Claude creates a JavaScript file with presentation logic, styling, and content structure:

```javascript
const pptxgen = require("pptxgenjs");
const { renderToStaticMarkup } = require("react-dom/server");
const React = require("react");
const { FiFileText, FiDatabase, FiCpu } = require("react-icons/fi");
const sharp = require("sharp");

// Create presentation
let pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';
pres.author = 'Document Processing Solutions';
pres.title = 'Document Processing Pipelines & Automation';

// Color palette
const colors = {
  primary: "185087",     // Deep blue
  secondary: "2F9477",   // Teal
  accent: "F56D40",      // Orange
  text: "2C3E50",        // Dark gray
  white: "FFFFFF"
};

// Helper function to create icons
async function createIcon(IconComponent, color, size = 100) {
  const svgString = renderToStaticMarkup(
    React.createElement(IconComponent, {
      size, color: `#${color}`, strokeWidth: 2
    })
  );
  const buffer = await sharp(Buffer.from(svgString)).png().toBuffer();
  return `data:image/png;base64,${buffer.toString('base64')}`;
}

// Create slides
async function createPresentation() {
  const icons = await createAllIcons();

  // Slide 1: Title Slide
  let slide1 = pres.addSlide();
  slide1.background = { color: colors.primary };
  slide1.addText("Document Processing Pipelines", {
    x: 0.5, y: 1.5, w: 9, h: 1,
    fontSize: 48, bold: true, color: colors.white,
    fontFace: "Arial", align: "center"
  });

  // Add more slides with content, charts, and icons...

  // Save presentation
  await pres.writeFile({
    fileName: "/mnt/user-data/outputs/document_processing_pipelines.pptx"
  });
}

createPresentation().catch(console.error);
```

#### Step 5: Execution
Run the generated script to build the presentation
```bash
cd /home/claude && node create_presentation.js
# Output: Presentation created successfully!
```

#### Step 6: Verification
Confirm successful file creation and validate output
```bash
ls -lh /mnt/user-data/outputs/document_processing_pipelines.pptx
# Output: -rw-r--r-- 1 999 root 174K document_processing_pipelines.pptx
```

#### Final Output
**Professional presentation ready for delivery**: `document_processing_pipelines.pptx`

### Key Workflow Benefits

- **Automated Discovery**: Claude automatically finds and loads relevant skills
- **Documentation-Driven**: Skills include comprehensive guides for proper API usage
- **Code Generation**: Creates production-ready scripts with proper error handling
- **Quality Assurance**: Validates output and confirms successful creation

### API Integration

Skills can be used with the Claude Messages API through the code execution tool. For detailed implementation guidance, see the [Skills API Guide](https://docs.claude.com/en/api/skills-guide).

**Quick Start Example:**

```python
import anthropic

client = anthropic.Anthropic(api_key="your-api-key")

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    betas=["code-execution-2025-08-25", "skills-2025-10-02"],
    container={
        "skills": [
            {"type": "anthropic", "skill_id": "xlsx", "version": "latest"},
            {"type": "anthropic", "skill_id": "pptx", "version": "latest"}
        ]
    },
    messages=[
        {"role": "user", "content": "Create a financial spreadsheet with charts"}
    ],
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}]
)
```

**Key Points:**

- **Skills available**: `xlsx`, `docx`, `pptx`, `pdf` (use `"version": "latest"` or specific dates like `"20251013"`)
- **Up to 8 skills per request**: Mix and match skills as needed
- **Required beta headers**: `code-execution-2025-08-25`, `skills-2025-10-02`
- **Custom skills**: Upload your own skills (max 8MB) using the Skills API
- **No network access**: Skills run in a sandboxed environment

**Creating Custom Skills:**

```python
from anthropic.lib import files_from_dir

skill = client.beta.skills.create(
    display_title="Financial Analysis",
    files=files_from_dir("/path/to/skill"),
    betas=["skills-2025-10-02"]
)

# Use custom skill with its generated ID
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    betas=["code-execution-2025-08-25", "skills-2025-10-02"],
    container={
        "skills": [
            {"type": "custom", "skill_id": skill.id}
        ]
    },
    messages=[{"role": "user", "content": "Analyze quarterly financials"}],
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}]
)
```

---

# Document Suite (Public)

Production-ready skills for Microsoft Office documents and PDFs. These provide comprehensive Python and JavaScript/TypeScript toolkits for creating, editing, and analyzing professional documents.

## Features

### 📊 Excel (.xlsx)
- Create spreadsheets with formulas and formatting
- Preserve existing templates and styles
- Automatic formula recalculation via LibreOffice
- Financial modeling with industry-standard color coding
- Data analysis with pandas integration

### 📝 Word (.docx)
- Create professional documents with formatting
- Edit existing documents preserving structure
- Support for tracked changes and comments
- Text extraction with pandoc
- OOXML manipulation for advanced editing

### 🎯 PowerPoint (.pptx)
- Create presentations from scratch with PptxGenJS
- Template-based presentation generation
- Slide rearrangement and duplication
- Text replacement while preserving formatting
- Thumbnail grid generation for visual analysis
- OOXML editing for advanced modifications

### 📄 PDF
- Fill fillable PDF forms programmatically
- Add text annotations to non-fillable PDFs
- Extract tables and text content
- Merge, split, and rotate PDFs
- OCR support for scanned documents
- Convert PDFs to images

## Installation (Core Skills)

### System Requirements

```bash
# Linux/Ubuntu
sudo apt-get install libreoffice poppler-utils pandoc

# macOS
brew install libreoffice poppler pandoc
```

### Python Dependencies

```bash
pip install openpyxl pandas pypdf pdfplumber reportlab pytesseract pdf2image markitdown
```

### JavaScript Dependencies

```bash
npm install -g pptxgenjs docx-js
```

## Quick Start

### Excel - Create a Financial Model

```python
from openpyxl import Workbook
from openpyxl.styles import Font

wb = Workbook()
sheet = wb.active

# Add headers
sheet['A1'] = 'Revenue'
sheet['A1'].font = Font(bold=True)

# Add data with formulas
sheet['B1'] = 2024
sheet['C1'] = 2025
sheet['B2'] = 1000000
sheet['C2'] = '=B2*1.1'  # 10% growth formula

wb.save('financial_model.xlsx')

# Recalculate formulas
# python xlsx/recalc.py financial_model.xlsx
```

### PowerPoint - Create from Template

```bash
# 1. Analyze template
python pptx/scripts/thumbnail.py template.pptx

# 2. Rearrange slides (0-indexed)
python pptx/scripts/rearrange.py template.pptx working.pptx 0,5,5,12

# 3. Extract text inventory
python pptx/scripts/inventory.py working.pptx inventory.json

# 4. Replace text (create replacement.json first)
python pptx/scripts/replace.py working.pptx replacement.json final.pptx
```

### PDF - Fill a Form

```bash
# 1. Check if form is fillable
python pdf/scripts/check_fillable_fields.py form.pdf

# 2. Extract field information
python pdf/scripts/extract_form_field_info.py form.pdf fields.json

# 3. Edit fields.json with your data

# 4. Fill the form
python pdf/scripts/fill_fillable_fields.py form.pdf fields.json filled.pdf
```

### Word - Extract Content

```bash
# Extract text with tracked changes
pandoc --track-changes=all document.docx -o content.md

# For XML manipulation
python pptx/ooxml/scripts/unpack.py document.docx unpacked/
# Edit XML files
python pptx/ooxml/scripts/validate.py unpacked/ --original document.docx
python pptx/ooxml/scripts/pack.py unpacked/ modified.docx
```

## Project Structure

```
├── xlsx/                 # Excel tools
│   ├── recalc.py        # Formula recalculation
│   └── SKILL.md         # Excel documentation
│
├── docx/                 # Word tools
│   ├── ooxml.md         # OOXML documentation
│   └── SKILL.md         # Word documentation
│
├── pptx/                 # PowerPoint tools
│   ├── scripts/         # PowerPoint utilities
│   │   ├── thumbnail.py # Create slide thumbnails
│   │   ├── rearrange.py # Reorder slides
│   │   ├── inventory.py # Extract text inventory
│   │   └── replace.py   # Replace text content
│   ├── ooxml/           # OOXML utilities
│   │   └── scripts/     
│   │       ├── unpack.py   # Unpack Office files
│   │       ├── validate.py # Validate XML
│   │       └── pack.py     # Pack to Office format
│   ├── pptxgenjs.md     # PptxGenJS documentation
│   └── SKILL.md         # PowerPoint documentation
│
└── pdf/                  # PDF tools
    ├── scripts/         # PDF utilities
    │   ├── check_fillable_fields.py
    │   ├── extract_form_field_info.py
    │   ├── fill_fillable_fields.py
    │   └── convert_pdf_to_images.py
    ├── FORMS.md         # PDF forms documentation
    └── SKILL.md         # PDF documentation
```

## Advanced Usage

### Excel Formula Best Practices

Always use formulas instead of hardcoded values:

```python
# ❌ Wrong - Hardcoded calculation
total = sum([100, 200, 300])
sheet['A4'] = total  # Hardcodes 600

# ✅ Correct - Excel formula
sheet['A4'] = '=SUM(A1:A3)'  # Dynamic formula
```

After adding formulas, always recalculate:

```bash
python xlsx/recalc.py spreadsheet.xlsx
```

### PowerPoint Template Workflow

1. **Visual Analysis**: Create thumbnail grid to understand layout
2. **Structure Planning**: Map content to appropriate slide templates
3. **Slide Selection**: Use rearrange.py to duplicate and order slides
4. **Content Replacement**: Use inventory.py and replace.py for text updates

### PDF Form Types

- **Fillable Forms**: Use `fill_fillable_fields.py` for forms with interactive fields
- **Visual Forms**: Use `fill_pdf_form_with_annotations.py` for static forms requiring text overlay

### OOXML Editing

For advanced document manipulation:

1. Unpack the Office file to access XML
2. Edit XML carefully (maintain schema compliance)
3. Validate changes before repacking
4. Pack back to Office format

## Common Tasks

### Merge PDFs

```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
for pdf_file in ["doc1.pdf", "doc2.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)

with open("merged.pdf", "wb") as output:
    writer.write(output)
```

### Extract Tables from PDF

```python
import pdfplumber
import pandas as pd

with pdfplumber.open("document.pdf") as pdf:
    tables = []
    for page in pdf.pages:
        for table in page.extract_tables():
            if table:
                df = pd.DataFrame(table[1:], columns=table[0])
                tables.append(df)
    
    if tables:
        combined = pd.concat(tables, ignore_index=True)
        combined.to_excel("extracted_tables.xlsx", index=False)
```

### Create PowerPoint with JavaScript

```javascript
import pptxgen from "pptxgenjs";

let pres = new pptxgen();
let slide = pres.addSlide();

slide.addText("Hello World", {
    x: 1,
    y: 1,
    w: 8,
    h: 2,
    fontSize: 44,
    bold: true,
    color: "363636"
});

pres.writeFile({ fileName: "presentation.pptx" });
```

## Troubleshooting

### Excel Formula Errors

If `recalc.py` reports errors:
- `#REF!`: Check cell references
- `#DIV/0!`: Add zero checks
- `#VALUE!`: Verify data types
- `#NAME?`: Check formula syntax

### PowerPoint XML Validation

Always validate after XML edits:
```bash
python pptx/ooxml/scripts/validate.py edited/ --original template.pptx
```

### PDF Coordinate Systems

Remember coordinate transformation:
- Image coordinates: origin at top-left
- PDF coordinates: origin at bottom-left

# Specialized Skills (Examples)

Domain-specific example skills bundled with this repo.

## 🎵 Media & Communication

### code-to-music
- Convert code structures to musical compositions
- Algorithm sonification
- Pattern-based music generation

### music-generation
- Procedural music composition
- MIDI generation and manipulation
- Audio synthesis workflows

## 🔧 Skill Architecture

All skills follow a standardized structure:

```
skill-name/
├── SKILL.md              # Primary documentation and instructions
├── examples/             # Usage examples and templates
├── utils/                # Helper functions and utilities
└── tests/                # Validation and test cases
```

### SKILL.md Format

Every skill includes comprehensive documentation:

1. **Overview** - Purpose and capabilities
2. **Prerequisites** - Required tools and dependencies
3. **Usage Instructions** - Step-by-step workflows
4. **Best Practices** - Optimization tips and patterns
5. **Examples** - Real-world use cases
6. **Troubleshooting** - Common issues and solutions

## 💡 Design Philosophy

### Modularity
Each skill is self-contained and focused on a specific domain, enabling composition and reuse.

### Best Practices First
Skills encode proven workflows developed through extensive testing and iteration.

### Quality Over Speed
Prioritize professional-quality outputs over quick-and-dirty solutions.

### Progressive Enhancement
Start with simple use cases and progressively handle complex scenarios.

---

## 📚 References & Resources

### Documentation
- [Agent Skills Documentation](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) - Official Anthropic documentation
- [Skills API Guide](https://docs.claude.com/en/api/skills-guide) - API integration guide
- [Agent Skills Blog Post](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) - Equipping agents for the real world
- [Claude Cookbooks - Skills](https://github.com/anthropics/claude-cookbooks/tree/main/skills) - Examples and tutorials

### Source Files
- `Process Flow.md` - Detailed workflow example for PowerPoint generation
- `example-skils-flow-diagram.html` - Visual flow diagram for skill execution
- `CLAUDE.md` - Development guidance for this repository

### Core Skill Documentation
Each skill includes comprehensive documentation in its `SKILL.md` file:
- `/mnt/skills/public/xlsx/SKILL.md` - Excel spreadsheet creation
- `/mnt/skills/public/docx/SKILL.md` - Word document processing
- `/mnt/skills/public/pptx/SKILL.md` - PowerPoint presentation creation
- `/mnt/skills/public/pdf/SKILL.md` - PDF manipulation

### Additional Resources
- **Office Open XML**: Format specifications in `/mnt/skills/public/*/ooxml/`
- **Reference Guides**: Format-specific guides (FORMS.md, REFERENCE.md, html2pptx.md, etc.)
- **Example Skills**: 15+ specialized skills in `/mnt/skills/examples/`

---