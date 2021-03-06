from django.conf import settings
from django.conf.urls import patterns, url
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import get_callable
from feincms.module.mixins import ContentModelMixin

try:
    from feincms.admin.item_editor import ItemEditor
except ImportError:
    from feincms.admin.editor import ItemEditor

from feincms.content.application import models as app_models
from feincms.models import Base
from feincms.utils.managers import ActiveAwareContentManagerMixin
from feincms.extensions import ExtensionModelAdmin


class ArticleManager(ActiveAwareContentManagerMixin, models.Manager):
    active_filters = {'simple-active': Q(active=True)}


class Article(ContentModelMixin, Base):
    active = models.BooleanField(_('active'), default=True)

    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'), max_length=255, help_text=_('This will be automatically generated from the name'), unique=True, editable=True)

    class Meta:
        ordering = ['-publication_date']
        unique_together = []
        verbose_name = _('article')
        verbose_name_plural = _('articles')

    objects = ArticleManager()

    @classmethod
    def get_urlpatterns(cls):
        import views
        return patterns('',
            url(r'^$', views.ArticleList.as_view(), name='article_index'),
            url(r'^(?P<slug>[a-z0-9_-]+)/$', views.ArticleDetail.as_view(), name='article_detail'),
        )

    @classmethod
    def remove_field(cls, f_name):
        """Remove a field. Effectively inverse of contribute_to_class"""
        # Removes the field form local fields list
        cls._meta.local_fields = [f for f in cls._meta.local_fields if f.name != f_name]

        # Removes the field setter if exists
        if hasattr(cls, f_name):
            delattr(cls, f_name)

    @classmethod
    def register_extension(cls, register_fn):
        """Extended from FeinCMS base to add the Admin class."""
        register_fn(cls, ArticleAdmin)

    @classmethod
    def get_urls(cls):
        return cls.get_urlpatterns()

    def __unicode__(self):
        return u"%s" % self.title

    @models.permalink
    def get_absolute_url(self):
        return 'article_detail', (), {'slug': self.slug}

    @property
    def full_name_for_search(self):
        return u'{} ({})'.format(self.title, self._meta.verbose_name)

    @property
    def is_active(self):
        return Article.objects.active().filter(pk=self.pk).count() > 0


ModelAdmin = get_callable(getattr(settings, 'ARTICLE_MODELADMIN_CLASS', 'django.contrib.admin.ModelAdmin'))


class ArticleAdmin(ItemEditor, ExtensionModelAdmin):
    list_display = ['__unicode__', 'active' ]
    list_filter = []
    search_fields = ['title', 'slug']
    filter_horizontal = []
    prepopulated_fields = {
        'slug': ('title',),
    }
    fieldsets = [
        [None, {
            'fields': ['active', 'title', 'slug']
        }],
        # <-- insertion point, extensions appear here, see insertion_index above
    ]

    # TODO: add_extension_options is copied from feincms.module.page.modeladmins.PageAdmin

    fieldset_insertion_index = 1

