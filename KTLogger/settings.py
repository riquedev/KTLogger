import re
from django.conf import settings as django_settings

KT_LOG_VIEWER_FILES_PATTERN = getattr(django_settings, 'KT_LOG_VIEWER_FILES_PATTERN', [
    "*.log*"
])
KT_LOG_VIEWER_FILES_DIR = getattr(django_settings, 'KT_LOG_VIEWER_FILES_DIR', [
    "logs/"
])
KT_LOG_VIEWER_MAX_READ_LINES = getattr(django_settings, 'KT_LOG_VIEWER_MAX_READ_LINES', 100)
KT_LOG_VIEWER_PATTERNS = getattr(django_settings, "KT_LOG_VIEWER_PATTERNS",
                                 ['[INFO]', '[DEBUG]', '[WARNING]', '[ERROR]', '[CRITICAL]'])
KT_LOG_LEVEL_PATTERN = getattr(django_settings, "KT_LOG_LEVEL_PATTERN", {
    "INFO": re.compile(r'(\[INFO])', flags=re.IGNORECASE),
    "DEBUG": re.compile(r'(\[DEBUG])', flags=re.IGNORECASE),
    "WARNING": re.compile(r'(\[WARNING])', flags=re.IGNORECASE),
    "ERROR": re.compile(r'(\[ERROR])', flags=re.IGNORECASE),
    "CRITICAL": re.compile(r'(\[CRITICAL])', flags=re.IGNORECASE),
})

KT_LOG_VIEWER_EXCLUDE_TEXT_PATTERN = getattr(django_settings, "KT_LOG_VIEWER_EXCLUDE_TEXT_PATTERN", None)
