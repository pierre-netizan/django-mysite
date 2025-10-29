from django.db import models
from django.utils import timezone
from django.db.models.functions import Now
from django.conf import settings
from utils.db import schema_table


class BaseModel(models.Model):
    # created=models.DateTimeField(auto_now_add=True,default=timezone.now)#第一次添加记录的时间（只能添加一次add）
    created=models.DateTimeField(editable=False,default=timezone.now)#第一次添加记录的时间（只能添加一次add）
    updated=models.DateTimeField(auto_now=True)#当前更新的时间（更新多次）
    deleted=models.DateTimeField(default=None,null=True,blank=True)

    class Meta:
        abstract=True#抽象基类，不生成表


class PublishedManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset().filter(status=Post.Status.PUBLISHED)
        )
        

class Post(BaseModel):
    class Status(models.TextChoices):
        # name=value,label
        DRAFT='DF','Draft'  # 枚举名字=枚举值,可读字符串，通过Post.Status.values获取选项的值
        PUBLISHED='PB','Published'
        
    title=models.CharField(max_length=250)
    slug=models.SlugField(max_length=250)
    body=models.TextField()
    # publish=models.DateTimeField(default=timezone.now)#根据是否配置时区USE_TZ而定是否带时区
    # 实现代码：datetime.now(tz=timezone.utc if settings.USE_TZ else None)
    publish=models.DateTimeField(db_default=Now())#db_default使用数据库函数返回数值，对于pg来说就是select STATEMENT_TIMESTAMP()，对于mysql来说就是select CURRENT_TIMESTAMP(6)
    status=models.CharField(max_length=2,choices=Status,default=Status.DRAFT)
    author=models.ForeignKey(
        settings.AUTH_USER_MODEL,  # global_settings.py中AUTH_USER_MODEL = "auth.User"
        on_delete=models.CASCADE,
        related_name='blog_posts'  # 从关联模型反向访问当前模型时所使用的属性名，外键默认自动创建反向关系，默认反向关系名字：小写模型名_set，如user.post_set
    )
    
    objects=models.Manager()#默认管理器
    published=PublishedManager()#自定义管理器
    
    class Meta:
        # db_tablespace='mysite'  #表空间，物理隔离，schema则是逻辑隔离，相当于名字空间，一般不同项目或租户用schema
        db_table=schema_table('posts')
        ordering=['-publish']#最先添加的放在最上面
        indexes=[
            models.Index(fields=['-publish']),#添加索引
        ]
    
    def __str__(self):#用来打印对象的属性
        return f"{self.__class__.__name__}({self.title})"





















