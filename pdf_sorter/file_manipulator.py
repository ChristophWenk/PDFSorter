import os
import shutil
import logging

logger = logging.getLogger(__name__)

def rename_file(path, file, company, document_type, date, document_id):
    new_name = company + "_" + date + "_" + document_type + "_" + document_id + ".pdf"
    logger.info("Renaming file to..." + new_name)
    os.rename(path + "/" + file, path + "/" + new_name)
    return new_name


def move_file(path, file, target_directory):
    logger.info("Moving file to..." + target_directory)
    shutil.move(path + "/" + file, target_directory + "/" + file)