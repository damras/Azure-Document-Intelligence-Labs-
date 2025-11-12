# Lab 3: General Document Model - Key-Value Pair Extraction

## Overview
This lab demonstrates Azure AI Document Intelligence's **General Document Model** (`prebuilt-document`), which extracts key-value pairs from form-like documents. This model is ideal for documents containing structured information with field labels and values, such as:
- Employment applications
- Contracts and agreements
- Questionnaires and forms
- Drill reports and technical documents
- General business documents with labeled fields

### What You'll Learn
- Extract key-value pairs (field labels and their values) from documents
- Detect and extract tables from documents
- Understand when to use the General Document model vs. Read or Layout models
- Work with the `azure-ai-formrecognizer` SDK

---

## Prerequisites
Before starting this lab, you should have completed:
- **Lab 1 (Read API)**: Basic environment setup, .env configuration, and text extraction
- **Lab 2 (Layout API)**: Understanding of document structure analysis

You should already have:
- ✅ Python virtual environment (`.venv` in the Labs folder)
- ✅ `.env` file with Azure credentials configured
- ✅ `requirements.txt` with all dependencies installed

---

## Lab Setup

### Step 1: Create Lab Folder Structure
Navigate to the `Labs` folder and create the lab-3-general structure:

```bash
cd Labs
mkdir lab-3-general
cd lab-3-general
mkdir data
```

### Step 2: Add Sample Documents
Copy sample documents to the `data/` folder. You need documents with key-value pairs like:
- Forms with labeled fields (Name:, Date:, Amount:, etc.)
- Employment documents
- Technical reports
- Any document with label-value structure

For this lab, we're using:
- `generaldoc-drillreport.png` - Drill report with technical key-value pairs
- `generaldoc-employment.png` - Employment document with form fields
- `restructure.png` - Restructure document
- `restructure-power-bi.png` - Power BI restructure document

---

## Understanding the General Document Model

### Model Comparison

| Feature | Read Model | Layout Model | General Document Model |
|---------|-----------|--------------|------------------------|
| **Text Extraction** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Bounding Boxes** | ✅ Yes | ✅ Yes | ✅ Yes |
| **Tables** | ❌ No | ✅ Yes | ✅ Yes |
| **Selection Marks** | ❌ No | ✅ Yes | ✅ Yes |
| **Key-Value Pairs** | ❌ No | ❌ No | ✅ **Yes (Primary Feature)** |
| **Best For** | Plain text, OCR | Document structure, tables | Forms, labeled documents |

### Key-Value Pair Extraction
The General Document model automatically identifies:
- **Keys**: Field labels (e.g., "Employee Name:", "Date:", "Amount:")
- **Values**: Corresponding field values (e.g., "John Doe", "2024-01-15", "$1,000")

Example:
```
Document contains:     →    Extracted:
"Name: John Doe"       →    Key: "Name:", Value: "John Doe"
"Date: 2024-01-15"     →    Key: "Date:", Value: "2024-01-15"
"Amount: $1,000"       →    Key: "Amount:", Value: "$1,000"
```

---

## Code Implementation

### Step 3: Create the Python Script

Create a file named `general_document.py` in the `lab-3-general` folder with the following code:

```python
"""
Azure AI Document Intelligence - General Document Model Demo
This script demonstrates the prebuilt-document model for extracting key-value pairs from documents.

The General Document model (prebuilt-document) extracts:
- Key-value pairs (form fields and their values)
- Tables with structure
- Text content
- Document structure

This model is ideal for documents that contain form-like structures with labels and values,
such as contracts, applications, questionnaires, and general business documents.
"""

from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import os
from dotenv import load_dotenv

# Load credentials from parent Labs directory
# The ../ means go up one level from 'lab-3-general' folder to 'Labs' folder
load_dotenv(dotenv_path="../.env")

# Get Azure endpoint and API key from environment variables
endpoint = os.getenv("AZ_DOCINT_ENDPOINT")
key = os.getenv("AZ_DOCINT_KEY")


def analyze_general_document():
    """
    Main function to analyze a document using the General Document (prebuilt-document) model.
    
    The prebuilt-document model is designed for:
    - Extracting key-value pairs (e.g., "Name: John Doe", "Date: 2024-01-15")
    - Form-like documents with labels and values
    - General business documents with structured information
    - Documents where you need to identify field labels and their corresponding values
    """
    
    # Path to the document you want to analyze
    # Available sample files in data/ folder - try each one to see different results:
    # - "data/generaldoc-drillreport.png" - Drill report with key-value pairs
    # - "data/generaldoc-employment.png" - Employment document with form fields
    # - "data/restructure.png" - Restructure document
    # - "data/restructure-power-bi.png" - Power BI restructure document
    # Just change the filename below to try different documents!
    
    file_path = "data/generaldoc-employment.png"  # Change this to any file from the list above
    
    # Initialize Document Intelligence client with your credentials
    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, 
        credential=AzureKeyCredential(key)
    )
    
    print(f"Analyzing document: {file_path}")
    print("=" * 100)
    
    # Open and read the document file in binary mode
    with open(file_path, "rb") as file:
        # Start the analysis using the prebuilt-document model
        # The poller pattern is used for long-running operations
        poller = document_analysis_client.begin_analyze_document(
            "prebuilt-document",  # The model ID for general document analysis
            document=file  # The document to analyze
        )
        
        # Wait for the analysis to complete and get the result
        result = poller.result()
    
    print(f"✓ Analysis complete! Model used: {result.model_id}")
    print("=" * 100)
    
    # =========================================================================
    # KEY-VALUE PAIRS EXTRACTION
    # =========================================================================
    # Below code extracts key-value pairs (form fields) from the document
    # This is the primary feature of the prebuilt-document model
    print("\n📋 KEY-VALUE PAIRS FOUND IN DOCUMENT")
    print("=" * 100)
    
    if result.key_value_pairs:
        print(f"\nTotal key-value pairs detected: {len(result.key_value_pairs)}\n")
        
        for idx, kv_pair in enumerate(result.key_value_pairs, 1):
            # Each key-value pair contains:
            # - key: The field label (e.g., "Name:", "Date:", "Amount:")
            # - value: The field value (e.g., "John Doe", "2024-01-15", "$1,000")
            
            if kv_pair.key and kv_pair.value:
                # Both key and value are present
                key_text = kv_pair.key.content
                value_text = kv_pair.value.content
                
                print(f"  {idx}. Key: '{key_text}'")
                print(f"     Value: '{value_text}'")
                
                # Show confidence scores if available
                if hasattr(kv_pair.key, 'confidence') and kv_pair.key.confidence:
                    print(f"     Key confidence: {kv_pair.key.confidence:.2%}")
                if hasattr(kv_pair.value, 'confidence') and kv_pair.value.confidence:
                    print(f"     Value confidence: {kv_pair.value.confidence:.2%}")
                
                print()
                
            elif kv_pair.key:
                # Only key is present (value might be empty or not detected)
                key_text = kv_pair.key.content
                print(f"  {idx}. Key: '{key_text}'")
                print(f"     Value: [No value detected]")
                print()
    else:
        print("\n⚠️ No key-value pairs found in the document.")
        print("This might be because:")
        print("  • The document doesn't have a form-like structure")
        print("  • The document has only plain text without labeled fields")
        print("  • Try using the 'prebuilt-layout' model for such documents")
    
    # =========================================================================
    # TABLES EXTRACTION (if any)
    # =========================================================================
    # Below code extracts tables from the document
    # The prebuilt-document model also detects tables
    if result.tables:
        print("\n" + "=" * 100)
        print("📊 TABLES FOUND IN DOCUMENT")
        print("=" * 100)
        print(f"\nTotal tables detected: {len(result.tables)}\n")
        
        for table_idx, table in enumerate(result.tables, 1):
            print(f"--- TABLE #{table_idx} ---")
            print(f"  • Rows: {table.row_count}")
            print(f"  • Columns: {table.column_count}")
            print(f"  • Total cells: {len(table.cells)}")
            
            if table.bounding_regions:
                print(f"  • Location: Page {table.bounding_regions[0].page_number}")
            
            print(f"\n  TABLE CONTENT (first 5 rows):")
            
            # Display table in row format (first 5 rows only to avoid clutter)
            displayed_rows = 0
            for row_idx in range(min(5, table.row_count)):
                row_cells = [c for c in table.cells if c.row_index == row_idx]
                row_cells.sort(key=lambda c: c.column_index)
                row_content = " | ".join([c.content for c in row_cells])
                print(f"    {row_content}")
                displayed_rows += 1
            
            if table.row_count > 5:
                print(f"    ... and {table.row_count - 5} more rows")
            
            print()
    
    # =========================================================================
    # PAGES SUMMARY
    # =========================================================================
    # Below code provides a summary of pages in the document
    print("=" * 100)
    print("📄 DOCUMENT PAGES SUMMARY")
    print("=" * 100)
    
    if result.pages:
        print(f"\nTotal pages: {len(result.pages)}\n")
        
        for page_idx, page in enumerate(result.pages, 1):
            print(f"  Page {page_idx}:")
            print(f"    • Dimensions: {page.width} x {page.height} {page.unit}")
            print(f"    • Rotation: {page.angle}°")
            print(f"    • Lines: {len(page.lines)}")
            print(f"    • Words: {len(page.words)}")
    
    # =========================================================================
    # FULL TEXT CONTENT
    # =========================================================================
    # Below code displays the complete extracted text
    print("\n" + "=" * 100)
    print("📋 FULL EXTRACTED TEXT CONTENT")
    print("=" * 100)
    print(f"\nTotal characters: {len(result.content)}\n")
    print(result.content)
    print("\n" + "=" * 100)
    
    print("\n✓ General document analysis complete!")


if __name__ == "__main__":
    # Run the general document analysis
    analyze_general_document()
```

---

## Running the Lab

### Step 4: Activate Virtual Environment

Navigate to the `lab-3-general` folder and activate the virtual environment:

**PowerShell:**
```powershell
cd Labs\lab-3-general
..\.venv\Scripts\Activate.ps1
```

**Command Prompt:**
```cmd
cd Labs\lab-3-general
..\.venv\Scripts\activate.bat
```

### Step 5: Run the Script

```bash
python general_document.py
```

---

## Expected Output

When you run the script, you should see output similar to:

```
Analyzing document: data/generaldoc-employment.png
====================================================================================================
✓ Analysis complete! Model used: prebuilt-document
====================================================================================================

📋 KEY-VALUE PAIRS FOUND IN DOCUMENT
====================================================================================================

Total key-value pairs detected: 15

  1. Key: 'Employee Name:'
     Value: 'John Smith'
     Key confidence: 99.50%
     Value confidence: 99.80%

  2. Key: 'Employee ID:'
     Value: 'EMP-12345'
     Key confidence: 98.70%
     Value confidence: 99.20%

  3. Key: 'Department:'
     Value: 'Engineering'
     Key confidence: 99.10%
     Value confidence: 98.50%

  ... (more key-value pairs)

====================================================================================================
📄 DOCUMENT PAGES SUMMARY
====================================================================================================

Total pages: 1

  Page 1:
    • Dimensions: 1700.0 x 2200.0 pixel
    • Rotation: 0.0°
    • Lines: 45
    • Words: 123

====================================================================================================
📋 FULL EXTRACTED TEXT CONTENT
====================================================================================================

Total characters: 587

[Full text content of the document...]

====================================================================================================

✓ General document analysis complete!
```

---

## Experiment and Learn

### Try Different Documents
The script includes 4 sample files. Change the `file_path` variable to analyze different documents:

```python
# Try each of these:
file_path = "data/generaldoc-drillreport.png"      # Technical drill report
file_path = "data/generaldoc-employment.png"        # Employment form
file_path = "data/restructure.png"                  # Restructure document
file_path = "data/restructure-power-bi.png"         # Power BI document
```

### Key Points to Observe

1. **Key-Value Pair Detection**
   - Notice how the model identifies field labels (keys) and their values
   - Check the confidence scores for each detection
   - Some documents may have more key-value pairs than others

2. **Table Detection**
   - If your document contains tables, they will be extracted
   - Compare with Lab 2's layout analysis for table extraction

3. **When to Use This Model**
   - ✅ Forms with labeled fields
   - ✅ Applications and questionnaires
   - ✅ Contracts with field-value structure
   - ❌ Plain text documents without labels → Use Read model
   - ❌ Complex layouts without form structure → Use Layout model

---

## SDK Differences: azure-ai-formrecognizer vs azure-ai-documentintelligence

This lab uses a **different SDK** than Labs 1 and 2:

| Aspect | Lab 1 & 2 | Lab 3 |
|--------|-----------|-------|
| **SDK** | `azure-ai-documentintelligence` | `azure-ai-formrecognizer` |
| **Client Class** | `DocumentIntelligenceClient` | `DocumentAnalysisClient` |
| **Method** | `begin_analyze_document(model, body=file)` | `begin_analyze_document(model, document=file)` |
| **Models** | `prebuilt-read`, `prebuilt-layout` | `prebuilt-document` |
| **Status** | Newer SDK | Established SDK |

### Why Two SDKs?
- The `azure-ai-formrecognizer` SDK is the established SDK with broader model support
- The `azure-ai-documentintelligence` SDK is newer with modern API design
- Both are officially supported by Microsoft

---

## Common Issues and Solutions

### Issue 1: "Model not found" Error
**Solution:** Make sure you're using `azure-ai-formrecognizer`, not `azure-ai-documentintelligence`

```python
# ✅ Correct for Lab 3
from azure.ai.formrecognizer import DocumentAnalysisClient

# ❌ Wrong SDK for this lab
from azure.ai.documentintelligence import DocumentIntelligenceClient
```

### Issue 2: No Key-Value Pairs Found
**Possible Reasons:**
- Document doesn't have a form-like structure with labels
- Text is too dense or unstructured
- **Solution:** Try the Layout model (Lab 2) for such documents

### Issue 3: Low Confidence Scores
- Some key-value pairs may have lower confidence if:
  - Text is handwritten or unclear
  - Label-value association is ambiguous
  - Document quality is poor

---

## Next Steps

� **Ready for the final lab?**

### Continue to Lab 4: Prebuilt Models
After mastering the general-purpose models (Read, Layout, and General Document), you're ready to explore **industry-specific prebuilt models**:

- **Lab 4 - Prebuilt Models**: Specialized models for common business documents
  - Bank Statements (accounts, transactions, balances)
  - Invoices (vendor, customer, line items, payment details)
  - Credit Cards (card numbers, expiration, CVV - with PCI DSS considerations)
  - Identity Documents (licenses, passports, national IDs - with privacy compliance)
  - Receipts (merchant info, items, totals, tax)

### Summary of Your Learning Journey

| Lab | Model | Primary Use Case | Key Feature |
|-----|-------|------------------|-------------|
| **Lab 1** | Read API | Text extraction | OCR, searchable PDFs, batch processing |
| **Lab 2** | Layout API | Structure analysis | Tables, selection marks, page layout |
| **Lab 3** | General Document | Form processing | **Key-value pairs** ✅ |
| **Lab 4** | Prebuilt Models | Industry-specific processing | Specialized field extraction |

### Further Exploration
- Try analyzing your own documents with the General Document model
- Combine multiple models in a single workflow
- Explore the Azure Document Intelligence Studio for visual testing
- Consider custom models for unique document types specific to your business

---

## Additional Resources
- [Azure Document Intelligence Documentation](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/)
- [Python SDK Reference - Form Recognizer](https://learn.microsoft.com/en-us/python/api/azure-ai-formrecognizer/)
- [Prebuilt Models Overview](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/concept-model-overview)
- [Document Intelligence Studio](https://documentintelligence.ai.azure.com/studio)

---

**Happy Learning! 🚀**
