#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2018/12/6

from django.urls import path

from .views import basic


urlpatterns = [
    path("login/", basic.LoginApi.as_view()),
    path("surveys/", basic.SurveyApi.as_view()),
    path("surveys/<int:pk>/", basic.SurveyDetailApi.as_view()),
]
