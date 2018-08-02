from django.conf.urls import url

from admin_app.views import *

urlpatterns = [
    url('^blog/$', BlogListView.as_view(), name='blog_list'),
    url('^blog/(?P<id>[a-zA-Z0-9-]{36})/$', BlogView.as_view(), name='blog_view'),
    url('^topic/$', TopicView.as_view(), name='topic_list'),
]
