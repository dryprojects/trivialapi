# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
filename: zjj_xa_gov.py
usename: nico
date: 2022/1/15 23:44

MIT License

Copyright (c) 2022 nico

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from django.db import models

from .mixins import CreateModifyAtMixin


# 西安市二手房交易服务平台信息模型定义

class PreOwnedItem(CreateModifyAtMixin, models.Model):
    """二手房信息"""
    reference_monthly_repayment = models.FloatField(
        verbose_name='参考月供（¥）',
        null=True,
        blank=True
    )

    building_area = models.FloatField(
        verbose_name="建筑面积（m2）"
    )

    building_layout = models.CharField(
        verbose_name='户型,eg: 2-2-1',
        max_length=20
    )

    floor_level = models.CharField(
        verbose_name='楼层位置',
        max_length=20
    )

    age_of_building = models.DateField(
        verbose_name='建筑年代'
    )

    decoration_type = models.CharField(
        verbose_name='装修类型',
        max_length=20
    )

    building_orientation = models.CharField(
        verbose_name='朝向',
        max_length=20
    )

    building_structure = models.CharField(
        verbose_name='建筑结构',
        max_length=20
    )

    building_type = models.CharField(
        verbose_name='建筑类型',
        max_length=20
    )

    building_description = models.TextField(
        verbose_name='描述'
    )

    residential_quarter = models.CharField(
        verbose_name='小区',
        max_length=50
    )

    address = models.CharField(
        verbose_name="地址",
        max_length=255
    )

    affiliated_transportation = models.CharField(
        verbose_name='交通',
        max_length=255
    )

    affiliated_facilities = models.CharField(
        verbose_name='配套设施',
        max_length=255
    )

    published_at = models.DateTimeField(
        verbose_name='发布时间'
    )

    info_from = models.CharField(
        verbose_name='信息来源地址',
        max_length=255
    )

    check_code = models.CharField(
        verbose_name='房源校验码',
        max_length=50
    )

    related_sources = models.JSONField(
        default=[],
        verbose_name='小区其它在售房源'
    )
