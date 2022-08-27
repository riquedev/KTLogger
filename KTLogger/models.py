import copy
import re
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_mock_queries.query import MockModel
from .settings import KT_LOG_LEVEL_PATTERN

class KTFile(MockModel, models.Model):
    """
        Don't worry, we're not going to use the real Database.
    """

    file_name = models.CharField(max_length=360)
    file_uri = models.FilePathField()
    lines_count = models.IntegerField(default=0)
    _prefetched_objects_cache = ()

    class Meta:
        managed = False
        abstract = True

    def get_absolute_url(self):
        return reverse('KTLogger:file', kwargs={
            "file": self.file_uri
        })

class KTFileLog(MockModel, models.Model):
    class Level(models.TextChoices):
        INFO = 'IN', _('Info')
        DEBUG = 'DE', _('Debug')
        WARNING = 'WA', _('Warning')
        ERROR = 'ER', _('Error')
        CRITICAL = 'CR', _('Critical')

    line = models.IntegerField(default=1)
    content = models.TextField(blank=True)
    level = models.CharField(max_length=2, choices=Level.choices, default=Level.DEBUG)
    timestamp = models.DateTimeField(null=True)

    _prefetched_objects_cache = ()

    @classmethod
    def pattern_info(cls) -> re.Pattern:
        return KT_LOG_LEVEL_PATTERN.get("INFO", re.compile(r'(\[INFO])', flags=re.IGNORECASE))

    @classmethod
    def pattern_warning(cls) -> re.Pattern:
        return KT_LOG_LEVEL_PATTERN.get("WARNING", re.compile(r'(\[WARNING])', flags=re.IGNORECASE))

    @classmethod
    def pattern_error(cls) -> re.Pattern:
        return KT_LOG_LEVEL_PATTERN.get("ERROR", re.compile(r'(\[ERROR])', flags=re.IGNORECASE))

    @classmethod
    def pattern_critical(cls) -> re.Pattern:
        return KT_LOG_LEVEL_PATTERN.get("CRITICAL", re.compile(r'(\[CRITICAL])', flags=re.IGNORECASE))

    @classmethod
    def pattern_debug(cls) -> re.Pattern:
        return KT_LOG_LEVEL_PATTERN.get("DEBUG", re.compile(r'(\[DEBUG])', flags=re.IGNORECASE))

    def get_clean_content(self) -> str:
        clean_content = self.content

        if self.level == self.Level.INFO:
            clean_content = re.sub(self.pattern_info(), "", clean_content)
        elif self.level == self.Level.WARNING:
            clean_content = re.sub(self.pattern_warning(), "", clean_content)
        elif self.level == self.Level.ERROR:
            clean_content = re.sub(self.pattern_error(), "", clean_content)
        elif self.level == self.Level.CRITICAL:
            clean_content = re.sub(self.pattern_critical(), "", clean_content)
        else:
            clean_content = re.sub(self.pattern_debug(), "", clean_content)

        return clean_content.lstrip()

    @classmethod
    def get_level(cls, content: str):
        if re.match(cls.pattern_info(), content):
            return cls.Level.INFO
        elif re.match(cls.pattern_warning(), content):
            return cls.Level.WARNING
        elif re.match(cls.pattern_error(), content):
            return cls.Level.ERROR
        elif re.match(cls.pattern_critical(), content):
            return cls.Level.CRITICAL
        else:
            return cls.Level.DEBUG

    class Meta:
        managed = False
        abstract = True

