# Azure Document Intelligence Workshop

A comprehensive hands-on workshop for learning Azure AI Document Intelligence through 4 progressive labs, covering text extraction, document structure analysis, form processing, and industry-specific document processing.

## 🎯 Workshop Overview

This workshop teaches you how to extract text, tables, and structured data from various document types using Azure AI Document Intelligence. Progress through 4 labs that build on each other:

| Lab | Focus | Duration | Key Learning |
|-----|-------|----------|--------------|
| **Lab 1** | Read API | 45-60 min | Text extraction, OCR, searchable PDFs |
| **Lab 2** | Layout API | 45-60 min | Tables, selection marks, document structure |
| **Lab 3** | General Document | 30-45 min | Key-value pair extraction from forms |
| **Lab 4** | Prebuilt Models | 60-90 min | Industry-specific processing (5 models) |

**Total Time:** ~3-4 hours

## 📋 Prerequisites

- **Azure Subscription** with Document Intelligence resource created
- **Python 3.8+** (Python 3.12 recommended)
- **Visual Studio Code** (recommended)
- Basic Python knowledge

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd DIworkshop
```

### 2. Set Up Azure Credentials

Navigate to the `Labs` folder and create a `.env` file:

```bash
cd Labs
```

Copy `.env.example` to `.env` and fill in your Azure credentials:

```env
AZ_DOCINT_ENDPOINT=https://your-resource-name.cognitiveservices.azure.com/
AZ_DOCINT_KEY=your-api-key-here
```

**Where to find your credentials:**
- Go to [Azure Portal](https://portal.azure.com)
- Navigate to your Document Intelligence resource
- Click "Keys and Endpoint" in the left menu
- Copy the Endpoint and Key 1

### 3. Create Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate it
# Windows PowerShell:
.venv\Scripts\Activate.ps1

# Windows Command Prompt:
.venv\Scripts\activate.bat

# macOS/Linux:
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Start Lab 1

```bash
cd lab-1-read
# Follow the README.md in the lab-1-read folder
```

## 📚 Workshop Structure

```
DIworkshop/
├── README.md                          ← You are here
├── .gitignore
├── Labs/
│   ├── README.md                      ← Complete workshop guide
│   ├── .env.example                   ← Template for credentials
│   ├── .env                           ← Your credentials (not in git)
│   ├── requirements.txt               ← Python dependencies
│   ├── .venv/                         ← Virtual environment (not in git)
│   │
│   ├── lab-1-read/                    ← Lab 1: Read API
│   │   ├── README.md
│   │   ├── data/                      ← Sample documents
│   │   ├── read.py
│   │   ├── searchable_pdf.py
│   │   └── read_batch_demo.py
│   │
│   ├── lab-2-layout/                  ← Lab 2: Layout API
│   │   ├── README.md
│   │   ├── data/
│   │   └── layout.py
│   │
│   ├── lab-3-general/                 ← Lab 3: General Document
│   │   ├── README.md
│   │   ├── data/
│   │   └── general_document.py
│   │
│   └── lab-4-prebuilt-models/         ← Lab 4: Prebuilt Models
│       ├── README.md
│       ├── 1-bank-statements/
│       │   ├── data/
│       │   └── bank_statement.py
│       ├── 2-invoices/
│       │   ├── data/
│       │   └── invoice.py
│       ├── 3-credit-cards/
│       │   ├── data/
│       │   └── credit_card.py
│       ├── 4-identity-documents/
│       │   ├── data/
│       │   └── identity_document.py
│       └── 5-receipts/
│           ├── data/
│           └── receipt.py
```

## 🎓 What You'll Learn

### Technical Skills
- ✅ Extract text from images and PDFs using OCR
- ✅ Analyze document structure (tables, checkboxes, layout)
- ✅ Extract key-value pairs from forms
- ✅ Process industry-specific documents (invoices, receipts, IDs, etc.)
- ✅ Work with Azure Document Intelligence SDKs
- ✅ Handle batch processing and multiple file formats
- ✅ Implement security and compliance best practices

### Business Applications
- Automate invoice processing
- Build expense management systems
- Implement KYC (Know Your Customer) workflows
- Process bank statements for analysis
- Extract data from receipts for accounting
- Verify identity documents
- Convert images to searchable PDFs

## 📖 Labs Overview

### Lab 1: Read API - Text Extraction
Extract text from documents using OCR, create searchable PDFs, and process multiple files in batch mode.

**Skills:** Basic text extraction, confidence scores, language detection, handwriting recognition

➡️ [Start Lab 1](Labs/lab-1-read/README.md)

---

### Lab 2: Layout API - Document Structure
Extract tables, detect checkboxes, and understand document layout and page structure.

**Skills:** Table extraction, selection marks, page objects, handwriting vs. printed text

➡️ [Start Lab 2](Labs/lab-2-layout/README.md)

---

### Lab 3: General Document - Form Processing
Extract key-value pairs from form-like documents such as applications, contracts, and reports.

**Skills:** Key-value extraction, labeled fields, SDK differences

➡️ [Start Lab 3](Labs/lab-3-general/README.md)

---

### Lab 4: Prebuilt Models - Industry-Specific Processing
Use specialized models for bank statements, invoices, credit cards, identity documents, and receipts.

**Skills:** Specialized field extraction, security compliance, multi-language support

➡️ [Start Lab 4](Labs/lab-4-prebuilt-models/README.md)

---

## 🛠️ Models Covered

| Model | Use Case | Key Features |
|-------|----------|--------------|
| **Read** | Text extraction | OCR, language detection, handwriting |
| **Layout** | Document structure | Tables, checkboxes, page layout |
| **General Document** | Forms | Key-value pairs, labeled fields |
| **Bank Statement** | Account analysis | Transactions, balances, account info |
| **Invoice** | AP automation | Vendor, line items, totals |
| **Credit Card** | Payment processing | Card details (PCI DSS compliant) |
| **Identity Document** | KYC verification | Licenses, passports, IDs (GDPR/CCPA) |
| **Receipt** | Expense tracking | Merchant, items, payment summary |

## 🔒 Security Notes

- ⚠️ **Never commit your `.env` file** - It contains your Azure credentials
- ⚠️ The `.gitignore` file prevents `.env` from being committed
- ⚠️ Use `.env.example` as a template for others
- ⚠️ Lab 4 covers PCI DSS and GDPR/CCPA compliance for sensitive documents

## 📚 Additional Resources

- [Azure Document Intelligence Documentation](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/)
- [Python SDK - Document Intelligence](https://learn.microsoft.com/en-us/python/api/azure-ai-documentintelligence/)
- [Python SDK - Form Recognizer](https://learn.microsoft.com/en-us/python/api/azure-ai-formrecognizer/)
- [Document Intelligence Studio](https://documentintelligence.ai.azure.com/studio) - Visual testing tool
- [Pricing Information](https://azure.microsoft.com/en-us/pricing/details/ai-document-intelligence/)

## 🤝 Contributing

This is a workshop repository. Feel free to:
- Report issues or suggestions
- Submit improvements to documentation
- Share your experiences

## 📝 License

This workshop is provided for educational purposes.

## 🎉 Get Started

Ready to begin? Navigate to the [Labs folder](Labs/README.md) for the complete workshop guide!

---

**Workshop Version:** 1.0  
**Last Updated:** November 2024  
**Target Audience:** Developers, Data Engineers, Solution Architects
