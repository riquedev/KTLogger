import pathlib, datefinder
from typing import Iterator
from django.db.models import QuerySet
from django_mock_queries.query import MockSet
from django.core.cache import cache
from KTLogger.models import KTFile, KTFileLog
from KTLogger.settings import KT_LOG_VIEWER_FILES_DIR, KT_LOG_VIEWER_FILES_PATTERN, KT_LOG_VIEWER_MAX_READ_LINES
from KTLogger.utils import blocks
from file_read_backwards import FileReadBackwards


class KTCore:

    @classmethod
    def get_files(cls) -> Iterator[pathlib.Path]:
        for file_dir in KT_LOG_VIEWER_FILES_DIR:
            for pattern in KT_LOG_VIEWER_FILES_PATTERN:
                for file in pathlib.Path(file_dir).glob(pattern):
                    yield file

    @classmethod
    def get_kt_files(cls) -> QuerySet[KTFile]:
        files = [KTFile(
            file_name=file.name,
            file_uri=str(file),
            lines_count=cls.get_file_line_count(file)
        ) for file in cls.get_files()]
        qs = MockSet(*files)
        return qs

    @classmethod
    def get_file_line_count(cls, file):
        key = f"ktlogger:line_count:{file}"
        lines = cache.get(key)

        if lines is None:
            lines = sum(bl.count("\n") for bl in blocks(open(file, "r")))

            # Let's avoid opening the file multiple times during the 30s period.
            cache.set(key, lines, 30)
        return lines

    @classmethod
    def get_file_lines(cls, file):
        lines = []
        pos = cls.get_file_line_count(file)
        max_lines = KT_LOG_VIEWER_MAX_READ_LINES
        line_limit = (pos - max_lines) + 1
        pos += 1
        if line_limit < 0:
            line_limit = 0
        if pathlib.Path(file).exists():
            with FileReadBackwards(file) as frb:
                while True:
                    line = frb.readline()
                    if not line:
                        break
                    # line = line.split("\n")
                    if pos < line_limit:
                        break
                    if line.strip():
                        pos -= 1
                        try:
                            data = {
                                'line': pos,
                                'content': line,
                                'level': KTFileLog.get_level(line),
                                'timestamp': list(datefinder.find_dates(line))[0]
                            }
                            lines.append(
                                KTFileLog(**data)
                            )

                        except IndexError:
                            pos += 1
                            lines[-1].content += line

        return MockSet(*lines)
