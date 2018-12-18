#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2018/12/6

import os
import xlwt

from urllib.parse import quote

from django.conf import settings
from django.views import View
from django.views.generic import TemplateView
from django.http.response import StreamingHttpResponse
# from django.http.response import FileResponse

from .. import models


class SurveyIndexView(TemplateView):

    template_name = "web/index.html"

    extra_context = {
        "title": "欢迎使用问卷调查系统"
    }


class SurveyDetailView(TemplateView):

    template_name = "web/detail.html"

    extra_context = {
        "title": "讲师问卷调查"
    }


class SurveyDownloadView(View):

    """
        1、将唯一码写入文件
        2、下载`xls`文件
    """
    queryset = models.SurveyCode.objects.all()

    file_name = "唯一码.xls"

    def get(self, request, *args, **kwargs):
        queryset = self.queryset.filter(survey_id=kwargs.get("pk"))

        xls = xlwt.Workbook(encoding="utf-8", style_compression=2)
        sheet = xls.add_sheet("唯一码", cell_overwrite_ok=True)

        for index, code in enumerate(queryset.iterator(), ):
            sheet.write(index, 0, code.unique_code)

        xls.save(self.file_name)

        file_path = os.path.join(settings.BASE_DIR, self.file_name)

        # 形式一
        # response = FileResponse(open(file_path, "rb"), as_attachment=True, filename=self.file_name)
        # return response

        # 形式二
        # response = StreamingHttpResponse(open(file_path, "rb"))

        def iter_file(path, size=1024):

            # with open(path, "rb", ) as f:
            #     while True:
            #         data = f.read(size)
            #         if data:
            #             yield data
            #         else:
            #             break

            with open(path, "rb", ) as f:
                for data in iter(lambda: f.read(size), b''):
                    yield data

        response = StreamingHttpResponse(iter_file(file_path))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment; {}'.format(
            "filename*=utf-8''{}".format(quote(self.file_name))
        )

        return response
