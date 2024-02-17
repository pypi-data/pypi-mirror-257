from celery import shared_task
from celery.utils.log import get_task_logger
from time import sleep

from ..celery import report_progress

logger = get_task_logger(__name__)

@shared_task(bind=True, default_retry_delay=3)
def demo(self, total: int = 1, interval: float = 1.0, retry: bool = False, noresult: bool = False):
    try:
        logger.info(f"Starting{f' (retry {self.request.retries}/{self.max_retries})' if self.request.retries else ''}")
        
        for i in range(0, total):
            report_progress(f"Doing {i+1}/{total}.", index=i, total=total)
            sleep(interval)
        
        if total >= 2:
            logger.warning("I emit a warning.")

        if total == 3 and self.request.retries <= 1:
            raise ValueError(f"I fail.")
        
        if not noresult:
            return total
    
    except Exception as exc:
        if retry:
            raise self.retry(exc=exc)
        else:
            raise
