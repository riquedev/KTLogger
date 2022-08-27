import pathlib

from django.views.generic import TemplateView, View
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings as django_settings
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import localtime, now
from ajax_datatable.views import AjaxDatatableView
from .models import KTFile, KTFileLog
from .controller.ktcore import KTCore
from .utils import compress
from django.http import HttpResponse, Http404, FileResponse


@method_decorator(staff_member_required, name='dispatch')
class KTLoggerFilesView(TemplateView):
    template_name = "KTLogger/files.html"


@method_decorator(staff_member_required, name='dispatch')
class KTLoggerFilesDownloadView(View):
    def get(self, request, file = None, *args, **kwargs):
        response = None
        if file is None:
            files = list(KTCore.get_files())

            response = HttpResponse(compress(files), content_type="application/zip")
            generation_time = localtime() if django_settings.USE_TZ else now()
            response['Content-Disposition'] = 'inline; filename=' + "log_%s.zip" % generation_time.strftime(
                "%Y%m%dT%H%M%S")
        else:
            file = pathlib.Path(file)
            if file.exists():
                response = FileResponse(file.absolute().open("rb"))

        if response is None:
            raise Http404()
        return response


@method_decorator(staff_member_required, name='dispatch')
class KTLoggerFileLogsView(TemplateView):
    template_name = "KTLogger/file.html"

    def get(self, request, file, *args, **kwargs):
        context = self.get_context_data()
        context["file"] = pathlib.Path(file)
        return self.render_to_response(context)


@method_decorator(staff_member_required, name='dispatch')
class FilesAjaxDatatableView(AjaxDatatableView):
    model = KTFile
    title = _("Files")
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'all']]
    search_values_separator = '+'

    column_defs = [
        {'name': 'file_name', 'visible': True, },
        {'name': 'file_uri', 'visible': True, },
        {'name': 'lines_count', 'visible': True, 'searchable': False}
    ]

    def get_initial_queryset(self, request=None):
        return KTCore.get_kt_files()

    def customize_row(self, row, obj: KTFile):
        row["file_name"] = f"<a href='{obj.get_absolute_url()}'>{row['file_name']}</a>"


@method_decorator(staff_member_required, name='dispatch')
class FileLogAjaxDatatableView(AjaxDatatableView):
    model = KTFileLog
    title = _("Logs")
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'all']]
    search_values_separator = '+'
    initial_order = [["line", "desc"], ]

    column_defs = [
        {'name': 'line', 'visible': True, 'searchable': False},
        {'name': 'level', 'visible': True, },
        {'name': 'timestamp', 'visible': True, 'searchable': False},
        {'name': 'content', 'visible': True},
    ]

    def get_initial_queryset(self, request=None):
        uri = self.kwargs.get("file")
        return KTCore.get_file_lines(uri)

    def customize_row(self, row, obj: KTFileLog):
        row["content"] = f"<code>{obj.get_clean_content()}</code>"
