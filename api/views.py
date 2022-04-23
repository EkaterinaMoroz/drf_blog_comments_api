from rest_framework import generics
from rest_framework.generics import get_object_or_404

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer


class PostsView(generics.ListCreateAPIView):
    model = Post
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostsDetailView(generics.RetrieveUpdateDestroyAPIView):
    model = Post
    serializer_class = PostSerializer

    def get_queryset(self):
        return get_object_or_404(Post, id=self.kwargs['pk'])


class CommentsView(generics.ListCreateAPIView):
    model = Comment
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_object = get_object_or_404(Post, id=self.kwargs['pk'])
        return post_object.get_comments()

    def perform_create(self, serializer):
        parent = get_object_or_404(Comment, id=self.request.data.get('parent_id'))
        return serializer.save(thread_id=parent.thread_id, level=parent.level + 1)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    model = Comment
    serializer_class = CommentSerializer

    def get_object(self):
        return get_object_or_404(Comment, id=self.kwargs['id'])


class RepliesView(generics.ListCreateAPIView):
    model = Comment
    serializer_class = CommentSerializer

    def get_queryset(self):
        comment_object = get_object_or_404(Comment, id=self.kwargs['id'])
        return comment_object.get_replies()


class ReplyDetailView(generics.RetrieveUpdateDestroyAPIView):
    model = Comment
    serializer_class = CommentSerializer

    def get_object(self):
        return get_object_or_404(Comment, id=self.kwargs['id1'])
