import os
import logging

def logging_formatter(self, logger, logger_name):

    fh = logging.FileHandler(os.path.join(self.folder_results, f"{logger_name}.log"))
    fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', "%Y-%m-%d %H:%M:%S"))
    logger.addHandler(fh)
    logger.setLevel(logging.INFO)

    return logger