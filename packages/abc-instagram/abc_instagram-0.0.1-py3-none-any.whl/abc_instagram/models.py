# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals

from django.db import models


class Account(models.Model):
    class Meta:
        verbose_name_plural = verbose_name = "帐号"
        ordering = ('-create_time',)

    name = models.CharField("名称", max_length=64, blank=True, default='', unique=True)
    memo = models.CharField("备注", max_length=255, blank=True, default='')
    avatar = models.URLField("头像", max_length=255, blank=True, null=True)
    is_active = models.BooleanField("有效", blank=False, default=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True, db_index=True)

    def __str__(self):
        return self.name


class Image(models.Model):
    class Meta:
        verbose_name_plural = verbose_name = "图片"
        ordering = ('-create_time',)

    account = models.ForeignKey(Account, verbose_name=Account._meta.verbose_name, on_delete=models.PROTECT,
                                related_name="images")
    url = models.URLField("网址", max_length=255, unique=True)
    post_time = models.DateTimeField("发布时间", blank=True, null=True)
    is_active = models.BooleanField("有效", blank=False, default=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True, db_index=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)

    def __str__(self):
        return '图%s' % self.id
