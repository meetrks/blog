import time

from rest_framework import status, serializers
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from admin_app.models import Blog, Comment
from admin_app.serializers import BlogSerializer
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
            print e
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
            print e
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
            print e
            return Response({"detail": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)


class BlogView(ListAPIView):
    serializer_class = BlogSerializer

    def get(self, request, id=None, title_slug=None):
        if id and title_slug:
            try:
                query = Blog.objects.get(pk=id, slug=title_slug, status=1)
            except Blog.DoesNotExist:
                return Response({"detail": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
            serializer = self.get_serializer(query)
            return Response(serializer.data, status=status.HTTP_200_OK)
        try:
            queryset = Blog.objects.filter(status=1)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Blog.DoesNotExist:
            return Response({"detail": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
