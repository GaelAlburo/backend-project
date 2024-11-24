import logging as log

class Logger:
    """Logger class to log messages with different severity levels"""
    def __init__(self, log_file="atemporal_orders_api.log", level=log.INFO):
        log.basicConfig(
            level=level,
            format="%(asctime)s: %(levelname)s [%(filename)s:%(lineno)s] %(message)s",
            datefmt="%I:%M:%S %p",
            handlers=[log.StreamHandler(), log.FileHandler(log_file)],
        )
        self.logger = log.getLogger()

    def debug(self, message):
        """Log a message with severity 'DEBUG' on the logger"""
        self.logger.debug(message, stacklevel=2)

    def info(self, message):
        """Log a message with severity 'INFO' on the logger"""
        self.logger.info(message, stacklevel=2)

    def warning(self, message):
        """Log a message with severity 'WARNING' on the logger"""
        self.logger.warning(message, stacklevel=2)

    def error(self, message):
        """Log a message with severity 'ERROR' on the logger"""
        self.logger.error(message, stacklevel=2)

    def critical(self, message):
        """Log a message with severity 'CRITICAL' on the logger"""
        self.logger.critical(message, stacklevel=2)

"""TEST"""
if __name__ == "__main__":
    logger = Logger()
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")