from django.conf.urls import url

from log.views import *

urlpatterns = [
    url('', BlogView.as_view(), name='blog_list_view'),
    url('^blog/(?P<id>[a-zA-Z0-9-]{36})/(?P<title_slug>.+)/$', BlogView.as_view(), name='blog_detail_view'),
    url('^comment/(?P<blog_id>[a-zA-Z0-9-]{36})/$', CommentView.as_view(), name='comment_view'),
]
