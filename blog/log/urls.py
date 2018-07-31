from django.conf.urls import url

from log.views import *

urlpatterns = [
    url('^blog/$', BlogListView.as_view(), name='blog_list'),
    url('^blog/(?P<id>[a-zA-Z0-9-]{36})/$', BlogView.as_view(), name='blog_view'),
    url('^blog/(?P<id>[a-zA-Z0-9-]{36})/(?P<title_slug>.+)/$', BlogPublicView.as_view(),
        name='blog_public_view'),
    url('^topic/$', TopicView.as_view(), name='topic_list'),
]
