# _*_ coding: utf-8 _*_
__author__ = 'Huu'
__date__ = '2018/8/8 9:33'
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100