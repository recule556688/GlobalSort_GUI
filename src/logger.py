import logging


def setup_logging(log_file="application.log"):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s:%(message)s",
    )


def log_message(message):
    logging.info(message)
