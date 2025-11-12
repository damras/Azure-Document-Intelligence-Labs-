"""
Azure AI Document Intelligence - Layout API Basic Demo
This script demonstrates how to use the prebuilt-layout model to understand document structure.

The Layout model extracts:
- Text with reading order
- Tables with structure
- Selection marks (checkboxes)
- Document styles (handwritten vs printed)
- Page structure and layout
"""

from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
import os
from dotenv import load_dotenv

# Load credentials from parent Labs directory
# The ../ means go up one level from 'layout' folder to 'Labs' folder
load_dotenv(dotenv_path="../.env")

# Get Azure endpoint and API key from environment variables
endpoint = os.getenv("AZ_DOCINT_ENDPOINT")
key = os.getenv("AZ_DOCINT_KEY")


def analyze_layout():
    """
    Main function to analyze a document using the Layout model.
    
    The Layout model is designed for:
    - Understanding document structure (tables, paragraphs, sections)
    - Detecting selection marks (checkboxes, radio buttons)
    - Identifying handwritten vs printed text
    - Extracting text with precise positioning
    """
    
    # Path to the document you want to analyze
    # Available sample files in data/ folder - try each one to see different results:
    # - "data/layout.png" - Basic layout analysis
    # - "data/layout-pageobject.png" - Page object structure demonstration
    # - "data/layout-finacialreport.png" - Financial report with tables
    # - "data/sample-layout.pdf" - PDF document with mixed content
    # Just change the filename below to try different documents!
    
    file_path = "data/layout-pageobject.png"  # Change this to any file from the list above
    
    # Initialize Document Intelligence client with your credentials
    document_intelligence_client = DocumentIntelligenceClient(
        endpoint=endpoint, 
        credential=AzureKeyCredential(key)
    )
    
    print(f"Analyzing document: {file_path}")
    print("=" * 100)
    
    # Open and read the document file in binary mode
    with open(file_path, "rb") as file:
        # Start the analysis using the prebuilt-layout model
        # The poller pattern is used for long-running operations
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-layout",  # The model ID for layout analysis
            body=file  # The document to analyze
        )
        
        # Wait for the analysis to complete and get the result
        result = poller.result()
    
    print(f"✓ Analysis complete! Model used: {result.model_id}")
    print("=" * 100)
    
    # =========================================================================
    # STYLE DETECTION (Handwritten vs Printed Text)
    # =========================================================================
    # Below code identifies whether the document contains handwritten text
    print("\n📝 DOCUMENT STYLE ANALYSIS:")
    if result.styles:
        for idx, style in enumerate(result.styles, 1):
            # Check if this style represents handwritten content
            if style.is_handwritten:
                print(f"  Style #{idx}: Document contains handwritten content")
                print(f"    • Confidence: {style.confidence:.2%}")
                
                # Show a sample of the handwritten text if available
                if style.spans:
                    span = style.spans[0]
                    sample_text = result.content[span.offset:span.offset + min(span.length, 100)]
                    print(f"    • Sample: '{sample_text}...'")
            else:
                print(f"  Style #{idx}: Document contains no handwritten content (printed/typed)")
    else:
        print("  No style information available")
    
    # =========================================================================
    # PAGE-BY-PAGE ANALYSIS
    # =========================================================================
    # Below code processes each page to extract lines and selection marks
    print("\n" + "=" * 100)
    print("📄 PAGE-BY-PAGE LAYOUT ANALYSIS")
    print("=" * 100)
    
    for page_idx, page in enumerate(result.pages, 1):
        print(f"\n--- PAGE {page_idx} ---")
        print(f"  • Dimensions: {page.width} x {page.height} {page.unit}")
        print(f"  • Rotation angle: {page.angle}°")
        print(f"  • Total lines: {len(page.lines)}")
        print(f"  • Total words: {len(page.words)}")
        
        # ---------------------------------------------------------------------
        # TEXT LINES EXTRACTION
        # ---------------------------------------------------------------------
        # Below code extracts all text lines in their reading order
        print(f"\n  📖 TEXT LINES (showing first 10 of {len(page.lines)} lines):")
        for line_idx, line in enumerate(page.lines[:10], 1):
            # Each line contains:
            # - content: The actual text
            # - polygon: Bounding box coordinates showing where the line appears
            print(f"    Line #{line_idx}: '{line.content}'")
            print(f"      Position: {line.polygon[:8]}")  # Show first 4 coordinate points
        
        if len(page.lines) > 10:
            print(f"    ... and {len(page.lines) - 10} more lines")
        
        # ---------------------------------------------------------------------
        # SELECTION MARKS DETECTION (Checkboxes)
        # ---------------------------------------------------------------------
        # Below code detects checkboxes and their state (checked/unchecked)
        if page.selection_marks:
            print(f"\n  ☑️ SELECTION MARKS (checkboxes found: {len(page.selection_marks)}):")
            for mark_idx, selection_mark in enumerate(page.selection_marks, 1):
                # Each selection mark has:
                # - state: "selected" (checked) or "unselected" (unchecked)
                # - confidence: Accuracy of the detection
                state_symbol = "✓" if selection_mark.state == "selected" else "☐"
                print(f"    Selection Mark #{mark_idx}: {state_symbol} {selection_mark.state.upper()}")
                print(f"      Confidence: {selection_mark.confidence:.2%}")
                print(f"      Position: {selection_mark.polygon[:8]}")
        else:
            print("\n  ☑️ SELECTION MARKS: None detected")
    
    # =========================================================================
    # TABLE EXTRACTION
    # =========================================================================
    # Below code extracts all tables with their complete structure
    print("\n" + "=" * 100)
    print("📊 TABLE ANALYSIS")
    print("=" * 100)
    
    if result.tables:
        print(f"\nFound {len(result.tables)} table(s) in the document\n")
        
        for table_idx, table in enumerate(result.tables, 1):
            print(f"--- TABLE #{table_idx} ---")
            print(f"  • Rows: {table.row_count}")
            print(f"  • Columns: {table.column_count}")
            print(f"  • Total cells: {len(table.cells)}")
            
            # Show which page the table is on
            if table.bounding_regions:
                print(f"  • Location: Page {table.bounding_regions[0].page_number}")
            
            print(f"\n  TABLE CONTENT (Cell-by-Cell):")
            
            # Display each cell with its position and content
            for cell in table.cells:
                # Each cell contains:
                # - row_index: Row position (0-based)
                # - column_index: Column position (0-based)
                # - content: Text inside the cell
                # - kind: Type of cell (columnHeader, rowHeader, or regular content)
                
                cell_type = ""
                if cell.kind == "columnHeader":
                    cell_type = " [HEADER]"
                elif cell.kind == "rowHeader":
                    cell_type = " [ROW HEADER]"
                
                # Show cell spans if it's a merged cell
                span_info = ""
                if cell.row_span and cell.row_span > 1:
                    span_info += f" (spans {cell.row_span} rows)"
                if cell.column_span and cell.column_span > 1:
                    span_info += f" (spans {cell.column_span} columns)"
                
                print(f"    Cell[{cell.row_index}][{cell.column_index}]: '{cell.content}'{cell_type}{span_info}")
            
            print()  # Empty line between tables
    else:
        print("\nNo tables detected in the document")
    
    # =========================================================================
    # FULL TEXT CONTENT
    # =========================================================================
    # Below code displays the complete extracted text in reading order
    print("=" * 100)
    print("📋 FULL EXTRACTED TEXT CONTENT")
    print("=" * 100)
    print(result.content)
    print("=" * 100)
    print(f"\nTotal characters extracted: {len(result.content)}")
    print("\n✓ Layout analysis complete!")


if __name__ == "__main__":
    # Run the layout analysis
    analyze_layout()
