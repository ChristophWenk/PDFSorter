import locale
import logging

# Do (False) or do not (True) rename files and move them
dry_run = True

# Folder that contains the PDFs to process
pdf_files_dir = 'C:/Users/chris/OneDrive/Dokumentenupload'

# Folder that contains the document configuration files
config_files_dir = '../resources/config_files'

# Folder that contains script log files
log_files_dir = '../generated/logs'

# Folder that contains the generated images
image_output_dir = '../generated/images'

# Language configurations for date operations (e.g. names of the months)
locale.setlocale(locale.LC_ALL, 'de_CH')

# Language configurations for the OCR reader
ocr_languages = ['de']

# Log level used by the common logger
log_level = logging.INFO