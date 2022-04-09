from django.contrib.auth.decorators import login_required
from django.shortcuts import render,Http404, redirect, HttpResponse
from django.contrib.auth import authenticate,login as user_login,logout as user_logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from newswebsite.models import *
from newswebsite.forms import *
# Create your views here.
# Index
def index(request):
    cates = Category.objects.all().order_by("-id") # category list
    print(Best.objects.filter(select_reason="todaynews"))
    todaynew_big = Best.objects.filter(select_reason="todaynews")[0].select_article # select a piece of news
    print(todaynew_big)
    todaynew = Best.objects.filter(select_reason="todaynews")[:3]
    todaynew_top3 = [i.select_article for i in todaynew]                          # select three news

    index_recommend = Best.objects.filter(select_reason="indexnews")[:4]
    index_recommendlist = [i.select_article for i in index_recommend]   # select four index recomendations

    editor_recommendtop3 = Best.objects.filter(select_reason="recomendnews")[:3]
    editor_recommendtop3list = [i.select_article for i in editor_recommendtop3] # select three index recomendations

    editor_recommend = Best.objects.filter(select_reason="recomendnews")[3:10]
    editor_recommendlist = [i.select_article for i in editor_recommend]     # select seven recomendations

    article_list = Article.objects.all().order_by("-publish_time") # select all news
    pagerobot = Paginator(article_list,5)                         # page divider
    page_num = request.GET.get("page",1)                            # current page
    try:
        article_list = pagerobot.page(page_num)                   # return current page
    except EmptyPage:
        article_list = pagerobot.page(pagerobot.num_pages)        # if not exist, the last page
    except PageNotAnInteger:
        article_list = pagerobot.page(1)                          # if not exist, page 1
    context={}
    context={
      "cates":cates,
      "todaynew_big":todaynew_big,
      "todaynew_top3":todaynew_top3,
      "index_recommendlist":index_recommendlist,
      "editor_recommendtop3list":editor_recommendtop3list,
      "editor_recommendlist":editor_recommendlist,
      "article_list":article_list
    }


    return render(request,'index.html',context=context)
# 分类和编辑推荐等
def category(request,cate_id):
    cates = Category.objects.all().order_by("-id") # Category list

    editor_recommendtop3 = Best.objects.filter(select_reason="recomendnews")[:3]
    editor_recommendtop3list = [i.select_article for i in editor_recommendtop3]

    editor_recommend = Best.objects.filter(select_reason="recomendnews")[3:10]
    editor_recommendlist = [i.select_article for i in editor_recommend]

    article_list = Article.objects.filter(category=int(cate_id)).order_by("-publish_time")
    print(article_list[0].category)
    pagerobot = Paginator(article_list,5)
    page_num = request.GET.get("page",1)
    try:
        article_list = pagerobot.page(page_num)
    except EmptyPage:
        article_list = pagerobot.page(pagerobot.num_pages)
    except PageNotAnInteger:
        article_list = pagerobot.page(1)

    context={}
    context={
      "cates":cates,
      "editor_recommendtop3list":editor_recommendtop3list,
      "editor_recommendlist":editor_recommendlist,
      "article_list":article_list
    }


    return render(request,'category.html',context=context)

# Detailed
def detail(request,article_id):
    cates = Category.objects.all().order_by("-id") # Category list

    editor_recommendtop3 = Best.objects.filter(select_reason="recomendnews")[:3]
    editor_recommendtop3list = [i.select_article for i in editor_recommendtop3]

    editor_recommend = Best.objects.filter(select_reason="recomendnews")[3:10]
    editor_recommendlist = [i.select_article for i in editor_recommend]

    article = Article.objects.get(id=article_id)

    comments = Comment.objects.filter(belong_article=article)
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            words = form.cleaned_data.get("comment")
            comment = Comment(belong_user=request.user,words=words,belong_article=Article.objects.get(id=article_id))
            comment.save()
            form = CommentForm()

    context ={}
    context ={
       "cates":cates,
       "editor_recommendtop3list":editor_recommendtop3list,
       "editor_recommendlist":editor_recommendlist,
       "article":article,
       "comments":comments,
       "form":form
    }

    return render(request,'detail.html',context=context)

# Login
def login(request):
    if request.method == 'GET':
        form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username,password=password)
            if user:
                user_login(request,user)
                return redirect(to='index')
            else:
                return HttpResponse('No user or error password!')

    context={}
    context['form'] = form

    return render(request,'login.html',context=context)
# Register
def register(request):
    if request.method == 'GET':
        form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
           username = form.cleaned_data.get("username")
           email = form.cleaned_data.get("email")
           password = form.cleaned_data.get("password")
           user = User(username=username,email=email)
           user.set_password(password)
           user.save()                                                         # Save
           userprofile = UserProfile(belong_to=user,avatar='avatar/avatar.png')
           userprofile.save()                                                  # Information
           return redirect(to='login')

    context={}
    context['form']=form

    return render(request,'register.html',context=context)
# User information
@login_required(login_url='login')              # to login page
def profile(request):
    if request.method == 'GET':
        form = EditForm(initial={'username':request.user.username,'email':request.user.email})
    if request.method == 'POST':
        form = EditForm(request.POST,request.FILES)

        if form.is_valid():
           user = request.user
           email = form.cleaned_data.get("email")
           password = form.cleaned_data.get("password")
           avatar = form.cleaned_data.get("avatar")
           user.email = email
           if avatar:
                user_profile = UserProfile.objects.get(belong_to=user)
                user_profile.avatar = avatar
                user_profile.save()             # replace the exist avatar
           user.set_password(password)
           user.save()
           return redirect(to='login')

    context={}
    context['form']=form

    return render(request,'profile.html',context=context)
# Logout
def logout(request):
    user_logout(request)

    return redirect(to='login')
