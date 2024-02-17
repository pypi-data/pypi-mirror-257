"""This module contains the settings for the negotium application.
"""
import os

# default settings
DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 6379
DEFAULT_USERNAME = 'guest'
DEFAULT_PASSWORD = 'guest'

# message settings
_MESSAGE_MAIN = 'negotium_queue'
_MESSAGE_SCHEDULER = 'negotium_scheduler_queue'
_MESSAGE_SCHEDULER_SORTED_SET = 'negotium_scheduler_sorted_set'
_MESSAGE_TRACKER = 'negotium_tracker'
_MESSAGE_PERIODIC_TASKS = 'negotium_periodic_tasks'

# logging settings
LOGGING_FORMAT = '[%(asctime)s] [negotium: %(name)s] [%(levelname)s] %(message)s\n'
LOGGING_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# worker settings
def disable_worker() -> bool:
    """Disable the worker to execute tasks asynchronously
    """
    os.environ['NEGOTIUM_WORKER'] = '0'
    return True

def enable_worker() -> bool:
    """Enable the worker to execute tasks asynchronously
    """
    os.environ['NEGOTIUM_WORKER'] = '1'
    return True

def is_worker_enabled() -> bool:
    """Check if the worker is enabled
    """
    return os.environ.get('NEGOTIUM_WORKER', '1') == '1'
