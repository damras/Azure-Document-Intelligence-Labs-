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
