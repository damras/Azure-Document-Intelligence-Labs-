# Lab: Azure Document Intelligence - Layout API

This lab demonstrates the capabilities of Azure AI Document Intelligence's **Layout API** for understanding document structure. You'll learn how to extract tables, detect selection marks (checkboxes), analyze page layouts, and distinguish between handwritten and printed text.

---

## 📋 Prerequisites

This lab assumes you have **completed the Read API lab** and have:

✅ `Labs/` folder with `.env` file containing Azure credentials  
✅ Virtual environment created (`.venv`) in the `Labs/` folder  
✅ Dependencies installed from `requirements.txt`  

If not, please complete the **Read API lab** first to set up your environment.

---

## 🛠️ Setup Instructions

### Step 1: Create Layout Lab Directory

```bash
# Navigate to the Labs directory
cd Labs

# Create the lab-2-layout folder
mkdir lab-2-layout

# Navigate into the lab-2-layout folder
cd lab-2-layout
```

### Step 2: Create Data Folder

```bash
# Create folder for sample documents
mkdir data
```

Your directory structure should now look like:
```
Labs/
├── .env
├── requirements.txt
├── .venv/
├── lab-1-read/
│   ├── data/
│   ├── read.py
│   ├── searchable_pdf.py
│   └── read_batch_demo.py
└── lab-2-layout/
    └── data/
```

### Step 3: Add Sample Documents

Place your sample documents in the `data/` folder. For this lab, you'll need documents that demonstrate:
- Tables (invoices, reports, spreadsheets)
- Page structure (multi-page documents)
- Text content for extraction

**Sample files for this lab** (if provided):
- `layout.png` - Basic layout analysis
- `layout-pageobject.png` - Page object structure demonstration
- `layout-finacialreport.png` - Financial report with tables
- `sample-layout.pdf` - PDF document with mixed content

---

## 🎯 Lab Exercise: Understanding Document Layout

### Objective

Learn how to use the **prebuilt-layout model** to extract complete document structure including:
- **Text** with reading order and positioning
- **Tables** with cell-by-cell structure
- **Selection marks** (checkboxes) and their states
- **Handwriting detection** vs printed text
- **Page layout** information (dimensions, angles, structure)

### What You'll Learn

- How to use the Layout API for document structure understanding
- Detecting and extracting tables automatically with row/column/cell information
- Identifying selection marks (checkboxes/radio buttons) and their states
- Distinguishing between handwritten and printed content
- Understanding page objects and layout structure
- Extracting text lines with precise positioning (bounding boxes)

---

### Step 1: Create the Python Script

In the `lab-2-layout` directory, create a new file named `layout.py`:

```bash
# Make sure you're in the Labs/lab-2-layout directory
type nul > layout.py
```

---

### Step 2: Copy the Complete Code

Open `layout.py` in VS Code and paste the following code:

```python
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
# The ../ means go up one level from 'lab-2-layout' folder to 'Labs' folder
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
```

---

### Step 3: What This Code Does

This script demonstrates the complete capabilities of the **Layout API**:

#### 1. **Authentication & Setup**
- Loads Azure credentials from the `../.env` file (in the parent `Labs` folder)
- Initializes the Document Intelligence client with your endpoint and API key

#### 2. **Document Analysis**
- Opens a local document file (PNG, JPG, or PDF)
- Sends it to Azure's **prebuilt-layout** model for comprehensive structure extraction
- Uses the **poller pattern** for asynchronous processing (submit → wait → retrieve results)

#### 3. **Style Detection (Handwritten vs Printed Text)**
- Identifies whether the document contains handwritten or printed text
- Provides confidence scores for handwriting detection
- Shows samples of handwritten content if detected

#### 4. **Page-by-Page Processing**

**Page Information:**
- Extracts page dimensions (width × height)
- Detects rotation angle
- Counts total lines and words

**Text Lines Extraction:**
- Shows all text lines in their reading order
- Provides bounding box coordinates (polygon points) for each line
- Displays the first 10 lines to avoid overwhelming output

**Selection Marks Detection:**
- Detects checkboxes and radio buttons
- Determines their state: `selected` (checked ✓) or `unselected` (unchecked ☐)
- Provides confidence scores for detection accuracy
- Shows precise positioning with bounding boxes

#### 5. **Table Extraction**
- Automatically detects all tables in the document
- Extracts complete table structure:
  - **Row count** and **column count**
  - **Cell-by-cell content** with positions
  - **Cell types**: column headers, row headers, or data cells
  - **Merged cells**: Detects row spans and column spans
  - **Page location**: Which page the table appears on

#### 6. **Full Text Content**
- Displays the complete extracted text in reading order
- Shows total character count

---

### Step 4: Understanding Key Concepts

#### **Bounding Boxes (Polygons)**
```python
line.polygon = [x1, y1, x2, y2, x3, y3, x4, y4]
```
- Represents 4 corner points of a rectangle surrounding text
- Coordinates are in pixels from the top-left corner (0,0)
- Example: `[468, 593, 818, 593, 818, 610, 468, 609]`
  - Top-left: (468, 593)
  - Top-right: (818, 593)
  - Bottom-right: (818, 610)
  - Bottom-left: (468, 609)
  - Width: 350 pixels, Height: 17 pixels

#### **Selection Mark States**
```python
selection_mark.state = "selected"  # or "unselected"
```
- **selected**: Checkbox is checked (✓)
- **unselected**: Checkbox is empty (☐)
- Confidence score indicates detection accuracy

#### **Table Cell Properties**
```python
cell.kind = "columnHeader"  # or "rowHeader" or None (regular data)
cell.row_span = 2  # Cell spans 2 rows (merged cell)
cell.column_span = 1  # Cell spans 1 column (normal)
```

#### **Page Objects**
- `page.width` and `page.height`: Page dimensions in pixels
- `page.angle`: Rotation angle (0° = upright, 90° = rotated clockwise)
- `page.unit`: Measurement unit (usually "pixel")

---

### Step 5: Try Different Sample Files

The script is configured to work with multiple sample files. You can experiment by changing the `file_path` variable in the code:

```python
# Try each of these files to see different results:
file_path = "data/layout.png"                    # Basic layout
file_path = "data/layout-pageobject.png"         # Page objects demo
file_path = "data/layout-finacialreport.png"     # Financial report with tables
file_path = "data/sample-layout.pdf"             # PDF with mixed content
```

**What each file demonstrates:**
- **layout.png**: Basic layout structure and text extraction
- **layout-pageobject.png**: Page object properties (dimensions, angles, structure)
- **layout-finacialreport.png**: Complex tables and financial data
- **sample-layout.pdf**: Multi-page PDF with various elements

---

### Step 6: Run the Script

```bash
# Ensure you're in the Labs/lab-2-layout directory
# Make sure your virtual environment is activated (.venv)
python layout.py
```

---

### Step 7: Expected Output

When you run the script, you'll see output similar to this:

```
Analyzing document: data/layout-pageobject.png
====================================================================================================
✓ Analysis complete! Model used: prebuilt-layout
====================================================================================================

📝 DOCUMENT STYLE ANALYSIS:
  Style #1: Document contains no handwritten content (printed/typed)

====================================================================================================
📄 PAGE-BY-PAGE LAYOUT ANALYSIS
====================================================================================================

--- PAGE 1 ---
  • Dimensions: 2550 x 3300 pixel
  • Rotation angle: 0°
  • Total lines: 45
  • Total words: 320

  📖 TEXT LINES (showing first 10 of 45 lines):
    Line #1: 'Document Title'
      Position: [468, 593, 818, 593, 818, 610, 468, 609]
    Line #2: 'Section 1: Introduction'
      Position: [120, 680, 450, 680, 450, 698, 120, 698]
    Line #3: 'This is sample text for layout analysis.'
      Position: [120, 720, 580, 720, 580, 738, 120, 738]
    ...

  ☑️ SELECTION MARKS: None detected

====================================================================================================
📊 TABLE ANALYSIS
====================================================================================================

Found 2 table(s) in the document

--- TABLE #1 ---
  • Rows: 4
  • Columns: 3
  • Total cells: 12
  • Location: Page 1

  TABLE CONTENT (Cell-by-Cell):
    Cell[0][0]: 'Item' [HEADER]
    Cell[0][1]: 'Quantity' [HEADER]
    Cell[0][2]: 'Price' [HEADER]
    Cell[1][0]: 'Product A'
    Cell[1][1]: '2'
    Cell[1][2]: '$50.00'
    Cell[2][0]: 'Product B'
    Cell[2][1]: '3'
    Cell[2][2]: '$30.00'
    ...

====================================================================================================
📋 FULL EXTRACTED TEXT CONTENT
====================================================================================================
Document Title
Section 1: Introduction
This is sample text for layout analysis.
Item | Quantity | Price
Product A | 2 | $50.00
Product B | 3 | $30.00
...
====================================================================================================

Total characters extracted: 1,245

✓ Layout analysis complete!
```

---

## 🔍 Understanding the Layout API

### Key Differences: Read API vs Layout API

| Feature | Read API | Layout API |
|---------|----------|------------|
| **Primary Purpose** | Text extraction only | Document structure understanding |
| **Tables** | ❌ Not detected | ✅ Full table structure with cells |
| **Selection Marks** | ❌ Not detected | ✅ Checkboxes and state detection |
| **Handwriting Detection** | ✅ Basic detection | ✅ Detailed style analysis |
| **Document Structure** | ❌ Not available | ✅ Page layout and hierarchy |
| **Cell Types** | ❌ N/A | ✅ Headers vs data cells |
| **Merged Cells** | ❌ N/A | ✅ Row/column spans detected |
| **Performance** | Faster | Slightly slower (more analysis) |
| **Best For** | Simple text extraction | Structured document processing |

### When to Use Layout API

✅ **Use Layout API when you need:**
- **Table extraction** from invoices, reports, receipts, financial statements
- **Form processing** with checkboxes or radio buttons
- **Document structure** understanding (where elements are positioned)
- **Page layout analysis** (dimensions, rotation, structure)
- **Precise element positioning** with bounding boxes
- **Handwriting vs printed text** detection
- **Selection mark detection** for automated form processing

❌ **Use Read API instead when:**
- You **only need plain text** extraction (no structure needed)
- **Speed is critical** (Read API is faster)
- Documents have **no complex structure** (no tables/forms)
- No need for table or checkbox processing

---

## 🧪 Troubleshooting

### Issue: File Not Found Error
**Symptom**: 
```
FileNotFoundError: [Errno 2] No such file or directory: 'data/layout-pageobject.png'
```

**Solution**: 
- Ensure you're running the script from the `Labs/lab-2-layout/` directory
- Verify the `data/` folder exists: `cd lab-2-layout` → `dir` (should show `data/` folder)
- Check that sample files exist in the `data/` folder
- Update the `file_path` variable to match the actual filename

### Issue: No Tables Detected
**Symptom**: 
```
No tables detected in the document
```

**Solution**: 
- Ensure your document actually contains tables with clear row/column structure
- Try with the `layout-finacialreport.png` sample which has tables
- Tables must have visible borders or clear cell separation for detection

### Issue: No Selection Marks Found
**Symptom**: 
```
☑️ SELECTION MARKS: None detected
```

**Solution**:
- Document must contain actual checkboxes (☐ ☑) or radio buttons (○ ◉)
- HTML form symbols in screenshots might not be detected
- Use actual form PDFs with fillable fields or scanned paper forms
- Try creating a simple Word document with checkbox controls, save as PDF

### Issue: All Text Detected as Printed (No Handwriting)
**Symptom**: 
```
Style #1: Document contains no handwritten content (printed/typed)
```

**Solution**:
- This is **expected behavior** for typed/printed documents
- To test handwriting detection, use documents with actual handwritten text
- The provided sample files are mostly printed/typed content
- Try scanning a handwritten note or form

### Issue: Environment Variables Not Loaded
**Symptom**: 
```
endpoint = None
key = None
```

**Solution**:
- Verify the `.env` file exists in the `Labs/` folder (parent directory)
- Check `.env` file contains:
  ```
  AZ_DOCINT_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
  AZ_DOCINT_KEY=your-api-key-here
  ```
- Ensure no extra spaces or quotes around values
- Virtual environment must be activated

---

## 📚 Additional Resources

- [Layout Model Documentation](https://learn.microsoft.com/azure/ai-services/document-intelligence/concept-layout)
- [Table Extraction Guide](https://learn.microsoft.com/azure/ai-services/document-intelligence/concept-layout#tables)
- [Selection Marks Documentation](https://learn.microsoft.com/azure/ai-services/document-intelligence/concept-layout#selection-marks)
- [Python SDK Reference](https://learn.microsoft.com/python/api/azure-ai-documentintelligence/)
- [Document Intelligence Studio](https://documentintelligence.ai.azure.com/) - Test models visually

---

## 🎓 What You've Learned

By completing this lab, you've gained hands-on experience with:

✅ **Layout API fundamentals** and document structure extraction  
✅ **Table detection and extraction** with cell-by-cell structure analysis  
✅ **Selection mark detection** for automated checkbox/form processing  
✅ **Handwriting vs printed text** identification and style analysis  
✅ **Page object analysis** with dimensions, rotation, and positioning  
✅ **Bounding boxes** for precise element location on pages  
✅ **Multiple file format support** (PNG, JPG, PDF)  
✅ **Difference between Read and Layout APIs** and when to use each  
✅ **Cell types and merged cells** in table structures  

---

## 🚀 Next Steps

Continue your learning journey with:

- **Lab 3 - General Document Model**: Extract key-value pairs from forms and structured documents using the prebuilt-document model
  
- **Lab 4 - Prebuilt Models**: Explore specialized industry-specific models:
  - **prebuilt-bankStatement.us**: Extract bank statement data (accounts, transactions, balances)
  - **prebuilt-invoice**: Extract invoice-specific fields (vendor, customer, line items, totals)
  - **prebuilt-receipt**: Extract receipt data (merchant, items, payment summary)
  - **prebuilt-creditCard**: Extract credit/debit card information
  - **prebuilt-idDocument**: Extract ID card, passport, and license information

---

## 📝 Lab Files Summary

| File | Purpose | Key Features |
|------|---------|--------------|
| `layout.py` | Complete layout analysis demo | Tables, selection marks, handwriting detection, page objects, text extraction |
| `data/layout.png` | Basic layout sample | Simple document structure for testing |
| `data/layout-pageobject.png` | Page object demo | Page structure and properties demonstration |
| `data/layout-finacialreport.png` | Financial report sample | Complex tables and financial data |
| `data/sample-layout.pdf` | PDF sample | Multi-page PDF with various elements |

---

**Happy Learning! 🎉**
