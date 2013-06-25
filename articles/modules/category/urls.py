from articles.modules.category.views import CategoryArticleDetail, CategoryArticleList
from django.conf.urls import patterns, url

urlpatterns = patterns('articles.modules.category.views',
                       url(r'^(?P<category_url>[a-z0-9_/-]+/)(?P<article>[a-z0-9_-]+)/$', CategoryArticleDetail.as_view(),
                           name="article_detail"),
                       url(r'^(?P<category_url>[a-z0-9_/-]+/)$', CategoryArticleList.as_view(), name='article_category'),
                       url(r'^$', CategoryArticleList.as_view(), name='article_index'),
)


