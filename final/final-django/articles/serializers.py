from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth import get_user_model


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


# 상위 댓글 조회
class SuperCommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = ('super_comment',)

# 댓글 생성 및 수정
class CommentSerializer(serializers.ModelSerializer):

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('pk', 'username',)

    write_comment_user = UserSerializer(read_only=True)
    super_comment = SuperCommentSerializer(read_only=True)

    class Meta:
        model = Comment
        # 댓글 번호, 댓글 작성자 번호, 이름, 댓글 내용, 댓글이 작성된 리뷰글 번호, 상위 댓글 번호
        fields = ('pk', 'write_comment_user', 'content', 'commented_review', 'super_comment',)
        read_only_fields = ('commented_review', )


# 대댓글까지 조회하기 위한 중간 Serializer
class NewSuperCommentSerializer(serializers.ModelSerializer):
    commented = serializers.SerializerMethodField()
    write_comment_user_name = serializers.CharField(source='write_comment_user.username', read_only=True)

    class Meta:
        model = Comment
        # 댓글 번호, 댓글 작성자 이름, 댓글의 좋아요 수, 상위 댓글 번호, 댓글 내용, 작성 시간, 대댓글 정보(댓글 정보와 동일)
        fields = ('id', 'write_comment_user_name', 'like_comment_users', 'commented_review', 'super_comment', 'content', 'created_at', 'commented', 'updated_at')
        read_only_fields = ['write_comment_user_name']

    def get_commented(self, instance):
        serializer = self.__class__(instance.commented, many=True)
        serializer.bind('', self)
        return serializer.data



# 댓글 조회(대댓글 포함)
class ReviewOnlySerializer(serializers.ModelSerializer):

    reply_comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        # 게시글 번호, 댓글 정보 목록
        fields = ('id', 'reply_comments', )

    def get_reply_comments(self, obj):
        reply_comments = obj.review_comment.filter(super_comment=None)
        serializer = NewSuperCommentSerializer(reply_comments, many=True)
        return serializer.data


# 댓글별 좋아요 수 출력
class CommentLikeSerializer(serializers.ModelSerializer):
    like_comment_users_count = serializers.IntegerField()

    class Meta:
        model = Comment
        # 댓글 id, 댓글의 좋아요 개수, 댓글 내용
        fields = ('id', 'like_comment_users_count', 'content')
        
        
        
        
class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    likes = UserSerializer(read_only=True, many=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'user', 'image', 'content', 'created_at','updated_at', 'comments','likes']

    def get_comments(self, obj):
        comments = obj.review_comment.filter(super_comment=None)
        serializer = NewSuperCommentSerializer(comments, many=True)
        return serializer.data