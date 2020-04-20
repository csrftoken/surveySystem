#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2018/12/6

from django.urls import re_path
from django.urls import include
from django.contrib.auth.decorators import login_required

from .views import backend


survey_urlpatterns = [

    re_path('^$', login_required(backend.SurveyIndexView.as_view())),
    re_path('^login/$', backend.SurveyLoginView.as_view()),
    re_path(r'^(?P<pk>\d+)/report/$', login_required(backend.SurveyReportView.as_view()), name="survey-report"),
    re_path(r'^(?P<pk>\d+)/$', backend.SurveyDetailView.as_view(), name='survey-detail'),
    re_path(r'^(?P<pk>\d+)/download/$', login_required(backend.SurveyDownloadView.as_view()), name='survey-download'),
]


# 路由分发
urlpatterns = [
    re_path('^', include(survey_urlpatterns)),
]
