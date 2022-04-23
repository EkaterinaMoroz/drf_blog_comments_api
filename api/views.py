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

    def get_object(self):
        return get_object_or_404(Post, id=self.kwargs['pk'])


class CommentsView(generics.ListCreateAPIView):
    model = Comment
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_object = get_object_or_404(Post, id=self.kwargs['pk'])
        return post_object.get_comments()


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    model = Comment
    serializer_class = CommentSerializer

    def get_object(self):
        return get_object_or_404(Comment, id=self.kwargs['cid'])


class RepliesView(generics.ListCreateAPIView):
    model = Comment
    serializer_class = CommentSerializer


    def get_queryset(self):
        cid = self.kwargs['cid']
        comment = get_object_or_404(Comment, id=cid)
        level = comment.level
        if level == 0:
            return Comment.objects.filter(thread_id=cid, level__gt=level)
        else:
            parent_id = comment.parent_id.id
            return Comment.objects.filter(thread_id=parent_id, level__gt=level)

    def perform_create(self, serializer):
        parent = get_object_or_404(Comment, id=self.request.data.get('parent_id'))
        level = parent.level + 1
        return serializer.save(thread_id=self.kwargs['cid'], level=level)

