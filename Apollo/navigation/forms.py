from django import forms
from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class RelatedHashtags(forms.ModelForm):
    class Meta:
        model = BlogHeshtags
        fields = ['hashtag']

class Comment_form(forms.ModelForm):
    comment = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Comment_user
        fields = ['comment']


class CreatePost(forms.ModelForm):
    full_text = forms.CharField(widget=CKEditorUploadingWidget(),label="Текст статьи")
    blog_title = forms.CharField(label='Заголовок статьи')
    class Meta:
        model = Blog
        fields = ['blog_title','img','full_text']

