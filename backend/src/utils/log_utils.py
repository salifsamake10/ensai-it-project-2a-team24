import logging


def initialize_logs(name: str) -> None:
	logging.basicConfig(
		level=logging.INFO,
		format="%(asctime)s %(levelname)s %(name)s: %(message)s",
	)
	logging.getLogger(__name__).info("Starting %s", name)


def get_logger(module_name: str) -> logging.Logger:
	return logging.getLogger(module_name)