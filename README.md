# Office Suite Toolkit

A comprehensive Python and JavaScript/TypeScript toolkit for creating, editing, and analyzing Microsoft Office documents (Word, Excel, PowerPoint) and PDFs.

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

## Installation

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

## Contributing

This toolkit was originally part of Claude Desktop's interpreter skills repository. Contributions and improvements are welcome.

## License

See individual script headers for licensing information.

## Support

For detailed documentation on specific features:
- Excel: See `xlsx/SKILL.md`
- Word: See `docx/SKILL.md`
- PowerPoint: See `pptx/SKILL.md`
- PDF: See `pdf/SKILL.md` and `pdf/FORMS.md`