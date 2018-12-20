#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2018/12/6

from django.utils.timezone import now

from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from web import models

from ..serializers import curd
from ..service.response import CustomResponse


class SurveyApi(generics.ListAPIView):
    queryset = models.Survey.objects.all()
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


class SurveyDetailApi(generics.ListCreateAPIView):

    queryset = models.SurveyItem.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return curd.SurveyRecordSerializer
        else:
            return curd.SurveyItemSerializer

    def get_serializer_context(self):
        context = super(SurveyDetailApi, self).get_serializer_context()

        context["unique_code"] = self.request.data.get("unique_code")

        return context

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(survey=kwargs.get("pk"))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        unique_code = request.data.get("unique_code")

        if not unique_code:
            return CustomResponse(errcode=False, data="唯一码不能为空")

        codes = models.SurveyCode.objects.filter(unique_code=unique_code, survey=kwargs.get("pk"))
        if not codes.exists():
            return CustomResponse(errcode=False, data="无效的唯一码")

        if models.SurveyRecord.objects.filter(survey_code__unique_code=unique_code).exists():
            return CustomResponse(errcode=False, data="唯一已使用")

        serializer = self.get_serializer(data=request.data.get("data"), many=True)
        if serializer.is_valid():
            self.perform_create(serializer)
            code = codes.first()
            code.used = True
            code.used_time = now()
            code.save(update_fields=("used", "used_time", ), )
            return CustomResponse(errcode=True, data={})
        else:
            return CustomResponse(errcode=False, data=serializer.errors)
