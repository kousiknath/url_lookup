# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Host(models.Model):
    """
    Contains host specific information.
    """
    host_name = models.TextField(default='', blank=False, null=False, unique=True)
    is_host_blacklisted = models.BooleanField(default=False)


class URLMeta(models.Model):
    host = models.ForeignKey(Host, null=False, blank=False)
    port = models.CharField(max_length=10, null=True, blank=True)
    path = models.TextField(default='', blank=True)
    is_url_blacklisted = models.BooleanField(default=False)
    hash = models.CharField(max_length=100, db_index=True)
