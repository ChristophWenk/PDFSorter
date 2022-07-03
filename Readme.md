# Guides
https://realpython.com/pdf-python/

# Requirements
- As a user I want the script to determine to which company the PDF belongs to
- As a user I want the script to determine which type of company document the PDF is
- As a user I want the script to sort the PDFs into given folders according to company and document type

# Architecture
The script should be configurable with document type configurations.
General functionality should look like this:
1. Check which company is in scope
2. Check which document type is in scope
3. Retrieve desired information
4. Rename PDFs and move them to the target location

## Example document type configuration
### Document type configuration name
[Company]-[Document Type]-[Date]

Helsana-Leistungsabrechnung-20220628

### Structure
```
{
    "company_name": "Helsana"
    "document_type": "Leistungsabrechnung"
    "regex_paterns": 
    { 
        "document_id": "Rechnung Nr. .*"
        "date": " .* 15. Januar 2022"
    }
    "target_location": C:\Some_Directory\Helsana\Leistungsabrechnungen
}
```

## Output file name
[Company]-[Date]-[Document Type]-[Document ID]