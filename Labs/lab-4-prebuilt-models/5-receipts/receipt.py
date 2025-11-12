"""
Azure AI Document Intelligence - Receipt Model Demo
This script demonstrates the prebuilt-receipt model for extracting structured data from receipts.

The Receipt model extracts:
- Merchant information (name, address, phone)
- Transaction details (date, time)
- Items purchased (description, quantity, price, total)
- Payment summary (subtotal, tax, tip, total)
- Receipt metadata (receipt type, locale)

This model works with receipts in various formats and languages, and dynamically
detects fields based on what's present in the document (items, tables, taxes, tips, etc.).
"""

from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
import os
from dotenv import load_dotenv

# Load credentials from parent Labs directory
# The ../../ means go up two levels from '5-receipts' to 'Labs' folder
load_dotenv(dotenv_path="../../.env")

# Get Azure endpoint and API key from environment variables
endpoint = os.getenv("AZ_DOCINT_ENDPOINT")
key = os.getenv("AZ_DOCINT_KEY")


def analyze_receipt():
    """
    Main function to analyze a receipt using the prebuilt Receipt model.
    
    The prebuilt-receipt model is designed for:
    - Retail receipts from stores and restaurants
    - Hotel receipts and invoices
    - Receipts in various languages (English, Japanese, etc.)
    - Both itemized and summary receipts
    - Receipts with or without tables
    
    The model dynamically detects and extracts fields based on what's present in the receipt.
    """
    
    # Path to the receipt image
    # Available sample files in data/ folder - change the filename to analyze different receipts:
    # - "data/contoso-receipt.png" - Contoso retail receipt sample
    # - "data/receipt-app-like.png" - App-style receipt
    # - "data/receipt-hotel.png" - Hotel receipt
    # - "data/receipt-japanese.png" - Japanese language receipt
    # Just change the filename below to try different receipts!
    
    file_path = "data/contoso-receipt.png"  # Change this to any file from the list above
    
    # Initialize Document Intelligence client with your credentials
    document_intelligence_client = DocumentIntelligenceClient(
        endpoint=endpoint, 
        credential=AzureKeyCredential(key)
    )
    
    print(f"Analyzing receipt: {file_path}")
    print("=" * 100)
    
    # Open and read the receipt image in binary mode
    with open(file_path, "rb") as f:
        # Start the analysis using the prebuilt Receipt model
        # The poller pattern is used for long-running operations
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-receipt",  # The model ID for receipts
            body=f  # The document to analyze
        )
        
        # Wait for the analysis to complete and get the result
        receipts = poller.result()
    
    print(f"✓ Analysis complete! Model used: prebuilt-receipt")
    print("=" * 100)
    
    # =========================================================================
    # RECEIPT EXTRACTION
    # =========================================================================
    # The result may contain multiple receipts if the image has multiple receipts
    
    for idx, receipt in enumerate(receipts.documents):
        print(f"\n{'='*100}")
        print(f"🧾 RECEIPT #{idx + 1}")
        print("=" * 100)
        
        # =====================================================================
        # RECEIPT TYPE & METADATA
        # =====================================================================
        receipt_type = receipt.doc_type
        if receipt_type:
            print(f"\n📋 Receipt Type: {receipt_type}")
            print("-" * 100)
        
        # Locale (language/region of the receipt)
        locale = receipt.fields.get("Locale")
        if locale:
            print(f"  Locale: {locale.value_string}")
            print(f"  Confidence: {locale.confidence:.2%}")
        
        # =====================================================================
        # MERCHANT INFORMATION
        # =====================================================================
        print("\n🏪 MERCHANT INFORMATION")
        print("-" * 100)
        
        merchant_name = receipt.fields.get("MerchantName")
        if merchant_name:
            print(f"  Merchant Name: {merchant_name.value_string}")
            print(f"  Confidence: {merchant_name.confidence:.2%}")
        
        merchant_address = receipt.fields.get("MerchantAddress")
        if merchant_address:
            print(f"  Merchant Address: {merchant_address.value_address}")
            print(f"  Confidence: {merchant_address.confidence:.2%}")
        
        merchant_phone = receipt.fields.get("MerchantPhoneNumber")
        if merchant_phone:
            print(f"  Merchant Phone: {merchant_phone.value_phone_number}")
            print(f"  Confidence: {merchant_phone.confidence:.2%}")
        
        # =====================================================================
        # TRANSACTION DETAILS
        # =====================================================================
        print("\n📅 TRANSACTION DETAILS")
        print("-" * 100)
        
        transaction_date = receipt.fields.get("TransactionDate")
        if transaction_date:
            print(f"  Transaction Date: {transaction_date.value_date}")
            print(f"  Confidence: {transaction_date.confidence:.2%}")
        
        transaction_time = receipt.fields.get("TransactionTime")
        if transaction_time:
            print(f"  Transaction Time: {transaction_time.value_time}")
            print(f"  Confidence: {transaction_time.confidence:.2%}")
        
        # =====================================================================
        # ITEMS PURCHASED
        # =====================================================================
        # This section dynamically extracts items whether they're in a table or list format
        # The model intelligently detects item structure and extracts all available details
        
        items = receipt.fields.get("Items")
        if items:
            print("\n🛒 ITEMS PURCHASED")
            print("=" * 100)
            print(f"\nTotal Items: {len(items.value_array)}\n")
            
            for item_idx, item in enumerate(items.value_array):
                print(f"  🔹 ITEM #{item_idx + 1}")
                print("  " + "-" * 96)
                
                # Item Description
                item_description = item.value_object.get("Description")
                if item_description:
                    print(f"    Description: {item_description.value_string}")
                    print(f"    Confidence: {item_description.confidence:.2%}")
                
                # Item Quantity
                item_quantity = item.value_object.get("Quantity")
                if item_quantity:
                    print(f"    Quantity: {item_quantity.value_number}")
                    print(f"    Confidence: {item_quantity.confidence:.2%}")
                
                # Individual Item Price (unit price)
                item_price = item.value_object.get("Price")
                if item_price:
                    print(f"    Unit Price: ${item_price.value_currency.amount:,.2f}")
                    print(f"    Confidence: {item_price.confidence:.2%}")
                
                # Total Item Price (quantity × unit price)
                item_total_price = item.value_object.get("TotalPrice")
                if item_total_price:
                    print(f"    Total Price: ${item_total_price.value_currency.amount:,.2f}")
                    print(f"    Confidence: {item_total_price.confidence:.2%}")
                
                print()
        else:
            print("\n🛒 ITEMS PURCHASED")
            print("=" * 100)
            print("\n  ℹ️  No itemized list found in this receipt")
            print("  This receipt may only contain summary totals without item details.\n")
        
        # =====================================================================
        # PAYMENT SUMMARY
        # =====================================================================
        # This section dynamically shows only the payment fields that exist in the receipt
        # Not all receipts have subtotal, tax, tip, etc. - the model detects what's available
        
        print("=" * 100)
        print("💰 PAYMENT SUMMARY")
        print("-" * 100)
        
        subtotal = receipt.fields.get("Subtotal")
        if subtotal:
            print(f"  Subtotal: ${subtotal.value_currency.amount:,.2f}")
            print(f"  Confidence: {subtotal.confidence:.2%}")
        
        tax = receipt.fields.get("TotalTax")
        if tax:
            print(f"  Tax: ${tax.value_currency.amount:,.2f}")
            print(f"  Confidence: {tax.confidence:.2%}")
        
        tip = receipt.fields.get("Tip")
        if tip:
            print(f"  Tip: ${tip.value_currency.amount:,.2f}")
            print(f"  Confidence: {tip.confidence:.2%}")
        
        total = receipt.fields.get("Total")
        if total:
            print(f"  Total: ${total.value_currency.amount:,.2f}")
            print(f"  Confidence: {total.confidence:.2%}")
        
        # =====================================================================
        # ADDITIONAL FIELDS (if present)
        # =====================================================================
        # Some receipts may have additional fields like receipt ID, payment method, etc.
        
        print("\n📋 ADDITIONAL INFORMATION")
        print("-" * 100)
        
        receipt_id = receipt.fields.get("ReceiptId")
        if receipt_id:
            print(f"  Receipt ID: {receipt_id.value_string}")
            print(f"  Confidence: {receipt_id.confidence:.2%}")
        
        payment_method = receipt.fields.get("PaymentMethod")
        if payment_method:
            print(f"  Payment Method: {payment_method.value_string}")
            print(f"  Confidence: {payment_method.confidence:.2%}")
        
        print("\n" + "=" * 100)
    
    print("\n✓ Receipt analysis complete!")
    print("💡 TIP: The model dynamically detects fields - tables, items, tips, taxes are shown only if present!")
    print("=" * 100)


if __name__ == "__main__":
    # Run the receipt analysis
    analyze_receipt()
