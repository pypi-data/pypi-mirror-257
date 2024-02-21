from collections import deque
from wagtail_localize.tasks import BaseJobBackend
import threading, time, os, logging

from wagtail import hooks


logger = logging.getLogger(__name__)
_dj_logger = logging.getLogger("django")

class ThreadedBackend(BaseJobBackend):
    def __init__(self, options):
        self.options = options
        self.threads = self.options.get("THREADS", 2)
        self.sleep_timeout = self.options.get("SLEEP_TIMEOUT", 0.1)
        self.slow_sleep = self.options.get("SLOW_SLEEP", False)
        self.currently_running = 0
        self.queue = deque()
        self.lock = threading.RLock()
        self.main_queue_thread = threading.Thread(target=self.start, daemon=True)
        self.main_queue_thread.start()

        if not self.sleep_timeout or self.sleep_timeout <= 0:
            self.sleep_timeout = 0.1

        if not self.threads or self.threads <= 0:
            raise RuntimeError("THREADS must be greater than 0")
            
        if self.threads > os.cpu_count():
            logger.warning("[ThreadedBackend] THREADS is greater than the number of CPU cores (%s/%s)" % (self.threads, os.cpu_count()))

    def enqueue(self, func, args, kwargs):
        # Lock when enqueing to prevent loss of data.
        # If two threads add to it at the same time,
        # one of the functions might be lost.
        logger.debug("[ThreadedBackend] Enqueing task %s" % func.__name__)
        with self.lock:
            self.queue.append(func, args, kwargs)

    def start(self):
        def _run_fn(q: ThreadedBackend, func, args, kwargs):
            logger.debug("[ThreadedBackend] Running task %s" % func.__name__)
            start = time.time()

            page_id, locales, components, user = args
            for hook in hooks.get_hooks('before_translation_task_run'):
                hook(page_id=page_id, locales=locales, components=components, user=user)

            func(*args, **kwargs)

            for hook in hooks.get_hooks('after_translation_task_run'):
                hook(page_id=page_id, locales=locales, components=components, user=user)

            end = time.time()
            _dj_logger.info("[ThreadedBackend] Task %s took %s seconds" % (func.__name__, round(end - start, 2)))
            with q.lock:
                q._decrement_TC(False)

        while True:
            time.sleep(self.sleep_timeout)

            if len(self.queue) == 0:
                if isinstance(self.slow_sleep, (int, float)):
                    timeout = self.slow_sleep
                else:
                    timeout = self.sleep_timeout * 100
                logger.debug("[ThreadedBackend] No tasks to run, sleeping for %s seconds" % timeout)

            
            # Lock the thread when checking how many threads to run
            with self.lock:
                run_threads = (self.threads - self.currently_running)
                if run_threads <= 0:
                    continue
                    
            if run_threads > len(self.queue):
                run_threads = len(self.queue)

            # Log how many threads are being run
            _log_threads_to_run = run_threads
            if len(self.queue) < run_threads:
                _log_threads_to_run = len(self.queue)
            logger.debug("[ThreadedBackend] Running %s threads" % _log_threads_to_run)

            for _ in range(run_threads):

                # Lock the thread when dequeuing
                with self.lock:
                    if len(self.queue) == 0:
                        break
                    
                    n = self.queue.pop()
                    if n is None:
                        break
                
                    t = threading.Thread(target=_run_fn, args=(self, n.func, n.args, n.kwargs), daemon=True)
                    self._increment_TC(False)
                # Thread can be safely started outside of the lock
                t.start()

    def _increment_TC(self, use_lock=True):
        """
        Increment the currently running thread count
        """
        if use_lock:
            self.lock.acquire()

        self.currently_running += 1

        if use_lock:
            self.lock.release()

    def _decrement_TC(self, use_lock=True):
        """
        Decrement the currently running thread count
        """
        if use_lock:
            self.lock.acquire()

        if self.currently_running > 0:
            self.currently_running -= 1

        if use_lock:
            self.lock.release()
