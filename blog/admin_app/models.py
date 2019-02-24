# -*- coding: utf-8 -*-


import uuid

from django.contrib.auth.models import User
from django.db import models

from base.models import BaseModel


class Topic(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    topic = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)
        unique_together = (('slug',),)


class Blog(BaseModel):
    STATUS = (
        (0, 'EDIT'),
        (1, 'PUBLISHED'),
        (2, 'DELETED')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    creator = models.ForeignKey(User, related_name='blog_author')
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    related_topics = models.ManyToManyField(Topic, related_name='related_topics')
    description = models.TextField()
    published_time = models.PositiveIntegerField(null=True)
    status = models.PositiveIntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ('-created',)
        unique_together = (('slug',),)


class Comment(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    blog = models.ForeignKey(Blog, null=True, blank=True, related_name='parent_blog')
    commented_by = models.ForeignKey(User, related_name='commented_by')
    description = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name='reply')

    class Meta:
        ordering = ('created',)
