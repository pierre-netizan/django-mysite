from django.shortcuts import render,get_object_or_404
from django.http import Http404, HttpRequest, HttpResponse
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.views.generic import ListView
from django.core.mail import send_mail
from django.views.decorators.http import require_POST


from .models import Post
from .forms import EmailPostForm,CommentForm

def post_share(request,post_id)->HttpResponse:
    # 通过id获取文章
    post=get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    sent=False
    
    if request.method=='POST':
        # 提交表单
        form=EmailPostForm(request.POST)
        if form.is_valid():#有一项没通过校验则报错，报错信息在form.errors中
            # 表单字段通过校验返回的是cleaned_data
            cd=form.cleaned_data
            print(f"{cd=}")
            #发送邮件
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = (
                f"{cd['name']} ({cd['email']}) "
                f"recommends you read {post.title}"
            )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}'s comments: {cd['comments']}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd['to']],
            )
            sent = True
    else:
        form=EmailPostForm()
    return render(
        request,
        'blog/post/share.html',
        {
            'post':post,
            'form':form,
            'sent':sent
        }
    )


class PostListView(ListView):
    """
    Alternative post list view
    """
    queryset=Post.published.all()
    context_object_name='posts'
    paginate_by=2
    template_name='blog/post/list.html'
    
    
    
def post_list(request:HttpRequest)->HttpResponse:
    post_list=Post.published.all()#全部数据
    # Pagination with 3 posts per page
    paginator=Paginator(post_list,2)#分页器对象
    page_number=request.GET.get('page',1)#request.GET类似于字典
    # posts=paginator.page(page_number)#一页数据
    print(page_number)
    
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        # 如果页面不是一个整数，返回第一页
        page = paginator.page(1)
    except EmptyPage:
        # 如果页面超出范围（例如9999），返回最后一页
        page = paginator.page(paginator.num_pages)
    
    # 计算自定义页码范围
    custom_page_range = get_custom_page_range(page, paginator.num_pages, 2)

    return render(
        request, 
        'blog/post/list.html', 
        {'page': page, 'custom_page_range': custom_page_range,'posts':page.object_list}#object_list是django固定的
    )

    # return render(
    #     request,
    #     'blog/post/list.html',
    #     {'posts':posts}
    # )


# def post_list(request):
#     object_list = Post.published.all()  # 或其他 QuerySet
#     paginator = Paginator(object_list, 5)  # 每页显示 5 篇文章
#     page_number = request.GET.get('page')

#     try:
#         page = paginator.page(page_number)
#     except PageNotAnInteger:
#         # 如果页面不是一个整数，返回第一页
#         page = paginator.page(1)
#     except EmptyPage:
#         # 如果页面超出范围（例如9999），返回最后一页
#         page = paginator.page(paginator.num_pages)

#     # 计算自定义页码范围
#     custom_page_range = get_custom_page_range(page, paginator.num_pages, 2)

#     return render(request, 'blog/post/list.html', {'page': page, 'custom_page_range': custom_page_range})

def get_custom_page_range(page, total_pages, visible_pages=2):
    current_page = page.number
    start_page = max(current_page - visible_pages, 1)
    end_page = min(current_page + visible_pages, total_pages)

    # 添加省略号
    custom_page_range = []
    if start_page > 1:
        custom_page_range.append(1)
        if start_page > 2:
            custom_page_range.append('...')

    for i in range(start_page, end_page + 1):
        custom_page_range.append(i)

    if end_page < total_pages:
        if end_page < total_pages - 1:
            custom_page_range.append('...')
        custom_page_range.append(total_pages)

    return custom_page_range




# def post_detail(request,id):
#     try:
#         post=Post.published.get(id=id)#有三种情况：只有一个值，没有值，有多个值
#     except Post.DoesNotExist:
#         raise Http404("No Post found.")
#     return render(
#         request,
#         'blog/post/detail.html',
#         {'post':post}
#     )


def post_detail(request:HttpRequest,year:int,month:int,day:int,post:str)->HttpResponse:
    post=get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    comments=post.comments.filter(is_active=True)
    form=CommentForm()
    
    return render(
        request,
        'blog/post/detail.html',
        {
            'post':post,
            'comments':comments,
            'form':form,
        }
    )

"""
def _get_queryset(klass):
    if hasattr(klass, "_default_manager"):#_default_manager就是objects
        return klass._default_manager.all()#查询集，函数调用前不执行查询
    return klass


def get_object_or_404(klass, *args, **kwargs):
    queryset = _get_queryset(klass)#函数调用，取出全部结果到内存
    if not hasattr(queryset, "get"):
        klass__name = (
            klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        )
        raise ValueError(
            "First argument to get_object_or_404() must be a Model, Manager, "
            "or QuerySet, not '%s'." % klass__name
        )
    try:
        return queryset.get(*args, **kwargs)#筛选
    except queryset.model.DoesNotExist:
        raise Http404(
            "No %s matches the given query." % queryset.model._meta.object_name
        )

# 所以get_object_or_404其实就是下面动作
def get_object_or_404(klass, *args, **kwargs):
    try:
        post=Post.objects.get(id=id)
    except DoesNotExist:
        raise Http404("no post found")

#异步
async def aget_object_or_404(klass, *args, **kwargs):
    queryset = _get_queryset(klass)#这一步还是同步的，获取查询集是同步的
    try:
        return await queryset.aget(*args, **kwargs)#只有这里是异步的，因此需要await 协程对象
    except queryset.model.DoesNotExist:
        raise Http404("not found")
"""


@require_POST
def post_comment(request,post_id)->HttpResponse:
    post=get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    comment=None
    form=CommentForm(data=request.POST)
    if form.is_valid():
        comment=form.save(commit=False)#不提交是为了增加指定的评论
        comment.post=post
        comment.save()#增加评论之后才提交，落盘
    return render(
        request,
        'blog/post/comment.html',
        {
            'post':post,
            'form':form,
            'comment':comment
        }
    )





