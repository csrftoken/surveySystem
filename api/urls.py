#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2018/12/6

from django.urls import path

from .views import curd


urlpatterns = [
    path("surveys/", curd.SurveyApi.as_view()),
]
