import logging
import logging.handlers
import os
from pathlib import Path

from appdirs import user_log_dir
from tendo.singleton import SingleInstance, SingleInstanceException

from sleepytime.__version__ import __version__
from sleepytime.window import SleepyTimeWindow

FORMATTER = (
    "%(asctime)s - [%(process)d] - %(name)s:%(lineno)d - %(levelname)s - %(message)s"
)

base_logger = logging.getLogger("sleepytime")
base_logger.setLevel(os.environ.get("SLEEPYTIME_LOG_LEVEL", "INFO"))

sh = logging.StreamHandler()
sh.setFormatter(logging.Formatter(FORMATTER))
base_logger.addHandler(sh)

logdir = Path(user_log_dir("sleepytime"))
logdir.mkdir(parents=True, exist_ok=True)

rfh = logging.handlers.RotatingFileHandler(
    filename=logdir / "sleepytime.log",
    maxBytes=1024 * 1024 * 8,
    backupCount=5,
    delay=True,
)
rfh.setFormatter(logging.Formatter(FORMATTER))
base_logger.addHandler(rfh)

if __name__ == "__main__":
    # you must give a var for SingleInstance to live in... otherwise
    # __del__ is likely to get called in it and delete the instance file.
    try:
        t = SingleInstance()
    except SingleInstanceException:
        base_logger.error("Another instance of sleepytime is already running.")
        raise RuntimeError(
            "Another instance of sleepytime is already running, quitting."
        )

    base_logger.info(f"Starting sleepytime {__version__}.")
    SleepyTimeWindow().run()
