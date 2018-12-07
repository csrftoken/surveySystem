#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2018/12/6

from rest_framework import generics
from rest_framework.response import Response

from web import models

from ..serializer import curd


class SurveyApi(generics.ListAPIView):
    queryset = models.Survey.objects.all()
    serializer_class = curd.SurveySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_data = self.paginator.get_paginated_data(serializer.data)
            return Response({
                # "fields": self.fields,
                "result": paginated_data,
                # "search_fields": self.search_fields
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            # "fields": self.fields,
            "result": serializer.data,
            # "search_fields": self.search_fields
        })
