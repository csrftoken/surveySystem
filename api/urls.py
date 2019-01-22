#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2018/12/6

from django.urls import path
from django.urls import re_path

from .views import curd


urlpatterns = [
    path("login/", curd.LoginApi.as_view()),
    path("surveys/", curd.SurveyApi.as_view()),
    re_path("surveys/(?P<pk>\d+)/", curd.SurveyDetailApi.as_view()),
]
