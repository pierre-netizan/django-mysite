from django.contrib import admin
from .models import Post,Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=['title','slug','author','publish','status']
    list_filter=['status','created','publish','author']#按哪些字段过滤
    search_fields=['title','body']#在哪里搜索，可以是['title']
    prepopulated_fields={'slug':('title',)}#自动填充，依赖指定字段自动填充slug，可以是{'slug':("title", "category")}
    raw_id_fields=['author']#用一个输入框代替下拉选择框，让你通过输入主键（ID）来指定关联对象，而不是加载全部对象(比如100k+)的下拉列表，可以写成: raw_id_fields = ("author", "category", "tags")
    date_hierarchy='publish'#日期层级导航栏，允许按照 年 → 月 → 日 逐级筛选数据  管理后台为模型添加基于日期的导航层级（时间轴），让用户可以按年、月、日逐级筛选数据
    ordering=['status','-publish']
    show_facets=admin.ShowFacets.ALWAYS#总显示分类统计facets
    

# admin.site.register(Post)#往管理站点注册模型类，与装饰器写法二选一，即也可以写成@admin.register(Post)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=['name','email','post','created','is_active']
    list_filter=['is_active','created','updated']
    search_fields=['name','email','body']
