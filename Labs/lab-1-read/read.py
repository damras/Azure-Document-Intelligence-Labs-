
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
    - Width: 350 pixels (818-468)
    - Height: 17 pixels (610-593)
    """
    if not bounding_box:
        return "N/A"
    # Reshape flat array into coordinate pairs
    reshaped_bounding_box = np.array(bounding_box).reshape(-1, 2)
    return ", ".join(["[{}, {}]".format(x, y) for x, y in reshaped_bounding_box])

def analyze_read_local():
    """
    Analyzes a local document file using Azure Document Intelligence Read model.
    Extracts text content, lines, words with confidence scores, and detects handwriting.
    """
    # Path to the document file
    file_path = "data/read.png"

    # Initialize Document Intelligence client with credentials
    document_intelligence_client = DocumentIntelligenceClient(
        endpoint=endpoint, credential=AzureKeyCredential(key)
    )
    
    # Open and send the file to Azure for analysis
    with open(file_path, "rb") as file:
        # Start analysis using prebuilt-read model
        # This returns a "poller" object for tracking the long-running operation
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-read", body=file
        )
    
    # What is a Poller?
    # A poller is an object that tracks a long-running operation in Azure.
    # Document analysis can take several seconds, so Azure processes it asynchronously.
    # The poller allows us to:
    # 1. Check if the operation is complete
    # 2. Wait for completion
    # 3. Retrieve the final result when ready
    
    # Wait for analysis to complete and get results
    # poller.result() blocks until Azure finishes processing and returns the analysis result
    result = poller.result()

    # Display the full extracted text content
    print("Document contains content: ", result.content)

    # Check if document contains handwritten content
    for idx, style in enumerate(result.styles):
        print(
            "Document contains {} content".format(
                "handwritten" if style.is_handwritten else "no handwritten"
            )
        )

    # Process each page in the document
    for page in result.pages:
        print("----Analyzing Read from page #{}----".format(page.page_number))
        # Display page dimensions
        print(
            "Page has width: {} and height: {}, measured with unit: {}".format(
                page.width, page.height, page.unit
            )
        )

        # Extract and display each line of text with its bounding box
        for line_idx, line in enumerate(page.lines):
            print(
                "...Line # {} has text content '{}' within bounding box '{}'".format(
                    line_idx,
                    line.content,
                    format_bounding_box(line.polygon),
                )
            )

        # Extract and display each word with its confidence score
        for word in page.words:
            print(
                "...Word '{}' has a confidence of {}".format(
                    word.content, word.confidence
                )
            )

    print("----------------------------------------")


if __name__ == "__main__":
    # Run the analysis function
    analyze_read_local()
