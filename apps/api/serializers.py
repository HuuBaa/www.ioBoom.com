 # _*_ coding: utf-8 _*_
__author__ = 'Huu'
__date__ = '2018/8/7 20:04'


from rest_framework import serializers
from article.models import Tag,Subcomment,Comment,Article,UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    """
    list,read
    """
    avatar_url=serializers.SerializerMethodField()
    articles = serializers.HyperlinkedRelatedField(view_name="articles_v1-detail", read_only=True, many=True)
    sub_comments = serializers.HyperlinkedIdentityField(view_name="subcomments_v1-detail", read_only=True, many=True)
    comments = serializers.HyperlinkedRelatedField(view_name="comments_v1-detail", read_only=True, many=True)
    class Meta:
        model=UserProfile
        fields=('id','username','avatar','age','website','hometown','introduction','avatar_url','articles','comments','sub_comments')
    def get_avatar_url(self,user):
        if user.socialaccount_set.count():
            return user.socialaccount_set.all()[0].get_avatar_url()
        return None

class UserUpdateSerializer(serializers.ModelSerializer):
    """
    更新、部分更新
    """
    class Meta:
        model=UserProfile
        fields=('avatar','age','website','hometown','introduction')

class AuthorSerializer(serializers.ModelSerializer):
    """
    文章作者序列化serializer
    """
    avatar_url=serializers.SerializerMethodField()
    class Meta:
        model=UserProfile
        fields=('id','username','avatar','avatar_url')

    def get_avatar_url(self,user):
        if user.socialaccount_set.count():
            return user.socialaccount_set.all()[0].get_avatar_url()
        return ""


class TagListSerializer(serializers.ModelSerializer):
    """
    标签list
    """
    class Meta:
        model=Tag
        fields="__all__"


class ArticleListSerializer(serializers.ModelSerializer):
    """
    文章list
    """
    #author=serializers.HyperlinkedRelatedField(view_name="users_v1-detail",read_only=True)
    author=AuthorSerializer()
    tags=TagListSerializer(many=True)
    comment_count=serializers.SerializerMethodField()
    class Meta:
        model = Article
        exclude = ("content",)

    #获取评论总数
    def get_comment_count(self,article):
        return article.get_comment_count()

class SubCommentListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    reply_to=AuthorSerializer()
    article = serializers.HyperlinkedRelatedField(view_name="articles_v1-detail", read_only=True)
    class Meta:
        model=Subcomment
        fields="__all__"

class CommentListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    sub_comments=SubCommentListSerializer(many=True)
    article = serializers.HyperlinkedRelatedField(view_name="articles_v1-detail", read_only=True)
    class Meta:
        model=Comment
        fields="__all__"


class TagDetailSerializer(serializers.ModelSerializer):
    """
    文章retrieve
    """
    articles=ArticleListSerializer(many=True)
    class Meta:
        model=Tag
        fields="__all__"


class ArticleDetailSerializer(serializers.ModelSerializer):
    """
    文章retrieve
    """
    author=AuthorSerializer()
    tags=TagListSerializer(many=True)
    comments=CommentListSerializer(many=True)
    class Meta:
        model = Article
        fields = "__all__"


class SubCommentCreateSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model=Subcomment
        exclude = ('post_time',)

class CommentCreateSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model=Comment
        exclude=('post_time',)


