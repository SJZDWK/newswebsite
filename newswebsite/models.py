from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


# 分类表
class Category(models.Model):
    name = models.CharField(max_length=40, null=False)  # category name

    def __str__(self):
        return self.name


# 文章表
class Article(models.Model):
    title = models.CharField(max_length=100, null=False)  # title
    intro = models.CharField(max_length=1000)  # introduction
    abstract = models.TextField()  # abstract
    category = models.ForeignKey(Category, related_name="cate")
    content = models.TextField(null=False)  # article
    publish_time = models.DateTimeField(null=False, default=now)  # time that published
    image = models.FileField(upload_to='article_image')  # image of article
    source_link = models.CharField(max_length=200)  # original website
    author_name = models.CharField(max_length=100, null=False)  # user name
    author_avatar = models.FileField(upload_to='author_avatar')  # user avatar
    author_desc = models.CharField(max_length=100, null=False)  # user describe

    def __str__(self):
        return self.title    # title


# 精选文章
class Best(models.Model):
    select_article = models.ForeignKey(Article, related_name='select_article')  # recommend article
    SELECT_REASON = (
        ('todaynews', 'todaynews'),
        ('indexnews', 'indexnews'),
        ('recomendnews', 'recomendnews')
    )
    select_reason = models.CharField(choices=SELECT_REASON, max_length=50, null=False)  # reason that recommendation

    def __str__(self):
        return self.select_reason + '-' + self.select_article.title


# 用户信息表
class UserProfile(models.Model):
    belong_to = models.OneToOneField(to=User, related_name="profile")  # user
    avatar = models.FileField(upload_to='avatar')  # user avatar

    def __str__(self):
        return self.belong_to.username


# 评论表
class Comment(models.Model):
    belong_article = models.ForeignKey(Article, related_name='article')  # recommendation articles
    belong_user = models.ForeignKey(User, related_name='user')  # recommendation author
    words = models.CharField(max_length=200, null=False)  # recommendations
    created = models.DateTimeField(null=False, default=now)  # recommendation time

    def __str__(self):
        return self.belong_user.username + ': ' + self.words
