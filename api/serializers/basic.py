#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2018/12/6

from django.urls import reverse
from django.template import loader
from django.db.models import Count
from django.db import transaction
from django.utils.timezone import now

from rest_framework import serializers

from web import models

from ..service.fields import ValueField


class SurveyChoicesSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SurveyChoices
        fields = (
            "content",
            "points",
        )


class SurveyItemSerializer(serializers.ModelSerializer):
    survey_item = serializers.CharField(source="pk")
    choices = SurveyChoicesSerializer(source="answers", many=True, required=False, allow_null=True)
    value = ValueField(
        source="answer_type",
        required=True,
        allow_null=False
    )
    error = serializers.CharField(default="")

    class Meta:
        model = models.SurveyItem
        fields = (
            "id",
            "name",
            "answer_type",
            "choices",
            "value",
            "survey_item",
            "error"
        )

    def to_representation(self, instance):
        data = super(SurveyItemSerializer, self).to_representation(instance)

        data["survey_template"] = self.context.get("survey_id")

        return data


class SurveyRecordSerializer(serializers.ModelSerializer):

    value = ValueField(
        required=False,
        error_messages={
            "required": "该项为必填项",
            "blank": "该项为必填项"
        }
    )

    class Meta:
        model = models.SurveyRecord
        fields = (
            "survey_template",
            "survey_item",
            "value",
        )

    def validate(self, data):

        survey_item = data.get("survey_item")
        value = data.pop("value")
        if survey_item.answer_type == "single":
            data["choices"] = survey_item.answers.filter(points=value)
        elif survey_item.answer_type == "multiple":
            data["choices"] = survey_item.answers.filter(
                points__in=value
            )
        else:
            data["suggestion"] = value

        data["survey_code"] = self.context.get("unique_code")
        data["survey_id"] = self.context["view"].kwargs.get("pk")

        return data


class SurveyDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Survey
        fields = (
            "id",
            "name",
        )

    def to_representation(self, instance):

        data = super(SurveyDetailSerializer, self).to_representation(instance)

        self.context["survey_id"] = data["id"]
        data["questions"] = SurveyItemSerializer(
            instance.questions.all(), many=True, context=self.context
        ).data

        return data


class SurveyTemplateCreateSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    questions = SurveyRecordSerializer(many=True)

    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        return instance


class SurveyCreateSerializer(serializers.Serializer):

    unique_code = serializers.CharField(
        error_messages={
            "required": "唯一码不可为空", "null": "唯一码不可为空", "blank": "唯一码不可为空"
        }
    )
    surveys = serializers.ListSerializer(child=SurveyTemplateCreateSerializer())

    def validate_unique_code(self, value):

        codes = models.SurveyCode.objects.filter(unique_code=value)
        if not codes.exists():
            raise serializers.ValidationError("无效的唯一码")

        if models.SurveyRecord.objects.filter(survey_code__unique_code=value).exists():
            raise serializers.ValidationError("唯一码已使用")

        self.context["unique_code"] = codes.first()

        return self.context["unique_code"]

    @transaction.atomic
    def create(self, validated_data):

        # 创建数据
        for item in validated_data.get("surveys", []):

            survey_records = []

            for question in item.get("questions", []):
                choices = question.pop("choices", [])
                record = models.SurveyRecord.objects.create(**question)
                record.choices.set(choices)

            models.SurveyRecord.objects.bulk_create(survey_records)

        # 修改唯一状态
        unique_code = validated_data.get("unique_code")
        unique_code.used = True
        unique_code.used_time = now()
        unique_code.save(update_fields=("used", "used_time", ))

        return {}

    def update(self, instance, validated_data):
        return instance


class SurveySerializer(serializers.ModelSerializer):
    by_class = serializers.CharField(source="by_class.course")
    link = serializers.SerializerMethodField()
    handle = serializers.SerializerMethodField()

    surveys = SurveyDetailSerializer(many=True)

    HANDLE_TEMPLATE = "components/handle.html"

    class Meta:
        model = models.Survey
        fields = (
            "name",
            "by_class",
            "number",
            "link",
            "handle",
            "date",
            "surveys",
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

        data["number"] = instance.surveyrecord_set.values("survey_code").annotate(
            count=Count("survey_code")
        ).count()

        return data
