from django.shortcuts import render, redirect, reverse
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic import View, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

# from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
import markdown
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model

from .forms import UserProfileForm
from article.models import UserProfile, Article, Tag, Comment, Subcomment

User = get_user_model()


class CustomBackend(ModelBackend):
    """
    邮箱用户名同时登陆
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except Exception as e:
            return None


class IndexView(ListView):
    queryset = Article.objects.order_by("-post_time").all()[:5]
    context_object_name = "articles"
    template_name = "article/index.html"


class AllArticleView(ListView):
    queryset = Article.objects.order_by('-post_time').all()
    paginate_by = 5
    context_object_name = "articles"
    template_name = "article/all_articles.html"



class TagArticlesView(ListView):
    template_name = "article/tag_articles.html"
    paginate_by = 5
    context_object_name = "articles"

    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs.get("tag_slug"))
        return tag.articles.order_by('-post_time').all()


class AllTagsView(ListView):
    context_object_name = "all_tags"
    template_name = "article/all_tags.html"
    model = Tag
    ordering = "slug"


class UserProfileView(DetailView):
    model = User
    template_name = "article/profile.html"
    context_object_name = "c_user"


def visits_handler(request, article):
    last_view = request.session.get('article_{0}_last_view'.format(article.id))  # 获取最后一次浏览本站的时间last_view
    if last_view:
        last_visit_time = datetime.strptime(last_view[:-7], "%Y-%m-%d %H:%M:%S")
        if datetime.now() >= last_visit_time + timedelta(minutes=5):  # 判断如果最后一次访问网站的时间大于20分钟，则浏览量+1
            article.views += 1
            article.save()
            last_visit_time = datetime.now()
        else:
            last_visit_time = last_view
    else:
        article.views += 1
        article.save()
        last_visit_time = datetime.now()
    request.session['article_{0}_last_view'.format(article.id)] = str(last_visit_time)  # 更新session



class ArticleDetailView(DetailView):
    template_name = "article/article_detail.html"
    context_object_name = "article"
    model = Article

    def get(self, request, *args, **kwargs):
        res=super(ArticleDetailView,self).get(request, *args, **kwargs)
        visits_handler(request, self.object)
        return res

    def get_object(self, queryset=None):
        article=super(ArticleDetailView,self).get_object(queryset=None)
        md = markdown.Markdown(extensions=[
                    'markdown.extensions.extra',
                    'markdown.extensions.codehilite',
                    TocExtension(slugify=slugify),
                ])
        article.content = md.convert(article.content)
        article.toc=md.toc
        return article

    def get_context_data(self, **kwargs):
        context_data=super(ArticleDetailView,self).get_context_data(**kwargs)
        comments = self.object.comments.order_by('post_time').all()
        context_data.update(
            {
                "comments":comments
            }
        )
        return context_data

class CommentView(LoginRequiredMixin, View):
    def post(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        author = request.user
        content = request.POST.get('content')
        c = Comment.objects.create(article=article, author=author, content=content)
        # 评论成功后刷新即可
        return redirect(reverse('article:article_detail', args=[article_id, ])+"#comment_%s"%c.id)


class SubCommentView(LoginRequiredMixin, View):
    def post(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        author = request.user
        content = request.POST.get('content')
        reply_to_id = request.POST.get('reply_to_id')
        parent_comment_id = request.POST.get('parent_comment_id')
        reply_to = get_object_or_404(User, id=reply_to_id)
        parent_comment = get_object_or_404(Comment, id=parent_comment_id)
        c = Subcomment.objects.create(article=article, author=author, content=content, reply_to=reply_to,
                                      parent_comment=parent_comment)
        # 评论成功后刷新即可
        return redirect(reverse('article:article_detail', args=[article_id, ])+"#subcomment_%s"%c.id)


class UserProfileEditView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        user_profile = get_object_or_404(UserProfile, id=user.id)
        form = UserProfileForm(instance=user_profile)
        return render(request, 'article/profile_edit.html', {'form': form})

    def post(self, request):
        user = request.user
        user_profile = get_object_or_404(UserProfile, id=user.id)
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('profile', args=[user.id, ]))
        else:
            return render(request, 'article/profile_edit.html', {'form': form})



