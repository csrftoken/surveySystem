#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2018/12/20

from rest_framework.response import Response


class CustomResponse(Response):

    def __init__(self, errcode=True, data=None, status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None):

        data = {
            "errcode": errcode,
            "data": data
        }

        super(CustomResponse, self).__init__(data, status, template_name, headers, exception, content_type)
