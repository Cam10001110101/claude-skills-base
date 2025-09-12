#!/usr/bin/env python3
"""
Extract structured text content from PowerPoint presentations.

This module provides functionality to:
- Extract all text content from PowerPoint shapes
- Preserve paragraph formatting (alignment, bullets, fonts, spacing)
- Handle nested GroupShapes recursively with correct absolute positions
- Sort shapes by visual position on slides
- Filter out slide numbers and non-content placeholders
- Export to JSON with clean, structured data

Classes:
    ParagraphData: Represents a text paragraph with formatting
    ShapeData: Represents a shape with position and text content

Main Functions:
    extract_text_inventory: Extract all text from a presentation
    save_inventory: Save extracted data to JSON

Usage:
    python inventory.py input.pptx output.json
"""

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from pptx import Presentation
from pptx.enum.text import PP_ALIGN
from pptx.shapes.base import BaseShape

# Type aliases for cleaner signatures
JsonValue = Union[str, int, float, bool, None]
ParagraphDict = Dict[str, JsonValue]
ShapeDict = Dict[str, Union[str, float, List[ParagraphDict], None]]
SlideShapeDict = Dict[str, "ShapeData"]  # Dict of shape_id -> ShapeData
InventoryData = Dict[str, SlideShapeDict]  # Dict of slide_id -> shapes
InventoryDict = Dict[str, Dict[str, ShapeDict]]  # JSON-serializable inventory


@dataclass
class ShapeWithPosition:
    """A shape with its absolute position on the slide."""

    shape: BaseShape
    absolute_left: int  # in EMUs
    absolute_top: int  # in EMUs


class ParagraphData:
    """Data structure for paragraph properties extracted from a PowerPoint paragraph."""

    def __init__(self, paragraph: Any):
        """Initialize from a PowerPoint paragraph object.

        Args:
            paragraph: The PowerPoint paragraph object
        """
        self.text: str = paragraph.text.strip()
        self.bullet: bool = False
        self.level: Optional[int] = None
        self.alignment: Optional[str] = None
        self.space_before: Optional[float] = None
        self.space_after: Optional[float] = None
        self.font_name: Optional[str] = None
        self.font_size: Optional[float] = None
        self.bold: Optional[bool] = None
        self.italic: Optional[bool] = None
        self.underline: Optional[bool] = None
        self.color: Optional[str] = None
        self.line_spacing: Optional[float] = None

        # Check for bullet formatting
        if hasattr(paragraph, "_p") and paragraph._p is not None:
            pPr = paragraph._p.pPr
            if pPr is not None:
                ns = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
                if (
                    pPr.find(f"{ns}buChar") is not None
                    or pPr.find(f"{ns}buAutoNum") is not None
                ):
                    self.bullet = True
                    if hasattr(paragraph, "level"):
                        self.level = paragraph.level

        # Add alignment if not LEFT (default)
        if hasattr(paragraph, "alignment") and paragraph.alignment is not None:
            alignment_map = {
                PP_ALIGN.CENTER: "CENTER",
                PP_ALIGN.RIGHT: "RIGHT",
                PP_ALIGN.JUSTIFY: "JUSTIFY",
            }
            if paragraph.alignment in alignment_map:
                self.alignment = alignment_map[paragraph.alignment]

        # Add spacing properties if set
        if hasattr(paragraph, "space_before") and paragraph.space_before:
            self.space_before = paragraph.space_before.pt
        if hasattr(paragraph, "space_after") and paragraph.space_after:
            self.space_after = paragraph.space_after.pt

        # Extract font properties from first run
        if paragraph.runs and len(paragraph.runs) > 0:
            first_run = paragraph.runs[0]
            if hasattr(first_run, "font"):
                font = first_run.font
                if font.name:
                    self.font_name = font.name
                if font.size:
                    self.font_size = font.size.pt
                if font.bold is not None:
                    self.bold = font.bold
                if font.italic is not None:
                    self.italic = font.italic
                if font.underline is not None:
                    self.underline = font.underline
                if hasattr(font.color, "rgb") and font.color.rgb:
                    self.color = str(font.color.rgb)

        # Add line spacing if set
        if hasattr(paragraph, "line_spacing") and paragraph.line_spacing is not None:
            if hasattr(paragraph.line_spacing, "pt"):
                self.line_spacing = round(paragraph.line_spacing.pt, 2)
            else:
                # Multiplier - convert to points
                font_size = self.font_size if self.font_size else 12.0
                self.line_spacing = round(paragraph.line_spacing * font_size, 2)

    def to_dict(self) -> ParagraphDict:
        """Convert to dictionary for JSON serialization, excluding None values."""
        result: ParagraphDict = {"text": self.text}

        # Add optional fields only if they have values
        if self.bullet:
            result["bullet"] = self.bullet
        if self.level is not None:
            result["level"] = self.level
        if self.alignment:
            result["alignment"] = self.alignment
        if self.space_before is not None:
            result["space_before"] = self.space_before
        if self.space_after is not None:
            result["space_after"] = self.space_after
        if self.font_name:
            result["font_name"] = self.font_name
        if self.font_size is not None:
            result["font_size"] = self.font_size
        if self.bold is not None:
            result["bold"] = self.bold
        if self.italic is not None:
            result["italic"] = self.italic
        if self.underline is not None:
            result["underline"] = self.underline
        if self.color:
            result["color"] = self.color
        if self.line_spacing is not None:
            result["line_spacing"] = self.line_spacing

        return result


class ShapeData:
    """Data structure for shape properties extracted from a PowerPoint shape."""

    @staticmethod
    def emu_to_inches(emu: int) -> float:
        """Convert EMUs (English Metric Units) to inches."""
        return emu / 914400.0

    def __init__(
        self,
        shape: BaseShape,
        absolute_left: Optional[int] = None,
        absolute_top: Optional[int] = None,
    ):
        """Initialize from a PowerPoint shape object.

        Args:
            shape: The PowerPoint shape object (should be pre-validated)
            absolute_left: Absolute left position in EMUs (for shapes in groups)
            absolute_top: Absolute top position in EMUs (for shapes in groups)
        """
        self.shape = shape  # Store reference to original shape

        # Get placeholder type if applicable
        self.placeholder_type: Optional[str] = None
        if hasattr(shape, "is_placeholder") and shape.is_placeholder:  # type: ignore
            if shape.placeholder_format and shape.placeholder_format.type:  # type: ignore
                self.placeholder_type = (
                    str(shape.placeholder_format.type).split(".")[-1].split(" ")[0]  # type: ignore
                )

        # Get position information
        # Use absolute positions if provided (for shapes in groups), otherwise use shape's position
        left_emu = (
            absolute_left
            if absolute_left is not None
            else (shape.left if hasattr(shape, "left") else 0)
        )
        top_emu = (
            absolute_top
            if absolute_top is not None
            else (shape.top if hasattr(shape, "top") else 0)
        )

        self.left: float = round(self.emu_to_inches(left_emu), 2)  # type: ignore
        self.top: float = round(self.emu_to_inches(top_emu), 2)  # type: ignore
        self.width: float = round(
            self.emu_to_inches(shape.width if hasattr(shape, "width") else 0),
            2,  # type: ignore
        )
        self.height: float = round(
            self.emu_to_inches(shape.height if hasattr(shape, "height") else 0),
            2,  # type: ignore
        )

    @property
    def paragraphs(self) -> List[ParagraphData]:
        """Calculate paragraphs from the shape's text frame."""
        if not self.shape or not hasattr(self.shape, "text_frame"):
            return []

        paragraphs = []
        for paragraph in self.shape.text_frame.paragraphs:  # type: ignore
            if paragraph.text.strip():
                paragraphs.append(ParagraphData(paragraph))
        return paragraphs

    def to_dict(self) -> ShapeDict:
        """Convert to dictionary for JSON serialization."""
        result: ShapeDict = {
            "left": self.left,
            "top": self.top,
            "width": self.width,
            "height": self.height,
        }

        # Add optional fields if present
        if self.placeholder_type:
            result["placeholder_type"] = self.placeholder_type

        # Add paragraphs after placeholder_type
        result["paragraphs"] = [para.to_dict() for para in self.paragraphs]

        return result


def is_valid_shape(shape: BaseShape) -> bool:
    """Check if a shape contains meaningful text content."""
    # Must have a text frame with content
    if not hasattr(shape, "text_frame") or not shape.text_frame:  # type: ignore
        return False

    text = shape.text_frame.text.strip()  # type: ignore
    if not text:
        return False

    # Skip slide numbers and numeric footers
    if hasattr(shape, "is_placeholder") and shape.is_placeholder:  # type: ignore
        if shape.placeholder_format and shape.placeholder_format.type:  # type: ignore
            placeholder_type = (
                str(shape.placeholder_format.type).split(".")[-1].split(" ")[0]  # type: ignore
            )
            if placeholder_type == "SLIDE_NUMBER":
                return False
            if placeholder_type == "FOOTER" and text.isdigit():
                return False

    return True


def collect_shapes_with_absolute_positions(
    shape: BaseShape, parent_left: int = 0, parent_top: int = 0
) -> List[ShapeWithPosition]:
    """Recursively collect all shapes with valid text, calculating absolute positions.

    For shapes within groups, their positions are relative to the group.
    This function calculates the absolute position on the slide by accumulating
    parent group offsets.

    Args:
        shape: The shape to process
        parent_left: Accumulated left offset from parent groups (in EMUs)
        parent_top: Accumulated top offset from parent groups (in EMUs)

    Returns:
        List of ShapeWithPosition objects with absolute positions
    """
    if hasattr(shape, "shapes"):  # GroupShape
        result = []
        # Get this group's position
        group_left = shape.left if hasattr(shape, "left") else 0
        group_top = shape.top if hasattr(shape, "top") else 0

        # Calculate absolute position for this group
        abs_group_left = parent_left + group_left
        abs_group_top = parent_top + group_top

        # Process children with accumulated offsets
        for child in shape.shapes:  # type: ignore
            result.extend(
                collect_shapes_with_absolute_positions(
                    child, abs_group_left, abs_group_top
                )
            )
        return result

    # Regular shape - check if it has valid text
    if is_valid_shape(shape):
        # Calculate absolute position
        shape_left = shape.left if hasattr(shape, "left") else 0
        shape_top = shape.top if hasattr(shape, "top") else 0

        return [
            ShapeWithPosition(
                shape=shape,
                absolute_left=parent_left + shape_left,
                absolute_top=parent_top + shape_top,
            )
        ]

    return []


def sort_shapes_by_position(shapes: List[ShapeData]) -> List[ShapeData]:
    """Sort shapes by visual position (top-to-bottom, left-to-right).

    Shapes within 0.5 inches vertically are considered on the same row.
    """
    if not shapes:
        return shapes

    # Sort by top position first
    shapes = sorted(shapes, key=lambda s: (s.top, s.left))

    # Group shapes by row (within 0.5 inches vertically)
    result = []
    row = [shapes[0]]
    row_top = shapes[0].top

    for shape in shapes[1:]:
        if abs(shape.top - row_top) <= 0.5:
            row.append(shape)
        else:
            # Sort current row by left position and add to result
            result.extend(sorted(row, key=lambda s: s.left))
            row = [shape]
            row_top = shape.top

    # Don't forget the last row
    result.extend(sorted(row, key=lambda s: s.left))
    return result


def extract_text_inventory(pptx_path: Path, prs: Optional[Any] = None) -> InventoryData:
    """Extract text content from all slides in a PowerPoint presentation.

    Args:
        pptx_path: Path to the PowerPoint file
        prs: Optional Presentation object to use. If not provided, will load from pptx_path.

    Returns a nested dictionary: {slide-N: {shape-N: ShapeData}}
    Shapes are sorted by visual position (top-to-bottom, left-to-right).
    The ShapeData objects contain the full shape information and can be
    converted to dictionaries for JSON serialization using to_dict().
    """
    if prs is None:
        prs = Presentation(str(pptx_path))
    inventory: InventoryData = {}

    for slide_idx, slide in enumerate(prs.slides):
        # Collect all valid shapes from this slide with absolute positions
        shapes_with_positions = []
        for shape in slide.shapes:  # type: ignore
            shapes_with_positions.extend(collect_shapes_with_absolute_positions(shape))

        if not shapes_with_positions:
            continue

        # Convert to ShapeData with absolute positions and sort by visual position
        shape_data_list = [
            ShapeData(swp.shape, swp.absolute_left, swp.absolute_top)
            for swp in shapes_with_positions
        ]
        sorted_shapes = sort_shapes_by_position(shape_data_list)

        # Create slide inventory with incremental shape IDs
        slide_shapes = {
            f"shape-{idx}": shape_data for idx, shape_data in enumerate(sorted_shapes)
        }

        inventory[f"slide-{slide_idx}"] = slide_shapes

    return inventory


def get_inventory_as_dict(pptx_path: Path) -> InventoryDict:
    """Extract text inventory and return as JSON-serializable dictionaries.

    This is a convenience wrapper around extract_text_inventory that returns
    dictionaries instead of ShapeData objects, useful for testing and direct
    JSON serialization.

    Args:
        pptx_path: Path to the PowerPoint file

    Returns:
        Nested dictionary with all data serialized for JSON
    """
    inventory = extract_text_inventory(pptx_path)

    # Convert ShapeData objects to dictionaries
    dict_inventory: InventoryDict = {}
    for slide_key, shapes in inventory.items():
        dict_inventory[slide_key] = {
            shape_key: shape_data.to_dict() for shape_key, shape_data in shapes.items()
        }

    return dict_inventory


def save_inventory(inventory: InventoryData, output_path: Path) -> None:
    """Save inventory to JSON file with proper formatting.

    Converts ShapeData objects to dictionaries for JSON serialization.
    """
    # Convert ShapeData objects to dictionaries
    json_inventory: InventoryDict = {}
    for slide_key, shapes in inventory.items():
        json_inventory[slide_key] = {
            shape_key: shape_data.to_dict() for shape_key, shape_data in shapes.items()
        }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(json_inventory, f, indent=2, ensure_ascii=False)


def main():
    """Main entry point for command-line usage."""
    parser = argparse.ArgumentParser(
        description="Extract text inventory from PowerPoint with proper GroupShape support.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python inventory.py presentation.pptx inventory.json
    Extracts text inventory with correct absolute positions for grouped shapes

The output JSON includes:
  - All text content organized by slide and shape
  - Correct absolute positions for shapes in groups
  - Visual position and size in inches
  - Paragraph properties and formatting
        """,
    )

    parser.add_argument("input", help="Input PowerPoint file (.pptx)")
    parser.add_argument("output", help="Output JSON file for inventory")

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)

    if not input_path.suffix.lower() == ".pptx":
        print("Error: Input must be a PowerPoint file (.pptx)")
        sys.exit(1)

    try:
        print(f"Extracting text inventory from: {args.input}")
        inventory = extract_text_inventory(input_path)

        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        save_inventory(inventory, output_path)

        print(f"Output saved to: {args.output}")

        # Report statistics
        total_slides = len(inventory)
        total_shapes = sum(len(shapes) for shapes in inventory.values())
        print(f"Found text in {total_slides} slides with {total_shapes} text elements")

    except Exception as e:
        print(f"Error processing presentation: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
