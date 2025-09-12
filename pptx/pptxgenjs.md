# PptxGenJS Library Tutorial

Create professional PowerPoint presentations programmatically with JavaScript.

**Important: Read this entire document before starting.** Critical formatting rules and common pitfalls are covered throughout - skipping sections may result in corrupted files or rendering issues.

**Color Palette Requirement:** Use the predefined color palette in the "Standard Color Palette" section below. This ensures consistent, professional presentations with proper color harmony.

## Setup & Basic Structure

```bash
# react-icons is for professional icons (recommended)
npm install -g pptxgenjs react-icons react react-dom sharp
```

```javascript
const pptxgen = require("pptxgenjs");

// Create presentation
let pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';  // or 'LAYOUT_16x10', 'LAYOUT_4x3', 'LAYOUT_WIDE'
pres.author = 'Your Name';
pres.title = 'Presentation Title';

// Add slide with default background color
let slide = pres.addSlide();
slide.background = { color: "FFFFFF" };
slide.addText("Hello World!", { x: 0.5, y: 0.5, fontSize: 36, color: "363636" });

// Alternative: Add slide with gradient or image background
let slide2 = pres.addSlide();
slide2.background = { path: "background.jpg" };  // Image background

// Save
pres.writeFile({ fileName: "Presentation.pptx" });
```

## Slide Backgrounds

Set slide backgrounds using the `background` property:

```javascript
// Default background
slide.background = { color: "FFFFFF" };  // White

// Alternative colored backgrounds (remember: no # prefix!)
slide.background = { color: "FAF9F5" };  // Light cream
slide.background = { fill: "2C3E50" };   // Dark blue

// Image background
slide.background = { path: "background.jpg" };
slide.background = { data: "image/png;base64,..." };  // Base64 image

// Transparent/no background (shows master slide)
slide.background = { transparency: 100 };

## ⚠️ CRITICAL: Hex Colors

**NEVER use "#" with hex colors!** This corrupts documents.

```javascript
// ✅ CORRECT: No "#" prefix
color: "FF0000"
fill: { color: "0066CC" }
chartColors: ["2E74B5", "4A90A4", "FF6B6B"]

// ❌ WRONG: Causes corruption
color: "#FF0000"       // ❌ Document breaks
fill: { color: "#0066CC" }    // ❌ File invalid
chartColors: ["#2E74B5", "#4A90A4"]  // ❌ Breaks file
```

## ⚠️ Critical Layout & Positioning

### Layout Dimensions
**Slide dimensions** (coordinates in inches):
- `LAYOUT_16x9`: 10" × 5.625" (default)
- `LAYOUT_16x10`: 10" × 6.25"
- `LAYOUT_4x3`: 10" × 7.5"
- `LAYOUT_WIDE`: 13.3" × 7.5"

### Positioning & Overflow Prevention
**⚠️ Always verify bounds**: `x + width ≤ slide width` and `y + height ≤ slide height`

```javascript
// ✅ Safe positioning with bounds check
const slideWidth = 10, slideHeight = 5.625; // LAYOUT_16x9
const elementWidth = 3, elementHeight = 2;
const x = 1, y = 2;

if (x + elementWidth <= slideWidth && y + elementHeight <= slideHeight) {
    slide.addShape(pres.shapes.RECTANGLE, { x, y, w: elementWidth, h: elementHeight });
}
```

### Centering Multiple Elements
```javascript
// ✅ CORRECT: Calculate total width first to center properly
const slideWidth = 10;  // LAYOUT_16x9 width
const boxWidth = 3;
const spacing = 0.2;
const numBoxes = 3;
const totalWidth = (boxWidth * numBoxes) + (spacing * (numBoxes - 1));
const startX = (slideWidth - totalWidth) / 2; // Center horizontally

boxes.forEach((box, i) => {
    const x = startX + (i * (boxWidth + spacing));
    slide.addShape(pres.shapes.RECTANGLE, { x, y: 1, w: boxWidth, h: 3.5 });
});

// ❌ WRONG: Don't use arbitrary starting positions
// This will NOT center your elements:
boxes.forEach((box, i) => {
    const x = 0.5 + (i * 3.2);  // ❌ Arbitrary positioning
    slide.addShape(pres.shapes.RECTANGLE, { x, y: 1, w: 3, h: 3.5 });
});
```

### Spacing & Padding Guidelines
- **Text padding**: 0.3-0.4" from ALL edges of containers
- **Element spacing**: Minimum 0.3" between adjacent elements
- **Button text**: Make text area 0.2" smaller than button size
- **Safe margins**: Keep 0.5" from slide edges for important content

### Image Aspect Ratios
**Always calculate dimensions** to prevent distortion:

```javascript
// ✅ CORRECT: Maintain aspect ratio
const origWidth = 1978, origHeight = 923, maxHeight = 3.0;
const calcWidth = maxHeight * (origWidth / origHeight);
const centerX = (10 - calcWidth) / 2; // Center horizontally

slide.addImage({
    path: "chart.png", x: centerX, y: 1.2, w: calcWidth, h: maxHeight
});
```

### ⚠️ Common Layout Mistakes
**IMPORTANT**: Shapes render in addition order (no z-index). First added = back, last = front.

1. **Overflow**: Elements extending beyond slide boundaries
2. **Missing padding**: Text touching container edges
3. **Hidden corners**: Overlapping shapes obscure rounded corners
4. **Text wrapping**: Insufficient space causes unexpected line breaks
5. **Poor spacing**: Elements too close together (< 0.3" minimum)
6. **Bullet list overflow**: Not allocating enough height for lists (estimate ~0.4-0.5" per bullet with standard spacing)
7. **Excessive lineSpacing**: Using lineSpacing with bullets creates huge gaps - use paraSpaceAfter only!
8. **Double bullets**: NEVER use text bullet symbols (•, -, *, ▪, ▸) in your strings! They create double bullets when combined with `bullet: true`. Always use the `bullet: true` option instead of manually adding bullet characters
9. **Text overlap**: Elements positioned over text making text or content unreadable. All text must be fully visible.
10. **Content overflow**: Text or elements extending below slide boundaries. If content doesn't fit, reduce font size or split across multiple slides.

## Text & Formatting


```javascript
// Basic text with common properties
slide.addText("Simple Text", {
  x: 1, y: 1, w: 8, h: 2, fontSize: 24, fontFace: "Arial",  // Universal default
  color: "363636", bold: true, align: "center", valign: "middle"
});

// Rich text arrays
slide.addText([
  { text: "Bold ", options: { bold: true } },
  { text: "Italic ", options: { italic: true } },
  { text: "Underline", options: { underline: true } }
], { x: 1, y: 3, w: 8, h: 1 });

// Multi-line text (requires breakLine: true)
slide.addText([
  { text: "Line 1", options: { breakLine: true } },
  { text: "Line 2", options: { breakLine: true } },
  { text: "Line 3" }  // Last item doesn't need breakLine
], { x: 0.5, y: 0.5, w: 8, h: 2 });

// Text with padding inside shapes
const padding = 0.4;
slide.addShape(pres.shapes.RECTANGLE, { x: 1, y: 2, w: 8, h: 2 });
slide.addText("Content", {
  x: 1 + padding, y: 2 + padding,
  w: 8 - (padding * 2), h: 2 - (padding * 2)
});
```

## Lists & Bullets

⚠️ **CRITICAL: ALWAYS use `bullet: true` for bullet points - NEVER use unicode bullet symbols like "•"!**
⚠️ **CRITICAL: Add `breakLine: true` to each item (except last) or text runs together!**
⚠️ **CRITICAL: Avoid `lineSpacing` with bullet lists - it causes excessive gaps. Use `paraSpaceAfter` only!**

```javascript
// ✅ CORRECT: Simple bullet list with single text option
slide.addText("First bullet point", {
  x: 0.5, y: 0.5, w: 8, h: 0.5,
  bullet: true  // This creates a proper bullet point
});

// ✅ CORRECT: Multiple bullets with array syntax
slide.addText([
  { text: "First item", options: { bullet: true, breakLine: true } },
  { text: "Second item", options: { bullet: true, breakLine: true } },
  { text: "Third item", options: { bullet: true } }  // Last: no breakLine
], { x: 0.5, y: 0.5, w: 8, h: 3 });

// ✅ CORRECT: When looping through items
const items = ["Item 1", "Item 2", "Item 3"];
let yPos = 1.0;
items.forEach(item => {
  slide.addText(item, {
    x: 0.5, y: yPos, w: 8, h: 0.5,
    bullet: true,  // Proper bullet formatting
    fontSize: 14
  });
  yPos += 0.6;
});

// ❌ WRONG: Never use unicode/text bullets - creates double bullets!
slide.addText("• First item", { x: 0.5, y: 0.5, w: 8, h: 0.5 });  // ❌ DON'T DO THIS
slide.addText(`• ${item}`, { x: 0.5, y: 0.5, w: 8, h: 0.5 });    // ❌ DON'T DO THIS

// ❌ WRONG: Array with text bullets
slide.addText([
  { text: "• First item", options: { breakLine: true } },  // ❌ Creates double bullets
  { text: "• Second item", options: { breakLine: true } },  // ❌ Creates double bullets
  { text: "• Third item", options: {} }                     // ❌ Creates double bullets
], { x: 0.5, y: 0.5, w: 8, h: 3 });

// Professional spacing - BEST PRACTICE
slide.addText([...], {
  x: 0.5, y: 0.5, w: 8, h: 3,
  paraSpaceAfter: 12    // Space BETWEEN bullet points (12-20 recommended)
  // ⚠️ IMPORTANT: Don't use lineSpacing with bullets - it creates excessive gaps!
  // lineSpacing affects ALL line breaks including those from breakLine: true
  // For bullet lists, ONLY use paraSpaceAfter for spacing between items
  // Rule of thumb: 6 bullets need ~2.5-3" height with 16pt font and 12pt paraSpaceAfter
});

// Sub-items, custom bullets, numbered lists
{ text: "Sub-item", options: { bullet: true, indentLevel: 1 } }
{ text: "Check", options: { bullet: { code: "2713" }, breakLine: true } }  // ✓
{ text: "First", options: { bullet: { type: "number" }, breakLine: true } }
```

## Shapes & Basic Elements

```javascript
// Rectangle, Circle, Lines
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 0.8, w: 1.5, h: 3.0,
  fill: { color: "FF0000" }, line: { color: "000000", width: 2 }
});

slide.addShape(pres.shapes.OVAL, { x: 4, y: 1, w: 2, h: 2, fill: { color: "0000FF" } });

slide.addShape(pres.shapes.LINE, {
  x: 1, y: 3, w: 5, h: 0, line: { color: "FF0000", width: 3, dashType: "dash" },
  beginArrowType: "arrow", endArrowType: "arrow"
});

// Custom geometry
slide.addShape(pres.shapes.CUSTOM_GEOMETRY, {
  points: [{ x: 0.0, y: 0.0 }, { x: 0.5, y: 1.0 }, { x: 1.0, y: 0.0 }, { close: true }],
  x: 7, y: 4, w: 2, h: 2, fill: { color: "FF00FF" }
});
```

## Images & Media

```javascript
// Basic image
slide.addImage({ path: "image.png", x: 0.5, y: 0.6, w: 3.58, h: 2.68 });

// Image with hyperlink
slide.addImage({
  path: "logo.png", x: 1, y: 1, w: 2, h: 1,
  hyperlink: { url: "https://example.com", tooltip: "Visit site" }
});

// Video, Audio, YouTube
slide.addMedia({ x: 0.5, y: 1, w: 3.56, h: 2, type: "video", path: "video.mp4" });
slide.addMedia({ x: 4.5, y: 1, w: 3.5, h: 3.5, type: "audio", path: "audio.mp3" });
slide.addMedia({ x: 1, y: 1, w: 9, h: 5, type: "online", link: "https://youtube.com/embed/ID" });
```

## Tables

```javascript
// Basic table
slide.addTable([
  ["Header 1", "Header 2"],
  ["Cell 1", "Cell 2"]
], {
  x: 1, y: 1, w: 8, h: 2,
  border: { pt: 1, color: "999999" }, fill: { color: "F1F1F1" }
});

// Advanced formatting with merged cells
let tableData = [
  [{ text: "Header", options: { fill: { color: "6699CC" }, color: "FFFFFF", bold: true } }, "Cell"],
  [{ text: "Merged", options: { colspan: 2 } }]
];

slide.addTable(tableData, {
  x: 1, y: 3.5, w: 8, h: 2, colW: [4, 4], rowH: [0.5, 0.75], autoPage: true
});
```

## Charts

**Chart Colors**: Use the `chartColors` property with arrays from `chartColorSets` defined in the color palette section. Colors are applied in order:
- **Pie/Donut charts**: Each slice gets the next color in the array
- **Bar/Line charts**: Each data series gets one color
- **Auto-cycling**: If more data points than colors, the sequence repeats from the beginning

**Axis Labels Required**: Charts with X and Y axes (BAR, LINE, BAR3D, AREA, SCATTER, BUBBLE, RADAR) must include axis labels using `catAxisTitle` and `valAxisTitle`. Pie and doughnut charts are exempt.

```javascript
// Bar chart with axis labels
slide.addChart(pres.charts.BAR, [{
  name: "Sales 2024",
  labels: ["Q1", "Q2", "Q3", "Q4"],
  values: [4500, 5500, 6200, 7100]
}], {
  x: 0.5, y: 0.6, w: 6, h: 3, barDir: 'col', showTitle: true, title: 'Quarterly Sales',
  valAxisMaxVal: 8000, valAxisMinVal: 0,  // ⚠️ Control scaling for accuracy
  dataLabelPosition: 'outEnd', dataLabelColor: '000000',  // ⚠️ Visibility
  // Required axis labels
  showCatAxisTitle: true, catAxisTitle: 'Quarter',
  showValAxisTitle: true, valAxisTitle: 'Sales ($000s)'
});

// Line chart with axis labels
slide.addChart(pres.charts.LINE, [{
  name: "Temperature", labels: ["Jan", "Feb", "Mar", "Apr"], values: [32, 35, 42, 55]
}], {
  x: 0.5, y: 4, w: 6, h: 3, lineSize: 4, lineSmooth: true,
  // Required axis labels
  showCatAxisTitle: true, catAxisTitle: 'Month',
  showValAxisTitle: true, valAxisTitle: 'Temperature (°F)'
});

// Pie chart (no axis labels needed) with custom colors from palette
slide.addChart(pres.charts.PIE, [{
  name: "Market Share", labels: ["Product A", "Product B", "Other"], values: [35, 45, 20]
}], {
  x: 7, y: 1, w: 5, h: 4, showPercent: true, holeSize: 0,
  chartColors: chartColorSets.vibrant.slice(0, 3)  // Use first 3 colors from vibrant set
});

// Other chart types requiring axis labels: BAR3D, AREA, SCATTER, BUBBLE, RADAR
// Example with SCATTER chart:
slide.addChart(pres.charts.SCATTER, [{
  name: "Data Points", labels: ["A", "B", "C"], values: [10, 20, 15]
}], {
  x: 1, y: 1, w: 6, h: 4,
  // Required axis labels
  showCatAxisTitle: true, catAxisTitle: 'X Values',
  showValAxisTitle: true, valAxisTitle: 'Y Values'
});
```

## Slide Masters & Advanced

```javascript
// Define and use slide master
pres.defineSlideMaster({
  title: 'TITLE_SLIDE', background: { color: '283A5E' },
  objects: [{
    placeholder: { options: { name: 'title', type: 'title', x: 1, y: 2, w: 8, h: 2 } }
  }]
});

let titleSlide = pres.addSlide({ masterName: "TITLE_SLIDE" });
titleSlide.addText("My Title", { placeholder: "title" });

// Sections and notes
pres.addSlide({ sectionTitle: "Introduction" });
slide.addNotes("Key points:\n- First\n- Second");

// Export options
pres.writeFile({ fileName: "output.pptx", compression: true });
```

## Icons

**CRITICAL: NEVER use emojis (💰, 🌍, 📈, 😊, etc.) - ALWAYS use proper icons from react-icons library for professional presentations.**

```javascript
const React = require('react');
const ReactDOMServer = require('react-dom/server');
const sharp = require('sharp');
const { FaHome } = require('react-icons/fa');

async function rasterizeIconPng(IconComponent, color, size = "256", filename) {
  const svgString = ReactDOMServer.renderToStaticMarkup(
    React.createElement(IconComponent, { color: `#${color}`, size: size })
  );

  // Convert SVG to PNG using Sharp
  await sharp(Buffer.from(svgString))
    .png()
    .toFile(filename);

  return filename;
}

// Usage: Rasterize icon as PNG file and add to slide
const iconPath = await rasterizeIconPng(FaHome, "4472c4", "256", "home-icon.png");
slide.addImage({ path: iconPath, x: 1, y: 1, w: 0.4, h: 0.4 });
```

**Top Icon Libraries** (choose one for consistency):
- `fa` (Font Awesome) - Most comprehensive, best for business presentations
- `md` (Material Design) - Google's recognizable, modern icons
- `hi` (Heroicons) - Clean, professional, Tailwind ecosystem

**Icon Placement Rules:**
- **Each icon must have a clear purpose** - Label headers, represent specific items, or indicate categories
- **Never place icons randomly** in corners or margins without purpose
- **Align icons with their content** - Position icons directly next to or above what they represent

**Bad Examples:**
- ❌ Icons placed in corners or margins with no relationship to content
- ❌ Random icon placement as "visual filler"
- ❌ Scattered icons with no clear connection to text

**Good Examples:**
- ✅ Icons aligned next to their corresponding text items
- ✅ Icons as visual labels for section headers
- ✅ Icons integrated into lists to represent each item

**CRITICAL: Icons as Visual Bullets**
- When icons serve as bullet points, NEVER use `bullet: true` in the text options
- Icons and bullets together create visual redundancy and clutter
- Let the icon alone indicate the list structure

```javascript
// ❌ WRONG: Icon + bullet creates redundancy
slide.addImage({ path: iconPath, x: 0.6, y: 1.4, w: 0.4, h: 0.4 });
slide.addText("List item", { x: 1.1, y: 1.4, w: 8, h: 0.5, bullet: true }); // Redundant!

// ✅ CORRECT: Icon serves as the visual bullet
slide.addImage({ path: iconPath, x: 0.6, y: 1.4, w: 0.4, h: 0.4 });
slide.addText("List item", { x: 1.1, y: 1.4, w: 8, h: 0.5 }); // Clean and clear
```

**Best practices**: 0.3-0.5" size, match theme colors, max 3-5 icons per slide

## Gradients

```javascript
// Gradient background with Sharp rasterization
const sharp = require('sharp');
const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="562.5"><defs><linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#667eea"/><stop offset="100%" style="stop-color:#764ba2"/></linearGradient></defs><rect width="100%" height="100%" fill="url(#g)"/></svg>`;

// Convert SVG to PNG using Sharp
await sharp(Buffer.from(svg))
  .png()
  .toFile('gradient.png');

slide.addImage({
  path: 'gradient.png',
  x: 0, y: 0, w: 10, h: 5.625
});
```

## Best Practices & Tips

```javascript
// ⭐ PROFESSIONAL FONT COMBINATIONS - Choose one pairing for consistency:
// 🏢 Classic/Corporate: Arial (titles) + Arial (body) - Most universally supported
// 🚀 Modern/Clean: Tahoma (titles) + Verdana (body) - Cross-platform compatible
// 📚 Elegant/Editorial: Georgia (titles) + Verdana (body) - Serif/sans-serif contrast
// 💻 Minimal/Tech: Trebuchet MS (titles) + Arial (body) - Clean and readable

const styles = {
  title: { fontSize: 44, bold: true, color: "2E74B5", fontFace: "Arial" },
  body: { fontSize: 18, color: "333333", fontFace: "Arial" }
};

const theme = { primary: "2E74B5", secondary: "FF6B6B" };

// Error handling
try {
  await pres.writeFile({ fileName: "output.pptx" });
} catch (error) { console.error("Error:", error); }
```

## Standard Color Palette

**IMPORTANT: Use only these predefined colors for professional consistency:**

```javascript
const colorPalette = {
  // Aqua shades
  aqua100: "E9F7F2", aqua200: "BAE8D9", aqua300: "91D9C1", aqua400: "6BC9AA",
  aqua500: "4ABA95", aqua600: "2F9477", aqua700: "196E59", aqua800: "0B473B", aqua900: "02211C",

  // Green shades
  green100: "F1F7E9", green200: "D2E8BA", green300: "B5D991", green400: "95C96B",
  green500: "79BA4A", green600: "58942F", green700: "39701A", green800: "214A0B", green900: "0E2402",

  // Yellow shades
  yellow100: "FAF7E6", yellow200: "FAECB9", yellow300: "FADD8C", yellow400: "FAC65F",
  yellow500: "FAAD32", yellow600: "C7831E", yellow700: "965C11", yellow800: "633806", yellow900: "301901",

  // Orange shades
  orange100: "FAEFEB", orange200: "FACFC0", orange300: "F7AD94", orange400: "F78E6A",
  orange500: "F56D40", orange600: "C4532D", orange700: "943B1E", orange800: "612510", orange900: "301107",

  // Red shades
  red100: "FCEDED", red200: "F5C1C1", red300: "ED9595", red400: "E56E6E",
  red500: "DE4949", red600: "B23636", red700: "872424", red800: "5C1717", red900: "300B0B",

  // Magenta shades
  magenta100: "FCF0F4", magenta200: "F5C9D7", magenta300: "F0A8C0", magenta400: "E884A6",
  magenta500: "E0658E", magenta600: "B2476B", magenta700: "872E4C", magenta800: "591A2F", magenta900: "2E0B17",

  // Violet shades
  violet100: "F1F0FF", violet200: "CFCBF5", violet300: "B2ADED", violet400: "948DE3",
  violet500: "7971D9", violet600: "5A53B0", violet700: "413A87", violet800: "28235C", violet900: "141133",

  // Blue shades
  blue100: "EDF5FC", blue200: "C1DBF5", blue300: "98C2ED", blue400: "6FA9E3",
  blue500: "4B93DB", blue600: "2E70B2", blue700: "185087", blue800: "09345E", blue900: "011A33"
};

// Recommended color combinations for presentations:
const colorSchemes = {
  professional: {
    primary: colorPalette.blue700,
    secondary: colorPalette.orange600,
    accent: colorPalette.green600,
    text: "2C3E50",
    background: "FFFFFF"
  },
  modern: {
    primary: colorPalette.violet700,
    secondary: colorPalette.aqua600,
    accent: colorPalette.yellow600,
    text: "333333",
    background: "F5F5F5"
  },
  corporate: {
    primary: colorPalette.blue800,
    secondary: colorPalette.green700,
    accent: colorPalette.orange500,
    text: "212121",
    background: "FAFAFA"
  }
};

// Chart color sequences - automatically cycle through these for data visualization
const chartColorSets = {
  // Default line chart cycle - matches PowerPoint's default sequence
  // This is the standard order used by PowerPoint for line charts
  defaultLine: [
    colorPalette.aqua600,    // 1. Aqua 600
    colorPalette.violet700,  // 2. Violet 700
    colorPalette.magenta300, // 3. Magenta 300
    colorPalette.orange500,  // 4. Orange 500
    colorPalette.blue500,    // 5. Blue 500
    colorPalette.green800,   // 6. Green 800
    colorPalette.yellow500,  // 7. Yellow 500
    colorPalette.red500      // 8. Red 500
  ],

  // Vibrant set - good contrast for presentations
  vibrant: [
    colorPalette.blue600,    // Blue
    colorPalette.orange600,  // Orange
    colorPalette.green600,   // Green
    colorPalette.red600,     // Red
    colorPalette.violet600,  // Violet
    colorPalette.aqua600,    // Aqua
    colorPalette.yellow600,  // Yellow
    colorPalette.magenta600  // Magenta
  ],

  // Professional set - muted tones
  professional: [
    colorPalette.blue700,
    colorPalette.green700,
    colorPalette.orange700,
    colorPalette.violet700,
    colorPalette.aqua700,
    colorPalette.red700,
    colorPalette.yellow700,
    colorPalette.magenta700
  ],

  // Pastel set - soft colors
  pastel: [
    colorPalette.blue200,
    colorPalette.green200,
    colorPalette.orange200,
    colorPalette.violet200,
    colorPalette.red200,
    colorPalette.aqua200,
    colorPalette.yellow200,
    colorPalette.magenta200
  ]
};

// Usage in charts:
// chartColors: chartColorSets.defaultLine  // Use PowerPoint's default line chart colors
// chartColors: chartColorSets.vibrant  // Will cycle through all 8 colors
// chartColors: chartColorSets.vibrant.slice(0, 5)  // Use first 5 colors only
```

**Key Tips:**
1. **Colors**: Use hex without '#' (e.g., "FF0000") - prefer palette colors above
2. **Coordinates**: Top-left (0,0), measured in inches
3. **Images**: Use `path` for files, `data` for base64
4. **Contrast**: Never white text on white backgrounds - use dark fills
5. **External Charts**: Generate without titles to avoid duplication
```javascript
// Python/matplotlib: Skip plt.title() when chart will be in PowerPoint
// Add title via slide.addText() instead
```

## ⚠️ Limitations & Quick Reference

**Limitations:**
- No masking/clipping between shapes | No z-index (only addition order)
- Chart scaling: Set `valAxisMaxVal` to prevent misleading auto-scale
- Data labels: Use `dataLabelPosition: 'outEnd'` for bar visibility
- Bullet spacing: `lineSpacing` affects ALL lines including `breakLine: true` - avoid with bullets!

**Quick Reference:**
- **Shapes**: RECTANGLE, OVAL, LINE, ROUNDED_RECTANGLE, CUSTOM_GEOMETRY
- **Charts**: BAR, LINE, PIE, DOUGHNUT, SCATTER, BUBBLE, RADAR
- **Layouts**: LAYOUT_16x9 (10"×5.625"), LAYOUT_16x10, LAYOUT_4x3, LAYOUT_WIDE
- **Alignment**: "left", "center", "right" | **Chart positions**: "outEnd", "inEnd", "center"