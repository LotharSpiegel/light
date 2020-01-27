from django.db import models
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy

#from tags.models import TaggedItem
from pygments import formatters, highlight, lexers
from markdown import markdown
import datetime

from contents.utils import build_breadcrumbs


class Language(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    language_code = models.CharField(max_length=50)
    mime_type = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('snippets:language_detail', kwargs={'slug': self.slug})

    def get_lexer(self):
        return lexers.get_lexer_by_name(self.language_code)


class Snippet(models.Model):
    title = models.CharField(max_length=255)
    language = models.ForeignKey(Language, related_name='snippets', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='snippets', on_delete=models.CASCADE)
    description = models.TextField()
    description_html = models.TextField(editable=False)
    code = models.TextField()
    highlighted_code = models.TextField(editable=False)
    pub_date = models.DateTimeField(editable=False)
    updated_date = models.DateTimeField(editable=False)
    # linenos = BooleanField

    def is_editable(self, user):
        if user.is_superuser or user == self.author:
            return True
        return False

    def highlight(self):
        return highlight(self.code,
                         self.language.get_lexer(),
                         formatters.HtmlFormatter(linenos=True))

    def save(self, force_insert=False, force_update=False):
        if not self.id:
            self.pub_date = datetime.datetime.now()
        self.updated_date = datetime.datetime.now()
        self.description_html = markdown(self.description)
        self.highlighted_code = self.highlight()
        super().save(force_insert=force_insert, force_update=force_update)

    class Meta:
        ordering = ['-pub_date']

    def get_absolute_url(self):
        return reverse('snippets:snippet_detail', kwargs={'snippet_id': self.id})

    def get_edit_url(self):
        return reverse('snippets:snippet_edit', kwargs={'snippet_id': self.id})

    def get_breadcrumbs(self):
        parents = [
            ('Snippets', reverse_lazy('snippets:snippets_list')),
            ('Index', reverse_lazy('homepage')),
        ]
        breadcrumbs = build_breadcrumbs(self.title,
            self.get_absolute_url,
            parents)
        return breadcrumbs


    def get_template_name(self):
        return 'snippets/includes/snippet.html'

    def render(self):
        template_name = self.get_template_name()
        if template_name is not None:
            context = {'snippet': self}
            return render_to_string(template_name, context)
        else:
            raise NotImplemented

    def __str__(self):
        return self.title