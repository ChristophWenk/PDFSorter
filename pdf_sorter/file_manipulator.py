import os
import shutil
import logging

logger = logging.getLogger(__name__)


def rename_file(path, old_name, config):
    values = {}
    for key in config:
        values.update({key: config[key]})
    new_name = ""
    try:
        new_name = config['file_name_format'].format(**values)
    except KeyError as exception:
        logging.warning("Expected Token named " + exception + " but it was not found. Skipping rename.")

    logger.info("Renaming file to..." + new_name)
    os.rename(path + "/" + old_name, path + "/" + new_name)
    return new_name


def move_file(source_directory, file, target_directory):
    logger.info("Moving file to..." + target_directory)
    shutil.move(source_directory + "/" + file, target_directory + "/" + file)
