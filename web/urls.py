#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2018/12/6

from django.urls import re_path
from django.urls import include

from .views import backend


survey_urlpatterns = [
    re_path('^$', backend.SurveyIndexView.as_view()),
    re_path('^(?P<pk>\d+)/$', backend.SurveyDetailView.as_view(), name='survey-detail'),

    re_path('^(?P<pk>\d+)/download/$', backend.SurveyDownloadView.as_view(), name='survey-download'),
]


# 路由分发
urlpatterns = [
    re_path('^surveys/', include(survey_urlpatterns)),
]
