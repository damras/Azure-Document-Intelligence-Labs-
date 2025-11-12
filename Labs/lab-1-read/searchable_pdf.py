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
