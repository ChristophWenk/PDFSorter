# Requirements
## User Stories
- As a user I want a script to determine to which company a PDF belongs to
- As a user I want a script to determine which type of document a PDF is
- As a user I want a script to rename a file according to a predefined format
- As a user I want a script to sort PDFs into given folders according to a company and document type

## Functional & non-functional Requirements
The script should be configurable with document type configurations.
General functionality should look like this:
1. Check which company is in scope
2. Get the document types for the company and check which document type is in scope
3. Retrieve the desired information defined by the regex patterns in the configuration file
4. Rename PDFs according to the configuration file
5. Move PDFs to the target location

# Architecture
## Prerequisites
**Basic Prerequisites**
- Python 3.10.4
- pip 21.2.4

**Python Packages**
- pypdf2 2.4.2
- dateparser 1.1.1

Other Python or package versions might work but have not been tested. 

A conda environment configuration is provided in 
the `environment.yml` file. You can set it up with `conda env create -f environment.yml`. Activate it with
`conda activate PDFSorter`.

## Document Type Configuration
New document types can be added by creating new configuration files. The process is described below.
Place the files in the directory defined in `settings.config_files_dir`. 
The default is `'../resources/config_files'`.
### Configuration File Name
The configuration file name has to adhere to the scheme below. The [Company] and the [Document Type] values have both 
to be found in the PDF text content. This will only be used to select the correct configuration file for the PDF in 
processing. 

**Scheme:** [Company]-[Document Type]-[Creation Date].json

**Example:** Helsana-Leistungsabrechnung-20220717.json

### Configuration File Structure (Example Helsana-Leistungsabrechnung-20220717.json)
```
{
    "company_name": "Helsana",
    "document_type": "Leistungsabrechnung",
    "regex_patterns":
    {
        "document_id": "(?<=Rechnung Nr. )(.*)(\\n)",
        "date": "(?<=Dübendorf\\n)(.*)(?=\\nLeistungsabrechnung)"
    },
    "target_directory": "F:\\Dokumente\\Rechnungen\\Helsana\\Leistungsabrechnungen",
    "file_name_format":  "{company_name}_{date}_{document_type}_{document_id}.pdf"
}
```
`company_name` can have the same value as [Company] in the configuration file name, but it is not a requirement.

`document_type` can have the same value as [Document Type] in the configuration file name, but it is not a requirement.

`regex_patterns` can be expanded with additional patterns or the existing ones can be removed. All defined patterns will
be executed upon script execution. The retrieved values will be appended to the configuration with the same key as
defined in `regex_patterns`. The original file will not be altered by the script.

`target_directory` points to the directory where the files that match this configuration will be moved to. The script
will generate folders by year within this directory.

`file_name_format` defines the new name of the processed PDF file. The tokens refer to the top-level properties in 
the configuration file and may include property keys generated from the regex patterns.

### Configuration Structure after Parsing the Regex Patterns (In-Memory only)
```
{
    "company_name": "Helsana",
    "document_type": "Leistungsabrechnung",
    "regex_patterns":
    {
        "document_id": "(?<=Rechnung Nr. )(.*)(\\n)",
        "date": "(?<=Dübendorf\\n)(.*)(?=\\nLeistungsabrechnung)"
    },
    "target_directory": "F:\\Dokumente\\Rechnungen\\Helsana\\Leistungsabrechnungen",
    "file_name_format":  "{company_name}_{date}_{document_type}_{document_id}.pdf",
    "document_id": "ABCD",
    "date": "2022-12-31"
}
```

## Script settings
The script can be customized in multiple ways. The process is described below. To do so edit the settings in the
file `settings.py`.

### Dry Run (Preview) Mode
If the script should only be tested but the files should not be altered one can activate dry run mode. 
The generated names and directories will still be logged. To do so apply the following settings: 
```
# Do (False) or do not (True) rename files and move them
dry_run = True
```

### Folder Configurations
The following folder configurations can be customized:
```
# Folder that contains the PDFs to process
pdf_files_dir = 'F:/Downloads/02_pdf_sorter'

# Folder that contains the document configuration files
config_files_dir = '../resources/config_files'

# Folder that contains script log files
log_files_dir = '../generated/logs/'
```

### Language Configurations for Date Operations
Set language that will be used to write the names of the months / days of the week
```
# Language configurations for date operations (e.g. names of the months)
locale.setlocale(locale.LC_ALL, 'de_CH')
```

### Log Level
The Log level can be set with the `log_level` variable. E.g. switch from `logging.INFO` to `logging.DEBUG` for 
debugging purposes.
```
# Log level used by the common logger
log_level = logging.INFO
```