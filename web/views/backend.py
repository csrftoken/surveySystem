#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2018/12/6

from django.views.generic import TemplateView


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
