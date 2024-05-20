from django.urls import path
from . import views

urlpatterns = [
    path('find_similar_actor/', views.find_similar_actor, name='find_similar_actor'),
    path('upload_post/', views.upload_post, name='upload_post'),
    path('posts/',  views.get_posts),
    path('my_posts/',  views.get_my_posts),
    path('posts/<int:post_id>/like/',  views.like_post),
    path('posts/<int:post_id>/comments/',  views.add_comment),
    path('users/<int:user_id}/follow/',  views.follow_user),
]