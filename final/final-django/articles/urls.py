from django.urls import path
from . import views
app_name = 'articles'
urlpatterns = [
    path('find_similar_actor/', views.find_similar_actor, name='find_similar_actor'),
    path('create_post/', views.create_post, name='create_post'),
    path('get_posts/', views.get_posts, name='get_posts'),
    path('create_comment/', views.create_comment, name='create_comment'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('following_posts/', views.following_posts, name='following_posts'),
    path('upload_result/',views.upload_result, name='upload_result'),
    path('my_posts/', views.my_posts, name='my_posts'),
    path('follow_user/<int:user_id>/', views.follow_user, name='follow_user'),
    path('ImageGenerator/', views.GenerateImageView, name='generate_image'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('update_post/<int:post_id>/', views.update_post, name='update_post'),
]