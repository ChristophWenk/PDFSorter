import locale
import logging

# Do (False) or do not (True) rename files and move them
dry_run = False
# Set language that will be used to write the names of the months / days of the week
locale.setlocale(locale.LC_ALL, 'de_CH')
# Log level used by the common logger
log_level = logging.INFO
