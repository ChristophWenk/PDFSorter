import locale
import logging

# Do (False) or do not (True) rename files and move them
dry_run = False

# Folder that contains the PDFs to process
pdf_files_dir = 'F:/Downloads/02_pdf_sorter'

# Folder that contains the document configuration files
config_files_dir = '../resources/config_files'

# Folder that contains script log files
log_files_dir = '../generated/logs/'

# Language configurations for date operations (e.g. names of the months)
locale.setlocale(locale.LC_ALL, 'de_CH')

# Log level used by the common logger
log_level = logging.INFO
