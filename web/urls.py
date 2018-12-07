#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2018/12/6

from django.urls import re_path

from .views import backend

urlpatterns = [
    re_path('^surveys/$', backend.SurveyIndexView.as_view()),
    re_path('^surveys/(?P<pk>\d+)/$', backend.SurveyDetailView.as_view())
]
