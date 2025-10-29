from django.shortcuts import render,get_object_or_404
from django.http import Http404, HttpRequest, HttpResponse
from .models import Post


def post_list(request:HttpRequest)->HttpResponse:
    posts=Post.published.all()
    return render(
        request,
        'blog/post/list.html',
        {'posts':posts}
    )


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


def post_detail(request:HttpRequest,id:int)->HttpResponse:
    post=get_object_or_404(
        Post,
        id=id,
        status=Post.Status.PUBLISHED
    )
    return render(
        request,
        'blog/post/detail.html',
        {'post':post}
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








