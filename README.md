# Azure Language Service - PII Recognition (Polish)

A Python script demonstrating how to detect and redact Personally Identifiable Information (PII) in Polish text using Azure AI Language Service.

## Overview

This script (`recognizepiientities_pl_clean.py`) shows how to:
- Connect to Azure AI Language Service using Azure Identity
- Recognize PII entities in Polish documents
- Apply confidence-based redaction (≥60% threshold)
- Report low-confidence detections separately

**Use Case**: A payment processing company needs to anonymize sensitive data before making it public, in compliance with privacy guidelines.

## Features

| Feature | Description |
|---------|-------------|
| PII Detection | Identifies personal data like names, phone numbers, emails, PESEL numbers |
| Confidence Filtering | Separates high-confidence (≥60%) from low-confidence detections |
| Smart Redaction | Replaces detected PII with asterisks (`*`) while preserving text structure |
| Polish Language Support | Configured specifically for Polish (`pl`) language processing |
| Passwordless Auth | Uses `DefaultAzureCredential` for secure, keyless authentication |

## Supported PII Categories

The Azure Language Service can detect various PII categories including:

- **Person Names** - Full names, first names, surnames
- **Phone Numbers** - Various formats
- **Email Addresses** - Personal and professional emails
- **National IDs** - PESEL (Polish), SSN, etc.
- **Addresses** - Physical addresses
- **Credit Card Numbers** - Various card formats
- **And many more...**

📖 Full list: [Entity Categories](https://learn.microsoft.com/en-us/azure/ai-services/language-service/personally-identifiable-information/concepts/entity-categories-list)

## Prerequisites

### Azure Resources
1. **Azure Subscription** - [Create one for free](https://azure.microsoft.com/free/)
2. **Azure Language Resource** - Create via [Azure Portal](https://portal.azure.com)

### Local Environment
- Python 3.8+
- Azure CLI installed and configured

### Required Python Packages
```bash
pip install azure-ai-textanalytics azure-identity
```

## Configuration

### 1. Update the Endpoint

Edit the script and replace the endpoint with your Azure Language Service endpoint:

```python
endpoint = "https://YOUR-RESOURCE-NAME.cognitiveservices.azure.com/"
```

Find your endpoint in the Azure Portal under your Language resource → **Keys and Endpoint**.

### 2. Authenticate with Azure

This script uses `DefaultAzureCredential` which supports multiple authentication methods:

```bash
# Login to Azure (recommended for development)
az login
```

If `az login` doesn't work:
1. Install [Azure CLI](https://docs.microsoft.com/cli/azure/install-azure-cli)
2. Restart your terminal
3. Run `az login` again

## Usage

### Run the Script

```bash
python recognizepiientities_pl_clean.py
```

### Example Input

The script processes the following sample Polish text:

```
Jestem Anna Nowak.
Mój numer telefonu to 31256032344 a PESEL 86042146381. 
Można się ze mną skontaktować też pisząc na: anowak@microsoft.com.
```

### Example Output

```
Oryginalny tekst: Jestem Anna Nowak.
Mój numer telefonu to 31256032344 a PESEL 86042146381. 
Można się ze mną skontaktować też pisząc na: anowak@microsoft.com.

Zredagowany tekst: Jestem **********.
Mój numer telefonu to *********** a PESEL ***********. 
Można się ze mną skontaktować też pisząc na: **********************.

Powyżej zanonimizowane zostały dane wrażliwe zidentyfikowane z >= 60% pewności
Nie zidentyfikowano dodatkowych danych z pewnością < 60%.
```

## How It Works

### 1. Client Initialization
```python
text_analytics_client = TextAnalyticsClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(),
    language="pl"  # Polish language
)
```

### 2. PII Recognition
```python
result = text_analytics_client.recognize_pii_entities(documents)
```

### 3. Confidence-Based Filtering
```python
# Only redact entities with confidence >= 60%
high_confidence = [e for e in doc.entities if e.confidence_score >= 0.6]
```

### 4. Manual Redaction
```python
# Replace detected PII with asterisks
for entity in high_confidence:
    text = text[:entity.offset] + '*' * entity.length + text[entity.offset + entity.length:]
```

## Customization

### Adjust Confidence Threshold

Change the threshold value (default: 0.6) to be more or less strict:

```python
# More strict (only very confident detections)
high_confidence = [e for e in doc.entities if e.confidence_score >= 0.8]

# Less strict (include more potential PII)
high_confidence = [e for e in doc.entities if e.confidence_score >= 0.4]
```

### Process Multiple Documents

```python
documents = [
    "Document 1 with PII...",
    "Document 2 with PII...",
    "Document 3 with PII...",
]
```

### Filter by Category

Redact only specific PII types:

```python
categories_to_redact = ["PhoneNumber", "Email", "Person"]
filtered = [e for e in doc.entities 
            if e.confidence_score >= 0.6 
            and e.category in categories_to_redact]
```

## API Reference

| Method | Description |
|--------|-------------|
| `recognize_pii_entities()` | Detects PII in documents |
| `entity.text` | The detected PII text |
| `entity.category` | Type of PII (Person, Email, etc.) |
| `entity.confidence_score` | Detection confidence (0.0-1.0) |
| `entity.offset` | Start position in text |
| `entity.length` | Length of detected text |

## Documentation

- [Azure AI Language - PII Detection](https://aka.ms/azsdk/language/pii)
- [How to Redact PII](https://learn.microsoft.com/en-us/azure/ai-services/language-service/personally-identifiable-information/how-to/redact-text-pii)
- [Entity Categories](https://learn.microsoft.com/en-us/azure/ai-services/language-service/personally-identifiable-information/concepts/entity-categories)
- [Full Entity Categories List](https://learn.microsoft.com/en-us/azure/ai-services/language-service/personally-identifiable-information/concepts/entity-categories-list)
- [Text Analytics SDK for Python](https://docs.microsoft.com/python/api/azure-ai-textanalytics/)

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `AuthenticationError` | Run `az login` and ensure you have access to the Language resource |
| `ResourceNotFoundError` | Verify your endpoint URL is correct |
| `InvalidLanguageError` | Ensure `"pl"` is a supported language code |
| Empty results | Check that your text contains recognizable PII |

## License

This sample is provided for educational purposes. See the main repository LICENSE file for details.
