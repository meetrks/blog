from django.db.models import Q
from rest_framework import status, serializers
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from admin_app.models import Blog, Comment
from admin_app.serializers import BlogSerializer
from base.utils import pagination
from log.serializers import CommentSerializer


class CommentView(ListAPIView, CreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = CommentSerializer

    def get(self, request, blog_id):
        try:
            blog = Blog.objects.get(pk=blog_id, status=1)
            queryset = Comment.objects.filter(blog=blog, parent=None)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"detail": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, blog_id):
        try:
            data = request.data
            Blog.objects.get(pk=blog_id, status=1)
            data['blog'] = blog_id
            serializer = self.get_serializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Blog.DoesNotExist:
            return Response({"detail": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"detail": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, blog_id):
        try:
            Blog.objects.get(pk=blog_id, status=1)
            data = request.data
            id = data.get('id')
            if not id:
                return Response({"detail": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
            instance = Comment.objects.get(pk=id, commented_by=request.user)
            serializer = self.get_serializer(instance, data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Blog.DoesNotExist:
            return Response({"detail": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
        except Comment.DoesNotExist:
            return Response({"detail": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"detail": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)


class BlogView(ListAPIView):
    serializer_class = BlogSerializer

    def get_filters(self):
        filters = {}
        query_params = self.request.query_params
        reported_date_from = query_params.get('reported_date_from')
        reported_date_to = query_params.get('reported_date_to')
        if reported_date_from and reported_date_to:
            reported_date_to = int(reported_date_to) + 86400
            filters.update({"published_time__range": [reported_date_from, reported_date_to]})
        topic = query_params.get('topic')
        if topic:
            filters.update({"related_topics": topic})
        self.q = query_params.get('q')
        self.page_size = query_params.get('page_size', 10)
        return filters

    def get(self, request, id=None, title_slug=None):
        if id and title_slug:
            try:
                query = Blog.objects.get(pk=id, slug=title_slug, status=1)
            except Blog.DoesNotExist:
                return Response({"detail": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
            serializer = self.get_serializer(query)
            return Response(serializer.data, status=status.HTTP_200_OK)
        try:
            queryset = Blog.objects.filter(status=1, **self.get_filters())
            if self.q:
                queryset = queryset.filter(Q(title__icontains=self.q) | Q(description__icontains=self.q) |
                                           Q(related_topics__topic__icontains=self.q)).distinct()
            paginator, result = pagination(queryset, request, page_size=self.page_size)
            serializer = self.get_serializer(result, many=True)
            response_data = serializer.data
            return paginator.get_paginated_response(response_data)
        except Exception as e:
            print(e)
            return Response({"detail": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
