"""
Azure AI Document Intelligence - Batch Read Processing Demo
This script processes multiple documents in different formats (JPG, PNG, PDF)
and demonstrates:
- Multi-format support (JPEG, PNG, PDF)
- Multi-language text extraction
- Handwriting detection
- Batch automation with raw API response display
"""

# Import necessary libraries
from azure.core.credentials import AzureKeyCredential  # For API authentication
from azure.ai.documentintelligence import DocumentIntelligenceClient  # Main Document Intelligence client
import os
from dotenv import load_dotenv  # To load credentials from .env file

# Load credentials from .env file in the parent Labs directory
# The ../ means go up one level from 'read' folder to 'Labs' folder
load_dotenv(dotenv_path="../.env")

# Get Azure endpoint and API key from environment variables
endpoint = os.getenv("AZ_DOCINT_ENDPOINT")
key = os.getenv("AZ_DOCINT_KEY")


def analyze_document_with_read(file_path):
    """
    Analyzes a single document using the Read model.
    Returns the raw API response for detailed inspection.
    
    Parameters:
    -----------
    file_path : str
        Path to the document file (PNG, JPG, PDF, etc.)
    
    Returns:
    --------
    result : AnalyzeResult
        The complete analysis result from Azure Document Intelligence API
    """
    # Initialize Document Intelligence client with credentials
    client = DocumentIntelligenceClient(
        endpoint=endpoint, 
        credential=AzureKeyCredential(key)
    )
    
    print(f"\n📤 Uploading file to Azure: {os.path.basename(file_path)}")
    
    # Open the file in binary read mode
    with open(file_path, "rb") as file:
        # Start analysis with Read model
        # This sends the file to Azure and returns a poller to track progress
        poller = client.begin_analyze_document("prebuilt-read", body=file)
    
    print(f"⏳ Processing... (Azure is analyzing the document)")
    
    # Wait for analysis to complete and get the full result
    result = poller.result()
    
    print(f"✅ Analysis complete!\n")
    
    return result


def display_raw_results(doc_number, file_name, result):
    """
    Displays the RAW API response with all details.
    Shows exactly what Azure Document Intelligence returns.
    
    Parameters:
    -----------
    doc_number : int
        Document number in the batch (1, 2, 3, etc.)
    file_name : str
        Name of the file being analyzed
    result : AnalyzeResult
        The complete analysis result from the API
    """
    print("\n" + "=" * 100)
    print(f"DOCUMENT {doc_number} - RAW API RESPONSE".center(100))
    print("=" * 100)
    print(f"File: {file_name}")
    print("=" * 100)
    
    # =========================================================================
    # SECTION 1: MODEL INFORMATION
    # =========================================================================
    # Below code displays the Azure model ID and API version used for analysis
    print("\n🔧 MODEL INFORMATION:")
    print(f"   Model ID: {result.model_id}")
    print(f"   API Version: {result.api_version if hasattr(result, 'api_version') else 'N/A'}")
    
    # =========================================================================
    # SECTION 2: LANGUAGE DETECTION (Raw Response)
    # =========================================================================
    # Below code displays all languages detected in the document with confidence scores
    print("\n🌍 LANGUAGE DETECTION (Raw API Response):")
    if result.languages:
        print(f"   Total languages detected: {len(result.languages)}")
        for idx, lang in enumerate(result.languages, 1):
            print(f"\n   Language #{idx}:")
            print(f"      • Locale: {lang.locale}")
            print(f"      • Confidence: {lang.confidence}")
            # Show which parts of the document contain this language
            if hasattr(lang, 'spans') and lang.spans:
                print(f"      • Text spans: {len(lang.spans)} span(s)")
                for span_idx, span in enumerate(lang.spans, 1):
                    print(f"         - Span {span_idx}: offset={span.offset}, length={span.length}")
                    # Show the actual text for this language span
                    text_sample = result.content[span.offset:span.offset + min(span.length, 50)]
                    print(f"           Preview: '{text_sample}{'...' if span.length > 50 else ''}'")
    else:
        print("   ⚠️ No languages detected")
    
    # =========================================================================
    # SECTION 3: HANDWRITING DETECTION (Raw Response)
    # =========================================================================
    # Below code identifies handwritten vs printed text with confidence scores
    print("\n✍️ HANDWRITING/STYLE DETECTION (Raw API Response):")
    if result.styles:
        print(f"   Total styles detected: {len(result.styles)}")
        for idx, style in enumerate(result.styles, 1):
            print(f"\n   Style #{idx}:")
            print(f"      • Is Handwritten: {style.is_handwritten}")
            print(f"      • Confidence: {style.confidence}")
            # Show which parts are handwritten
            if style.spans:
                print(f"      • Text spans: {len(style.spans)} span(s)")
                for span_idx, span in enumerate(style.spans, 1):
                    print(f"         - Span {span_idx}: offset={span.offset}, length={span.length}")
                    if style.is_handwritten:
                        # Show the handwritten text
                        handwritten_text = result.content[span.offset:span.offset + min(span.length, 50)]
                        print(f"           Handwritten text: '{handwritten_text}{'...' if span.length > 50 else ''}'")
    else:
        print("   ⚠️ No style information detected (all text is printed)")
    
    # =========================================================================
    # SECTION 4: PAGE-BY-PAGE ANALYSIS (Raw Response)
    # =========================================================================
    # Below code shows page-by-page breakdown with dimensions, lines, and words
    print(f"\n📖 PAGE ANALYSIS (Raw API Response):")
    print(f"   Total pages: {len(result.pages)}")
    
    for page_idx, page in enumerate(result.pages, 1):
        print(f"\n   {'─' * 90}")
        print(f"   PAGE {page_idx}:")
        print(f"   {'─' * 90}")
        print(f"      • Page number: {page.page_number}")
        print(f"      • Width: {page.width} {page.unit}")
        print(f"      • Height: {page.height} {page.unit}")
        print(f"      • Angle: {page.angle}°")
        print(f"      • Total lines: {len(page.lines)}")
        print(f"      • Total words: {len(page.words)}")
        
        # Below code displays all text lines with their bounding box coordinates
        # Show all lines with their bounding boxes
        print(f"\n      📝 LINES (All {len(page.lines)} lines):")
        for line_idx, line in enumerate(page.lines, 1):
            print(f"\n         Line #{line_idx}:")
            print(f"            Content: '{line.content}'")
            print(f"            Bounding box (polygon): {line.polygon}")
            print(f"            Span: offset={line.spans[0].offset if line.spans else 'N/A'}, "
                  f"length={line.spans[0].length if line.spans else 'N/A'}")
        
        # Below code displays all words with confidence scores and bounding boxes
        # Show word-level details with confidence scores
        print(f"\n      🔤 WORDS (All {len(page.words)} words with confidence scores):")
        for word_idx, word in enumerate(page.words, 1):
            print(f"         Word #{word_idx}: '{word.content}' | "
                  f"Confidence: {word.confidence:.4f} | "
                  f"Bounding box: {word.polygon}")
    
    # =========================================================================
    # SECTION 5: FULL TEXT CONTENT (Raw)
    # =========================================================================
    # Below code displays the complete extracted text in raw format
    print(f"\n📋 FULL EXTRACTED TEXT CONTENT (Raw):")
    print(f"   Total characters: {len(result.content)}")
    print(f"\n   {'─' * 90}")
    print(f"   {result.content}")
    print(f"   {'─' * 90}")
    
    print("\n" + "=" * 100 + "\n")


def batch_process_documents():
    """
    Main function that processes multiple documents in batch mode.
    Collects results from all files and provides a summary.
    """
    # List of files to process - using the correct filenames
    files_to_process = [
        "data/batch1.png",   # JPEG format - should contain different language
        "data/batch2.jpg",   # PNG format - should contain different language
        "data/batch3.pdf"     # PDF format
    ]
    
    print("\n" + "🚀 AZURE DOCUMENT INTELLIGENCE - BATCH READ PROCESSING".center(100, "="))
    print(f"\nProcessing {len(files_to_process)} documents:")
    for f in files_to_process:
        print(f"   • {os.path.basename(f)}")
    print("\n" + "=" * 100)
    
    # Store results for final summary
    all_results = []
    successful = 0
    failed = 0
    
    # Process each file and display raw results
    for idx, file_path in enumerate(files_to_process, 1):
        
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"\n⚠️ ERROR: File not found - {file_path}")
            print(f"Please ensure the file exists in the data folder.")
            failed += 1
            continue
        
        try:
            # Analyze the document and get raw API response
            result = analyze_document_with_read(file_path)
            
            # Display the complete raw results with document number
            display_raw_results(idx, os.path.basename(file_path), result)
            
            # Store result for summary
            all_results.append({
                'file': os.path.basename(file_path),
                'result': result
            })
            successful += 1
            
        except Exception as e:
            print(f"\n❌ ERROR processing {file_path}:")
            print(f"   {str(e)}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    # =========================================================================
    # FINAL SUMMARY ACROSS ALL DOCUMENTS
    # =========================================================================
    print("\n\n" + "=" * 100)
    print("📊 BATCH PROCESSING SUMMARY - ALL DOCUMENTS".center(100))
    print("=" * 100)
    
    print(f"\n✅ Processing Statistics:")
    print(f"   • Total files processed: {len(files_to_process)}")
    print(f"   • Successfully analyzed: {successful}")
    print(f"   • Failed: {failed}")
    
    # Aggregate statistics across all documents
    if all_results:
        # Handwriting detection summary
        print(f"\n✍️ Handwriting Detection Summary:")
        handwriting_docs = []
        for item in all_results:
            has_handwriting = False
            if item['result'].styles:
                for style in item['result'].styles:
                    if style.is_handwritten:
                        has_handwriting = True
                        break
            if has_handwriting:
                handwriting_docs.append(item['file'])
        
        if handwriting_docs:
            print(f"   • Documents with handwritten content: {', '.join(handwriting_docs)}")
        else:
            print(f"   • No handwritten content detected in any document")
        
        # Total text extracted
        print(f"\n📄 Text Extraction Summary:")
        total_chars = sum(len(item['result'].content) for item in all_results)
        total_pages = sum(len(item['result'].pages) for item in all_results)
        print(f"   • Total pages processed: {total_pages}")
        print(f"   • Total characters extracted: {total_chars:,}")
    
    print("\n" + "=" * 100)
    print("✅ BATCH PROCESSING COMPLETE!".center(100))
    print("=" * 100 + "\n")


if __name__ == "__main__":
    # Run the batch processing demo
    batch_process_documents()
