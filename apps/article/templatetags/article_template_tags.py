#!/usr/bin/env python
#-*- coding: utf-8 -*-
from ..models import Article,Tag
from django import forms, template
import random
register=template.Library()

msg=['primary','info','success','danger','dark','warning']

@register.inclusion_tag('article/partials/_sidebar.html')
def get_sidebar_tag():
    all_tags=Tag.objects.order_by('slug').all()
    for tag in all_tags:
        tag.cls_msg=random.choice(msg)

    latest_articles=Article.objects.order_by('-post_time').all()[:5]
    return {'tags_cloud':all_tags,'latest_articles':latest_articles}

@register.inclusion_tag('article/partials/_navbar.html')
def get_navbar_tag():
    return {}


@register.filter
def is_checkbox(field):
    return isinstance(field.field.widget, forms.CheckboxInput)


@register.filter
def input_class(field):
    """
    Returns widgets class name in lowercase
    """
    return field.field.widget.__class__.__name__.lower()
