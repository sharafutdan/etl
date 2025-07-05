import logging
import sys


def create_logger() -> logging.Logger:
    from app.telemetry.logger.formatter import ColourizedFormatter

    logger = logging.getLogger("etl")
    logger.propagate = False
    logger.setLevel(level=logging.INFO)
    main_handler = logging.StreamHandler(stream=sys.stderr)
    main_handler.setFormatter(
        ColourizedFormatter(
            fmt="%(asctime)s %(levelname)8s - %(message)s",
            use_colors=True,
        )
    )
    logger.addHandler(main_handler)
    return logger
