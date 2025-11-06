import time
import functools
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

def retry(max_attempts: int = 3, backoff_seconds: float = 1.0, allowed_exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            last_exc = None
            while attempt < max_attempts:
                attempt += 1
                start_ts = time.time()
                try:
                    logger.info(f"Attempt {attempt}/{max_attempts} for {func.__name__} - args={args} kwargs={kwargs}")
                    result = func(*args, **kwargs)
                    elapsed = time.time() - start_ts
                    logger.info(f"Success on attempt {attempt} for {func.__name__} (elapsed={elapsed:.3f}s)")
                    return result
                except allowed_exceptions as e:
                    elapsed = time.time() - start_ts
                    logger.warning(f"Exception on attempt {attempt} for {func.__name__}: {e} (elapsed={elapsed:.3f}s)")
                    last_exc = e
                    if attempt < max_attempts:
                        sleep_time = backoff_seconds * attempt
                        logger.info(f"Sleeping {sleep_time}s before next attempt")
                        time.sleep(sleep_time)
            logger.error(f"All {max_attempts} attempts failed for {func.__name__}")
            raise last_exc
        return wrapper
    return decorator
