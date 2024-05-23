from django.urls import path
from . import views
app_name = 'articles'
urlpatterns = [
    ## 닮은 꼴
    path('find_similar_actor/', views.find_similar_actor, name='find_similar_actor'),
    
    ## 생성형AI
    path('ImageGenerator/', views.GenerateImageView, name='generate_image'),
    
    ## 게시글 CRUD
    path('create_post/', views.create_post, name='create_post'),
    path('get_posts/', views.get_posts, name='get_posts'),
    path('detail_post/<int:post_id>/',views.detail_post,name='detail_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('update_post/<int:post_id>/', views.update_post, name='update_post'),
    path('upload_result/',views.upload_result, name='upload_result'),
    path('my_posts/', views.my_posts, name='my_posts'),
    
    ## 댓글, 좋아요
    path('<int:review_pk>/comments/', views.comment_list_or_create), # 게시글 별 댓글 조회 및 최상위 댓글 생성
    path('<int:review_pk>/comments/<int:comment_pk>/', views.comment_update_or_delete), # 대댓글 생성 및 전체 댓글 수정 및 삭제
    path('<int:review_pk>/like/<int:comment_pk>/', views.comment_like),# 댓글 좋아요 등록 및 해제
    path('<int:review_pk>/like_count/<int:comment_pk>/', views.comment_like_count), # 댓글 별 좋아요 개수 조회
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    
    ## 프로필 페이지
    path('user_profile/<str:username>/', views.user_profile, name='user_profile'),
    path('upload_profile_image/', views.upload_profile_image, name='upload_profile_image'),
    path('user_liked_posts/', views.user_liked_posts, name='user_liked_posts'),
]