#!/usr/bin/env python
#-*- coding: utf-8 -*-

from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    avatar = forms.ImageField(label='上传头像', required=False, widget=forms.FileInput(attrs={'class': 'form-control'}),help_text="请上传头像")
    age = forms.IntegerField(label='年龄',required=False,widget=forms.TextInput(attrs={'class':'form-control'}),help_text="年龄",error_messages={
        "min_value":"你这年龄不合适吧",
        "max_value":"你这年龄不合适吧"
    },min_value=0,max_value=200)
    website = forms.URLField(label='个人网站',required=False,widget=forms.URLInput(attrs={'class':'form-control'}),help_text="个人网站")
    hometown = forms.CharField(label='家乡',max_length=64, required=False,widget=forms.TextInput(attrs={'class':'form-control'}),help_text="家乡")
    introduction = forms.CharField(label='个人简介',max_length=128, required=False,widget=forms.Textarea(attrs={'class':'form-control'}),help_text="个人简介")

    class Meta:
        model=UserProfile
        fields=('avatar','age','website','hometown','introduction')

