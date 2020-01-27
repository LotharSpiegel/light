from django import forms
# from django.db import IntegrityError

from .models import Page#, slugify


class PageCreateForm(forms.ModelForm):

    class Meta:
        model = Page
        fields = ['title', 'content', 'members_only']

    def __init__(self, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(**kwargs)

    # def clean_title(self):
    #     title = self.cleaned_data['title']
    #     print('check title:', title)
    #     #raise Exception(title)

    #     # self.instance.validate_unique()
    #     # print('instance.title:', self.instance)
    #     # try:
    #     #     self.instance.validate_unique()
    #     # except ValidationError:
    #     #     raise Exception('lot')
    #     return title

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.author = self.user
        # try:
        #     super().save(commit=commit)
        # except IntegrityError:
        #     print('IntegrityError')
        return super().save(commit=commit)

