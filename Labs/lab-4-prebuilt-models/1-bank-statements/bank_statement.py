"""
Azure AI Document Intelligence - US Bank Statement Model Demo
This script demonstrates the prebuilt-bankStatement.us model for extracting structured data from bank statements.

The Bank Statement model extracts:
- Account holder information (name, address)
- Bank information (name, address)
- Statement period (start date, end date)
- Account details (account number, type, balances)
- Transactions (date, description, amounts)

This model is specifically designed for US bank statements and automatically recognizes
the standard fields and transaction details.
"""

from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
import os
from dotenv import load_dotenv

# Load credentials from parent Labs directory
# The ../../ means go up two levels from '1-bank-statements' to 'Labs' folder
load_dotenv(dotenv_path="../../.env")

# Get Azure endpoint and API key from environment variables
endpoint = os.getenv("AZ_DOCINT_ENDPOINT")
key = os.getenv("AZ_DOCINT_KEY")


def analyze_bank_statement():
    """
    Main function to analyze a bank statement using the prebuilt US Bank Statement model.
    
    The prebuilt-bankStatement.us model is designed for:
    - US bank statements with standard format
    - Extracting account holder and bank information
    - Identifying account details and balances
    - Extracting all transactions with dates, descriptions, and amounts
    """
    
    # Path to the bank statement document
    # Available sample files in data/ folder - change the filename to analyze different statements:
    # - "data/US-bank-statement.jpg" - US bank statement sample
    # - "data/Bank-Statement.jpg" - Bank statement sample
    # - "data/RBS-Bank-Statement-TemplateLab.com_.jpg" - RBS bank statement template
    # Just change the filename below to try different statements!
    
    file_path = "data/US-bank-statement.jpg"  # Change this to any file from the list above
    
    # Initialize Document Intelligence client with your credentials
    document_intelligence_client = DocumentIntelligenceClient(
        endpoint=endpoint, 
        credential=AzureKeyCredential(key)
    )
    
    print(f"Analyzing bank statement: {file_path}")
    print("=" * 100)
    
    # Open and read the bank statement file in binary mode
    with open(file_path, "rb") as f:
        # Start the analysis using the prebuilt US Bank Statement model
        # The poller pattern is used for long-running operations
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-bankStatement.us",  # The model ID for US bank statements
            body=f  # The document to analyze
        )
        
        # Wait for the analysis to complete and get the result
        bankstatements = poller.result()
    
    print(f"✓ Analysis complete! Model used: prebuilt-bankStatement.us")
    print("=" * 100)
    
    # =========================================================================
    # BANK STATEMENT EXTRACTION
    # =========================================================================
    # The result may contain multiple statements if the PDF has multiple pages
    # or multiple statement periods
    
    for idx, statement in enumerate(bankstatements.documents):
        print(f"\n{'='*100}")
        print(f"📄 STATEMENT #{idx + 1}")
        print("=" * 100)
        
        # =====================================================================
        # ACCOUNT HOLDER INFORMATION
        # =====================================================================
        print("\n👤 ACCOUNT HOLDER INFORMATION")
        print("-" * 100)
        
        account_holder_name = statement.fields.get("AccountHolderName")
        if account_holder_name:
            print(f"  Name: {account_holder_name.value_string}")
            print(f"  Confidence: {account_holder_name.confidence:.2%}")
        
        account_holder_address = statement.fields.get("AccountHolderAddress")
        if account_holder_address:
            print(f"  Address: {account_holder_address.value_address}")
            print(f"  Confidence: {account_holder_address.confidence:.2%}")
        
        # =====================================================================
        # BANK INFORMATION
        # =====================================================================
        print("\n🏦 BANK INFORMATION")
        print("-" * 100)
        
        bank_name = statement.fields.get("BankName")
        if bank_name:
            print(f"  Bank Name: {bank_name.value_string}")
            print(f"  Confidence: {bank_name.confidence:.2%}")
        
        bank_address = statement.fields.get("BankAddress")
        if bank_address:
            print(f"  Bank Address: {bank_address.value_address}")
            print(f"  Confidence: {bank_address.confidence:.2%}")
        
        # =====================================================================
        # STATEMENT PERIOD
        # =====================================================================
        print("\n📅 STATEMENT PERIOD")
        print("-" * 100)
        
        statement_start_date = statement.fields.get("StatementStartDate")
        if statement_start_date:
            print(f"  Start Date: {statement_start_date.value_date}")
            print(f"  Confidence: {statement_start_date.confidence:.2%}")
        
        statement_end_date = statement.fields.get("StatementEndDate")
        if statement_end_date:
            print(f"  End Date: {statement_end_date.value_date}")
            print(f"  Confidence: {statement_end_date.confidence:.2%}")
        
        # =====================================================================
        # ACCOUNTS AND TRANSACTIONS
        # =====================================================================
        # A bank statement may contain multiple accounts (checking, savings, etc.)
        # Each account has details and a list of transactions
        
        accounts = statement.fields.get("Accounts")
        if accounts:
            print("\n💳 ACCOUNTS")
            print("=" * 100)
            
            for account_idx, account in enumerate(accounts.value_array):
                print(f"\n  📌 ACCOUNT #{account_idx + 1}")
                print("  " + "-" * 96)
                
                # Account Number
                account_number = account.value_object.get("AccountNumber")
                if account_number:
                    print(f"    Account Number: {account_number.value_string}")
                    print(f"    Confidence: {account_number.confidence:.2%}")
                
                # Account Type (e.g., Checking, Savings)
                account_type = account.value_object.get("AccountType")
                if account_type:
                    print(f"    Account Type: {account_type.value_string}")
                    print(f"    Confidence: {account_type.confidence:.2%}")
                
                # Beginning Balance
                beginning_balance = account.value_object.get("BeginningBalance")
                if beginning_balance:
                    print(f"    Beginning Balance: ${beginning_balance.value_number:,.2f}")
                    print(f"    Confidence: {beginning_balance.confidence:.2%}")
                
                # Ending Balance
                ending_balance = account.value_object.get("EndingBalance")
                if ending_balance:
                    print(f"    Ending Balance: ${ending_balance.value_number:,.2f}")
                    print(f"    Confidence: {ending_balance.confidence:.2%}")
                
                # Total Service Fees
                total_service_fees = account.value_object.get("TotalServiceFees")
                if total_service_fees:
                    print(f"    Total Service Fees: ${total_service_fees.value_number:,.2f}")
                    print(f"    Confidence: {total_service_fees.confidence:.2%}")
                
                # =============================================================
                # TRANSACTIONS
                # =============================================================
                # Each account contains a list of transactions
                # Transactions include date, description, deposits, and withdrawals
                
                transactions = account.value_object.get("Transactions")
                if transactions:
                    print(f"\n    💰 TRANSACTIONS (Total: {len(transactions.value_array)})")
                    print("    " + "-" * 92)
                    
                    for transaction_idx, transaction in enumerate(transactions.value_array):
                        print(f"\n      🔹 Transaction #{transaction_idx + 1}")
                        
                        # Transaction Date
                        transaction_date = transaction.value_object.get("Date")
                        if transaction_date:
                            print(f"        Date: {transaction_date.value_date}")
                            print(f"        Confidence: {transaction_date.confidence:.2%}")
                        
                        # Description
                        description = transaction.value_object.get("Description")
                        if description:
                            print(f"        Description: {description.value_string}")
                            print(f"        Confidence: {description.confidence:.2%}")
                        
                        # Deposit Amount
                        deposit_amount = transaction.value_object.get("DepositAmount")
                        if deposit_amount:
                            print(f"        Deposit: +${deposit_amount.value_number:,.2f}")
                            print(f"        Confidence: {deposit_amount.confidence:.2%}")
                        
                        # Withdrawal Amount
                        withdrawal_amount = transaction.value_object.get("WithdrawalAmount")
                        if withdrawal_amount:
                            print(f"        Withdrawal: -${withdrawal_amount.value_number:,.2f}")
                            print(f"        Confidence: {withdrawal_amount.confidence:.2%}")
        
        print("\n" + "=" * 100)
    
    print("\n✓ Bank statement analysis complete!")
    print("=" * 100)


if __name__ == "__main__":
    # Run the bank statement analysis
    analyze_bank_statement()
