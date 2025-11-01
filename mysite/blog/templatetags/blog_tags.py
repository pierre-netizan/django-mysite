from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe

import markdown

from ..models import Post

register=template.Library()

@register.simple_tag#注册简单模板标签，如果不用默认的函数名则要用name单独指定，此时@register.simple_tag(name='新名字')
def total_posts()->int:#标签名字是total_posts
    print(f"          >>{Post.published.count()}")
    return Post.published.count()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts=Post.published.order_by('-publish')[:count]
    return {'latest_posts':latest_posts}

@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]

@register.filter(name='markdown')
def markdown_format(text):
    """
    'fenced_code', #支持```代码块
    'extra'，      #表格、脚注等
    'nl2br'        #换行转<br>
    """
    return mark_safe(markdown.markdown(
        text,
        extensions=[
            'fenced_code',
            'extra',
            'nl2br',
        ]
    ))





