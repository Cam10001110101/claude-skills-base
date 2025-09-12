# Office Open XML Technical Reference

**Important: Read this entire document before starting.** Critical XML schema rules and formatting requirements are covered throughout. Incorrect implementation can create invalid DOCX files that Word cannot open.

## Technical Guidelines

### Schema Compliance
- **Element ordering in `<w:pPr>`**: `<w:pStyle>`, `<w:numPr>`, `<w:spacing>`, `<w:ind>`, `<w:jc>`
- **Whitespace**: Add `xml:space='preserve'` to `<w:t>` elements with leading/trailing spaces
- **Unicode**: Escape characters in ASCII content: `"` becomes `&#8220;`
- **Tracked changes**: Use `<w:del>` and `<w:ins>` tags with `w:author="Claude"` outside `<w:r>` elements
  - **Critical**: `<w:ins>` closes with `</w:ins>`, `<w:del>` closes with `</w:del>` - never mix
  - **RSIDs must be 8-digit hex**: Use values like `00AB1234` (only 0-9, A-F characters)
  - **trackRevisions placement**: Add `<w:trackRevisions/>` after `<w:proofState>` in settings.xml
- **Images**: Add to `word/media/`, reference in `document.xml`, set dimensions to prevent overflow

## Document Content Patterns

### Basic Structure
```xml
<w:p>
  <w:r><w:t>Text content</w:t></w:r>
</w:p>
```

### Headings and Styles
```xml
<w:p>
  <w:pPr>
    <w:pStyle w:val="Title"/>
    <w:jc w:val="center"/>
  </w:pPr>
  <w:r><w:t>Document Title</w:t></w:r>
</w:p>

<w:p>
  <w:pPr><w:pStyle w:val="Heading2"/></w:pPr>
  <w:r><w:t>Section Heading</w:t></w:r>
</w:p>
```

### Text Formatting
```xml
<!-- Bold -->
<w:r><w:rPr><w:b/><w:bCs/></w:rPr><w:t>Bold</w:t></w:r>
<!-- Italic -->
<w:r><w:rPr><w:i/><w:iCs/></w:rPr><w:t>Italic</w:t></w:r>
<!-- Underline -->
<w:r><w:rPr><w:u w:val="single"/></w:rPr><w:t>Underlined</w:t></w:r>
<!-- Highlight -->
<w:r><w:rPr><w:highlight w:val="yellow"/></w:rPr><w:t>Highlighted</w:t></w:r>
```

### Lists
```xml
<!-- Numbered list -->
<w:p>
  <w:pPr>
    <w:pStyle w:val="ListParagraph"/>
    <w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr>
    <w:spacing w:before="240"/>
  </w:pPr>
  <w:r><w:t>First item</w:t></w:r>
</w:p>

<!-- Restart numbered list at 1 - use different numId -->
<w:p>
  <w:pPr>
    <w:pStyle w:val="ListParagraph"/>
    <w:numPr><w:ilvl w:val="0"/><w:numId w:val="2"/></w:numPr>
    <w:spacing w:before="240"/>
  </w:pPr>
  <w:r><w:t>New list item 1</w:t></w:r>
</w:p>

<!-- Bullet list (level 2) -->
<w:p>
  <w:pPr>
    <w:pStyle w:val="ListParagraph"/>
    <w:numPr><w:ilvl w:val="1"/><w:numId w:val="1"/></w:numPr>
    <w:spacing w:before="240"/>
    <w:ind w:left="900"/>
  </w:pPr>
  <w:r><w:t>Bullet item</w:t></w:r>
</w:p>
```

### Tables
```xml
<w:tbl>
  <w:tblPr>
    <w:tblStyle w:val="TableGrid"/>
    <w:tblW w:w="0" w:type="auto"/>
  </w:tblPr>
  <w:tblGrid>
    <w:gridCol w:w="4675"/><w:gridCol w:w="4675"/>
  </w:tblGrid>
  <w:tr>
    <w:tc>
      <w:tcPr><w:tcW w:w="4675" w:type="dxa"/></w:tcPr>
      <w:p><w:r><w:t>Cell 1</w:t></w:r></w:p>
    </w:tc>
    <w:tc>
      <w:tcPr><w:tcW w:w="4675" w:type="dxa"/></w:tcPr>
      <w:p><w:r><w:t>Cell 2</w:t></w:r></w:p>
    </w:tc>
  </w:tr>
</w:tbl>
```

### Layout
```xml
<!-- Page break -->
<w:p><w:r><w:br w:type="page"/></w:r></w:p>

<!-- Centered paragraph -->
<w:p>
  <w:pPr>
    <w:spacing w:before="240" w:after="0"/>
    <w:jc w:val="center"/>
  </w:pPr>
  <w:r><w:t>Centered text</w:t></w:r>
</w:p>

<!-- Font change - paragraph level (applies to all runs) -->
<w:p>
  <w:pPr>
    <w:rPr><w:rFonts w:ascii="Courier New" w:hAnsi="Courier New"/></w:rPr>
  </w:pPr>
  <w:r><w:t>Monospace text</w:t></w:r>
</w:p>

<!-- Font change - run level (specific to this text) -->
<w:p>
  <w:r>
    <w:rPr><w:rFonts w:ascii="Courier New" w:hAnsi="Courier New"/></w:rPr>
    <w:t>This text is Courier New</w:t>
  </w:r>
  <w:r><w:t> and this text uses default font</w:t></w:r>
</w:p>
```

## File Updates

When adding content, update these files:

**`word/_rels/document.xml.rels`:**
```xml
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>
<Relationship Id="rId5" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image1.png"/>
```

**`[Content_Types].xml`:**
```xml
<Default Extension="png" ContentType="image/png"/>
<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
```

### Images
**CRITICAL**: Calculate dimensions to prevent page overflow and maintain aspect ratio.

```xml
<!-- Minimal required structure -->
<w:p>
  <w:r>
    <w:drawing>
      <wp:inline>
        <wp:extent cx="2743200" cy="1828800"/>
        <wp:docPr id="1" name="Picture 1"/>
        <a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
          <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
            <pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
              <pic:nvPicPr>
                <pic:cNvPr id="0" name="image1.png"/>
                <pic:cNvPicPr/>
              </pic:nvPicPr>
              <pic:blipFill>
                <a:blip r:embed="rId5"/>
                <!-- Add for stretch fill with aspect ratio preservation -->
                <a:stretch>
                  <a:fillRect/>
                </a:stretch>
              </pic:blipFill>
              <pic:spPr>
                <a:xfrm>
                  <a:ext cx="2743200" cy="1828800"/>
                </a:xfrm>
                <a:prstGeom prst="rect"/>
              </pic:spPr>
            </pic:pic>
          </a:graphicData>
        </a:graphic>
      </wp:inline>
    </w:drawing>
  </w:r>
</w:p>
```

### Links (Hyperlinks)

**IMPORTANT**: All hyperlinks (both internal and external) require the Hyperlink style to be defined in styles.xml. Without this style, links will look like regular text instead of blue underlined clickable links.

**External Links:**
```xml
<!-- In document.xml -->
<w:hyperlink r:id="rId5">
  <w:r>
    <w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr>
    <w:t>Link Text</w:t>
  </w:r>
</w:hyperlink>

<!-- In word/_rels/document.xml.rels -->
<Relationship Id="rId5" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" 
              Target="https://www.example.com/" TargetMode="External"/>
```

**Internal Links:**

```xml
<!-- Link to bookmark -->
<w:hyperlink w:anchor="myBookmark">
  <w:r>
    <w:rPr><w:rStyle w:val="Hyperlink"/></w:rPr>
    <w:t>Link Text</w:t>
  </w:r>
</w:hyperlink>

<!-- Bookmark target -->
<w:bookmarkStart w:id="0" w:name="myBookmark"/>
<w:r><w:t>Target content</w:t></w:r>
<w:bookmarkEnd w:id="0"/>
```

**Hyperlink Style (required in styles.xml):**
```xml
<w:style w:type="character" w:styleId="Hyperlink">
  <w:name w:val="Hyperlink"/>
  <w:basedOn w:val="DefaultParagraphFont"/>
  <w:uiPriority w:val="99"/>
  <w:unhideWhenUsed/>
  <w:rPr>
    <w:color w:val="467886" w:themeColor="hyperlink"/>
    <w:u w:val="single"/>
  </w:rPr>
</w:style>
```

## Tracked Changes (Redlining)

When adding tracked changes to documents, you need to enable change tracking and use specific XML structures for insertions and deletions. **Always use `w:author="Claude"` for all tracked changes.**

### Validation Rules
The validator checks that the document text matches the original after reverting Claude's changes. This means:
- **NEVER modify text inside another author's `<w:ins>` or `<w:del>` tags**
- **ALWAYS use nested deletions** to remove another author's insertions
- **Every edit must be properly tracked** with `<w:ins>` or `<w:del>` tags

### Required Files and Settings

**Add people information in `word/people.xml`:**
```xml
<w15:people xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml">
  <w15:person w15:author="Claude">
    <w15:presenceInfo w15:providerId="None" w15:userId="Claude"/>
  </w15:person>
</w15:people>
```

**Update relationships in `word/_rels/document.xml.rels`:**
```xml
<Relationship Id="rId6" Type="http://schemas.microsoft.com/office/2011/relationships/people" Target="people.xml"/>
```

**Update content types in `[Content_Types].xml`:**
```xml
<Override PartName="/word/people.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.people+xml"/>
```

### Tracked Change Patterns

**CRITICAL RULE**: Never modify the content inside another author's tracked changes. Always use nested deletions.

**Text Insertion:**
```xml
<w:ins w:id="1" w:author="Claude" w:date="2025-07-30T23:05:00Z" w16du:dateUtc="2025-07-31T06:05:00Z">
  <w:r w:rsidR="00792858">
    <w:t>inserted text</w:t>
  </w:r>
</w:ins>
```

**Text Deletion:**
```xml
<w:del w:id="2" w:author="Claude" w:date="2025-07-30T23:05:00Z" w16du:dateUtc="2025-07-31T06:05:00Z">
  <w:r w:rsidRPr="00982B76" w:rsidDel="00792858">
    <w:delText>deleted text</w:delText>
  </w:r>
</w:del>
```

**Deleting Another Author's Insertion (MUST use nested structure):**
```xml
<!-- WRONG: Don't modify the text content -->
<w:ins w:author="Jane Smith" w:id="16">
  <w:r><w:t>weekly</w:t></w:r>  <!-- DON'T change "monthly" to "weekly" -->
</w:ins>

<!-- CORRECT: Nest deletion inside the original insertion -->
<w:ins w:author="Jane Smith" w:id="16">
  <w:del w:author="Claude" w:id="40">
    <w:r><w:delText>monthly</w:delText></w:r>
  </w:del>
</w:ins>
<w:ins w:author="Claude" w:id="41">
  <w:r><w:t>weekly</w:t></w:r>
</w:ins>
```

**Modifying Existing Text + Tracked Changes:**
```xml
<!-- When existing text has tracked changes from another author -->
<w:r><w:t>The report will be delivered</w:t></w:r>
<w:ins w:author="Alex Chen" w:id="20">
  <w:r><w:t> with appendices</w:t></w:r>
</w:ins>

<!-- To delete Alex's addition, nest inside their insertion -->
<w:r><w:t>The report will be delivered</w:t></w:r>
<w:ins w:author="Alex Chen" w:id="20">
  <w:del w:author="Claude" w:id="42">
    <w:r><w:delText> with appendices</w:delText></w:r>
  </w:del>
</w:ins>
```

### Unique IDs and RSIDs

- **Track change IDs**: Each `<w:ins>` and `<w:del>` needs unique `w:id` values (increment sequentially)
- **RSIDs**: Add new RSIDs to `word/settings.xml` for each edit session:
```xml
<w:rsids>
  <w:rsidRoot w:val="00982B76"/>
  <w:rsid w:val="00792858"/>  <!-- New RSID for this edit -->
  <w:rsid w:val="00381D62"/>  <!-- Another new RSID -->
</w:rsids>
```

## Comments

Comments allow adding feedback and annotations to specific text ranges in documents.

### Required Files and Settings

**Create `word/comments.xml`:**
```xml
<w:comments xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml">
  <w:comment w:id="0" w:author="Claude" w:date="2025-07-02T21:54:00Z" w:initials="C">
    <w:p w14:paraId="06DC92BE" w14:textId="77777777" w:rsidR="008F7154" w:rsidRDefault="008F7154" w:rsidP="008F7154">
      <w:r>
        <w:rPr>
          <w:rStyle w:val="CommentReference"/>
        </w:rPr>
        <w:annotationRef/>
      </w:r>
      <w:r>
        <w:rPr>
          <w:color w:val="000000"/>
          <w:sz w:val="20"/>
          <w:szCs w:val="20"/>
        </w:rPr>
        <w:t>Comment text goes here.</w:t>
      </w:r>
    </w:p>
  </w:comment>
</w:comments>
```

**Supporting comment files:**

`word/commentsExtended.xml`:
```xml
<w15:commentsEx xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml">
  <w15:commentEx w15:paraId="06DC92BE" w15:done="0"/>
</w15:commentsEx>
```

`word/commentsExtensible.xml`:
```xml
<w16cex:commentsExtensible xmlns:w16cex="http://schemas.microsoft.com/office/word/2018/wordml/cex">
  <w16cex:commentExtensible w16cex:durableId="4185D2C8" w16cex:dateUtc="2025-07-03T04:54:00Z"/>
</w16cex:commentsExtensible>
```

`word/commentsIds.xml`:
```xml
<w16cid:commentsIds xmlns:w16cid="http://schemas.microsoft.com/office/word/2016/wordml/cid">
  <w16cid:commentId w16cid:paraId="06DC92BE" w16cid:durableId="4185D2C8"/>
</w16cid:commentsIds>
```

### File Updates for Comments

**Update relationships in `word/_rels/document.xml.rels`:**
```xml
<Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments" Target="comments.xml"/>
<Relationship Id="rId5" Type="http://schemas.microsoft.com/office/2011/relationships/commentsExtended" Target="commentsExtended.xml"/>
<Relationship Id="rId6" Type="http://schemas.microsoft.com/office/2016/09/relationships/commentsIds" Target="commentsIds.xml"/>
<Relationship Id="rId7" Type="http://schemas.microsoft.com/office/2018/08/relationships/commentsExtensible" Target="commentsExtensible.xml"/>
<Relationship Id="rId9" Type="http://schemas.microsoft.com/office/2011/relationships/people" Target="people.xml"/>
```

**Update content types in `[Content_Types].xml`:**
```xml
<Override PartName="/word/comments.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.comments+xml"/>
<Override PartName="/word/commentsExtended.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.commentsExtended+xml"/>
<Override PartName="/word/commentsIds.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.commentsIds+xml"/>
<Override PartName="/word/commentsExtensible.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.commentsExtensible+xml"/>
<Override PartName="/word/people.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.people+xml"/>
```

**Add comment styles to `word/styles.xml`:**
```xml
<w:style w:type="character" w:styleId="CommentReference">
  <w:name w:val="annotation reference"/>
  <w:basedOn w:val="DefaultParagraphFont"/>
  <w:uiPriority w:val="99"/>
  <w:semiHidden/>
  <w:unhideWhenUsed/>
  <w:rPr>
    <w:sz w:val="16"/>
    <w:szCs w:val="16"/>
  </w:rPr>
</w:style>
```

### Adding Comments to Text

**In `word/document.xml`, wrap the target text:**
```xml
<w:commentRangeStart w:id="0"/>
<w:r w:rsidRPr="00982B76">
  <w:t>Text being commented on</w:t>
</w:r>
<w:commentRangeEnd w:id="0"/>
<w:r w:rsidR="008F7154">
  <w:rPr>
    <w:rStyle w:val="CommentReference"/>
  </w:rPr>
  <w:commentReference w:id="0"/>
</w:r>
```

### Comment Replies

**Parent comment structure remains the same, but replies use `w15:paraIdParent`:**

In `word/commentsExtended.xml`:
```xml
<w15:commentEx w15:paraId="00782E84" w15:paraIdParent="6365264B" w15:done="0"/>
```

**Multiple comments on same text:** Use multiple `<w:commentRangeStart>` and `<w:commentRangeEnd>` pairs with different IDs.