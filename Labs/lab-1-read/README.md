# Lab: Azure Document Intelligence - Read API

This lab demonstrates the capabilities of Azure AI Document Intelligence's **Read API** through three progressive exercises. You'll learn how to extract text from documents, create searchable PDFs, and process multiple files in batch mode.

---

## 📋 Prerequisites

Before starting this lab, ensure you have:

### 1. Azure Document Intelligence Resource
- An active Azure subscription
- Azure AI Document Intelligence service already created
- Endpoint URL and API Key available (you'll use these in the setup)

### 2. Development Environment
- **Python**: Version 3.8 or above (Python 3.12 recommended)
  - Verify installation: `python --version`
- **Visual Studio Code** (recommended)

---

## 🛠️ Setup Instructions

### Step 1: Create Project Directory Structure

Create the folder structure for your labs:

```bash
# Create the main Labs directory and the lab-1-read subdirectory
mkdir Labs
cd Labs
mkdir lab-1-read
```

Your directory structure should look like:
```
Labs/
└── lab-1-read/
```

### Step 2: Create Environment Configuration File

Create a `.env` file in the `Labs` directory to store your Azure credentials:

```bash
# From the Labs directory, create the .env file
cd Labs
```

Create a new file named `.env` and add your Azure Document Intelligence credentials:

```env
AZ_DOCINT_ENDPOINT=https://<your-resource-name>.cognitiveservices.azure.com/
AZ_DOCINT_KEY=<your-api-key>
```

> **Important**: Replace `<your-resource-name>` with your actual Azure Document Intelligence resource name and `<your-api-key>` with your API key from the Azure Portal.

**Where to find your credentials:**
- Go to Azure Portal → Your Document Intelligence Resource
- Click on "Keys and Endpoint" in the left menu
- Copy "Endpoint" and "KEY 1"

### Step 3: Create Requirements File

In the `Labs` directory, create a `requirements.txt` file with the following dependencies:

```txt
azure-ai-documentintelligence
azure-core
python-dotenv
numpy
```

Your directory structure should now look like:
```
Labs/
├── .env
├── requirements.txt
└── lab-1-read/
```

### Step 4: Create Python Virtual Environment

Create and activate a virtual environment in the `Labs` directory:

```bash
# From the Labs directory
python -m venv .venv

# Activate the virtual environment
# On Windows (PowerShell):
.venv\Scripts\Activate.ps1

# On Windows (Command Prompt):
.venv\Scripts\activate.bat
```

You should see `(.venv)` prefix in your terminal prompt, indicating the virtual environment is active.

### Step 5: Install Required Dependencies

With the virtual environment activated, install the required packages:

```bash
pip install -r requirements.txt
```

Wait for the installation to complete. Verify the installation:

```bash
pip list
```

You should see these packages installed:
- `azure-ai-documentintelligence`
- `azure-core`
- `python-dotenv`
- `numpy`

### Step 6: Create Data Folder for Sample Documents

Navigate to the `lab-1-read` directory and create a `data` folder to store sample documents:

```bash
cd lab-1-read
mkdir data
```

Your directory structure should now look like:
```
Labs/
├── .env
├── requirements.txt
├── .venv/
└── lab-1-read/
    └── data/
```

> **Note**: You'll need to add sample documents to the `data/` folder. For this lab, you'll need:
> - `read.png` - For Exercise 1
> - `batch1.png`, `batch2.jpg`, `batch3.pdf` - For Exercise 3

---

## 🎯 Lab Exercises

### Exercise 1: Working with Read API - Basic Text Extraction

**Objective**: Learn how to extract text from a document using Azure Document Intelligence Read API, understand bounding boxes, confidence scores, and the poller pattern for asynchronous operations.

#### What You'll Learn:
- How to authenticate with Azure Document Intelligence
- Understanding the **poller pattern** for long-running operations
- Extracting text with **bounding box coordinates**
- Analyzing **confidence scores** for OCR accuracy
- Detecting **languages** and **handwriting**

#### Step 1: Create the Python Script

In the `lab-1-read` directory, create a new file named `read.py`:

```bash
# Make sure you're in the Labs/lab-1-read directory
cd Labs\lab-1-read
```

Create a new file `read.py` in VS Code or using:
```bash
type nul > read.py
```

#### Step 2: Copy the Code

Open `read.py` and paste the following code:

```python

# Import necessary libraries
from azure.core.credentials import AzureKeyCredential  # For API authentication
from azure.ai.documentintelligence import DocumentIntelligenceClient  # Main Document Intelligence client
import numpy as np  # For array operations
import os
from dotenv import load_dotenv  # To load credentials from .env file

# Load credentials from .env file
load_dotenv()

# Get Azure endpoint and API key from environment variables
endpoint = os.getenv("AZ_DOCINT_ENDPOINT", "https://<your-resource>.cognitiveservices.azure.com/")
key = os.getenv("AZ_DOCINT_KEY", "<your-key>")

def format_bounding_box(bounding_box):
    """
    Converts flat bounding box coordinates into readable format.
    
    A bounding box is a rectangle that surrounds text in the document.
    It's defined by 4 corner points (top-left, top-right, bottom-right, bottom-left).
    
    Input: [x1, y1, x2, y2, x3, y3, x4, y4] (flat list of 8 numbers)
    Output: "[x1, y1], [x2, y2], [x3, y3], [x4, y4]" (4 coordinate pairs)
    
    Example:
    Input:  [468, 593, 818, 593, 818, 610, 468, 609]
    Output: "[468, 593], [818, 593], [818, 610], [468, 609]"
    
    This represents a rectangle:
    - Top-left: (468, 593)
    - Top-right: (818, 593)
    - Bottom-right: (818, 610)
    - Bottom-left: (468, 609)
    - Width: 818 - 468 = 350 pixels
    - Height: 610 - 593 = 17 pixels
    """
    if not bounding_box:
        return "[]"
    
    # Reshape flat array [x1,y1,x2,y2,x3,y3,x4,y4] into pairs [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
    pairs = np.array(bounding_box).reshape(-1, 2)
    return str(pairs.tolist())

def analyze_read_local():
    """
    Main function to analyze a local document using the Read model.
    
    The Read model is optimized for:
    - Text extraction from images and PDFs
    - Multi-language support
    - Handwriting recognition
    - Getting text locations (bounding boxes)
    """
    # Initialize the Document Intelligence client with your credentials
    client = DocumentIntelligenceClient(endpoint, AzureKeyCredential(key))
    
    # Path to the document you want to analyze
    file_path = "data/read.png"
    
    print(f"Analyzing document: {file_path}")
    print("=" * 100)
    
    # Open and read the document file in binary mode
    with open(file_path, "rb") as file:
        """
        The poller pattern explained:
        
        Document analysis is a long-running operation (can take seconds to minutes).
        Instead of waiting synchronously, Azure uses a "poller" pattern:
        
        1. begin_analyze_document() - Starts the analysis and returns a "poller" object
           (Think of this like ordering food - you get a receipt number)
        
        2. poller.result() - Waits for completion and returns the final result
           (Like waiting for your order number to be called)
        
        This allows you to:
        - Check progress: poller.status()
        - Cancel if needed: poller.cancel()
        - Do other work while waiting
        """
        
        # Start the analysis using the prebuilt "read" model
        poller = client.begin_analyze_document(
            "prebuilt-read",  # The model ID for text extraction
            body=file  # The document to analyze (must use 'body' parameter)
        )
        
        # Wait for the analysis to complete and get the result
        result = poller.result()
    
    print(f"✓ Analysis complete! Model used: {result.model_id}")
    print("=" * 100)
    
    # =========================================================================
    # LANGUAGE DETECTION
    # =========================================================================
    print("\n📍 DETECTED LANGUAGES:")
    if result.languages:
        for lang in result.languages:
            print(f"  • {lang.locale} (confidence: {lang.confidence:.2%})")
    else:
        print("  No specific languages detected")
    
    # =========================================================================
    # HANDWRITING DETECTION
    # =========================================================================
    print("\n✍️ HANDWRITING DETECTION:")
    if result.styles:
        handwritten_found = False
        for style in result.styles:
            if style.is_handwritten:
                handwritten_found = True
                print(f"  • Handwritten text detected (confidence: {style.confidence:.2%})")
                # Show a sample of the handwritten text
                if style.spans:
                    span = style.spans[0]
                    sample = result.content[span.offset:span.offset + min(span.length, 100)]
                    print(f"    Sample: '{sample}...'")
        
        if not handwritten_found:
            print("  • No handwriting detected (all text is printed/typed)")
    else:
        print("  • No style information available")
    
    # =========================================================================
    # PAGE-BY-PAGE ANALYSIS
    # =========================================================================
    print("\n" + "=" * 100)
    print("📄 PAGE-BY-PAGE ANALYSIS")
    print("=" * 100)
    
    for page_num, page in enumerate(result.pages, start=1):
        print(f"\n--- Page {page_num} ---")
        print(f"Size: {page.width} x {page.height} {page.unit}")
        print(f"Angle: {page.angle}°")
        print(f"Lines detected: {len(page.lines)}")
        print(f"Words detected: {len(page.words)}")
        
        # =====================================================================
        # LINE-BY-LINE TEXT EXTRACTION
        # =====================================================================
        print(f"\n  📝 TEXT LINES (showing all {len(page.lines)} lines):")
        for line_idx, line in enumerate(page.lines, start=1):
            """
            Each line contains:
            - content: The actual text
            - polygon: 8 coordinates defining the bounding box [x1,y1,x2,y2,x3,y3,x4,y4]
            - spans: Character positions in the full document (offset and length)
            
            Note: Lines don't have confidence scores - only individual words do
            """
            print(f"\n    Line {line_idx}: '{line.content}'")
            print(f"      Bounding box: {format_bounding_box(line.polygon)}")
            if line.spans:
                print(f"      Position in document: offset={line.spans[0].offset}, length={line.spans[0].length}")
        
        # =====================================================================
        # WORD-BY-WORD ANALYSIS WITH CONFIDENCE SCORES
        # =====================================================================
        print(f"\n  🔍 WORD DETAILS (first 10 of {len(page.words)} words):")
        for word_idx, word in enumerate(page.words[:10], start=1):
            """
            Each word contains:
            - content: The word text
            - confidence: OCR confidence score (0.0 to 1.0)
            - polygon: Bounding box coordinates
            - span: Character position in the full document
            
            Confidence interpretation:
            - 0.95-1.00: Very high confidence (clear, printed text)
            - 0.80-0.95: Good confidence (may be handwritten or lower quality)
            - Below 0.80: Lower confidence (verify the text)
            """
            print(f"    Word {word_idx}: '{word.content}' | Confidence: {word.confidence:.2%} | Box: {format_bounding_box(word.polygon)}")
        
        if len(page.words) > 10:
            print(f"    ... and {len(page.words) - 10} more words")
    
    # =========================================================================
    # FULL EXTRACTED TEXT
    # =========================================================================
    print("\n" + "=" * 100)
    print("📋 FULL EXTRACTED TEXT CONTENT")
    print("=" * 100)
    print(result.content)
    print("=" * 100)
    print(f"\nTotal characters extracted: {len(result.content)}")

if __name__ == "__main__":
    analyze_read_local()
```

#### Step 3: What This Code Does

This script demonstrates the complete workflow of the Azure Document Intelligence Read API:

1. **Authentication**: Connects to Azure using your endpoint and API key from the `.env` file
2. **Document Loading**: Opens a local image file (`data/read.png`)
3. **Analysis**: Sends the document to Azure's prebuilt-read model for text extraction
4. **Language Detection**: Identifies which languages are present in the document
5. **Handwriting Detection**: Determines if text is handwritten or printed
6. **Text Extraction**: Extracts all text with:
   - **Line-level data**: Complete lines of text with bounding boxes
   - **Word-level data**: Individual words with confidence scores (accuracy ratings)
   - **Bounding boxes**: Coordinates showing exactly where text appears on the page
7. **Output**: Displays all extracted information in a structured format

**Key concepts explained in the code:**
- **Poller Pattern**: How Azure handles long-running operations asynchronously
- **Bounding Boxes**: Rectangular coordinates `[x1,y1, x2,y2, x3,y3, x4,y4]` showing text location
- **Confidence Scores**: Values from 0-1 indicating OCR accuracy (0.98 = 98% confident)
- **Spans**: Character offsets showing where each element appears in the full text

#### Step 4: Add a Sample Document

Place a sample image file (PNG, JPG, or PDF) in the `data/` folder and name it `read.png`. You can use:
- A scanned document
- A photo of a page
- Any image containing text

#### Step 5: Run the Script

```bash
# Make sure you're in the Labs/lab-1-read directory and virtual environment is active
python read.py
```

#### Expected Output:
- Document metadata (page dimensions, rotation angle)
- Detected languages with confidence scores
- Handwriting detection results
- Line-by-line text extraction with bounding boxes
- Word-level extraction with confidence scores
- Full extracted text content

---

### Exercise 2: Creating Searchable PDFs

**Objective**: Convert image files (PNG, JPG) into searchable PDF documents with embedded text layers, making scanned documents fully searchable and selectable.

#### What You'll Learn:
- How to generate searchable PDFs from images
- Using `AnalyzeOutputOption.PDF` to request PDF output
- Extracting and saving generated PDFs from the API response
- Understanding text layer embedding

#### Step 1: Create the Python Script

In the `read` directory, create a new file named `searchable_pdf.py`:

```bash
# Make sure you're in the Labs/lab-1-read directory
type nul > searchable_pdf.py
```

#### Step 2: Copy the Code

Open `searchable_pdf.py` and paste the following code:

```python
"""
Azure AI Document Intelligence - Create Searchable PDF
This sample converts image files (PNG, JPG, etc.) into searchable PDFs with embedded text.
"""

# Import necessary libraries
from azure.core.credentials import AzureKeyCredential  # For API authentication
from azure.ai.documentintelligence import DocumentIntelligenceClient  # Main Document Intelligence client
from azure.ai.documentintelligence.models import AnalyzeOutputOption  # For specifying PDF output format
import os
from dotenv import load_dotenv  # To load credentials from .env file

# Load credentials from .env file
load_dotenv()

# Get Azure endpoint and API key from environment variables
endpoint = os.getenv("AZ_DOCINT_ENDPOINT", "https://<your-resource>.cognitiveservices.azure.com/")
key = os.getenv("AZ_DOCINT_KEY", "<your-key>")

def create_searchable_pdf():
    """
    Converts a PNG/image file into a searchable PDF using Azure Document Intelligence.
    
    A searchable PDF embeds the extracted text so you can:
    - Search for text within the PDF
    - Copy and paste text from the PDF
    - Select text with your cursor
    
    The original image is preserved, with an invisible text layer overlaid on top.
    This makes scanned documents or images fully text-searchable.
    """
    # Path to the input image file
    file_path = "data/read.png"
    # Path where the searchable PDF will be saved
    output_pdf = "data/read_searchable.pdf"

    # Initialize Document Intelligence client with credentials
    document_intelligence_client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    
    print(f"Converting {file_path} to searchable PDF...")
    
    # Open and send the file to Azure for analysis with PDF output
    with open(file_path, "rb") as file:
        # Start analysis using prebuilt-read model with PDF output option
        # AnalyzeOutputOption.PDF tells Azure to generate a searchable PDF
        # This returns a poller object that tracks the operation
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-read",  # Use the Read model for text extraction
            body=file,  # The image file to convert
            output=[AnalyzeOutputOption.PDF]  # Request PDF output format
        )
    
    # Wait for analysis to complete and get the result
    result = poller.result()
    
    # Get the operation ID needed to retrieve the PDF
    operation_id = poller.details["operation_id"]
    
    print("Analysis complete. Downloading searchable PDF...")
    
    # Retrieve the generated searchable PDF from Azure
    # get_analyze_result_pdf() downloads the PDF with embedded text
    pdf_response = document_intelligence_client.get_analyze_result_pdf(
        model_id=result.model_id,  # The model that was used (prebuilt-read)
        result_id=operation_id  # The unique ID for this operation
    )
    
    # Save the PDF to a file
    with open(output_pdf, "wb") as pdf_file:
        # Write the PDF content to disk
        # pdf_response returns chunks of data, so we iterate and write each chunk
        for chunk in pdf_response:
            pdf_file.write(chunk)
    
    print(f"✅ Searchable PDF created successfully!")
    print(f"📄 Output file: {output_pdf}")
    print(f"You can now open this PDF and search/select/copy text!")


if __name__ == "__main__":
    # Run the searchable PDF creation function
    create_searchable_pdf()
```

#### Step 3: What This Code Does

This script converts an image file into a searchable PDF:

1. **Loads Configuration**: Reads Azure credentials from the `.env` file
2. **Initializes Client**: Connects to Azure Document Intelligence service
3. **Specifies Output Format**: Uses `output=[AnalyzeOutputOption.PDF]` to request PDF generation
4. **Analyzes Document**: Sends the image to Azure's Read model for text extraction
5. **Generates PDF**: Azure creates a PDF with:
   - The original image as the visual layer
   - Extracted text as an invisible, searchable layer positioned over the image
6. **Downloads PDF**: Retrieves the generated PDF using the operation ID
7. **Saves File**: Writes the PDF to `data/read_searchable.pdf`

**Real-world use cases:**
- Converting scanned paper documents to searchable digital files
- Making photos of receipts/forms text-searchable
- Creating accessible documents from image-only PDFs
- Digitizing historical documents or archives

#### Step 4: Run the Script

```bash
# Make sure you're in the Labs/lab-1-read directory
python searchable_pdf.py
```

#### Expected Output:
```
Converting data/read.png to searchable PDF...
Analysis complete. Downloading searchable PDF...
✅ Searchable PDF created successfully!
📄 Output file: data/read_searchable.pdf
You can now open this PDF and search/select/copy text!
```

#### Step 5: Verify the Results

1. Open `data/read_searchable.pdf` in a PDF viewer (Adobe Reader, Edge, Chrome)
2. Try selecting text with your cursor - you should be able to highlight and copy text
3. Press `Ctrl+F` and search for a word from the document - it should be found
4. Compare with the original `data/read.png` - the PNG is not searchable, but the PDF is!

---

### Exercise 3: Batch Processing with Raw API Responses

**Objective**: Process multiple documents in different formats (JPG, PNG, PDF) in batch mode and examine the complete raw API responses to understand all available data fields.

#### What You'll Learn:
- Batch processing multiple documents efficiently
- Handling different file formats (JPG, PNG, PDF)
- Examining raw API response structure
- Aggregating results across multiple documents
- Language detection across multi-lingual content
- Handwriting vs. printed text detection

#### Step 1: Prepare Sample Documents

You'll need three sample files for batch processing. Place these in the `data/` folder:

1. `batch1.png` - An image file (PNG format) - can be multi-language
2. `batch2.jpg` - An image file (JPG format) - can contain handwritten text
3. `batch3.pdf` - A PDF document

These files should contain different types of content (different languages, handwriting, printed text) to demonstrate the API's capabilities.

#### Step 2: Create the Python Script

In the `read` directory, create a new file named `read_batch_demo.py`:

```bash
# Make sure you're in the Labs/lab-1-read directory
type nul > read_batch_demo.py
```

#### Step 3: Copy the Code

Open `read_batch_demo.py` and paste the complete code. Due to length, here's the structure:

**The script includes:**
- Import statements and environment setup
- `analyze_document_with_read(file_path)` - Processes a single document
- `display_raw_results(doc_number, file_name, result)` - Shows complete API response
- `batch_process_documents()` - Main batch processing function

**Key sections in the code:**

```python
# Import necessary libraries
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
import os
from dotenv import load_dotenv

# Load credentials from parent Labs directory
load_dotenv(dotenv_path="../.env")

endpoint = os.getenv("AZ_DOCINT_ENDPOINT")
key = os.getenv("AZ_DOCINT_KEY")

def analyze_document_with_read(file_path):
    """Analyzes a single document and returns the raw API response"""
    client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    
    with open(file_path, "rb") as file:
        poller = client.begin_analyze_document("prebuilt-read", body=file)
    
    result = poller.result()
    return result

def display_raw_results(doc_number, file_name, result):
    """Displays the complete raw API response for educational purposes"""
    # Shows: Model Information, Language Detection, Handwriting Detection,
    # Page Analysis (all lines and words), Full Text Content
    # ... (detailed implementation in the full script)

def batch_process_documents():
    """Main function that processes multiple documents"""
    files_to_process = [
        "data/batch1.png",
        "data/batch2.jpg",
        "data/batch3.pdf"
    ]
    
    results = []
    for file_path in files_to_process:
        result = analyze_document_with_read(file_path)
        results.append((file_path, result))
        display_raw_results(len(results), os.path.basename(file_path), result)
    
    # Display final summary
    # ... (aggregated statistics)

if __name__ == "__main__":
    batch_process_documents()
```

> **Note**: The complete code is quite long (~290 lines) with detailed comments. You can copy it from the provided `read_batch_demo.py` file or build it following this structure with the display functions showing all API response sections.

#### Step 4: What This Code Does

This script demonstrates batch processing with complete API transparency:

1. **Batch Processing Loop**: Iterates through multiple files in the `data/` folder
2. **Multi-Format Support**: Handles PNG, JPG, and PDF files with the same code
3. **Raw API Response Display**: For each document, shows complete details:
   - **Model Information**: Which model and API version was used
   - **Language Detection**: All detected languages with confidence scores and text spans
   - **Handwriting Detection**: Identifies handwritten vs. printed text with samples
   - **Page-by-Page Analysis**:
     - Page dimensions and rotation angle
     - All text lines with bounding box coordinates
     - All words with individual confidence scores
   - **Full Text Content**: Complete extracted text
4. **Result Aggregation**: Collects results from all files
5. **Final Summary**: Shows:
   - Total files processed successfully
   - Handwriting detection summary across all documents
   - Total pages and characters processed

**Educational value:**
- Students see the complete raw API response, not just formatted output
- Helps understand what data is available from the API
- Demonstrates how to extract and use specific fields
- Shows the structure of bounding boxes, spans, confidence scores

#### Step 5: Run the Script

```bash
# Make sure you're in the Labs/lab-1-read directory
python read_batch_demo.py
```

#### Expected Output:

For **each document**, you'll see:

```
======================================================================================================
DOCUMENT 1 - RAW API RESPONSE: batch1.png
======================================================================================================

🔧 MODEL INFORMATION:
   Model ID: prebuilt-read
   API Version: 2024-02-29-preview

🌍 LANGUAGE DETECTION (Raw API Response):
   Total languages detected: 2
   
   Language #1:
      • Locale: en
      • Confidence: 0.98
      • Text spans: 1 span(s)
         - Span 1: offset=0, length=150
           Preview: 'This is sample English text...'

✍️ HANDWRITING/STYLE DETECTION (Raw API Response):
   Total styles detected: 1
   
   Style #1:
      • Is Handwritten: True
      • Confidence: 0.95
      • Text spans: 1 span(s)
         - Span 1: offset=50, length=30
           Handwritten text: 'Signature text here...'

📖 PAGE ANALYSIS (Raw API Response):
   Total pages: 1
   
   ──────────────────────────────────────────────────────────────────────────────────────
   PAGE 1:
   ──────────────────────────────────────────────────────────────────────────────────────
      • Page number: 1
      • Width: 2550 pixel
      • Height: 3300 pixel
      • Angle: 0°
      • Total lines: 25
      • Total words: 150

      📝 LINES (All 25 lines):
         [Shows all lines with content and bounding boxes]

      🔤 WORDS (All 150 words with confidence scores):
         [Shows all words with confidence and bounding boxes]

📋 FULL EXTRACTED TEXT CONTENT (Raw):
   [Complete text content]
```

**Final Summary:**
```
========================================
📊 BATCH PROCESSING SUMMARY
========================================
✅ Total files processed: 3
✍️ Handwriting Detection Summary:
   • batch1.png: Handwritten content detected
   • batch2.jpg: Handwritten content detected
   • batch3.pdf: No handwriting detected (printed only)
📈 Total Statistics:
   • Total pages processed: 5
   • Total characters extracted: 3,456
```

#### Step 6: Experiment and Learn

Try the following experiments:

1. **Add Your Own Files**: Place your own documents in `data/` and update the `files_to_process` list
2. **Different Languages**: Try documents in Arabic, French, Spanish, etc. to see language detection
3. **Mixed Content**: Use documents with both printed and handwritten text
4. **Compare Confidence**: Notice how confidence scores differ between clear printed text and handwriting

---

## 🔍 Understanding the Output

### Bounding Box Coordinates
```
[x1, y1, x2, y2, x3, y3, x4, y4]
```
- Represents 4 corner points of a rectangle surrounding text
- Coordinates are in pixels from the top-left corner
- Example: `[468, 593, 818, 593, 818, 610, 468, 609]`
  - Width: 818 - 468 = 350 pixels
  - Height: 610 - 593 = 17 pixels

### Confidence Scores
```
Confidence: 0.987
```
- Range: 0.0 to 1.0 (0% to 100%)
- Higher values indicate greater OCR accuracy
- Typical values: 0.95+ for clear printed text, 0.80-0.95 for handwriting

### Spans
```
offset=125, length=42
```
- **offset**: Starting position in the full document text (character index)
- **length**: Number of characters in this text element
- Used to locate text elements within the complete content

---

## 🧪 Troubleshooting

### Issue: ModuleNotFoundError
```
ModuleNotFoundError: No module named 'azure.ai.documentintelligence'
```
**Solution**: Ensure virtual environment is activated and dependencies are installed:
```bash
.venv\Scripts\activate
pip install -r requirements.txt
```

### Issue: Authentication Error
```
Error: Invalid credentials
```
**Solution**: Verify your `.env` file contains correct endpoint and key:
- Endpoint should end with `.cognitiveservices.azure.com/`
- Key should be a 32-character string (no quotes needed)

### Issue: File Not Found
```
FileNotFoundError: data/read.png not found
```
**Solution**: Ensure you're running the script from the `read` directory and the `data/` folder exists with sample files.

### Issue: Virtual Environment Not Activating (PowerShell)
```
cannot be loaded because running scripts is disabled
```
**Solution**: Run PowerShell as Administrator and execute:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📚 Additional Resources

- [Azure AI Document Intelligence Documentation](https://learn.microsoft.com/azure/ai-services/document-intelligence/)
- [Read Model Documentation](https://learn.microsoft.com/azure/ai-services/document-intelligence/concept-read)
- [Python SDK Reference](https://learn.microsoft.com/python/api/azure-ai-documentintelligence/)
- [Pricing Information](https://azure.microsoft.com/pricing/details/ai-document-intelligence/)

---

## 🎓 What You've Learned

By completing this lab, you've gained hands-on experience with:

✅ **Azure Document Intelligence Read API** fundamentals  
✅ **Text extraction** with bounding boxes and confidence scores  
✅ **Asynchronous operations** using the poller pattern  
✅ **Searchable PDF generation** from images  
✅ **Batch processing** multiple documents efficiently  
✅ **Multi-format support** (JPG, PNG, PDF)  
✅ **Multi-language detection** and handwriting recognition  
✅ **Raw API responses** and complete data structure analysis  

---

## 🚀 Next Steps

Continue your learning journey with:
- **Lab 2 - Layout API**: Understand document structure (tables, selection marks, page objects)
- **Lab 3 - General Document Model**: Extract key-value pairs from forms and structured documents
- **Lab 4 - Prebuilt Models**: Industry-specific document processing (invoices, receipts, bank statements, IDs, credit cards)

---

## 📝 Lab Files Summary

| File | Purpose | Key Features |
|------|---------|--------------|
| `read.py` | Basic text extraction demo | Bounding boxes, confidence scores, detailed comments |
| `searchable_pdf.py` | Image to searchable PDF conversion | PDF output generation, text layer embedding |
| `read_batch_demo.py` | Batch processing with raw responses | Multi-format, multi-language, handwriting detection |
| `data/` | Sample documents | PNG, JPG, PDF files for testing |
| `.env` | Configuration file | Azure credentials (in parent Labs folder) |
| `requirements.txt` | Python dependencies | Azure SDK, numpy, dotenv (in parent Labs folder) |

---

**Happy Learning! 🎉**
