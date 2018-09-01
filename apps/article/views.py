from django.shortcuts import render, redirect, reverse
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic import View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
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


class IndexView(View):
    def get(self, request):
        articles = Article.objects.order_by("-post_time").all()
        return render(request, 'article/index.html', {'articles': articles})


class AllArticleView(View):
    def get(self, request):
        all_articles_list = Article.objects.order_by('-post_time').all()
        current_page = request.GET.get('page', 1)
        paginator = Paginator(all_articles_list, 5, request=request)
        try:
            all_articles_page = paginator.page(current_page)
        except PageNotAnInteger:
            all_articles_page = paginator.page(1)
        res_dict = {
            'articles': all_articles_page.object_list,
            'page': all_articles_page,
        }
        return render(request, 'article/all_articles.html', res_dict)


class TagArticlesView(View):
    def get(self, request, tag_slug):
        tag = get_object_or_404(Tag, slug=tag_slug)
        if tag is not None:
            tag_articles_list = tag.articles.order_by('-post_time').all()
            current_page = request.GET.get('page', 1)
            paginator = Paginator(tag_articles_list, 5, request=request)
            try:
                tag_articles_page = paginator.page(current_page)
            except PageNotAnInteger:
                tag_articles_page = paginator.page(1)
            con_dict = {
                'tag': tag,
                'articles': tag_articles_page.object_list,
                'page': tag_articles_page
            }
            return render(request, 'article/tag_articles.html', con_dict)


class AllTagsView(ListView):
    context_object_name = "all_tags"
    template_name = "article/all_tags.html"
    model = Tag
    ordering = "slug"


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


class ArticleDetailView(View):
    def get(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        visits_handler(request, article)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])
        article.content = md.convert(article.content)
        comments = article.comments.order_by('post_time').all()
        con_dict = {
            'article': article,
            'comments': comments,
            'toc': md.toc
        }
        return render(request, 'article/article_detail.html', con_dict)


class CommentView(LoginRequiredMixin, View):
    def post(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        author = request.user
        content = request.POST.get('content')
        c = Comment.objects.create(article=article, author=author, content=content)
        # 评论成功后刷新即可
        return redirect(reverse('article:article_detail', args=[article_id, ]))


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
        return redirect(reverse('article:article_detail', args=[article_id, ]))


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


class UserProfileView(View):
    def get(self, request, user_id):
        user_profile = get_object_or_404(User, id=user_id)
        return render(request, 'article/profile.html', {
            'c_user': user_profile,
            'userprofile': user_profile
        })
