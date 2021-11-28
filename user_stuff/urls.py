from django.urls import path
from . import views


urlpatterns = [
    path('', views.user_home, name='user_home_page'),
    path('post', views.post, name='post'),
    path('delete/<int:post_id>', views.delete_post, name='delete_post'),
    path('<str:username>/profile', views.user_profile, name='user_profile'),
    path('<str:username>/profile/see_more', views.user_profile_see_more, name='user_profile_see_more'),
    path('<int:post_id>/bxcF/react', views.love_post, name='love_post'),
    path('<int:post_id>/bxcf/react', views.love_post2, name='love_post2'),
    path('<int:post_id>/comment', views.comment_on_post, name='comment_on_post'),
    path('<int:comment_id>/del_cm', views.delete_comment, name='delete_comment'),
    path('<int:comment_id>/xfrC/lv_cm', views.love_comment, name='love_comment'),
    path('<int:comment_id>/xfrc/lv_cm', views.love_comment2, name='love_comment2'),
    path('<int:user_id>/bbxf/add', views.add_friend, name='add_friend'),
    path('<int:user_id>/bbbxf/cnc', views.cancel_request, name='cancel_request'),
    path('<int:user_id>/bbbxf/acc', views.accept_request, name='accept_request'),
    path('<int:user_id>/bbbxf/ccaunnn_acc', views.unfriend_user, name='unfriend_user'),
    path('userquery', views.search_users, name='search_users'),
    path('noti', views.notific, name='notific'),
    path('showAllofthemp/<int:post_id>', views.show_them, name='show_for_post'),
    path('showAllofthempP/<int:comment_id>', views.show_them2, name='show_for_comment'),
    path('pial', views.activeers, name='pial'),
    # path('user_details_view', views.user_details_view, name='user_details_view')
    path('edit/<int:type>/<str:username>', views.edit_user_profile_data, name = 'edit_user_profile_data')
]
