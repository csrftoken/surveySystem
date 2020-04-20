#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2018/12/6

import os
import json
import xlwt
import operator

from urllib.parse import quote

from django.conf import settings
from django.views import View
from django.views.generic import TemplateView
from django.db.models import Count
from django.http.response import StreamingHttpResponse
from django.http.response import JsonResponse
# from django.http.response import FileResponse

from .. import models


class SurveyLoginView(TemplateView):

    template_name = "web/login.html"

    extra_context = {
        "title": "问卷调查"
    }


class SurveyIndexView(TemplateView):

    template_name = "web/index.html"

    extra_context = {
        "title": "欢迎使用问卷调查系统"
    }


class SurveyDetailView(TemplateView):

    template_name = "web/detail.html"

    extra_context = {
        "title": "问卷调查"
    }


class SurveyReportView(TemplateView):

    template_name = "web/report.html"

    extra_context = {
        "title": "问卷调查报告"
    }

    queryset = models.SurveyRecord.objects.all()

    @staticmethod
    def get_survey_data(survey, survey_template):
        records = models.SurveyRecord.objects.filter(
            **{
                "survey": survey, "survey_template": survey_template
            }
        ).select_related()
        suggestions, answers = [], {}

        # 获取填写的记录
        for record in records.iterator():
            # 将单选的选项进行封装
            unique_code = record.survey_code.unique_code

            # 如果是建议
            if not record.choices.exists():
                suggestions.append(record.suggestion)
                continue

            score = sum(choice.points for choice in record.choices.iterator())
            if unique_code in answers:
                answers[unique_code]["questions"].append({
                    "id": record.survey_item.pk,
                    "name": record.survey_item.name,
                    "score": score
                })
                answers[unique_code]["score_sum"] = answers[unique_code]["score_sum"] + score
            else:
                answers[unique_code] = {
                    "questions": [
                        {
                            "id": record.survey_item.pk,
                            "name": record.survey_item.name,
                            "score": score
                        }
                    ],
                    "is_hide": record.is_hide,
                    "score_sum": score
                }

        _answers = list(filter(lambda item: not item["is_hide"], answers.values()))

        # 去除极值问题, 最高分和最低分
        if len(_answers) > 2:
            sorted_data = [
                {"code": code, "score_sum": value["score_sum"]} for code, value in answers.items()
            ]
            sorted_data.sort(key=operator.itemgetter("score_sum"))
            # 去除最低分
            answers[sorted_data[0]["code"]]["is_hide"] = True
            # 去除最高分
            answers[sorted_data[-1]["code"]]["is_hide"] = True

        choices = {
            question.pk: {
                "name": question.name, "real_score": 0,
                "score": getattr(
                    question.answers.order_by("-points").only("points").first(), "points", 0
                ) * (len(_answers) - 2 if len(_answers) > 2 else len(_answers))
            }
            for question in survey_template.questions.exclude(answer_type="suggestion").iterator()
        }

        score = 0
        real_score = 0

        for _, value in answers.items():

            # 如果不计入统计项目, 则不进行统计
            if value.get("is_hide", True):
                continue

            for question in value.get("questions", []):
                if question.get("id") in choices:
                    choices[question["id"]]["real_score"] += question["score"]

        for value in choices.values():

            score += value["score"]
            real_score += value["real_score"]

        return choices, suggestions, answers, "{:.2f}".format(real_score / (score or 1) * 100)

    def get_context_data(self, **kwargs):
        context = super(SurveyReportView, self).get_context_data(**kwargs)

        pk = kwargs.get("pk")

        instance = models.Survey.objects.filter(pk=pk).first()

        result = []

        # 构造数据结构体
        for item in instance.surveys.iterator():
            choices, suggestions, answers, percent = self.get_survey_data(instance, item)

            result.append(
                {
                    "id": "survey-{}".format(item.pk),
                    "percent": percent,
                    "name": item.name,
                    "answers": answers,
                    "suggestions": suggestions,
                    "choices": choices,
                }
            )

        context["result"] = result

        # 问卷份数
        context["count"] = instance.surveyrecord_set.values("survey_code").annotate(
            count=Count("survey_code")
        ).count()

        # 问卷问题
        questions = {}
        records = instance.surveyrecord_set.filter(survey_item__answer_type__in=(
            "single", "multiple"
        ))
        for record in records.iterator():
            name = record.survey_item.name
            choices = record.choices.all()
            if name not in questions:
                questions[name] = {}
                for choice in choices:
                    if choice not in questions[name]:
                        questions[name][choice.content] = 1
                    else:
                        questions[name][choice.content] += 1
            else:
                for choice in choices:
                    if choice not in questions[name]:
                        questions[name][choice.content] = 1
                    else:
                        questions[name][choice.content] += 1
        context["questions"] = {
            key: json.dumps(val)
            for key, val in questions.items()
        }
        return context

    def post(self, request, **kwargs):
        hide_codes = request.POST.getlist("hide_codes")
        show_codes = request.POST.getlist("show_codes")
        queryset = self.queryset.filter(
            survey_id=kwargs.get("pk"), survey_template_id=request.POST.get("survey_id", "")[-1]
        )
        queryset.filter(survey_code__unique_code__in=hide_codes).update(is_hide=True)
        queryset.filter(survey_code__unique_code__in=show_codes).update(is_hide=False)
        return JsonResponse({"status": True})


class SurveyDownloadView(View):

    """
        1、将唯一码写入文件
        2、下载`xls`文件
    """
    queryset = models.SurveyCode.objects.all()

    file_name = "唯一码.xls"

    def get(self, *args, **kwargs):
        _ = args[0]
        queryset = self.queryset.filter(survey_id=kwargs.get("pk"))

        xls = xlwt.Workbook(encoding="utf-8", style_compression=2)
        sheet = xls.add_sheet("唯一码", cell_overwrite_ok=True)

        for index, code in enumerate(queryset.iterator(), ):
            sheet.write(index, 0, code.unique_code)

        xls.save(self.file_name)

        file_path = os.path.join(settings.BASE_DIR, self.file_name)

        def iter_file(path, size=1024):

            with open(path, "rb", ) as f:
                for data in iter(lambda: f.read(size), b''):
                    yield data

        response = StreamingHttpResponse(iter_file(file_path))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment; {}'.format(
            "filename*=utf-8''{}".format(quote(self.file_name))
        )

        return response
