from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now as timezone_now


User = settings.AUTH_USER_MODEL


class CreationModificationDateMixin(models.Model):
    """
    Abstract base class with a creation and modification
    date and time. Since it is an abstract model,
    all extending model classes will create all the fields in the same db table
    """

    created = models.DateTimeField(
        _("Creation date and time"),
        editable=False,
        auto_now_add=True,
        #default=timezone_now
    )

    modified = models.DateTimeField(
        _("Modification date and time"),
        null=True,
        editable=False,
        auto_now=True,
        #default=None
    )

    # def save(self, *args, **kwargs):
    #     if not self.pk: # a new, not-yet-saved instance
    #         self.created = timezone_now()
    #      #else:
    #          # To ensure that we have a creation data always,
    #          # we add this one
    #     if not self.created:
    #         self.created = timezone_now()
    #     else:
    #         self.modified = timezone_now()
    #     return super(CreationModificationDateMixin, self).\
    #     save(*args, **kwargs)
    #     #save.alters_data = True

    class Meta:
        abstract = True


class AuthoredMixin(models.Model):
    """
    Abstract base class to mixin to models which are supposed to have an author/creator
    """

    author = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def save(self, *args, **kwargs):
        if 'request' in kwargs and self.author is None:
            request = kwargs.pop('request')
            self.author = request.user
        super(AuthoredMixin, self).save(**kwargs)

    class Meta:
        abstract = True