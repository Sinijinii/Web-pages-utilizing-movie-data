from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


# 닮은꼴
class Actor(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='actors')

# 커뮤니티
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/', blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)
    like_review_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_reviews')


class Comment(models.Model):
    content = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 댓글 작성자
    write_comment_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='write_comment')
    # 상위 댓글
    super_comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name='commented', null=True, blank=True)
    # 댓글을 좋아요한 사용자
    like_comment_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_comments')
    # 댓글이 달린 게시물
    commented_review= models.ForeignKey(Post, on_delete=models.CASCADE, related_name='review_comment')
    
    