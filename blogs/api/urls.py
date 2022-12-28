from django.urls import path,include
from blogs.api.views import (BlogAV,BlogDetailAV,CategoryAV,CategoryDetailAV,AdminToAssignReviewer,ReviewerAV,CommentAV)
urlpatterns = [
    path("blog/list/",BlogAV.as_view(),name="Blog-list"),
    path("blog/<int:pk>/",BlogDetailAV.as_view(),name="blog-detail"),
    path("category/list/",CategoryAV.as_view(),name="Category-list"),
    path("blog/<int:pk>/",CategoryDetailAV.as_view(),name="Category-detail"),
    path("assign/blog/",AdminToAssignReviewer.as_view(),name="Assign-blog-review"),
    path("review/blog/",ReviewerAV.as_view(),name="blog-to-review"),
    path("blog/comment/list",CommentAV.as_view(),name="comment-on-blog"),
    
]