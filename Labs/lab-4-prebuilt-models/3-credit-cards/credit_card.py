"""
Azure AI Document Intelligence - Credit Card Model Demo
This script demonstrates the prebuilt-creditCard model for extracting structured data from credit cards.

The Credit Card model extracts:
- Card holder name
- Card number
- Card verification value (CVV)
- Expiration date
- Issuing bank
- Payment network (Visa, Mastercard, etc.)
- Customer service phone numbers

This model works with credit cards in various formats and orientations.
"""

from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
import os
from dotenv import load_dotenv

# Load credentials from parent Labs directory
# The ../../ means go up two levels from '3-credit-cards' to 'Labs' folder
load_dotenv(dotenv_path="../../.env")

# Get Azure endpoint and API key from environment variables
endpoint = os.getenv("AZ_DOCINT_ENDPOINT")
key = os.getenv("AZ_DOCINT_KEY")


def analyze_credit_card():
    """
    Main function to analyze a credit card using the prebuilt Credit Card model.
    
    The prebuilt-creditCard model is designed for:
    - Credit cards in various formats (horizontal, vertical)
    - Extracting card holder information
    - Identifying card details and security information
    - Recognizing payment networks and issuing banks
    
    ⚠️ SECURITY NOTE: This demo is for educational purposes only.
    Never store or transmit sensitive credit card information without proper encryption and compliance.
    """
    
    # Path to the credit card image
    # Available sample files in data/ folder - change the filename to analyze different cards:
    # - "data/credit-cards-horizontal.png" - Horizontal credit card layout
    # - "data/credit-cards-vertical.png" - Vertical credit card layout
    # Just change the filename below to try different credit cards!
    
    file_path = "data/credit-cards-horizontal.png"  # Change this to any file from the list above
    
    # Initialize Document Intelligence client with your credentials
    document_intelligence_client = DocumentIntelligenceClient(
        endpoint=endpoint, 
        credential=AzureKeyCredential(key)
    )
    
    print(f"Analyzing credit card: {file_path}")
    print("=" * 100)
    print("⚠️  SECURITY NOTICE: Handle credit card data with proper security measures")
    print("=" * 100)
    
    # Open and read the credit card image in binary mode
    with open(file_path, "rb") as f:
        # Start the analysis using the prebuilt Credit Card model
        # The poller pattern is used for long-running operations
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-creditCard",  # The model ID for credit cards
            body=f  # The document to analyze
        )
        
        # Wait for the analysis to complete and get the result
        credit_cards = poller.result()
    
    print(f"\n✓ Analysis complete! Model used: prebuilt-creditCard")
    print("=" * 100)
    
    # =========================================================================
    # CREDIT CARD EXTRACTION
    # =========================================================================
    # The result may contain multiple credit cards if the image has multiple cards
    
    for idx, document in enumerate(credit_cards.documents):
        print(f"\n{'='*100}")
        print(f"💳 CREDIT CARD #{idx + 1}")
        print("=" * 100)
        
        # =====================================================================
        # DOCUMENT TYPE
        # =====================================================================
        doc_type = document.doc_type
        if doc_type:
            print(f"\n📋 Document Type: {doc_type}")
            print("-" * 100)
        
        # =====================================================================
        # CARD HOLDER INFORMATION
        # =====================================================================
        print("\n👤 CARD HOLDER INFORMATION")
        print("-" * 100)
        
        card_holder_name = document.fields.get("CardHolderName")
        if card_holder_name:
            print(f"  Card Holder Name: {card_holder_name.value_string}")
            print(f"  Confidence: {card_holder_name.confidence:.2%}")
        
        # =====================================================================
        # CARD DETAILS
        # =====================================================================
        print("\n💳 CARD DETAILS")
        print("-" * 100)
        
        card_number = document.fields.get("CardNumber")
        if card_number:
            # Mask the card number for security (show only last 4 digits)
            masked_number = "XXXX-XXXX-XXXX-" + card_number.value_string[-4:] if len(card_number.value_string) >= 4 else card_number.value_string
            print(f"  Card Number: {masked_number}")
            print(f"  Full Number (for demo): {card_number.value_string}")
            print(f"  Confidence: {card_number.confidence:.2%}")
        
        expiration_date = document.fields.get("ExpirationDate")
        if expiration_date:
            print(f"  Expiration Date: {expiration_date.value_string}")
            print(f"  Confidence: {expiration_date.confidence:.2%}")
        
        card_verification_value = document.fields.get("CardVerificationValue")
        if card_verification_value:
            print(f"  CVV: {card_verification_value.value_string}")
            print(f"  Confidence: {card_verification_value.confidence:.2%}")
        
        # =====================================================================
        # ISSUER INFORMATION
        # =====================================================================
        print("\n🏦 ISSUER INFORMATION")
        print("-" * 100)
        
        issuing_bank = document.fields.get("IssuingBank")
        if issuing_bank:
            print(f"  Issuing Bank: {issuing_bank.value_string}")
            print(f"  Confidence: {issuing_bank.confidence:.2%}")
        
        payment_network = document.fields.get("PaymentNetwork")
        if payment_network:
            print(f"  Payment Network: {payment_network.value_string}")
            print(f"  Confidence: {payment_network.confidence:.2%}")
        
        # =====================================================================
        # CUSTOMER SERVICE
        # =====================================================================
        customer_service_phone_numbers = document.fields.get("CustomerServicePhoneNumbers")
        if customer_service_phone_numbers:
            print("\n📞 CUSTOMER SERVICE PHONE NUMBERS")
            print("-" * 100)
            
            for phone_idx, phone in enumerate(customer_service_phone_numbers.value_array):
                print(f"  Phone #{phone_idx + 1}: {phone.value_phone_number}")
                print(f"  Confidence: {phone.confidence:.2%}")
        
        print("\n" + "=" * 100)
    
    print("\n✓ Credit card analysis complete!")
    print("⚠️  Remember: Always handle credit card data securely and comply with PCI DSS standards")
    print("=" * 100)


if __name__ == "__main__":
    # Run the credit card analysis
    analyze_credit_card()
