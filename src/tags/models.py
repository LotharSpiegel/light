from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import ugettext_lazy as _

from utils.misc import create_slug

#from photo.models import Photo

# Idea: not only tagged item have content_type, but also Tag itself could be represented by
# a django model..


# class TaggedItemMangager(models.Manager):


def tag_item(self, item, tag):
    TaggedItem.objects.get_or_create(tag=tag, item=item)


# remove_tag_from_item(self, item, tag):
# get_item_tags(self, item)


class Tag(models.Model):
    """A tag, which has a name and is represented one-to-one via the item-field as some model object.
    For example, the city Vienna (instance of model City) can have a tag. Then we would add a tag with content_type = City and object_id = the City-db_table primary key id of vienna."""

    name = models.CharField(_('Name'), max_length=80, unique=True, db_index=True)
    slug = models.SlugField(unique=True, max_length=80)
    popularity = models.IntegerField(default=0)
    parents = models.ManyToManyField('Tag', verbose_name=_('Parents'), blank=True)

    # def get_absolute_url(self):
    #     return reverse('tag_detail', kwargs={'tag_slug': self.slug})

    class Meta:
        ordering = ('popularity',)
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.name


class TaggedItem(models.Model):
    """
    Represents a tag on a item (item = instance of any django model).
    A model instance can have several tags - it then has several associated
    TaggedItem instances.
    """

    tag = models.ForeignKey(
        Tag, null=True, blank=True,
        verbose_name=_('Tags'), related_name='items', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, verbose_name=_('Content Type'),
        on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(_('Object Id'), db_index=True)
    item = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = _('Tagged Item')
        verbose_name_plural = _('Tagged Items')

    def __str__(self):
        return '{} <{}>'.format(str(self.item), str(self.tag))


@receiver(pre_save, sender=Tag)
def pre_save_tag_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(sender, instance, attribute='name')