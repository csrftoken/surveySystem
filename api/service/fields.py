#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2018/12/8


from rest_framework import fields


class CustomCharField(fields.Field):

    def to_representation(self, value):
        return "{}第{}期".format(value.course, value.semester)

    def to_internal_value(self, data):
        return data
