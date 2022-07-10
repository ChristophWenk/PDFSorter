import locale
import logging

# Do (False) or do not (True) rename files and move them
dry_run = True

# Dir configurations
pdf_files_dir = 'F:/Downloads/02_pdf_sorter'
config_files_dir = 'F:/Christoph/Sonstiges/Development/PDFSorter/resources/config_files'
log_files_dir = 'F:/Christoph/Sonstiges/Development/PDFSorter/target/logs'

# Set language that will be used to write the names of the months / days of the week
locale.setlocale(locale.LC_ALL, 'de_CH')
# Log level used by the common logger
log_level = logging.INFO
