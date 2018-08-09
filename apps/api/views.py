from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin
from article.models import Tag, Comment, Article, Subcomment, UserProfile
from .serializers import TagListSerializer, TagDetailSerializer, ArticleListSerializer, ArticleDetailSerializer, \
    CommentListSerializer, SubCommentListSerializer, CommentCreateSerializer, SubCommentCreateSerializer, \
    UserProfileSerializer, UserUpdateSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework import permissions


class UserProfileViewSet_v1(GenericViewSet, ListModelMixin, RetrieveModelMixin, UpdateModelMixin):
    """
    list:
        全部用户列表
    retrieve:
        单个用户信息
    partial_update:
        更新用户资料
    update:
        更新用户资料
    """
    queryset = UserProfile.objects.order_by("-id").all()
    permission_classes = (IsOwnerOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserProfileSerializer


class TagViewSet_v1(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """
    标签
    list:
        所有标签
    read:
        标签详情
    """
    queryset = Tag.objects.order_by("name").all()

    def get_serializer_class(self):
        if self.action == "list":
            return TagListSerializer
        return TagDetailSerializer


class ArticleViewSet_v1(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """
        文章
        list:
            所有文章
        read:
            文章详情
        """
    queryset = Article.objects.order_by('-post_time').all()

    def get_serializer_class(self):
        if self.action == "list":
            return ArticleListSerializer
        return ArticleDetailSerializer


class CommentViewSet_v1(GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin):
    """
        一级评论
        list:
            所有一级评论
        read:
            一级评论内容
        create:
            发表一级评论
    """
    queryset = Comment.objects.order_by('post_time').all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action == 'create':
            return CommentCreateSerializer
        return CommentListSerializer


class SubCommentViewSet_v1(GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin):
    """
    二级评论
    list:
         所有二级评论
    read:
        二级评论内容
    create:
        回复一级评论
    """
    queryset = Subcomment.objects.order_by('post_time').all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action == 'create':
            return SubCommentCreateSerializer
        return SubCommentListSerializer
