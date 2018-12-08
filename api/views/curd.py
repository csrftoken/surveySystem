#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2018/12/6

from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from web import models

from ..serializer import curd


class SurveyApi(generics.ListAPIView):
    queryset = models.Survey.objects.all()
    serializer_class = curd.SurveySerializer

    filter_backends = (SearchFilter,)
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
