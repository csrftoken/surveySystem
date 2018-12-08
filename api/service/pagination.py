#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Date: 2018/12/8

import re

from collections import OrderedDict

from rest_framework import pagination


class CustomLimitOffsetPagination(pagination.LimitOffsetPagination):

    max_limit = 100

    def get_paginated_data(self, data):
        return OrderedDict([
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ])

    def get_next_link(self):
        next_link = super().get_next_link()
        return self._get_link(next_link)

    def get_previous_link(self):
        previous_link = super().get_previous_link()
        return self._get_link(previous_link)

    def _get_link(self, link):
        if link is not None:
            host = self.request.get_host()
            res = re.search(r"(http|https)://{}".format(host), link)
            return link.replace(res.group() if res else "", "")
        else:
            return link
