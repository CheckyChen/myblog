from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from blog import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# 测试
def hello(request):
    return HttpResponse("hello word!")


# 首页
def index(request):
    # 查询所有的文章分类
    allcategory = models.Category.objects.all()

    # 幻灯片 并进行切片
    banner = models.Banner.objects.filter(is_active=True)[0:4]

    # 推荐位
    tui = models.Article.objects.filter(tui__id=1)[:3]

    # 文章列表
    allarticle = models.Article.objects.all().order_by("-id")[:10]

    # 获取推荐文章,根据点击量推荐前10片文章
    hot = models.Article.objects.all().order_by("views")[:10]

    # 热门文章 以推荐位为2
    remen = models.Article.objects.filter(tui__id=2)[:6]

    # 标签
    tags = models.Tag.objects.all()
    print(tags)
    # 链接
    link = models.Link.objects.all()

    context = {
        "allcategory": allcategory,
        "banner": banner,
        "tui": tui,
        "allarticle": allarticle,
        "hot": hot,
        "remen": remen,
        "tags": tags,
        "link": link,
    }
    return render(request, "index.html", context)


# 列表
def list(request, lid):
    # 获取通过URL传进来的lid，然后筛选出对应文章
    list = models.Article.objects.filter(category_id=lid)

    # 获取当前文章的栏目名
    cname = models.Category.objects.get(id=lid)

    # 右侧的热门推荐
    remen = models.Article.objects.filter(tui__id=2)[:6]

    # 导航所有分类
    allcategory = models.Category.objects.all()

    # 右侧所有文章标签
    tags = models.Tag.objects.all()

    page = request.GET.get('page')  # 在URL中获取当前页面数
    paginator = Paginator(list, 5)  # 对查询到的数据对象list进行分页，设置超过5条数据就分页
    try:
        list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    # locals()的作用是返回一个包含当前作用域里面的所有变量和它们的值的字典
    return render(request, 'list.html', locals())


# 展示界面
def show(request,sid):
    # 查询指定ID的文章
    show = models.Article.objects.get(id=sid)

    # 导航上的分类
    allcategory = models.Category.objects.all()

    # 右侧所有标签
    tags = models.Tag.objects.all()

    # 右侧热门推荐
    remen = models.Article.objects.filter(tui__id=2)[:6]

    # 内容下面的您可能感兴趣的文章，随机推荐
    hot = models.Article.objects.all().order_by('?')[:10]
    previous_blog = models.Article.objects.filter(created_time__gt=show.created_time,category=show.category.id).first()
    netx_blog = models.Article.objects.filter(created_time__lt=show.created_time,category=show.category.id).last()
    show.views = show.views + 1
    show.save()
    return render(request, 'show.html', locals())


# 标签页
def tag(request, tag):
    list = models.Article.objects.filter(tags__name=tag)#通过文章标签进行查询文章
    remen = models.Article.objects.filter(tui__id=2)[:6]
    allcategory = models.Category.objects.all()
    tname = models.Tag.objects.get(name=tag)#获取当前搜索的标签名
    page = request.GET.get('page')
    tags = models.Tag.objects.all()
    paginator = Paginator(list, 5)
    try:
        list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return render(request, 'tags.html', locals())


# 搜索页
def search(request):

    # 获取搜索的关键词
    ss=request.GET.get('search')

    # 获取到搜索关键词通过标题进行匹配
    list = models.Article.objects.filter(title__icontains=ss)
    remen = models.Article.objects.filter(tui__id=2)[:6]
    allcategory = models.Category.objects.all()
    page = request.GET.get('page')
    tags = models.Tag.objects.all()
    paginator = Paginator(list, 10)
    try:
        list = paginator.page(page) # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1) # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages) # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return render(request, 'search.html', locals())


# 关于我们
def about(request):
    allcategory = models.Category.objects.all()
    return render(request, 'page.html',locals())
