from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.template.loader import render_to_string
from django.utils.timezone import now as timezone_now
from django.utils.translation import gettext_lazy as _

from model_utils import Choices
#from tags.models import Tag
from utils.models import CreationModificationDateMixin, AuthoredMixin

from .fields import OrderField


User = settings.AUTH_USER_MODEL



class PageManager(models.Manager):

    def get_published_pages(self):
        queryset = Page.objects.all()
        queryset = queryset.filter(status=Page.STATUS.published)


class Page(CreationModificationDateMixin, AuthoredMixin):
    """
    Page model representing a page created by a user.
    """

    STATUS = Choices(
        ('draft', _('draft')),
        ('template', _('template')),
        ('published', _('published')),
        ('archived', _('archived')),
        ('deleted', _('deleted')),
    )

    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    status = models.CharField(choices=STATUS, max_length=25, default=STATUS.draft)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
    author = models.ForeignKey(User, related_name=_('pages'), on_delete=models.SET_NULL, blank=True, null=True)
    published = models.DateTimeField(null=True, blank=True) # editable=True so that it can be changed in the admin
    members_only = models.BooleanField(default=False)
    #tags = models.ManyToManyField(Tag, blank=True, related_name='pages') # on_delete?

    objects = PageManager()

    class Meta:
        get_latest_by = "created"
        ordering = ('-created',)
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('view_page', kwargs={'slug': self.slug})
        # if self.is_published():
        #     return reverse('view_page', kwargs={'slug': self.slug})
        # else:
        #     return reverse('view_page_not_published', kwargs={'slug': self.slug})

    #     elif self.status == STATUS.deleted:
    #         pass
    #     elif self.status == STATUS.draft:
    #         return reverse('page_draft_view', kwargs={'page_slug': self.slug})

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

    def is_published(self):
        return self.status == STATUS.published

    def build(self):
        pass

    def get_breadcrumbs(self):
        breadcrumbs = [(self.title, self.get_absolute_url),]
        parent = self.parent
        while parent is not None:
            breadcrumbs.append((parent.title, parent.get_absolute_url))
            parent = parent.parent
        return breadcrumbs[::-1]


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