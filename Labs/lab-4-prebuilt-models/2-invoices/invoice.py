"""
Azure AI Document Intelligence - Invoice Model Demo
This script demonstrates the prebuilt-invoice model for extracting structured data from invoices.

The Invoice model extracts:
- Vendor information (name, address)
- Customer information (name, ID, address)
- Invoice details (ID, date, total, due date)
- Line items (description, quantity, unit price, amount)
- Payment details (subtotal, tax, amount due)
- Service information (dates, addresses)

This model works with invoices in various languages and formats.
"""

from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
import os
from dotenv import load_dotenv

# Load credentials from parent Labs directory
# The ../../ means go up two levels from '2-invoices' to 'Labs' folder
load_dotenv(dotenv_path="../../.env")

# Get Azure endpoint and API key from environment variables
endpoint = os.getenv("AZ_DOCINT_ENDPOINT")
key = os.getenv("AZ_DOCINT_KEY")


def analyze_invoice():
    """
    Main function to analyze an invoice using the prebuilt Invoice model.
    
    The prebuilt-invoice model is designed for:
    - Invoices in various formats and languages
    - Extracting vendor and customer information
    - Identifying invoice details and line items
    - Calculating totals, taxes, and amounts due
    """
    
    # Path to the invoice document
    # Available sample files in data/ folder - change the filename to analyze different invoices:
    # - "data/invoice-english.png" - English invoice sample
    # - "data/invoice-german.png" - German invoice sample
    # - "data/sample-invoice.pdf" - Sample invoice PDF
    # - "data/Invoice-6.pdf" - Invoice #6 PDF
    # Just change the filename below to try different invoices!
    
    file_path = "data/invoice-english.png"  # Change this to any file from the list above
    
    # Initialize Document Intelligence client with your credentials
    document_intelligence_client = DocumentIntelligenceClient(
        endpoint=endpoint, 
        credential=AzureKeyCredential(key)
    )
    
    print(f"Analyzing invoice: {file_path}")
    print("=" * 100)
    
    # Open and read the invoice file in binary mode
    with open(file_path, "rb") as f:
        # Start the analysis using the prebuilt Invoice model
        # The poller pattern is used for long-running operations
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-invoice",  # The model ID for invoices
            body=f  # The document to analyze
        )
        
        # Wait for the analysis to complete and get the result
        invoices = poller.result()
    
    print(f"✓ Analysis complete! Model used: prebuilt-invoice")
    print("=" * 100)
    
    # =========================================================================
    # INVOICE EXTRACTION
    # =========================================================================
    # The result may contain multiple invoices if the document has multiple pages
    
    for idx, invoice in enumerate(invoices.documents):
        print(f"\n{'='*100}")
        print(f"🧾 INVOICE #{idx + 1}")
        print("=" * 100)
        
        # =====================================================================
        # VENDOR INFORMATION
        # =====================================================================
        print("\n🏢 VENDOR INFORMATION")
        print("-" * 100)
        
        vendor_name = invoice.fields.get("VendorName")
        if vendor_name:
            print(f"  Vendor Name: {vendor_name.value_string}")
            print(f"  Confidence: {vendor_name.confidence:.2%}")
        
        vendor_address = invoice.fields.get("VendorAddress")
        if vendor_address:
            print(f"  Vendor Address: {vendor_address.value_address}")
            print(f"  Confidence: {vendor_address.confidence:.2%}")
        
        vendor_address_recipient = invoice.fields.get("VendorAddressRecipient")
        if vendor_address_recipient:
            print(f"  Vendor Address Recipient: {vendor_address_recipient.value_string}")
            print(f"  Confidence: {vendor_address_recipient.confidence:.2%}")
        
        # =====================================================================
        # CUSTOMER INFORMATION
        # =====================================================================
        print("\n👤 CUSTOMER INFORMATION")
        print("-" * 100)
        
        customer_name = invoice.fields.get("CustomerName")
        if customer_name:
            print(f"  Customer Name: {customer_name.value_string}")
            print(f"  Confidence: {customer_name.confidence:.2%}")
        
        customer_id = invoice.fields.get("CustomerId")
        if customer_id:
            print(f"  Customer ID: {customer_id.value_string}")
            print(f"  Confidence: {customer_id.confidence:.2%}")
        
        customer_address = invoice.fields.get("CustomerAddress")
        if customer_address:
            print(f"  Customer Address: {customer_address.value_address}")
            print(f"  Confidence: {customer_address.confidence:.2%}")
        
        customer_address_recipient = invoice.fields.get("CustomerAddressRecipient")
        if customer_address_recipient:
            print(f"  Customer Address Recipient: {customer_address_recipient.value_string}")
            print(f"  Confidence: {customer_address_recipient.confidence:.2%}")
        
        # =====================================================================
        # INVOICE DETAILS
        # =====================================================================
        print("\n📋 INVOICE DETAILS")
        print("-" * 100)
        
        invoice_id = invoice.fields.get("InvoiceId")
        if invoice_id:
            print(f"  Invoice ID: {invoice_id.value_string}")
            print(f"  Confidence: {invoice_id.confidence:.2%}")
        
        invoice_date = invoice.fields.get("InvoiceDate")
        if invoice_date:
            print(f"  Invoice Date: {invoice_date.value_date}")
            print(f"  Confidence: {invoice_date.confidence:.2%}")
        
        due_date = invoice.fields.get("DueDate")
        if due_date:
            print(f"  Due Date: {due_date.value_date}")
            print(f"  Confidence: {due_date.confidence:.2%}")
        
        purchase_order = invoice.fields.get("PurchaseOrder")
        if purchase_order:
            print(f"  Purchase Order: {purchase_order.value_string}")
            print(f"  Confidence: {purchase_order.confidence:.2%}")
        
        invoice_total = invoice.fields.get("InvoiceTotal")
        if invoice_total:
            print(f"  Invoice Total: ${invoice_total.value_currency.amount:,.2f}")
            print(f"  Confidence: {invoice_total.confidence:.2%}")
        
        # =====================================================================
        # BILLING & SHIPPING ADDRESSES
        # =====================================================================
        print("\n📍 BILLING & SHIPPING INFORMATION")
        print("-" * 100)
        
        billing_address = invoice.fields.get("BillingAddress")
        if billing_address:
            print(f"  Billing Address: {billing_address.value_address}")
            print(f"  Confidence: {billing_address.confidence:.2%}")
        
        billing_address_recipient = invoice.fields.get("BillingAddressRecipient")
        if billing_address_recipient:
            print(f"  Billing Address Recipient: {billing_address_recipient.value_string}")
            print(f"  Confidence: {billing_address_recipient.confidence:.2%}")
        
        shipping_address = invoice.fields.get("ShippingAddress")
        if shipping_address:
            print(f"  Shipping Address: {shipping_address.value_address}")
            print(f"  Confidence: {shipping_address.confidence:.2%}")
        
        shipping_address_recipient = invoice.fields.get("ShippingAddressRecipient")
        if shipping_address_recipient:
            print(f"  Shipping Address Recipient: {shipping_address_recipient.value_string}")
            print(f"  Confidence: {shipping_address_recipient.confidence:.2%}")
        
        # =====================================================================
        # LINE ITEMS
        # =====================================================================
        # Each invoice contains line items with product/service details
        print("\n📦 INVOICE LINE ITEMS")
        print("=" * 100)
        
        items = invoice.fields.get("Items")
        if items:
            print(f"\nTotal Items: {len(items.value_array)}\n")
            
            for item_idx, item in enumerate(items.value_array):
                print(f"  🔹 ITEM #{item_idx + 1}")
                print("  " + "-" * 96)
                
                item_description = item.value_object.get("Description")
                if item_description:
                    print(f"    Description: {item_description.value_string}")
                    print(f"    Confidence: {item_description.confidence:.2%}")
                
                item_quantity = item.value_object.get("Quantity")
                if item_quantity:
                    print(f"    Quantity: {item_quantity.value_number}")
                    print(f"    Confidence: {item_quantity.confidence:.2%}")
                
                unit = item.value_object.get("Unit")
                if unit:
                    print(f"    Unit: {unit.value_string}")
                    print(f"    Confidence: {unit.confidence:.2%}")
                
                unit_price = item.value_object.get("UnitPrice")
                if unit_price:
                    print(f"    Unit Price: ${unit_price.value_currency.amount:,.2f}")
                    print(f"    Confidence: {unit_price.confidence:.2%}")
                
                product_code = item.value_object.get("ProductCode")
                if product_code:
                    print(f"    Product Code: {product_code.value_string}")
                    print(f"    Confidence: {product_code.confidence:.2%}")
                
                item_date = item.value_object.get("Date")
                if item_date:
                    print(f"    Date: {item_date.value_date}")
                    print(f"    Confidence: {item_date.confidence:.2%}")
                
                tax = item.value_object.get("Tax")
                if tax:
                    print(f"    Tax: ${tax.value_currency.amount:,.2f}")
                    print(f"    Confidence: {tax.confidence:.2%}")
                
                amount = item.value_object.get("Amount")
                if amount:
                    print(f"    Amount: ${amount.value_currency.amount:,.2f}")
                    print(f"    Confidence: {amount.confidence:.2%}")
                
                print()
        
        # =====================================================================
        # PAYMENT SUMMARY
        # =====================================================================
        print("=" * 100)
        print("💰 PAYMENT SUMMARY")
        print("-" * 100)
        
        subtotal = invoice.fields.get("SubTotal")
        if subtotal:
            print(f"  Subtotal: ${subtotal.value_currency.amount:,.2f}")
            print(f"  Confidence: {subtotal.confidence:.2%}")
        
        total_tax = invoice.fields.get("TotalTax")
        if total_tax:
            print(f"  Total Tax: ${total_tax.value_currency.amount:,.2f}")
            print(f"  Confidence: {total_tax.confidence:.2%}")
        
        previous_unpaid_balance = invoice.fields.get("PreviousUnpaidBalance")
        if previous_unpaid_balance:
            print(f"  Previous Unpaid Balance: ${previous_unpaid_balance.value_currency.amount:,.2f}")
            print(f"  Confidence: {previous_unpaid_balance.confidence:.2%}")
        
        amount_due = invoice.fields.get("AmountDue")
        if amount_due:
            print(f"  Amount Due: ${amount_due.value_currency.amount:,.2f}")
            print(f"  Confidence: {amount_due.confidence:.2%}")
        
        # =====================================================================
        # SERVICE INFORMATION
        # =====================================================================
        print("\n🔧 SERVICE INFORMATION")
        print("-" * 100)
        
        service_start_date = invoice.fields.get("ServiceStartDate")
        if service_start_date:
            print(f"  Service Start Date: {service_start_date.value_date}")
            print(f"  Confidence: {service_start_date.confidence:.2%}")
        
        service_end_date = invoice.fields.get("ServiceEndDate")
        if service_end_date:
            print(f"  Service End Date: {service_end_date.value_date}")
            print(f"  Confidence: {service_end_date.confidence:.2%}")
        
        service_address = invoice.fields.get("ServiceAddress")
        if service_address:
            print(f"  Service Address: {service_address.value_address}")
            print(f"  Confidence: {service_address.confidence:.2%}")
        
        service_address_recipient = invoice.fields.get("ServiceAddressRecipient")
        if service_address_recipient:
            print(f"  Service Address Recipient: {service_address_recipient.value_string}")
            print(f"  Confidence: {service_address_recipient.confidence:.2%}")
        
        remittance_address = invoice.fields.get("RemittanceAddress")
        if remittance_address:
            print(f"  Remittance Address: {remittance_address.value_address}")
            print(f"  Confidence: {remittance_address.confidence:.2%}")
        
        remittance_address_recipient = invoice.fields.get("RemittanceAddressRecipient")
        if remittance_address_recipient:
            print(f"  Remittance Address Recipient: {remittance_address_recipient.value_string}")
            print(f"  Confidence: {remittance_address_recipient.confidence:.2%}")
        
        print("\n" + "=" * 100)
    
    print("\n✓ Invoice analysis complete!")
    print("=" * 100)


if __name__ == "__main__":
    # Run the invoice analysis
    analyze_invoice()
