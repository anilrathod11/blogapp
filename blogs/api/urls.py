from django.urls import path,include
from blogs.api.views import (BlogAV,BlogDetailAV,CategoryAV,CategoryDetailAV,
                             AdminToAssignReviewer,ReviewerAV,CommentAV,author_blog_comment,UploadPicture,
                             get_active_blog,get_public_active_blog)
urlpatterns = [
    path("blog/list/",BlogAV.as_view(),name="Blog-list"),
    path("accounts/google/login/callback/blog/list/",BlogAV.as_view(),name="Blog-list"),
    path("blog/<int:pk>/",BlogDetailAV.as_view(),name="blog-detail"),
    path("category/list/",CategoryAV.as_view(),name="Category-list"),
    path("category/<int:pk>/",CategoryDetailAV.as_view(),name="Category-detail"),
    path("assign/blog/",AdminToAssignReviewer.as_view(),name="Assign-blog-review"),
    path("review/blog/",ReviewerAV.as_view(),name="blog-to-review"),
    path("blog/comment/list",CommentAV.as_view(),name="comment-on-blog"),
    path("comment/",CommentAV.as_view(),name="comment-on-blog"),
    path("blog/comments/<int:pk>/",author_blog_comment,name="author-blog-comment"),
    path("image/list/",UploadPicture.as_view(),name="Image-list"),   
    path("active/blog/list/",get_active_blog,name="Active Blog list"),
    path("public/active/blog/list/",get_public_active_blog,name="Public Active blog"),
]