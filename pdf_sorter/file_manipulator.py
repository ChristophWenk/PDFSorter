import os
import shutil
import logging
import settings

logger = logging.getLogger(__name__)


def rename_file(path, old_name, config):
    values = {}
    for key in config:
        values.update({key: config[key]})
    new_name = ""
    try:
        # Replace tokens with dictionary values
        new_name = config['file_name_format'].format(**values)
    except KeyError as exception:
        logging.warning("Expected Token named " + exception.args[0] + " but it was not defined. Skipping rename.")

    logger.info("Renaming file to..." + new_name)
    if settings.dry_run is False:
        os.rename(path + "/" + old_name, path + "/" + new_name)
    return new_name


def move_file(source_directory, file, target_directory):
    logger.info("Moving file to..." + target_directory)
    if settings.dry_run is False:
        shutil.move(source_directory + "/" + file, target_directory + "/" + file)
