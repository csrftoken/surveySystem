#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2018/12/6

from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.shortcuts import redirect

from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from web import models

from ..serializers import curd
from ..service.response import CustomResponse


class LoginApi(generics.CreateAPIView):

    def create(self, request, *args, **kwargs):
        username = self.request.data.get('username')
        password = self.request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return CustomResponse(errcode=True)
        else:
            return CustomResponse(errcode=False, data="用户名或密码错误")


class SurveyApi(generics.ListAPIView):
    queryset = models.MiddleSurvey.objects.all()
    serializer_class = curd.SurveySerializer

    filter_backends = (SearchFilter, OrderingFilter, )
    search_fields = ("name",)

    fields = [
        {
            'prop': 'name',
            'label': '问卷名称',
        },
        {
            'prop': 'by_class',
            'label': '班级',
        },
        {
            'prop': 'number',
            'label': '填写人数',
        },
        {
            'prop': 'link',
            'label': '填写链接'
        },
        {
            'prop': 'date',
            'label': '创建日期'
        },
        {
            'prop': 'handle',
            'label': '操作'
        }
    ]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_data = self.paginator.get_paginated_data(serializer.data)
            return Response({
                "fields": self.fields,
                "result": paginated_data,
                # "search_fields": self.search_fields
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "fields": self.fields,
            "result": serializer.data,
            # "search_fields": self.search_fields
        })


class SurveyDetailApi(generics.CreateAPIView, generics.RetrieveAPIView):

    queryset = models.MiddleSurvey.objects.all()
    pagination_class = None

    def get_serializer_class(self):
        if self.request.method == "POST":
            # return curd.SurveyRecordSerializer
            return curd.MiddleSurveyCreateSerializer
        else:
            return curd.MiddleSurveySerializer

    def get_serializer_context(self):
        context = super(SurveyDetailApi, self).get_serializer_context()

        context["unique_code"] = self.request.data.get("unique_code")

        return context

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return CustomResponse(errcode=True)
        else:
            return CustomResponse(errcode=False, data=serializer.errors)
