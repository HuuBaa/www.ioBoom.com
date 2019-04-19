#!/usr/bin/env python
#-*- coding: utf-8 -*-

from django.urls import path, include, re_path
from .views import AllArticleView,ArticleDetailView,CommentView,SubCommentView,TagArticlesView,AllTagsView

app_name='article'

urlpatterns=[
    path('all/',AllArticleView.as_view(),name='all_articles'),
    path('<int:pk>/',ArticleDetailView.as_view(),name='article_detail'),
    path('comment/<int:article_id>)/',CommentView.as_view(),name='article_comment'),
    path('subcomment/<int:article_id>/',SubCommentView.as_view(),name='article_sub_comment'),
    path('tag/<slug:tag_slug>/',TagArticlesView.as_view(),name='tag_articles'),
    path('tags/',AllTagsView.as_view(),name='all_tags'),
]