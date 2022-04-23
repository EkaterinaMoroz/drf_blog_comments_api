from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, blank=True, default='')
    body = models.TextField(blank=True, default='')
    author = models.ForeignKey(User, null=True, related_name='posts', on_delete=models.CASCADE)

    class Meta:
        ordering = ('created',)

    def get_comments(self):
        """Получение всех комментариев к статье до 3 уровня вложенности"""
        return self.comments.filter(level__lt=4)


class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    body = models.TextField(blank=False)
    author = models.ForeignKey(User, null=True, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)
    parent_id = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    thread_id = models.IntegerField(default=0, db_index=True)
    level = models.SmallIntegerField(default=0)

    class Meta:
        ordering = ('created',)

    def get_replies(self):
        """Получение всех ответов на комментарий"""
        return Comment.objects.filter(thread_id=self.thread_id, parent_id__gt=self.pk)
