# -*- coding: utf-8 -*-
# Author Michał Dydecki <michal.dydecki@laboratorium.ee>

from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


def register(cls, admin_cls):
    cls.add_to_class('created_by',
                     models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Author'), null=True, blank=True))
    if admin_cls:
        admin_cls.add_extension_options('created_by')