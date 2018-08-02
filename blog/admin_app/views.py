import time

from django.utils.text import slugify
from rest_framework import status, serializers
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from base.utils import pagination
from admin_app.models import Blog, Topic
from admin_app.serializers import BlogSerializer, TopicSerializer


class BlogListView(ListAPIView, CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BlogSerializer

    def get(self, request):
        queryset = Blog.objects.all()
        paginator, result = pagination(queryset, request)
        serializer = self.get_serializer(result, many=True)
        response_data = serializer.data
        return paginator.get_paginated_response(response_data)

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            data['slug'] = slugify(data['title'])
            data['published_time'] = int(time.time())
            serializer = self.get_serializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print e
            return Response({"detail": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)


class BlogView(ListAPIView, UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BlogSerializer

    def get(self, request, id):
        if not id:
            return Response({"detail": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            queryset = Blog.objects.get(pk=id)
        except Blog.DoesNotExist:
            return Response({"detail": "Invalid id provided"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        if not id:
            return Response({"detail": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            data = request.data
            data['slug'] = slugify(data['title'])
            instance = Blog.objects.get(pk=id, creator=request.user)
            serializer = self.get_serializer(instance, data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Blog.DoesNotExist:
            return Response({"detail": "Invalid id provided"}, status=status.HTTP_400_BAD_REQUEST)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"detail": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)


class TopicView(ListAPIView, CreateAPIView, UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TopicSerializer

    def get(self, request):
        queryset = Topic.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            data['slug'] = slugify(data['topic'])
            serializer = self.get_serializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print e
            return Response({"detail": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            data = request.data
            id = data.get('id')
            if not id:
                return Response({"detail": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
            data['slug'] = slugify(data['topic'])
            instance = Topic.objects.get(pk=id)
            serializer = self.get_serializer(instance, data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Topic.DoesNotExist:
            return Response({"detail": "Invalid id provided"}, status=status.HTTP_400_BAD_REQUEST)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print e
            return Response({"detail": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
