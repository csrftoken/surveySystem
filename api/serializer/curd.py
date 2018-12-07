#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2018/12/6

from rest_framework import serializers

from web import models


class SurveySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Survey
        fields = "__all__"
