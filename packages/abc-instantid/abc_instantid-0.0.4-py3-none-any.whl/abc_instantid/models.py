# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals

from django.db import models
from django.utils.crypto import get_random_string
from xyz_util.modelutils import JSONField


class Account(models.Model):
    class Meta:
        verbose_name_plural = verbose_name = "帐号"
        ordering = ('-create_time',)

    name = models.CharField("名称", max_length=64, unique=True)
    memo = models.CharField("备注", max_length=255, blank=True, default='')
    avatar = models.URLField("头像", max_length=255, blank=True, null=True)
    is_active = models.BooleanField("有效", blank=False, default=True)
    lora = models.OneToOneField("loratraining.lora", verbose_name="Lora", blank=True, null=True,
                                related_name='instantid_account', on_delete=models.PROTECT)
    update_time = models.DateTimeField("更新时间", auto_now=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True, db_index=True)

    def __str__(self):
        return self.name

    def gen_lora(self):
        from media.helper import owner_add_images
        from loratraining.models import Lora
        if not self.lora:
            name = get_random_string(8)
            lora = Lora.objects.create(
                name=name,
                memo=f'from instantid:{self.id}',
                cover=self.avatar
            )
            self.lora = lora
            self.save()
        for img in self.images.filter(is_active=True):
            owner_add_images(self.lora, img.url)
        from worktask.signals import to_create_task
        return to_create_task.send_robust(sender=Lora, owner=self.lora)


class Image(models.Model):
    class Meta:
        verbose_name_plural = verbose_name = "图片"
        ordering = ('-create_time',)

    account = models.ForeignKey(Account, verbose_name=Account._meta.verbose_name, on_delete=models.PROTECT,
                                related_name="images")
    url = models.URLField("网址", max_length=255, unique=True)
    is_active = models.BooleanField("有效", blank=False, default=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True, db_index=True)
    update_time = models.DateTimeField("更新时间", auto_now=True)

    def __str__(self):
        return '图%s' % self.id
