"""
Azure AI Document Intelligence - Identity Document Model Demo
This script demonstrates the prebuilt-idDocument model for extracting structured data from identity documents.

The Identity Document model extracts:
- Personal information (first name, last name, date of birth)
- Document details (document number, expiration date)
- Address information
- Country/Region and location details
- Gender/Sex information

This model works with various types of identity documents including:
- Driver's licenses
- Passports
- National ID cards
- Social Security cards
- Green cards
"""

from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
import os
from dotenv import load_dotenv

# Load credentials from parent Labs directory
# The ../../ means go up two levels from '4-identity-documents' to 'Labs' folder
load_dotenv(dotenv_path="../../.env")

# Get Azure endpoint and API key from environment variables
endpoint = os.getenv("AZ_DOCINT_ENDPOINT")
key = os.getenv("AZ_DOCINT_KEY")


def analyze_identity_document():
    """
    Main function to analyze an identity document using the prebuilt ID Document model.
    
    The prebuilt-idDocument model is designed for:
    - Driver's licenses from various countries
    - Passports and travel documents
    - National ID cards
    - Social Security cards
    - Resident permits and green cards
    
    ⚠️ PRIVACY NOTE: This demo is for educational purposes only.
    Never store or transmit personally identifiable information (PII) without proper security and compliance.
    """
    
    # Path to the identity document image
    # Available sample files in data/ folder - change the filename to analyze different documents:
    # - "data/DriverLicense.png" - Driver's license sample
    # - "data/Passport.png" - Passport sample
    # - "data/id-us-green-card.png" - US Green Card sample
    # - "data/id-us-social-security-card.png" - US Social Security Card sample
    # Just change the filename below to try different identity documents!
    
    file_path = "data/DriverLicense.png"  # Change this to any file from the list above
    
    # Initialize Document Intelligence client with your credentials
    document_intelligence_client = DocumentIntelligenceClient(
        endpoint=endpoint, 
        credential=AzureKeyCredential(key)
    )
    
    print(f"Analyzing identity document: {file_path}")
    print("=" * 100)
    print("⚠️  PRIVACY NOTICE: Handle personal identity data with proper security measures and compliance")
    print("=" * 100)
    
    # Open and read the identity document image in binary mode
    with open(file_path, "rb") as f:
        # Start the analysis using the prebuilt ID Document model
        # The poller pattern is used for long-running operations
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-idDocument",  # The model ID for identity documents
            body=f  # The document to analyze
        )
        
        # Wait for the analysis to complete and get the result
        id_documents = poller.result()
    
    print(f"\n✓ Analysis complete! Model used: prebuilt-idDocument")
    print("=" * 100)
    
    # =========================================================================
    # IDENTITY DOCUMENT EXTRACTION
    # =========================================================================
    # The result may contain multiple identity documents if the image has multiple IDs
    
    for idx, id_document in enumerate(id_documents.documents):
        print(f"\n{'='*100}")
        print(f"🪪 IDENTITY DOCUMENT #{idx + 1}")
        print("=" * 100)
        
        # =====================================================================
        # PERSONAL INFORMATION
        # =====================================================================
        print("\n👤 PERSONAL INFORMATION")
        print("-" * 100)
        
        first_name = id_document.fields.get("FirstName")
        if first_name:
            print(f"  First Name: {first_name.value_string}")
            print(f"  Confidence: {first_name.confidence:.2%}")
        
        last_name = id_document.fields.get("LastName")
        if last_name:
            print(f"  Last Name: {last_name.value_string}")
            print(f"  Confidence: {last_name.confidence:.2%}")
        
        dob = id_document.fields.get("DateOfBirth")
        if dob:
            print(f"  Date of Birth: {dob.value_date}")
            print(f"  Confidence: {dob.confidence:.2%}")
        
        sex = id_document.fields.get("Sex")
        if sex:
            print(f"  Sex: {sex.content}")
            print(f"  Confidence: {sex.confidence:.2%}")
        
        # =====================================================================
        # DOCUMENT DETAILS
        # =====================================================================
        print("\n📄 DOCUMENT DETAILS")
        print("-" * 100)
        
        document_number = id_document.fields.get("DocumentNumber")
        if document_number:
            print(f"  Document Number: {document_number.value_string}")
            print(f"  Confidence: {document_number.confidence:.2%}")
        
        doe = id_document.fields.get("DateOfExpiration")
        if doe:
            print(f"  Date of Expiration: {doe.value_date}")
            print(f"  Confidence: {doe.confidence:.2%}")
        
        doi = id_document.fields.get("DateOfIssue")
        if doi:
            print(f"  Date of Issue: {doi.value_date}")
            print(f"  Confidence: {doi.confidence:.2%}")
        
        # =====================================================================
        # ADDRESS INFORMATION
        # =====================================================================
        print("\n📍 ADDRESS INFORMATION")
        print("-" * 100)
        
        address = id_document.fields.get("Address")
        if address:
            print(f"  Address: {address.value_address}")
            print(f"  Confidence: {address.confidence:.2%}")
        
        country_region = id_document.fields.get("CountryRegion")
        if country_region:
            print(f"  Country/Region: {country_region.value_country_region}")
            print(f"  Confidence: {country_region.confidence:.2%}")
        
        region = id_document.fields.get("Region")
        if region:
            print(f"  Region/State: {region.value_string}")
            print(f"  Confidence: {region.confidence:.2%}")
        
        # =====================================================================
        # ADDITIONAL FIELDS (Document-specific)
        # =====================================================================
        # Some identity documents may have additional fields like:
        # - MachineReadableZone (MRZ) for passports
        # - DocumentDiscriminator for driver's licenses
        # - Endorsements, restrictions, vehicle classes, etc.
        
        print("\n📋 ADDITIONAL FIELDS")
        print("-" * 100)
        
        # Check for Machine Readable Zone (MRZ) - common in passports
        mrz = id_document.fields.get("MachineReadableZone")
        if mrz:
            print(f"  Machine Readable Zone (MRZ): {mrz.value_object}")
            print(f"  Confidence: {mrz.confidence:.2%}")
        
        # Check for Document Discriminator - common in driver's licenses
        discriminator = id_document.fields.get("DocumentDiscriminator")
        if discriminator:
            print(f"  Document Discriminator: {discriminator.value_string}")
            print(f"  Confidence: {discriminator.confidence:.2%}")
        
        # Check for Nationality - common in passports
        nationality = id_document.fields.get("Nationality")
        if nationality:
            print(f"  Nationality: {nationality.value_country_region}")
            print(f"  Confidence: {nationality.confidence:.2%}")
        
        # Check for Place of Birth
        place_of_birth = id_document.fields.get("PlaceOfBirth")
        if place_of_birth:
            print(f"  Place of Birth: {place_of_birth.value_string}")
            print(f"  Confidence: {place_of_birth.confidence:.2%}")
        
        # Check for Endorsements (driver's license)
        endorsements = id_document.fields.get("Endorsements")
        if endorsements:
            print(f"  Endorsements: {endorsements.value_string}")
            print(f"  Confidence: {endorsements.confidence:.2%}")
        
        # Check for Restrictions (driver's license)
        restrictions = id_document.fields.get("Restrictions")
        if restrictions:
            print(f"  Restrictions: {restrictions.value_string}")
            print(f"  Confidence: {restrictions.confidence:.2%}")
        
        # Check for Vehicle Classifications (driver's license)
        vehicle_classifications = id_document.fields.get("VehicleClassifications")
        if vehicle_classifications:
            print(f"  Vehicle Classifications: {vehicle_classifications.value_string}")
            print(f"  Confidence: {vehicle_classifications.confidence:.2%}")
        
        print("\n" + "=" * 100)
    
    print("\n✓ Identity document analysis complete!")
    print("⚠️  Remember: Always handle PII data securely and comply with privacy regulations (GDPR, CCPA, etc.)")
    print("=" * 100)


if __name__ == "__main__":
    # Run the identity document analysis
    analyze_identity_document()
