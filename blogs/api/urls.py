from django.urls import path,include
from blogs.api.views import (BlogAV,BlogDetailAV,CategoryAV,CategoryDetailAV)
urlpatterns = [
    path("blog/list/",BlogAV.as_view(),name="Blog-list"),
    path("blog/<int:pk>/",BlogDetailAV.as_view(),name="blog-detail"),
    path("category/list/",CategoryAV.as_view(),name="Category-list"),
    path("blog/<int:pk>/",CategoryDetailAV.as_view(),name="Category-detail"),
]