from django import template
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.html import mark_safe
from django.utils.text import slugify
from django.utils.timezone import now as timezone_now
from django.utils.translation import gettext_lazy as _

from model_utils import Choices
#from tags.models import Tag
from utils.models import CreationModificationDateMixin, AuthoredMixin

from .fields import OrderField
from .utils import build_breadcrumbs
from .validators import validate_title

User = settings.AUTH_USER_MODEL


class PageManager(models.Manager):

    def get_pages(self, status_filter=None):
        qs = Page.objects.all()
        if status_filter is None:
            status_filter = []
        for status in status_filter:
            if status == Page.STATUS.published:
                qs = qs.filter(status=status)
        return qs

    def get_published_pages(self):
        return self.get_published_pages(status_filter=[Page.STATUS.published])


class Page(CreationModificationDateMixin, AuthoredMixin):
    """
    Page model representing a page created by a user.
    """

    STATUS = Choices(
        ('draft', _('draft')), # stub?
        ('template', _('template')),
        ('published', _('published')),
        ('archived', _('archived')),
        ('deleted', _('deleted')),
    )

    title = models.CharField(max_length=120) #, validators=[validate_title])
    slug = models.SlugField(unique=True)
    content = models.TextField(_('Content'), blank=True)
    status = models.CharField(choices=STATUS, max_length=25, default=STATUS.draft)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
    author = models.ForeignKey(User, related_name=_('pages'), on_delete=models.SET_NULL, blank=True, null=True)
    published = models.DateTimeField(null=True, blank=True) # editable=True so that it can be changed in the admin
    members_only = models.BooleanField(default=False)
    built = models.BooleanField(default=False, blank=True)
    built_template_name = models.CharField(max_length=255, blank=True, null=True)
    #tags = models.ManyToManyField(Tag, blank=True, related_name='pages') # on_delete?

    objects = PageManager()

    class Meta:
        get_latest_by = "modified"
        ordering = ('-modified',)
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")

    def __str__(self):
        return self.title

    def clean(self):
        slug = slugify(self.title)
        # Page = apps.get_model('contents', 'Page')
        qs = Page.objects.filter(slug=slug)
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        if qs.exists():
            raise ValidationError('Page with this title already exists!')

    def render_content(self):
        page_content = mark_safe(self.content)
        context = {
            'page_content': page_content,
            'page_title': mark_safe(self.title),
        }
        complete_content = '{% load static snippets %}\n' + page_content
        #print('complete_content:', complete_content)
        t = template.Template(complete_content)
        render_context = template.Context(context)
        # template_libraries
        rendered_page_content = t.render(context=render_context)
        return rendered_page_content

    # def render_content(self):
    #     return render_to_string("contents/page_content.html", {'page_content': mark_safe(self.content)})

    def get_template_name(self):
        return '_build/{}'.format(self.built_template_name)

    def get_preview_url(self):
        return reverse_lazy('contents:preview_page', kwargs={'page_slug': self.slug})

    @staticmethod
    def get_create_url():
        return reverse_lazy('contents:create_page')

    def get_edit_url(self):
        return reverse_lazy('contents:edit_page', kwargs={'page_slug': self.slug})

    def get_delete_url(self):
        return reverse_lazy('contents:delete_page', kwargs={'page_slug': self.slug})

    def get_absolute_url(self):
        return reverse_lazy('contents:view_page', kwargs={'page_slug': self.slug})


        # if self.is_published():
        #     return reverse('view_page', kwargs={'slug': self.slug})
        # else:
        #     return reverse('view_page_not_published', kwargs={'slug': self.slug})

    #     elif self.status == STATUS.deleted:
    #         pass
    #     elif self.status == STATUS.draft:
    #         return reverse('page_draft_view', kwargs={'page_slug': self.slug})

    def is_editable(self, user):
        if user.is_superuser or user == self.author:
            return True
        return False

    def publish(self, time_stamp=None):
        """Sets the status of the article as published. If no time_stamp is given,
        it will set the published time to timezone.now()."""

        if not self.pk: # a new, not-yet-saved instance
            return
        if time_stamp:
            self.published = time_stamp
        else:
            self.published = timezone_now()
        self.status = STATUS.published
        self.build()
        self.save()

    @property
    def is_published(self):
        return self.status == STATUS.published

    def build(self):
        pass

    def get_preview_breadcrumbs(self):
        parents = [
            ('Pages', reverse_lazy('contents:pages_index')),
            ('Index', reverse_lazy('homepage')),
        ]
        return build_breadcrumbs(self.title,
            self.get_preview_url(),
            parents)

    def get_view_breadcrumbs(self):
        parents = [
            ('Pages', reverse_lazy('contents:pages_index')),
            ('Index', reverse_lazy('homepage')),
        ]
        return build_breadcrumbs(self.title,
            self.get_absolute_url(),
            parents)

    @classmethod
    def get_create_breadcrumbs(self):
        parents = [
            ('Pages', reverse_lazy('contents:pages_index')),
            ('Index', reverse_lazy('homepage')),
        ]
        return build_breadcrumbs('New Page',
            Page.get_create_url(),
            parents)

    def get_edit_breadcrumbs(self):
        parents = [
            (self.title, self.get_absolute_url()),
            ('Pages', reverse_lazy('contents:pages_index')),
            ('Index', reverse_lazy('homepage')),
        ]
        return build_breadcrumbs('Edit Page',
            self.get_edit_url(),
            parents)

    def get_delete_breadcrumbs(self):
        parents = [
            ('Pages', reverse_lazy('contents:pages_index')),
            ('Index', reverse_lazy('homepage')),
        ]
        return build_breadcrumbs('Delete Page',
            self.get_delete_url(),
            parents)


class Series(AuthoredMixin):
    """
    Model representing a series of blog posts or pages that belong together
    """
    pass


@receiver(pre_save, sender=Page)
def pre_save_page_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


# TODO: class ContentManager


class Content(models.Model):
    page = models.ForeignKey(Page,
                             related_name='contents',
                             on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     # limit_choices_to={'model__in':(
                                     #     'text',
                                     #     'video',
                                     #     'image',
                                     #     'file'
                                     # )}
                                     )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    # we need 3 diff fields to set up a generic relationship. in our content model these are
    # content_type, object_id to store the pk of the related object and item, to the related object by combining the
    # two prev fields
    # only cnotent_tye and object_id have col in db table of this model

    order = OrderField(blank=True, for_fields=['page'])

    class Meta:
        ordering = ['order']


class ItemBase(CreationModificationDateMixin, AuthoredMixin):

    default_css_class = ""


    author = models.ForeignKey(User,
                              related_name='%(class)s_related',
                              on_delete=models.CASCADE)
    css_class = models.CharField(max_length=100, default="", blank=True)
    # the reverse relation for child models will be text_related, file_related, etc.
    # title = models.CharField(max_length=250)

    # created = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['css_class'].default = self.default_css_class

    class Meta:
        abstract = True

    def render(self):
        if self.template_name is not None:
            render_to_string(self.template_name, {'item': self})
        else:
            raise NotImplemented


class TextContent(ItemBase):
    template_name = 'contents/text.html'

    text = models.TextField()


class FileContent(ItemBase):
    file = models.FileField(upload_to='files')


class ImageContent(ItemBase):
    file = models.FileField(upload_to='images')


class VideoContent(ItemBase):
    url = models.URLField()