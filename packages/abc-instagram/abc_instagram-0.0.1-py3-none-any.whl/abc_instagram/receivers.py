# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from django.dispatch import receiver
from xyz_util.datautils import access
from worktask.signals import on_get_task_data, on_notify_task_owner
from . import models
import logging

log = logging.getLogger('django')


@receiver(on_get_task_data, sender=models.Account)
def account_task_context(sender, **kwargs):
    account = kwargs.get('instance')
    return dict(
        instagram=dict(
            name=account.name
        )
    )


@receiver(on_notify_task_owner, sender=models.Account)
def notify_account_task_result(sender, **kwargs):
    task = kwargs.get('instance')
    account = task.owner
    d = task.result.data
    fs = bool(access(d, 'images'))
    for url, post_time in fs.items():
        account.images.get_or_create(
            url=url,
            defaults=dict(
                post_time=post_time
            )
        )
    # if 'tickboom' in lora.data:
    #     helper.sync_news_to_tickboom(lora)


