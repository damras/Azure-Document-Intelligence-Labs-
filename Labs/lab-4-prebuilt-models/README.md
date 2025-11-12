# Lab 4: Prebuilt Models - Industry-Specific Document Processing

## Overview
This lab demonstrates Azure AI Document Intelligence's **Prebuilt Models** for industry-specific document types. Unlike the general-purpose models in Labs 1-3 (Read, Layout, General Document), prebuilt models are **specialized and trained** for specific document types commonly used in finance, healthcare, legal, and business operations.

### What You'll Learn
- Use specialized prebuilt models for common business documents
- Extract industry-specific fields automatically without custom training
- Understand when to use prebuilt models vs. general models
- Process financial documents (bank statements, invoices, receipts, credit cards)
- Extract structured data from identity documents
- Compare extraction capabilities across different models

---

## Lab Objectives

By the end of this lab, you will be able to:
1. ✅ Analyze bank statements and extract account details, balances, and transactions
2. ✅ Process invoices to extract vendor information, line items, and payment details
3. ✅ Read credit card information including card numbers, expiration dates, and CVV
4. ✅ Extract personal information from identity documents (licenses, passports, IDs)
5. ✅ Analyze receipts to capture merchant details, items purchased, and totals
6. ✅ Understand the security and compliance considerations for sensitive documents

---

## Prerequisites
Before starting this lab, you should have completed:
- **Lab 1 (Read API)**: Basic environment setup, .env configuration, and text extraction
- **Lab 2 (Layout API)**: Understanding of document structure analysis
- **Lab 3 (General Document)**: Key-value pair extraction concepts

You should already have:
- ✅ Python virtual environment (`.venv` in the Labs folder)
- ✅ `.env` file with Azure credentials configured
- ✅ `requirements.txt` with all dependencies installed

**No additional setup required!** All prebuilt models use the same Azure Document Intelligence resource.

---

## Lab Structure

This lab contains **5 specialized prebuilt models**, each in its own folder:

```
lab-4-prebuilt-models/
├── 1-bank-statements/          ← US Bank Statement analysis
├── 2-invoices/                 ← Invoice processing
├── 3-credit-cards/             ← Credit/Debit card extraction
├── 4-identity-documents/       ← ID, License, Passport processing
└── 5-receipts/                 ← Receipt analysis
```

Each folder contains:
- `data/` - Sample documents for testing
- Python script - Ready-to-run code for that model
- Commented code explaining model-specific features

---

## Understanding Prebuilt Models

### What Makes Prebuilt Models Special?

| Aspect | General Models (Labs 1-3) | Prebuilt Models (Lab 4) |
|--------|---------------------------|-------------------------|
| **Training** | General-purpose OCR and layout | Industry-specific, pre-trained |
| **Fields** | Generic (text, tables, key-value) | Domain-specific (invoice ID, card number, etc.) |
| **Use Case** | Any document type | Specific document types |
| **Customization** | Not needed | Not needed (ready to use) |
| **Accuracy** | Good for general text | Optimized for specific fields |

### When to Use Prebuilt Models?

✅ **Use Prebuilt Models When:**
- Processing standard business documents (invoices, receipts, bank statements)
- Extracting known fields from common document types
- You need immediate results without training custom models
- Documents follow industry-standard formats

❌ **Use General Models When:**
- Document type doesn't match any prebuilt model
- Unique or custom document formats
- Only need text extraction or layout analysis

---

## Model Capabilities Matrix

| Model | Primary Use Case | Key Fields Extracted | Data Structures | Security Considerations |
|-------|------------------|---------------------|-----------------|------------------------|
| **Bank Statement** | Account activity analysis | Account holder, bank info, balances, transactions | Nested arrays (accounts → transactions) | ⚠️ Financial PII |
| **Invoice** | AP automation, billing | Vendor, customer, line items, totals, dates | Arrays (line items), tables | Standard business data |
| **Credit Card** | Payment processing, verification | Card number, CVV, expiration, holder name | Simple fields, phone arrays | ⚠️ **PCI DSS compliance required** |
| **Identity Document** | KYC, verification | Name, DOB, document number, address | Simple fields, document-specific (MRZ, endorsements) | ⚠️ **Personal PII, GDPR/CCPA** |
| **Receipt** | Expense tracking, accounting | Merchant, items, totals, tax, tip | Nested arrays (items) | Standard transactional data |

---

## Lab Exercises

### Exercise 1: Bank Statement Analysis
**Model:** `prebuilt-bankStatement.us`  
**Folder:** `1-bank-statements/`

**What You'll Extract:**
- Account holder information (name, address)
- Bank details (name, address)
- Statement period (start date, end date)
- Account information (account number, type, balances)
- **Transactions** - Date, description, deposits, withdrawals

**Business Value:**
- Automated account reconciliation
- Expense tracking and categorization
- Fraud detection through transaction monitoring
- Tax preparation and documentation

**Learning Focus:**
- Working with nested data structures (accounts contain transactions)
- Handling multiple accounts in a single statement
- Understanding transaction-level detail extraction

---

### Exercise 2: Invoice Processing
**Model:** `prebuilt-invoice`  
**Folder:** `2-invoices/`

**What You'll Extract:**
- Vendor information (name, address)
- Customer information (name, ID, address)
- Invoice details (ID, date, due date, purchase order)
- **Line items** - Description, quantity, unit price, amount
- Payment summary (subtotal, tax, total, amount due)
- Addresses (billing, shipping, service, remittance)

**Business Value:**
- Accounts Payable (AP) automation
- Purchase order matching
- Payment processing automation
- Vendor management and analytics

**Learning Focus:**
- Extracting structured line items (table-like data)
- Working with currency values and calculations
- Multi-language invoice support
- Understanding optional fields (not all invoices have all fields)

---

### Exercise 3: Credit Card Extraction
**Model:** `prebuilt-creditCard`  
**Folder:** `3-credit-cards/`

**What You'll Extract:**
- Card holder name
- Card number (with masking for security)
- Card verification value (CVV)
- Expiration date
- Issuing bank
- Payment network (Visa, Mastercard, Amex, etc.)
- Customer service phone numbers

**Business Value:**
- Payment form automation
- Card verification processes
- Digital wallet integration
- Customer onboarding

**Security Considerations:**
- ⚠️ **PCI DSS Compliance Required**
- Never log or store card numbers in plain text
- Use tokenization for storage
- Implement proper encryption in transit
- Follow secure coding practices

**Learning Focus:**
- Handling sensitive payment data securely
- Understanding compliance requirements
- Working with multiple card formats (horizontal, vertical)
- Masking sensitive information in logs/output

---

### Exercise 4: Identity Document Processing
**Model:** `prebuilt-idDocument`  
**Folder:** `4-identity-documents/`

**What You'll Extract:**
- Personal information (first name, last name, date of birth)
- Document details (document number, expiration date, issue date)
- Address information
- Country/Region and state
- Gender/Sex
- **Document-specific fields:**
  - Passports: Machine Readable Zone (MRZ), nationality
  - Driver's Licenses: Endorsements, restrictions, vehicle classifications
  - National IDs: Document discriminator

**Business Value:**
- Know Your Customer (KYC) processes
- Identity verification for onboarding
- Age verification systems
- Travel document processing
- Background check automation

**Security Considerations:**
- ⚠️ **Personal Identifiable Information (PII)**
- GDPR compliance for EU citizens
- CCPA compliance for California residents
- Data retention policies
- Audit logging requirements

**Learning Focus:**
- Handling different document types (passport vs. license vs. ID)
- Understanding document-specific fields (MRZ, endorsements)
- Working with multi-national formats
- Privacy and compliance best practices

---

### Exercise 5: Receipt Analysis
**Model:** `prebuilt-receipt`  
**Folder:** `5-receipts/`

**What You'll Extract:**
- Merchant information (name, address, phone)
- Transaction details (date, time)
- **Items purchased** - Description, quantity, unit price, total price
- Payment summary (subtotal, tax, tip, total)
- Receipt metadata (locale, receipt type)

**Business Value:**
- Expense report automation
- Tax deduction tracking
- Budget management
- Reimbursement processing
- Sales analytics

**Learning Focus:**
- Dynamic field detection (model adapts to what's present)
- Handling itemized vs. summary-only receipts
- Multi-language support
- Working with various receipt formats (retail, hotel, restaurant)

---

## Key Concepts

### 1. Dynamic Field Detection
All prebuilt models use **dynamic extraction** - they only extract fields that exist in the document:
- If a receipt has a tip → extracts it
- If a receipt has NO tip → skips it (no error)
- If an invoice has 10 line items → extracts all 10
- If an invoice has 100 line items → extracts all 100

**Your code doesn't need to change!** The `if` checks handle missing fields automatically.

### 2. Confidence Scores
Every extracted field includes a **confidence score** (0-100%):
- High confidence (>95%) - Field is clearly visible and recognized
- Medium confidence (80-95%) - Field detected but may need review
- Low confidence (<80%) - May require manual verification

**Best Practice:** Set thresholds based on your use case (e.g., require >90% for automated processing).

### 3. Multi-Language Support
Most prebuilt models support **multiple languages**:
- Invoices: English, Spanish, German, French, Italian, Portuguese, Dutch, and more
- Receipts: English, Japanese, French, German, Italian, Spanish, Portuguese, and more
- Identity Documents: Global support for various document formats

The models **automatically detect** the language - no configuration needed!

### 4. Data Structures

**Simple Fields:** Single values (e.g., `merchant_name`, `invoice_total`)
```python
merchant_name = receipt.fields.get("MerchantName")
if merchant_name:
    print(merchant_name.value_string)  # "Contoso Store"
```

**Arrays:** Lists of objects (e.g., items, transactions, phone numbers)
```python
items = receipt.fields.get("Items")
for item in items.value_array:
    description = item.value_object.get("Description")
    print(description.value_string)  # "Coffee", "Sandwich", etc.
```

**Nested Structures:** Objects containing other objects/arrays
```python
accounts = statement.fields.get("Accounts")
for account in accounts.value_array:
    transactions = account.value_object.get("Transactions")
    for transaction in transactions.value_array:
        # Process each transaction
```

---

## Running the Lab

### General Workflow for Each Exercise

1. **Navigate to the model folder**
   ```bash
   cd lab-4-prebuilt-models/1-bank-statements
   ```

2. **Activate virtual environment**
   ```powershell
   # PowerShell
   ..\..\..\.venv\Scripts\Activate.ps1
   
   # Command Prompt
   ..\..\..\.venv\Scripts\activate.bat
   ```

3. **Review sample data**
   ```bash
   # Check what sample files are available
   dir data
   ```

4. **Run the script**
   ```bash
   python bank_statement.py
   ```

5. **Analyze the results**
   - Review extracted fields
   - Check confidence scores
   - Understand data structure

6. **Experiment**
   - Try different sample files (change `file_path` in the script)
   - Observe how extraction varies by document
   - Note which fields are present/absent

7. **Repeat for other models**
   - Move to next folder (2-invoices, 3-credit-cards, etc.)
   - Follow the same workflow

---

## Comparison with Previous Labs

### Lab Progression

| Lab | Model Type | Capability | Use Case |
|-----|------------|------------|----------|
| **Lab 1** | Read API | Text extraction + OCR | Plain text documents, searchable PDFs |
| **Lab 2** | Layout API | Structure analysis | Documents with tables, forms with checkboxes |
| **Lab 3** | General Document | Key-value pairs | Generic forms, any labeled document |
| **Lab 4** | Prebuilt Models | **Specialized extraction** | **Industry-standard documents** |

### When to Use What?

**Decision Tree:**
```
Is your document type one of: Invoice, Receipt, Bank Statement, Credit Card, ID?
├─ YES → Use Lab 4 Prebuilt Model (specialized, optimized)
└─ NO
   ├─ Has labeled fields (Name: ___, Date: ___)?
   │  └─ YES → Use Lab 3 General Document
   └─ NO
      ├─ Has tables or checkboxes?
      │  └─ YES → Use Lab 2 Layout
      └─ NO → Use Lab 1 Read (plain text)
```

---

## Security & Compliance Best Practices

### Handling Sensitive Data

1. **Credit Cards (PCI DSS)**
   - Never log card numbers in plain text
   - Use tokenization for storage
   - Encrypt data in transit (HTTPS)
   - Implement access controls
   - Regular security audits

2. **Identity Documents (PII)**
   - Comply with GDPR (EU), CCPA (California), and local privacy laws
   - Implement data retention policies
   - Provide data deletion capabilities
   - Audit access to PII data
   - Encrypt data at rest and in transit

3. **Financial Documents**
   - Secure storage for bank statements and invoices
   - Role-based access control (RBAC)
   - Audit logging for compliance
   - Regular data purging per retention policies

4. **General Best Practices**
   - Use Azure Key Vault for credentials (not .env in production)
   - Implement least privilege access
   - Enable Azure Monitor for audit trails
   - Use managed identities when possible
   - Regular security reviews

---

## Troubleshooting

### Common Issues

**Issue 1: Model Not Found Error**
```
Error: ModelNotFound
```
**Solution:** Verify you're using the correct model ID:
- Bank Statements: `prebuilt-bankStatement.us` (note the `.us` suffix)
- Others: `prebuilt-invoice`, `prebuilt-creditCard`, `prebuilt-idDocument`, `prebuilt-receipt`

**Issue 2: No Fields Extracted**
**Possible Reasons:**
- Document quality is poor (blurry, low resolution)
- Document type doesn't match the model (e.g., using receipt model on invoice)
- Unsupported document format or variation

**Solution:** 
- Use high-quality scans (300 DPI recommended)
- Verify document type matches the model
- Try Document Intelligence Studio to test the document

**Issue 3: Low Confidence Scores**
**Possible Reasons:**
- Handwritten text (some models support it, others don't)
- Unusual document formats
- Poor image quality

**Solution:**
- Improve scan/photo quality
- Use printed documents when possible
- Consider custom models for non-standard formats

**Issue 4: Missing Expected Fields**
**Remember:** Prebuilt models use **dynamic extraction**
- If a field doesn't exist in the document, it won't be extracted
- Check the actual document - is the field really there?
- Field names vary (e.g., "Total" vs "Grand Total") - model adapts

---

## Advanced Topics (Optional)

### 1. Batch Processing
Process multiple documents in a loop:
```python
import os

data_folder = "data/"
for filename in os.listdir(data_folder):
    if filename.endswith(('.png', '.jpg', '.pdf')):
        file_path = os.path.join(data_folder, filename)
        # Analyze file_path
        print(f"Processing: {filename}")
```

### 2. Combining Models
Use multiple models in a workflow:
1. Use **Layout** to detect document structure
2. Use **Invoice** model if tables detected
3. Use **General Document** as fallback for unknown fields

### 3. Custom Post-Processing
Add business logic after extraction:
```python
# Validate invoice total matches line items
calculated_total = sum(item.total for item in line_items)
if abs(calculated_total - invoice_total) > 0.01:
    print("⚠️ Total mismatch - manual review needed")
```

### 4. Integration Patterns
- Export to databases (SQL, Cosmos DB)
- Send to message queues (Azure Service Bus, Event Grid)
- Trigger workflows (Logic Apps, Power Automate)
- Store in blob storage with metadata

---

## Best Practices Summary

✅ **DO:**
- Use high-quality document images (300 DPI)
- Check confidence scores before trusting extracted data
- Handle missing fields gracefully (use `if` checks)
- Implement proper security for sensitive data
- Log extraction results for audit trails
- Test with various document samples

❌ **DON'T:**
- Store sensitive data (credit cards, PII) without encryption
- Skip validation of critical fields
- Assume all fields will always be present
- Use low-quality images (blurry, skewed)
- Ignore compliance requirements (PCI DSS, GDPR, CCPA)
- Hard-code field positions or assumptions

---

## Next Steps

After completing this lab, you can:

1. **Explore Custom Models** (Future Lab)
   - Train models for your specific document types
   - Handle unique formats not covered by prebuilt models

2. **Build Real-World Applications**
   - Expense management system
   - Invoice processing pipeline
   - Identity verification service
   - Payment automation

3. **Integrate with Azure Services**
   - Azure Functions for serverless processing
   - Logic Apps for workflow automation
   - Blob Storage for document management
   - Cosmos DB for extracted data storage

4. **Explore Document Intelligence Studio**
   - Visual model testing
   - Custom model training
   - Composed model creation
   - API testing and debugging

---

## Additional Resources

- [Azure Document Intelligence Documentation](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/)
- [Prebuilt Models Overview](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/concept-model-overview)
- [Invoice Model Schema](https://github.com/Azure-Samples/document-intelligence-code-samples/blob/main/schema/2024-11-30-ga/invoice.md)
- [Bank Statement Model](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/prebuilt/bank-statement)
- [Credit Card Model](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/prebuilt/credit-card)
- [Identity Document Model](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/prebuilt/id-document)
- [Receipt Model](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/prebuilt/receipt)
- [Document Intelligence Studio](https://documentintelligence.ai.azure.com/studio)
- [PCI DSS Compliance](https://www.pcisecuritystandards.org/)
- [GDPR Guidelines](https://gdpr.eu/)

---

## Summary

In this lab, you learned to:
- ✅ Use 5 specialized prebuilt models for common business documents
- ✅ Extract industry-specific fields automatically
- ✅ Understand when to use prebuilt vs. general models
- ✅ Handle sensitive data securely and compliantly
- ✅ Work with dynamic field detection
- ✅ Process documents in multiple languages
- ✅ Implement real-world document processing scenarios

---

## 🎉 Workshop Complete!

**Congratulations!** You've successfully completed all four Azure Document Intelligence labs!

### Your Learning Journey

| Lab | Model | What You Mastered |
|-----|-------|-------------------|
| **Lab 1** | Read API | Text extraction, OCR, searchable PDFs, batch processing |
| **Lab 2** | Layout API | Document structure, tables, selection marks, page layout |
| **Lab 3** | General Document | Key-value pair extraction from forms |
| **Lab 4** | Prebuilt Models | Industry-specific processing (bank statements, invoices, credit cards, IDs, receipts) |

You now have **comprehensive knowledge** of Azure Document Intelligence and can:
- Choose the right model for any document processing task
- Extract text, structure, and specific fields from various document types
- Build real-world document automation solutions
- Handle sensitive data with proper security and compliance considerations

**Ready to build amazing document processing solutions!** 🚀

---

**Workshop Files:** Navigate to `1-bank-statements/` to start exploring the prebuilt models!
