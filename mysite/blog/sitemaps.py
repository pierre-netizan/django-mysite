from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
    changefreq='weekly'
    priority=0.9
    
    def items(self):
        return Post.published.all()
    
    def lastmod(self,obj):
        return obj.updated#items()返回任意对象obj的最近一次修改时间
    





    
