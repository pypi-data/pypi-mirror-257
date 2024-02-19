# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class Config(AppConfig):
    name = 'abc_instantid'
    label = 'instantid'

    # def ready(self):
    #     from . import receivers