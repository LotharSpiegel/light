from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateResponseMixin, View, TemplateView
from django.views.generic.detail import DetailView

from .models import Page


# class BreadcrumbsMixin:
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['breadcrumbs'] = self.get_breadcrumbs()
#         return context

#     def get_breadcrumbs(self):
#         return (base_breadcrumbs('Home'),)


class PageCreateView(CreateView):
    model = Page
    fields = ['title', 'members_only']
    context_object_name = 'page'
    template_name = 'contents/edit/page.html'

    def get_success_url(self):
        #self.object
        return reverse_lazy('page_preview', kwargs={'page_slug': self.object.slug})


class PageUpdateView(UpdateView):
    model = Page
    fields = ['title', 'members_only']
    context_object_name = 'page'
    template_name = 'contents/edit/page.html'

    def get_success_url(self):
        #self.object
        return reverse_lazy('page_preview', kwargs={'page_slug': self.object.slug})



def view_page(request, slug):
    page = get_object_or_404(Page, slug=slug)
    context = {
        'page': page,
        'breadcrumbs': page.get_breadcrumbs(),
    }
    if page.status == Page.STATUS.published:
        template_name = "contents/page.html"
        return render(request, template_name, context)
    else:
        template_name = "contents/page_not_published_yet.html"
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