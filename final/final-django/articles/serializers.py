from rest_framework import serializers
from .models import Post, Comment
from accounts.models import User, UserInfo
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

# 커스텀 사용자 모델 가져오기
User = get_user_model()

# 사용자 이미지 정보를 포함하기 위한 UserInfo
class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['id', 'user_image']

# UserInfo를 포함하는 사용자
class UserSerializer(serializers.ModelSerializer):
    userinfo = UserInfoSerializer(read_only=True)  # UserInfo 포함

    class Meta:
        model = User
        fields = ['id', 'username', 'userinfo']  # userinfo 필드를 포함

# 중첩 댓글을 처리하기 위한 SuperComment
class SuperCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('super_comment',)


# 댓글
class CommentSerializer(serializers.ModelSerializer):
    write_comment_user = UserSerializer(read_only=True)  # 사용자 이름과 이미지를 포함하기 위해 UserSerializer 사용
    super_comment = SuperCommentSerializer(read_only=True)  # 중첩 댓글을 포함하기 위해 SuperCommentSerializer 사용

    class Meta:
        model = Comment
        fields = ('pk', 'write_comment_user', 'content', 'commented_review', 'super_comment',)
        read_only_fields = ('commented_review', )

# 중첩 댓글을 포함한 댓글 , 사용자 정보와 이미지를 포함
class NewSuperCommentSerializer(serializers.ModelSerializer):
    commented = serializers.SerializerMethodField()  # 중첩 댓글을 가져오는 메소드
    write_comment_user = UserSerializer(read_only=True)  # 사용자 정보 포함

    class Meta:
        model = Comment
        fields = ('id', 'write_comment_user', 'like_comment_users', 'commented_review', 'super_comment', 'content', 'created_at', 'commented', 'updated_at')
        read_only_fields = ['write_comment_user']

    # 중첩 댓글을 가져오는 메소드
    def get_commented(self, instance):
        serializer = self.__class__(instance.commented, many=True)
        serializer.bind('', self)
        return serializer.data

# 리뷰에 대한 댓글을 가져오기
class ReviewOnlySerializer(serializers.ModelSerializer):
    reply_comments = serializers.SerializerMethodField()  # 리뷰에 대한 댓글을 가져오는 메소드

    class Meta:
        model = Post
        fields = ('id', 'reply_comments', )

    # 대댓글이 아닌 댓글을 가져오는 메소드
    def get_reply_comments(self, obj):
        reply_comments = obj.review_comment.filter(super_comment=None)
        serializer = NewSuperCommentSerializer(reply_comments, many=True)
        return serializer.data

# 댓글의 좋아요 수를 계산하여 포함
class CommentLikeSerializer(serializers.ModelSerializer):
    like_comment_users_count = serializers.IntegerField()  # 좋아요 수를 계산하는 필드

    class Meta:
        model = Comment
        fields = ('id', 'like_comment_users_count', 'content')

# 게시글
class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # 사용자 정보를 포함하기 위해 UserSerializer 사용
    user_info = serializers.PrimaryKeyRelatedField(read_only=True)  # user_info 필드를 추가
    likes = UserSerializer(read_only=True, many=True)  # 좋아요한 사용자 정보를 포함
    comments = serializers.SerializerMethodField()  # 댓글을 가져오는 메소드

    class Meta:
        model = Post
        fields = ['id', 'user', 'user_info', 'image', 'content', 'created_at', 'updated_at', 'comments', 'likes']

    # 게시글에 대한 댓글을 가져오는 메소드
    def get_comments(self, obj):
        comments = obj.review_comment.filter(super_comment=None)
        serializer = NewSuperCommentSerializer(comments, many=True)
        return serializer.data

    def create(self, validated_data):
        user = self.context['request'].user
        user_info = get_object_or_404(UserInfo, user=user)
        validated_data['user'] = user
        validated_data['user_info'] = user_info
        return super().create(validated_data)