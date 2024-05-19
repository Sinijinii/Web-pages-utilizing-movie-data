from django.urls import path
from . import views
app_name = 'articles'
urlpatterns = [
    path('find_similar_actor/', views.find_similar_actor, name='find_similar_actor'),
    path('create_post/', views.create_post, name='create_post'),
    path('get_posts/', views.get_posts, name='get_posts'),
    path('create_comment/', views.create_comment, name='create_comment'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('follow_user/<int:user_id>/', views.follow_user, name='follow_user'),
]