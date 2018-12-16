#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2018/12/6

from django.urls import reverse
from django.template import loader

from rest_framework import serializers

from web import models

from ..service.fields import CustomCharField


class SurveySerializer(serializers.ModelSerializer):

    by_class = CustomCharField()
    link = serializers.SerializerMethodField()
    handle = serializers.SerializerMethodField()

    HANDLE_TEMPLATE = "components/handle.html"

    class Meta:
        model = models.Survey
        fields = (
            "name",
            "by_class",
            "link",
            "handle",
            "date",
        )

    def get_link(self, instance):
        request = self.context["request"]
        link = "{}://{}{}".format(
            request.scheme,
            request.get_host(),
            reverse('survey-detail', args=(instance.pk, ))
        )
        return "<a href='{link}'>{link}</a>".format(link=link)

    def get_handle(self, instance):
        """
        获取操作相关

            查看报告 编辑
        """
        handle_html = loader.render_to_string(
            self.HANDLE_TEMPLATE,
            context={
                "pk": instance.pk
            }
        )
        return handle_html

    def to_representation(self, instance):

        data = super(SurveySerializer, self).to_representation(instance)

        data["number"] = instance.surveyrecord_set.count()

        return data


class SurveyChoicesSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SurveyChoices
        fields = (
            "content",
            "points",
        )


class SurveyItemSerializer(serializers.ModelSerializer):

    choices = SurveyChoicesSerializer(source="answers", many=True)
    value = serializers.CharField(default="")

    class Meta:
        model = models.SurveyItem
        fields = (
            "id",
            "name",
            "answer_type",
            "choices",
            "value",
        )
