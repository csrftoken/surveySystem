#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2018/12/13

from django.urls import path

from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import verify_jwt_token

urlpatterns = [

    path(r'api-token-auth/', obtain_jwt_token),

    path(r'protected-url/', verify_jwt_token),

    path('api-token-verify/', verify_jwt_token),

]
