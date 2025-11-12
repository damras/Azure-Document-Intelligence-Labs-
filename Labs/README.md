# Azure Document Intelligence Workshop

Welcome to the **Azure Document Intelligence Workshop**! This hands-on workshop will guide you through Azure AI Document Intelligence's powerful capabilities for extracting text, structure, and specific fields from various document types.

---

## 🎯 Workshop Overview

This workshop consists of **4 progressive labs** that build on each other, taking you from basic text extraction to industry-specific document processing:

| Lab | Model | Focus | Duration |
|-----|-------|-------|----------|
| **Lab 1** | Read API | Text extraction, OCR, searchable PDFs | 45-60 min |
| **Lab 2** | Layout API | Document structure, tables, selection marks | 45-60 min |
| **Lab 3** | General Document | Key-value pair extraction from forms | 30-45 min |
| **Lab 4** | Prebuilt Models | Industry-specific processing (5 models) | 60-90 min |

**Total Workshop Time:** ~3-4 hours

---

## 📚 Learning Path

### Lab 1: Read API - Text Extraction Fundamentals
**Folder:** `lab-1-read/`

**What You'll Learn:**
- Extract text from images and PDFs using OCR
- Detect languages and handwriting
- Work with bounding boxes and confidence scores
- Create searchable PDFs from images
- Process multiple documents in batch mode

**Exercises:**
1. Basic text extraction with detailed metadata
2. Image to searchable PDF conversion
3. Batch processing with raw API responses

**Prerequisites:** Azure Document Intelligence resource, Python 3.8+

➡️ **Start here:** [Lab 1 README](lab-1-read/README.md)

---

### Lab 2: Layout API - Document Structure Analysis
**Folder:** `lab-2-layout/`

**What You'll Learn:**
- Extract complete document structure
- Detect and extract tables with cell-by-cell structure
- Identify selection marks (checkboxes) and their states
- Distinguish between handwritten and printed text
- Understand page objects and layout properties

**Key Features:**
- Table extraction with headers and merged cells
- Selection mark detection (checked/unchecked)
- Handwriting vs. printed text identification
- Page dimensions, rotation, and positioning

**Prerequisites:** Completion of Lab 1

➡️ **Continue to:** [Lab 2 README](lab-2-layout/README.md)

---

### Lab 3: General Document Model - Form Processing
**Folder:** `lab-3-general/`

**What You'll Learn:**
- Extract key-value pairs from form-like documents
- Work with labeled fields and their values
- Understand SDK differences (formrecognizer vs. documentintelligence)
- Process structured documents (employment forms, contracts, reports)

**Key Features:**
- Automatic key-value pair detection
- Table extraction with structure
- Field labels and values with confidence scores
- Working with the `azure-ai-formrecognizer` SDK

**Prerequisites:** Completion of Labs 1 and 2

➡️ **Continue to:** [Lab 3 README](lab-3-general/README.md)

---

### Lab 4: Prebuilt Models - Industry-Specific Processing
**Folder:** `lab-4-prebuilt-models/`

**What You'll Learn:**
- Use specialized prebuilt models for common business documents
- Extract industry-specific fields without custom training
- Handle sensitive data with security and compliance considerations
- Process financial and identity documents

**5 Specialized Models:**

1. **Bank Statements** (`prebuilt-bankStatement.us`)
   - Account holder information
   - Bank details and balances
   - Transaction arrays with nested data
   - File: `1-bank-statements/bank_statement.py`

2. **Invoices** (`prebuilt-invoice`)
   - Vendor and customer information
   - Line items with quantities and prices
   - Payment summary (subtotal, tax, total)
   - File: `2-invoices/invoice.py`

3. **Credit Cards** (`prebuilt-creditCard`)
   - Card numbers with automatic masking
   - Expiration dates and CVV
   - PCI DSS compliance considerations
   - File: `3-credit-cards/credit_card.py`

4. **Identity Documents** (`prebuilt-idDocument`)
   - Licenses, passports, national IDs
   - Personal information extraction
   - Privacy and GDPR/CCPA compliance
   - File: `4-identity-documents/identity_document.py`

5. **Receipts** (`prebuilt-receipt`)
   - Merchant information
   - Itemized purchases
   - Payment summary with tax and tip
   - File: `5-receipts/receipt.py`

**Prerequisites:** Completion of Labs 1, 2, and 3

➡️ **Complete the workshop:** [Lab 4 README](lab-4-prebuilt-models/README.md)

---

## 🛠️ Initial Setup (Do This First!)

> **⚠️ IMPORTANT:** Before starting Lab 1, you must create an Azure Document Intelligence resource and configure your credentials.

### 📖 Complete Setup Guide

**Follow this guide first:** [Azure Document Intelligence Service Setup Guide](AZURE_SETUP.md)

This comprehensive guide includes:
- ✅ Step-by-step Azure Portal instructions with screenshots
- ✅ How to create the Document Intelligence resource
- ✅ How to retrieve your Endpoint and API Key
- ✅ Pricing information and cost management
- ✅ Troubleshooting common issues

### Quick Setup Summary

Once you've created your Azure resource (see guide above):

### 1. Azure Resources
- ✅ Azure Document Intelligence resource created in Azure Portal
- ✅ **Endpoint URL** and **API Key** retrieved from "Keys and Endpoint"

### 2. Project Structure
Create the main Labs directory:
```bash
mkdir Labs
cd Labs
```

### 3. Environment Configuration
Create a `.env` file in the Labs directory:
```env
AZ_DOCINT_ENDPOINT=https://<your-resource-name>.cognitiveservices.azure.com/
AZ_DOCINT_KEY=<your-api-key>
```

> **Where to find credentials:** Azure Portal → Your Resource → Keys and Endpoint

### 4. Python Dependencies
Create `requirements.txt` in the Labs directory:
```txt
azure-ai-documentintelligence
azure-ai-formrecognizer
azure-core
python-dotenv
numpy
```

### 5. Virtual Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate it
# PowerShell:
.venv\Scripts\Activate.ps1
# Command Prompt:
.venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt
```

### 6. Folder Structure
After completing all labs, your structure will look like:
```
Labs/
├── .env                           ← Azure credentials (shared)
├── requirements.txt               ← Python dependencies (shared)
├── .venv/                         ← Virtual environment (shared)
├── README.md                      ← This file
├── lab-1-read/
│   ├── data/                      ← Sample images/PDFs
│   ├── read.py                    ← Exercise 1
│   ├── searchable_pdf.py          ← Exercise 2
│   ├── read_batch_demo.py         ← Exercise 3
│   └── README.md
├── lab-2-layout/
│   ├── data/                      ← Sample documents
│   ├── layout.py                  ← Layout analysis
│   └── README.md
├── lab-3-general/
│   ├── data/                      ← Form-like documents
│   ├── general_document.py        ← Key-value extraction
│   └── README.md
└── lab-4-prebuilt-models/
    ├── 1-bank-statements/
    │   ├── data/
    │   └── bank_statement.py
    ├── 2-invoices/
    │   ├── data/
    │   └── invoice.py
    ├── 3-credit-cards/
    │   ├── data/
    │   └── credit_card.py
    ├── 4-identity-documents/
    │   ├── data/
    │   └── identity_document.py
    ├── 5-receipts/
    │   ├── data/
    │   └── receipt.py
    └── README.md
```

---

## 🎓 What You'll Master

By completing this workshop, you will:

### Technical Skills
- ✅ Extract text from any document type (images, PDFs, scans)
- ✅ Analyze document structure (tables, selection marks, layout)
- ✅ Extract key-value pairs from forms
- ✅ Process industry-specific documents automatically
- ✅ Work with two Azure Document Intelligence SDKs
- ✅ Handle batch processing and multiple file formats
- ✅ Implement security and compliance best practices

### Business Applications
- ✅ Automate invoice processing
- ✅ Build expense management systems
- ✅ Implement KYC (Know Your Customer) workflows
- ✅ Process bank statements for analysis
- ✅ Extract data from receipts for accounting
- ✅ Verify identity documents
- ✅ Convert images to searchable PDFs

### Model Selection
- ✅ Choose the right model for each use case
- ✅ Understand when to use general vs. prebuilt models
- ✅ Combine multiple models in workflows
- ✅ Optimize for speed vs. detail

---

## 📖 Model Comparison Guide

| Model | Text | Tables | Key-Value | Checkboxes | Specialized Fields | Best For |
|-------|------|--------|-----------|------------|-------------------|----------|
| **Read** | ✅ | ❌ | ❌ | ❌ | ❌ | Plain text extraction, OCR |
| **Layout** | ✅ | ✅ | ❌ | ✅ | ❌ | Document structure, tables |
| **General Document** | ✅ | ✅ | ✅ | ✅ | ❌ | Forms, labeled documents |
| **Prebuilt Models** | ✅ | ✅ | ✅ | ✅ | ✅ | Industry-specific documents |

---

## 🚀 Getting Started

1. **Complete the Initial Setup** (above) to configure your environment
2. **Start with Lab 1** - [Read API](lab-1-read/README.md)
3. **Progress sequentially** through Labs 2, 3, and 4
4. **Experiment** with your own documents as you learn

---

## 💡 Tips for Success

- **Follow the sequence:** Each lab builds on previous knowledge
- **Read the comments:** Code is extensively commented for learning
- **Try all samples:** Each lab provides multiple sample documents
- **Experiment:** Change file paths to test different documents
- **Ask questions:** Use the troubleshooting sections in each README
- **Take breaks:** This is a comprehensive workshop!

---

## 🔧 Troubleshooting

### Common Issues Across All Labs

**Issue: Authentication Error**
```
Error: Unauthorized (401)
```
**Solution:** 
- Verify `.env` file exists in the Labs directory
- Check endpoint and key are correct
- Ensure no extra spaces or quotes in `.env` values

**Issue: Module Not Found**
```
ModuleNotFoundError: No module named 'azure.ai.documentintelligence'
```
**Solution:**
- Activate virtual environment: `.venv\Scripts\Activate.ps1`
- Install dependencies: `pip install -r requirements.txt`
- Verify installation: `pip list | findstr azure`

**Issue: File Not Found**
```
FileNotFoundError: data/sample.png
```
**Solution:**
- Ensure you're in the correct lab directory
- Check that sample files exist in the `data/` folder
- Use correct file paths in scripts

---

## 📚 Additional Resources

- [Azure Document Intelligence Documentation](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/)
- [Python SDK - Document Intelligence](https://learn.microsoft.com/en-us/python/api/azure-ai-documentintelligence/)
- [Python SDK - Form Recognizer](https://learn.microsoft.com/en-us/python/api/azure-ai-formrecognizer/)
- [Document Intelligence Studio](https://documentintelligence.ai.azure.com/studio) - Visual testing tool
- [Pricing Information](https://azure.microsoft.com/en-us/pricing/details/ai-document-intelligence/)
- [Model Overview](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/concept-model-overview)

---

## 🎉 Ready to Begin?

**Start your journey:** Navigate to [Lab 1 - Read API](lab-1-read/README.md) and begin extracting text from documents!

---

**Workshop Version:** 1.0  
**Last Updated:** November 2024  
**Target Audience:** Developers, Data Engineers, Solution Architects
