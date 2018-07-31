# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.contrib.auth.models import User
from django.db import models

from base.models import BaseModel


class Topic(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    topic = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)

    class Meta:
        ordering = ('-created',)
        unique_together = (('slug',),)


class Blog(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    creator = models.ForeignKey(User)
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    related_topics = models.ManyToManyField(Topic, related_name='related_topics')
    description = models.TextField()
    published_time = models.PositiveIntegerField()

    class Meta:
        ordering = ('-created',)
        unique_together = (('slug',),)
