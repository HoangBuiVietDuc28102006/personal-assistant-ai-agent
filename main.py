from config.logging_config import setup_logging
from interfaces.cli import CLI

if __name__ == "__main__":
    setup_logging()
    import logging
    logger = logging.getLogger(__name__)
    logger.info("Application started")
    
    cli = CLI()
    cli.run()