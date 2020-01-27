from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django import template
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.html import mark_safe
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateResponseMixin, View, TemplateView
from django.views.generic.detail import DetailView

from .forms import PageCreateForm
from .models import Page
from .utils import build_breadcrumbs


# class BreadcrumbsMixin:
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['breadcrumbs'] = self.get_breadcrumbs()
#         return context

#     def get_breadcrumbs(self):
#         return (base_breadcrumbs('Home'),)


class PageCreateView(CreateView):
    model = Page
    #fields = ['title', 'content', 'members_only']
    form_class = PageCreateForm
    context_object_name = 'page'
    template_name = 'contents/edit/page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = Page.get_create_breadcrumbs()
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     self.object.author = self.request.user
    #     self.object.save()
    #     return HttpResponseRedirect(self.get_success_url())

    def get_breadcrumbs(self):
        parents = [
            ('Pages', reverse_lazy('contents:pages_index')),
            ('Index', reverse_lazy('homepage')),
        ]
        return build_breadcrumbs('Create Page',
            reverse_lazy('contents:create_page'),
            parents)

    # def form_invalid(self):
    #     raise Exception('form_invalid')
    #     #print('form_invalid')

    def get_success_url(self):
        messages.success(self.request, 'Successfully created new Page!')
        return reverse_lazy('contents:preview_page', kwargs={'page_slug': self.object.slug})


class PageDeleteView(DeleteView):

    model = Page
    context_object_name = 'page'
    template_name = 'contents/edit/delete_page.html'

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Page, slug=self.kwargs['page_slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = self.object.get_delete_breadcrumbs()
        return context

    def get_success_url(self):
        #print('get_success_url:', self.object.get_preview_url())
        messages.success(self.request, 'Successfully delete Page!')
        return reverse_lazy('contents:pages_index')


class PageUpdateView(UpdateView):

    model = Page
    fields = ['title', 'content', 'members_only']
    context_object_name = 'page'
    template_name = 'contents/edit/page.html'

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Page, slug=self.kwargs['page_slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = self.object.get_edit_breadcrumbs()
        return context

    def get_success_url(self):
        #print('get_success_url:', self.object.get_preview_url())
        return self.object.get_preview_url()


def view_page(request, page_slug):
    page = get_object_or_404(Page, slug=page_slug)
    # TODO check page.status
    #    ('draft', _('draft')),
    #    ('template', _('template')),
    #    ('published', _('published')),
    #    ('archived', _('archived')),
    #    ('deleted', _('deleted')),
    context = {
        'breadcrumbs': page.get_view_breadcrumbs(),
        'page_is_editable': page.is_editable(request.user)
    }
    if page.status == Page.STATUS.published:
        if page.built:
            context['page_template_name'] = page.get_template_name()
            template_name = "contents/page.html"
        else:
            context['page_content'] = page.render_content()
            #template_name = "contents/page_published_not_built.html"
            template_name = "contents/page_content.html"
    else:
        return redirect(page.get_preview_url())
        # context['page'] = page
        # template_name = "contents/page_not_published_yet.html"
    return render(request, template_name, context)

def preview_page(request, page_slug):
    page = get_object_or_404(Page, slug=page_slug)
    # parents = [
    #     ('Edit Page', reverse_lazy('contents:edit_page', kwargs={'page_slug': page_slug})),
    #     ('Index', reverse_lazy('homepage')),
    # ]
    # breadcrumbs = build_breadcrumbs('Page Preview: {}'.format(page.title),
    #     reverse_lazy('contents:preview_page', kwargs={'page_slug': page_slug}),
    #     parents)

    # print('page.content:', page.content)
    # page_content = mark_safe(page.content)
    # preview_context = {
    #     'page_content': page_content,
    #     'page_title': mark_safe(page.title),
    # }
    # complete_content = '{% load static snippets %}\n' + page_content

    # print('complete_content:', complete_content)

    # t = template.Template(complete_content)
    # preview_context = template.Context(preview_context)
    # # template_libraries
    # page_content = t.render(context=preview_context)
    context = {
        'breadcrumbs': page.get_preview_breadcrumbs(),
        'page_title': mark_safe(page.title),
        'page_slug': page.slug,
        'page_author': page.author,
        'page_content': page.render_content(),
    }
    #print('page_content:', page_content)
    template_name = "contents/preview_page.html"
    return render(request, template_name, context)

def pages_index(request):
    status_filter = request.GET.getlist('status')
    pages = Page.objects.get_pages(status_filter=status_filter)
    parents = [('Index', reverse_lazy('homepage')),]
    context = {
        'pages': pages,
        'breadcrumbs': build_breadcrumbs('Page Index', reverse_lazy('contents:pages_index'), parents),
    }
    template_name = "contents/pages_index.html"
    return render(request, template_name, context)

# class NotPublishedYetPageView(TemplateView):
#     template_name = "contents/page_not_published.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['page'] = self.get_built_page()
#         context['breadcrumbs'] = self.get_breadcrumbs()
#         return context


# # class BaseDetailView(SingleObjectMixin, View):
# #     def get(self, request, **kwargs):
# #         self.object = self.get_object()
# #         context = self.get_context_data(object=self.object)
# #         return self.render_to_response(context)


# def get(self, request, **kwargs):
#     self.object = self.get_object()
#     if self.object.status == Page.STATUS.published:

#     if self.request.path != self.object.get_absolute_url():
#         return HttpResponseRedirect(self.object.get_absolute_url())
#     else:
#         context = self.get_context_data(object=self.object)
#         return self.render_to_response(context)


# class PublishedPageView(DetailView):
#     """

#     """

#     model = Page
#     slug_field = "slug"
#     context_object_name = 'page'
#     template_name = "contents/page.html"

#     def get_built_page(self, **kwargs):
#         return "{build_dir}/{page_slug}.html".format(
#             build_dir=settings.BUILD_DIR,
#             page_slug=self.object.slug)

#     # def get_object(queryset=None):

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['page'] = self.get_built_page()
#         context['breadcrumbs'] = self.get_breadcrumbs()
#         return context

#     def get_breadcrumbs(self):
#         breadcrumbs = [(self.object.title, self.object.get_absolute_url),]
#         parent = self.object.parent
#         while parent is not None:
#             breadcrumbs.append((parent.title, parent.get_absolute_url))
#             parent = parent.parent
#         return breadcrumbs[::-1]