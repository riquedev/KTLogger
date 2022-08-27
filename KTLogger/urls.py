from django.urls import path
from .views import (KTLoggerFilesView, FilesAjaxDatatableView, KTLoggerFileLogsView, FileLogAjaxDatatableView,
                    KTLoggerFilesDownloadView)

app_name = "KTLogger"

urlpatterns = [
    path("download/", KTLoggerFilesDownloadView.as_view(), name="files-download"),
    path("download/<path:file>", KTLoggerFilesDownloadView.as_view(), name="files-download"),
    path("", KTLoggerFilesView.as_view(), name="files"),
    path("file/<path:file>", KTLoggerFileLogsView.as_view(), name="file"),
    path("datatables/files", FilesAjaxDatatableView.as_view(), name="datatable-files"),
    path("datatables/file/<path:file>", FileLogAjaxDatatableView.as_view(), name="datatable-file")
]
