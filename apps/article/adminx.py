# _*_ coding: utf-8 _*_
__author__ = 'Huu'
__date__ = '2018/8/7 20:03'

import xadmin
from .models import Article,Tag,Comment,Subcomment

class ArticleAdmin(object):
    list_display=('title',)

class TagAdmin(object):
    list_display=('name','chinese_name')

class CommentAdmin(object):
    list_display=('content','article','author')

class SubcommentAdmin(object):
    list_display=('content','article','author','reply_to')

xadmin.site.register(Article,ArticleAdmin)
xadmin.site.register(Tag,TagAdmin)
xadmin.site.register(Comment,CommentAdmin)
xadmin.site.register(Subcomment,SubcommentAdmin)